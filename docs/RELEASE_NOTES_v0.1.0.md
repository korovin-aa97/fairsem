# FairSem v0.1.0

The first public release of FairSem: a fair, observable semaphore for expensive
commands sharing one Linux machine.

## Highlights

- Persistent FIFO tickets with a strict slot ceiling.
- Human and stable JSON views of holders, waiters, and capacity.
- Fail-closed owner-only state; explicit, noisy `--best-effort` escape hatch.
- PID plus `/proc` start identity, zombie cleanup, and child-aware crash
  recovery—even if the FairSem wrapper is killed.
- Monotonic wait timeouts, cancellation cleanup, and process-group signal
  forwarding.
- No runtime packages beyond Linux, `/proc`, and Python 3.10+.

## Install

Download both release files, verify the archive, inspect it, and install:

```bash
sha256sum --check SHA256SUMS
tar -xzf fairsem-v0.1.0.tar.gz
cd fairsem-v0.1.0
./install.sh --prefix "$HOME/.local"
```

## Validation evidence

The deterministic 15-case suite passed on Python 3.10, 3.11, 3.12, and 3.13,
plus clean Ubuntu 22.04 and 24.04 containers. It includes a 24-process/3-slot
stress case, controlled FIFO progress, signal/KILL recovery, PID reuse,
timeouts, corruption, fail-closed paths, nesting, names, JSON, and command
status propagation. The release archive is byte-reproducible and its exact
install/run/status/uninstall path was rehearsed in clean containers.

## Limits

Linux-only, one user, one machine. FairSem is not a distributed lock or
resource limiter. Commands that daemonize or escape their process group are
outside its lifecycle guarantee. Priorities are intentionally deferred.

See [the contract](https://github.com/korovin-aa97/fairsem/blob/v0.1.0/docs/CONTRACT.md)
for precise guarantees and exit codes.
