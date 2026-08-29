# Security policy

## Supported versions

Security fixes are provided for the latest tagged release.

## Reporting a vulnerability

Please use GitHub's private **Report a vulnerability** form for this repository
rather than a public issue. Include the FairSem version, Linux distribution,
state-directory configuration, impact, and a minimal reproduction. Expect an
acknowledgement within 72 hours.

Do not include secrets or sensitive command arguments. FairSem's local state
is intentionally owner-readable and status exposes command arguments; it is
not a secret store or a security boundary between processes owned by the same
user.

## Security model

The state root, semaphore directories, and lock are owner-only. Unsafe paths
fail closed. State writes are atomic. PID plus `/proc` start time prevents PID
reuse from impersonating an old holder. `--best-effort` explicitly opts out of
admission when secure state setup is unavailable and is never automatic.
