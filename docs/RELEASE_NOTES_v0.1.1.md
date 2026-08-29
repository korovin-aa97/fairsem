# FairSem v0.1.1

This correctness patch closes three post-release edge cases without expanding
FairSem's scope or dependencies.

## Fixed

- `--timeout` now includes state-lock contention. A stuck lock can no longer
  delay a timed run and then allow its command to start after the deadline.
- Explicit `--best-effort` runs now use the same process-group signal
  forwarding and exit-status propagation as admitted commands.
- Wrapper signal consumption is deterministic during child waits instead of
  depending on when the Python runtime returns from `waitpid(2)`.

State recovery is also stronger: new identities include Linux boot ID, stale
atomic-write temp files are removed under the lock, modes must be exactly
`0700`/`0600`, and symlinked or replaceable state ancestors fail closed.

## Install

```bash
sha256sum --check SHA256SUMS
tar -xzf fairsem-v0.1.1.tar.gz
cd fairsem-v0.1.1
./install.sh --prefix "$HOME/.local"
"$HOME/.local/bin/fairsem" --version
```

## Validation

The expanded deterministic suite covers 23 behavioral cases across Python
3.10–3.14 on Ubuntu 22.04 and 24.04. Additional adversarial runs repeat
signal forwarding and high-contention slot/fairness checks. The release
archive is byte-reproducible and rehearsed through checksum, install, run,
JSON status, and uninstall in a clean Linux environment.

See [the contract](https://github.com/korovin-aa97/fairsem/blob/v0.1.1/docs/CONTRACT.md)
for precise guarantees and exit codes.
