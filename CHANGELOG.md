# Changelog

All notable changes are documented here. FairSem follows Semantic Versioning.

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
