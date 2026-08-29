# FairSem

[![CI](https://github.com/korovin-aa97/fairsem/actions/workflows/ci.yml/badge.svg)](https://github.com/korovin-aa97/fairsem/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/korovin-aa97/fairsem)](https://github.com/korovin-aa97/fairsem/releases)

**A fair, observable semaphore for expensive commands sharing one Linux machine.**

FairSem gives independent processes a named FIFO admission queue. It caps
concurrency, shows who is holding or waiting, recovers safely from dead
wrappers, and fails closed when its state cannot be trusted.

It is a traffic controller for local commands—not an agent scheduler,
distributed lock, container runtime, or cluster queue.

## Ten-second demo

Install locally, then launch five jobs with two slots:

```bash
./install.sh --prefix "$HOME/.local"
export PATH="$HOME/.local/bin:$PATH"

for job in 1 2 3 4 5; do
  fairsem run --name demo --slots 2 -- \
    sh -c 'echo "start job $1"; sleep 2; echo "done  job $1"' _ "$job" &
done

fairsem status --name demo
wait
```

At most two commands run together. With one slot, commands start in ticket
order. With multiple slots, only the oldest currently eligible tickets may
start.

## Install

FairSem v0.1 supports Linux with `/proc` and Python 3.10 or newer. It has no
third-party runtime dependencies.

From a release archive or source checkout:

```bash
./install.sh --prefix "$HOME/.local"
"$HOME/.local/bin/fairsem" --version
```

System-wide installation is explicit—download and inspect the archive first,
then run:

```bash
sudo ./install.sh --prefix /usr/local
```

To remove those two installed files:

```bash
./uninstall.sh --prefix "$HOME/.local"
```

FairSem deliberately does not recommend piping a network response into a
privileged shell.

## Usage

```text
fairsem run [--name NAME] [--slots N] [--timeout SECONDS]
            [--poll SECONDS] [--best-effort] -- COMMAND [ARG...]
fairsem status [--name NAME] [--json]
fairsem repair [--name NAME]
fairsem --version
```

Examples:

```bash
# Keep at most two test suites active.
fairsem run --name tests --slots 2 -- pytest -q

# Give up after 30 seconds without running the command.
fairsem run --name gpu --slots 1 --timeout 30 -- ./render-model

# Machine-readable operator view.
fairsem status --name tests --json | jq .
```

The first active caller defines the slot count for a name. A different count
is rejected while that semaphore has holders or waiters; it may be changed
once idle.

## What “fair” means

Tickets are assigned under one kernel lock and sorted by a persistent counter.
For one slot, admission is strict FIFO among live waiters. For `N` slots, only
the oldest waiters needed to fill the available capacity are eligible; kernel
scheduling can change their exact start order within that group. There is no
priority feature in v0.1, so newer work cannot continually jump the queue.

Timeouts—including state-lock waits—use the monotonic clock. A waiter that times out or receives
`INT`/`TERM`/`HUP` removes itself. Records identify both PID and Linux process
start time and, for new records, boot ID, preventing PID reuse or reboot from
preserving stale capacity.

The complete state and failure rules are in [the contract](docs/CONTRACT.md).

## Failure policy

FairSem's default is **fail closed**: if its owner-only state directory, lock,
configuration, or records cannot be trusted, your command does not run.

`--best-effort` is an explicit escape hatch only for secure state setup/lock
unavailability. It writes a prominent warning and runs without admission. It
does not bypass corrupt state or conflicting slot configuration.

State defaults to `/tmp/fairsem-$UID` with mode `0700`. Override it with
`FAIRSEM_STATE_DIR`; the target must be a real directory owned by the current
user with mode `0700`. Status output includes command arguments, so do not put
secrets on command lines.

## Signals, crashes, and exit status

FairSem runs the command in a new process group. `INT`, `TERM`, and `HUP` sent
to FairSem are forwarded to that group. A normal command's exit status is
preserved; signal exits use `128 + signal`.

If the FairSem wrapper is killed, the recorded child remains a holder until it
exits. This preserves the slot limit rather than silently admitting too much
work. The next operation removes dead or zombie records. See
[`fairsem(1)`](man/fairsem.1) and [the contract](docs/CONTRACT.md) for stable
tool exit codes.

## Validation

Run the deterministic Linux suite:

```bash
python3 -m unittest -v tests.test_fairsem
```

From macOS or any machine with Docker:

```bash
make test-containers
```

The suite stresses slot bounds and covers FIFO progress, timeout/cancellation,
TERM/KILL behavior, child-aware crash recovery, dead/PID-reused state, corrupt
state, fail-closed permissions, JSON shape, nesting, names, and exit-code
propagation.

## Scope and limitations

- Linux and Python 3.10+ only in v0.1; macOS is not claimed.
- One user and one machine; this is not a network/distributed semaphore.
- `/tmp` state does not survive reboot, by design.
- Commands that daemonize or deliberately escape their process group are
  outside the lifecycle guarantee.
- FairSem does not set CPU, memory, I/O, or cgroup limits. It only controls
  admission.
- Priorities are intentionally deferred; FIFO progress is simpler to verify.

See [known alternatives](docs/COMPETITORS.md), the [changelog](CHANGELOG.md),
the [packaging notes](docs/PACKAGING.md), and [contributing guide](CONTRIBUTING.md).

Built from operating a mixed Claude/Codex production fleet. This repository is
the generic admission primitive only; it contains no private orchestration.

## License

[MIT](LICENSE) © 2026 Alexander Korovin.
