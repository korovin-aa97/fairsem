#!/usr/bin/env sh
set -eu
CDPATH=''
export CDPATH

archive=${1:-dist/fairsem-v0.1.2.tar.gz}
archive=$(cd -- "$(dirname -- "$archive")" && pwd)/$(basename -- "$archive")
work=$(mktemp -d)
trap 'rm -rf -- "$work"' EXIT HUP INT TERM

tar -xzf "$archive" -C "$work"
release_dir=$work/fairsem-v0.1.2
install_root=$work/install-root

"$release_dir/install.sh" --prefix /usr/local --destdir "$install_root"
FAIRSEM_STATE_DIR=$work/state "$install_root/usr/local/bin/fairsem" --version
FAIRSEM_STATE_DIR=$work/state "$install_root/usr/local/bin/fairsem" run --name rehearsal --slots 2 -- true
FAIRSEM_STATE_DIR=$work/state "$install_root/usr/local/bin/fairsem" status --name rehearsal --json
"$release_dir/uninstall.sh" --prefix /usr/local --destdir "$install_root"
test ! -e "$install_root/usr/local/bin/fairsem"
test ! -e "$install_root/usr/local/share/man/man1/fairsem.1"
echo "release rehearsal passed"
