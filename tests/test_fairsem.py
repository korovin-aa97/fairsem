#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shlex
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FAIRSEM = ROOT / "bin" / "fairsem"
CRITICAL = ROOT / "tests" / "helpers" / "critical_section.py"
SIGNAL_CHILD = ROOT / "tests" / "helpers" / "signal_child.py"
PYTHON = sys.executable


class FairSemTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.state = self.base / "state"
        self.env = os.environ.copy()
        self.env["FAIRSEM_STATE_DIR"] = str(self.state)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_cli(self, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(FAIRSEM), *args],
            env=env or self.env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def popen(self, *args: str) -> subprocess.Popen[str]:
        return subprocess.Popen(
            [str(FAIRSEM), *args],
            env=self.env,
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def status(self, name: str = "test") -> dict[str, object]:
        result = self.run_cli("status", "--name", name, "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def wait_for(self, predicate: object, timeout: float = 5.0) -> None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if predicate():  # type: ignore[operator]
                return
            time.sleep(0.02)
        self.fail("condition did not become true")

    def test_version_help_and_usage_exit(self) -> None:
        version = self.run_cli("--version")
        self.assertEqual(version.returncode, 0)
        self.assertEqual(version.stdout.strip(), "fairsem 0.1.0")
        usage = self.run_cli("run")
        self.assertEqual(usage.returncode, 64)

    def test_command_exit_code_is_preserved(self) -> None:
        result = self.run_cli("run", "--name", "exit", "--", "sh", "-c", "exit 42")
        self.assertEqual(result.returncode, 42, result.stderr)

    def test_strict_slot_limit_under_stress(self) -> None:
        metrics = self.base / "metrics.json"
        jobs = [
            self.popen(
                "run",
                "--name",
                "stress",
                "--slots",
                "3",
                "--",
                PYTHON,
                str(CRITICAL),
                str(metrics),
                "0.08",
                str(index),
            )
            for index in range(24)
        ]
        results = [job.communicate(timeout=15) + (job.returncode,) for job in jobs]
        self.assertTrue(all(item[2] == 0 for item in results), results)
        observed = json.loads(metrics.read_text(encoding="utf-8"))
        self.assertEqual(observed["max"], 3)
        self.assertEqual(observed["active"], 0)
        self.assertEqual(len(observed["starts"]), 24)

    def test_fifo_progress_with_controlled_registration(self) -> None:
        metrics = self.base / "fifo.json"
        gate = self.base / "gate"
        first = self.popen(
            "run",
            "--name",
            "fifo",
            "--slots",
            "1",
            "--",
            "sh",
            "-c",
            f"python3 {shlex.quote(str(CRITICAL))} {shlex.quote(str(metrics))} 0.01 0; while [ ! -e {shlex.quote(str(gate))} ]; do sleep 0.02; done",
        )
        self.wait_for(lambda: self.status("fifo")["in_use"] == 1)
        waiters: list[subprocess.Popen[str]] = []
        for index in range(1, 6):
            waiter = self.popen(
                "run", "--name", "fifo", "--slots", "1", "--", PYTHON, str(CRITICAL), str(metrics), "0.03", str(index)
            )
            waiters.append(waiter)
            self.wait_for(lambda n=index: len(self.status("fifo")["waiters"]) == n)
        gate.touch()
        self.assertEqual(first.wait(timeout=10), 0)
        for waiter in waiters:
            self.assertEqual(waiter.wait(timeout=10), 0)
        observed = json.loads(metrics.read_text(encoding="utf-8"))
        self.assertEqual(observed["starts"], [str(i) for i in range(6)])

    def test_timeout_removes_waiter(self) -> None:
        holder = self.popen("run", "--name", "timeout", "--", "sleep", "0.5")
        self.wait_for(lambda: self.status("timeout")["in_use"] == 1)
        timed = self.run_cli("run", "--name", "timeout", "--timeout", "0.05", "--", "true")
        self.assertEqual(timed.returncode, 75)
        self.assertEqual(len(self.status("timeout")["waiters"]), 0)
        self.assertEqual(holder.wait(timeout=5), 0)

    def test_waiter_cancellation_cleans_record(self) -> None:
        holder = self.popen("run", "--name", "cancel", "--", "sleep", "0.5")
        self.wait_for(lambda: self.status("cancel")["in_use"] == 1)
        waiter = self.popen("run", "--name", "cancel", "--", "sleep", "0.1")
        self.wait_for(lambda: len(self.status("cancel")["waiters"]) == 1)
        waiter.send_signal(signal.SIGTERM)
        self.assertEqual(waiter.wait(timeout=5), 143)
        self.assertEqual(len(self.status("cancel")["waiters"]), 0)
        holder.wait(timeout=5)

    def test_term_is_forwarded_to_command_group(self) -> None:
        ready = self.base / "ready"
        received = self.base / "received"
        holder = self.popen(
            "run", "--name", "signal", "--", PYTHON, str(SIGNAL_CHILD), str(ready), str(received)
        )
        self.wait_for(ready.exists)
        holder.send_signal(signal.SIGTERM)
        self.assertEqual(holder.wait(timeout=5), 143)
        self.wait_for(received.exists)
        self.assertEqual(received.read_text(encoding="ascii"), str(int(signal.SIGTERM)))
        self.assertEqual(self.status("signal")["in_use"], 0)

    def test_killed_wrapper_keeps_live_child_as_holder_then_recovers(self) -> None:
        holder = self.popen("run", "--name", "crash", "--", "sleep", "0.7")
        self.wait_for(lambda: self.status("crash")["holders"] and self.status("crash")["holders"][0]["command_pid"])
        holder.kill()
        self.assertEqual(holder.wait(timeout=5), -signal.SIGKILL)
        self.assertEqual(self.status("crash")["in_use"], 1)
        blocked = self.run_cli("run", "--name", "crash", "--timeout", "0.05", "--", "true")
        self.assertEqual(blocked.returncode, 75)
        time.sleep(0.75)
        recovered = self.run_cli("run", "--name", "crash", "--timeout", "1", "--", "true")
        self.assertEqual(recovered.returncode, 0, recovered.stderr)

    def test_dead_pid_and_pid_reuse_records_are_cleaned(self) -> None:
        self.status("stale")
        waiter_dir = self.state / "stale" / "waiters"
        fake = {
            "schema": 1,
            "ticket": "00000000000000000001-fake",
            "owner": {"pid": os.getpid(), "start_ticks": "0"},
            "command": None,
            "argv": ["true"],
            "enqueued_monotonic_ns": time.monotonic_ns(),
            "enqueued_at": "2026-08-29T00:00:00Z",
        }
        (waiter_dir / "00000000000000000001-fake.json").write_text(json.dumps(fake), encoding="utf-8")
        result = self.status("stale")
        self.assertEqual(result["cleanup"]["removed_waiters"], 1)
        self.assertEqual(result["waiters"], [])

    def test_corrupt_state_fails_closed_and_repair_quarantines(self) -> None:
        self.status("corrupt")
        record = self.state / "corrupt" / "waiters" / "00000000000000000001-bad.json"
        record.write_text("not-json", encoding="utf-8")
        marker = self.base / "must-not-exist"
        failed = self.run_cli("run", "--name", "corrupt", "--", "touch", str(marker))
        self.assertEqual(failed.returncode, 70)
        self.assertFalse(marker.exists())
        repaired = self.run_cli("repair", "--name", "corrupt")
        self.assertEqual(repaired.returncode, 0, repaired.stderr)
        self.assertTrue(any((self.state / "corrupt" / "quarantine").iterdir()))
        passed = self.run_cli("run", "--name", "corrupt", "--", "touch", str(marker))
        self.assertEqual(passed.returncode, 0, passed.stderr)
        self.assertTrue(marker.exists())

    def test_insecure_state_fails_closed_and_best_effort_is_explicit(self) -> None:
        self.state.mkdir(mode=0o755)
        os.chmod(self.state, 0o755)
        marker = self.base / "marker"
        failed = self.run_cli("run", "--name", "unsafe", "--", "touch", str(marker))
        self.assertEqual(failed.returncode, 73)
        self.assertFalse(marker.exists())
        fallback = self.run_cli("run", "--name", "unsafe", "--best-effort", "--", "touch", str(marker))
        self.assertEqual(fallback.returncode, 0, fallback.stderr)
        self.assertTrue(marker.exists())
        self.assertIn("WARNING", fallback.stderr)

    def test_slot_mismatch_fails_while_active_and_reconfigures_when_idle(self) -> None:
        holder = self.popen("run", "--name", "config", "--slots", "2", "--", "sleep", "0.3")
        self.wait_for(lambda: self.status("config")["in_use"] == 1)
        mismatch = self.run_cli("run", "--name", "config", "--slots", "3", "--", "true")
        self.assertEqual(mismatch.returncode, 65)
        holder.wait(timeout=5)
        changed = self.run_cli("run", "--name", "config", "--slots", "3", "--", "true")
        self.assertEqual(changed.returncode, 0, changed.stderr)
        self.assertEqual(self.status("config")["slots"], 3)

    def test_names_are_independent(self) -> None:
        alpha = self.popen("run", "--name", "alpha", "--", "sleep", "0.3")
        beta = self.popen("run", "--name", "beta", "--", "sleep", "0.3")
        self.wait_for(lambda: self.status("alpha")["in_use"] == 1 and self.status("beta")["in_use"] == 1)
        alpha.wait(timeout=5)
        beta.wait(timeout=5)

    def test_nested_same_name_is_rejected(self) -> None:
        result = self.run_cli(
            "run", "--name", "nested", "--", str(FAIRSEM), "run", "--name", "nested", "--", "true"
        )
        self.assertEqual(result.returncode, 65)
        self.assertIn("would deadlock", result.stderr)

    def test_json_status_has_stable_top_level_shape(self) -> None:
        status = self.status("shape")
        self.assertEqual(
            set(status),
            {"schema", "name", "slots", "in_use", "available", "holders", "waiters", "cleanup"},
        )
        self.assertEqual(status["schema"], 1)
        self.assertEqual(status["name"], "shape")


if __name__ == "__main__":
    unittest.main(verbosity=2)
