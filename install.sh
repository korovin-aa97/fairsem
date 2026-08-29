#!/usr/bin/env sh
set -eu
CDPATH=''
export CDPATH

prefix=/usr/local
destdir=

usage() {
  echo "Usage: ./install.sh [--prefix PATH] [--destdir PATH]" >&2
  exit "${1:-64}"
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --prefix) [ "$#" -ge 2 ] || usage; prefix=$2; shift 2 ;;
    --destdir) [ "$#" -ge 2 ] || usage; destdir=$2; shift 2 ;;
    -h|--help) usage 0 ;;
    *) usage ;;
  esac
done

case "$prefix" in /*) ;; *) echo "install.sh: --prefix must be absolute" >&2; exit 65 ;; esac
case "$destdir" in ""|/*) ;; *) echo "install.sh: --destdir must be absolute" >&2; exit 65 ;; esac

script_dir=$(cd -- "$(dirname -- "$0")" && pwd)
bin_dir=$destdir$prefix/bin
man_dir=$destdir$prefix/share/man/man1

install -d -m 0755 "$bin_dir" "$man_dir"
install -m 0755 "$script_dir/bin/fairsem" "$bin_dir/fairsem"
install -m 0644 "$script_dir/man/fairsem.1" "$man_dir/fairsem.1"
echo "installed $bin_dir/fairsem"
echo "installed $man_dir/fairsem.1"
