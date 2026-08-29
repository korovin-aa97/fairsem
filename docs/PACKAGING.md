# Packaging

The supported v0.1 distribution is the checksummed GitHub release archive.
The installer accepts an arbitrary absolute prefix and `DESTDIR`-style staging,
which is sufficient for downstream distro packages.

## Homebrew/Linuxbrew candidate

[`Formula/fairsem.rb`](../Formula/fairsem.rb) is pinned to the exact v0.1.0
release archive and checksum. After the public release exists, validate it on
a Linuxbrew host:

```bash
brew audit --strict Formula/fairsem.rb
brew install --build-from-source ./Formula/fairsem.rb
brew test fairsem
brew uninstall fairsem
```

Only then copy the formula to an existing maintained tap or propose it to an
appropriate registry. Creating a one-package tap solely to claim distribution
is intentionally deferred.

## Distribution packages

Stage without root:

```bash
./install.sh --prefix /usr --destdir "$PKGROOT"
```

This produces only:

```text
$PKGROOT/usr/bin/fairsem
$PKGROOT/usr/share/man/man1/fairsem.1
```

No service, state directory, network access, or post-install hook is required.
Runtime state is created per user on first use.

## Language registries

PyPI, npm, crates.io, and RubyGems were checked for name conflicts, but FairSem
is not a language library and v0.1 is not published there. Do not create a thin
registry wrapper until users need that installation path and it can be
maintained.
