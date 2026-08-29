# FairSem — Agent Bootstrap

Last updated: 2026-08-29. Repository status: **private extraction draft**.

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

- Private, unpublished Linux/bash draft.
- `bin/fairsem` supports named semaphores, a slot count, FIFO-like ticket order,
  stale-PID cleanup, status output, and command execution under a slot.
- It requires `flock` and stores state under `/tmp` by default.
- It has no tests, version command, install script, package, license, timeout,
  priority/aging contract, JSON status, or portability guarantees.

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

1. Write the state, fairness, failure, and cleanup contract.
2. Add deterministic concurrency tests for admission order, slot limits,
   crashes, signals, stale PIDs, and competing semaphore names.
3. Add timeout/cancellation, priority with aging, JSON status, and stable exit
   codes without weakening fairness.
4. Decide whether v0.1 stays bash/Linux or moves to a portable implementation.
5. Add install/uninstall paths, man page or shell help, and release archives.
6. Validate on at least one unrelated machine with no repository-specific edits.
7. Complete `docs/PUBLIC_RELEASE_PLAN.md`; publish only with explicit approval.

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
and launch drafts. Making the repository public, publishing packages, creating
a public release, or posting externally requires explicit owner authorization.
