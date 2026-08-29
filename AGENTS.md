# FairSem — Agent Bootstrap

Last updated: 2026-08-30. Repository status: **public v0.1.3 utility**.

Read this file first, then `README.md`, `bin/fairsem`, and
`docs/PUBLIC_RELEASE_PLAN.md`.

## Product in one sentence

FairSem is an observable, fair queue that prevents expensive commands from
overloading a shared machine or starving behind one noisy worker.

## Positioning

Think "traffic controller for heavy local commands", not an agent scheduler.
The OSS utility controls admission to a named resource. It does not launch
agents, route work, manage cloud capacity, or decide which task has business
priority.

## Current state

- Public Linux/Python 3.10+ `v0.1.3`, licensed under MIT.
- `bin/fairsem` provides named owner-scoped semaphores, verified FIFO
  eligibility, timeouts, signal forwarding, PID-start stale recovery, and
  stable human/JSON status.
- State uses Python's `flock(2)` binding and lives in owner-only
  `/tmp/fairsem-$UID` by default.
- Tests cover concurrency, progress, crash/signal cleanup, fail-closed paths,
  independent names, nesting, and command status propagation across the
  supported Python/Linux matrix.

## Non-negotiable boundaries

- Public default must fail closed when locking or state cannot be trusted.
  Best-effort/fail-open behaviour must require an explicit flag.
- Fairness claims need measured, adversarial tests; do not call the current
  draft strictly FIFO until scheduling behaviour is proven.
- Handle process death, signals, PID reuse, stale files, interrupted state
  updates, lock-directory permissions, and clock anomalies.
- Use monotonic time for waiting/aging decisions where the platform permits it.
- Keep the utility generic: no private runner names, host paths, schedules,
  incident IDs, or fleet orchestration.
- The first public version may be Linux-only if that boundary is prominent.

## Next work, in order

1. Collect real user reports before expanding the feature set.
2. Keep every scheduling/state change covered by deterministic tests.
3. Consider a more event-driven wakeup only with equivalent failure behavior.
4. Consider priorities only with a specified and adversarially tested aging
   rule; FIFO progress is more important than feature count.
5. Add package-manager distribution only where it can be maintained.
6. Do not claim macOS or distributed support without a new contract and matrix.

## v0.1 definition of done

- Slot limit is never exceeded under concurrent stress.
- Normal waiters make progress and priority cannot starve them indefinitely.
- A killed holder releases capacity; stale state cannot block forever.
- Lock or state failure is clear, observable, and fail-closed by default.
- `status` has stable human and JSON formats.
- Exit codes and signal forwarding are documented.
- Installation and removal work on supported Linux distributions.
- README contains a short reproducible contention demo and honest limitations.
- Community files, changelog, security policy, license, and tagged release
  assets are ready.

## Working rules for future agents

- Keep the dependency surface extremely small.
- Treat shell quoting, path permissions, and signal handling as security and
  correctness issues.
- Every concurrency fix needs a deterministic regression harness.
- Do not hide stale-state repair; expose it in status and logs.
- Benchmark overhead, but do not optimize before correctness is proven.
- Check current competitors and package names directly on launch day.

## Success criterion

The public candidate must run on another person's supported machine without
source edits. Continue only if users can describe a real shared-resource use
case; otherwise keep it as a compact maintained utility.

## Release authority

Agents can prepare code, validation, documentation, archives, package recipes,
and launch drafts. New releases, package publication, visibility changes, or
external launch posts still require explicit owner authorization.
