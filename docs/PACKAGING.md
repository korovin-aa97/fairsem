# Packaging

The supported v0.1 distribution is the checksummed GitHub release archive.
The installer accepts an arbitrary absolute prefix and `DESTDIR`-style staging,
which is sufficient for downstream distro packages.

## Homebrew/Linuxbrew candidate

[`Formula/fairsem.rb`](../Formula/fairsem.rb) is pinned to the exact v0.1.3
release archive and checksum. After the public release exists, validate it on
a Linuxbrew host. Current Homebrew audits formulae by tap-qualified name, so
use a disposable local tap rather than auditing the file path directly:

```bash
brew tap-new local/fairsem-test
cp Formula/fairsem.rb "$(brew --repository local/fairsem-test)/Formula/fairsem.rb"
brew audit --strict local/fairsem-test/fairsem
brew install --build-from-source local/fairsem-test/fairsem
brew test local/fairsem-test/fairsem
brew uninstall fairsem
brew untap local/fairsem-test
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
