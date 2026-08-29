# FairSem v0.1.2

This documentation patch makes FairSem's purpose understandable at a glance.
Runtime behavior is unchanged from v0.1.1.

## New visual overview

The README now opens with an accessible illustrated flow:

> many local jobs → fair queue → bounded parallel work

The source SVG includes a title and description for assistive technology. A
matching 1280×640 PNG is included for social previews and other surfaces that
do not render SVG. Both use a fixed high-contrast background, so they remain
legible in light and dark page themes without theme-specific controls.

## Install

```bash
sha256sum --check SHA256SUMS
tar -xzf fairsem-v0.1.2.tar.gz
cd fairsem-v0.1.2
./install.sh --prefix "$HOME/.local"
"$HOME/.local/bin/fairsem" --version
```

The release keeps the v0.1.1 correctness fixes for lock deadlines, signal
forwarding, stale recovery, and fail-closed state validation. The deterministic
23-case suite continues to run on Python 3.10–3.14 across Ubuntu 22.04 and
24.04.

See [the contract](https://github.com/korovin-aa97/fairsem/blob/v0.1.2/docs/CONTRACT.md)
for precise guarantees and exit codes.
