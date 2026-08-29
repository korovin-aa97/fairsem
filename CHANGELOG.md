# Changelog

All notable changes are documented here. FairSem follows Semantic Versioning.

## [0.1.3] — 2026-08-30

- Publish the release under repository-enforced immutable releases, locking
  its tag and uploaded assets and generating GitHub release attestation.
- Keep the v0.1.2 accessible README hero and the v0.1.1 runtime correctness
  fixes unchanged.

## [0.1.2] — 2026-08-30

- Add an accessible illustrated README hero showing how many local jobs flow
  through a fair queue into bounded parallel work.
- Ship matching SVG and 1280×640 PNG assets for documentation and social
  previews, with a palette that remains legible in light and dark contexts.

## [0.1.1] — 2026-08-30

- Make wait deadlines cover state-lock contention, preventing commands from
  starting after their timeout.
- Preserve signal forwarding and exit status in explicit `--best-effort` mode.
- Make wrapper signal consumption deterministic while waiting for child exit.
- Add boot ID to new process identities and clean interrupted atomic temp files.
- Reject weak state/lock modes and symlinked or replaceable state ancestors.
- Expand deterministic coverage for lock waits, SIGKILL waiters, corrupt
  config/counters, missing commands, installers, and Python 3.14.

## [0.1.0] — 2026-08-29

- Add owner-scoped named semaphores with persistent FIFO tickets.
- Enforce stable per-name slot counts while work is active.
- Add fail-closed secure state and explicit `--best-effort` fallback.
- Add PID-start identity checks and child-aware crash recovery.
- Add monotonic wait timeouts and signal forwarding to command groups.
- Add human and JSON status plus explicit corrupt-state repair.
- Add deterministic concurrency/failure tests, Linux CI, installer, man page,
  reproducible release archives, and checksums.

[0.1.0]: https://github.com/korovin-aa97/fairsem/releases/tag/v0.1.0
[0.1.1]: https://github.com/korovin-aa97/fairsem/releases/tag/v0.1.1
[0.1.2]: https://github.com/korovin-aa97/fairsem/releases/tag/v0.1.2
[0.1.3]: https://github.com/korovin-aa97/fairsem/releases/tag/v0.1.3
