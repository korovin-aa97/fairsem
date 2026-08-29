# FairSem v0.1.3

This is the first FairSem release published with GitHub's repository-level
immutable releases policy enabled. Runtime behavior is unchanged from v0.1.2.

## Immutable supply-chain record

The release tag and uploaded assets become locked when the prepared draft is
published. GitHub also generates a release attestation covering the tag,
commit, and assets. This protects consumers from later tag movement or asset
replacement.

The release retains the accessible README illustration introduced in v0.1.2
and all v0.1.1 correctness fixes for lock deadlines, signal forwarding, stale
recovery, and fail-closed state validation.

## Install

```bash
sha256sum --check SHA256SUMS
tar -xzf fairsem-v0.1.3.tar.gz
cd fairsem-v0.1.3
./install.sh --prefix "$HOME/.local"
"$HOME/.local/bin/fairsem" --version
```

The deterministic 23-case suite runs on Python 3.10–3.14 across Ubuntu 22.04
and 24.04. The Homebrew formula is audited and tested against the exact public
release archive.

See [the contract](https://github.com/korovin-aa97/fairsem/blob/v0.1.3/docs/CONTRACT.md)
for precise guarantees and exit codes.
