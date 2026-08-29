#!/usr/bin/env sh
set -eu

prefix=/usr/local
destdir=

usage() {
  echo "Usage: ./uninstall.sh [--prefix PATH] [--destdir PATH]" >&2
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

case "$prefix" in /*) ;; *) echo "uninstall.sh: --prefix must be absolute" >&2; exit 65 ;; esac
case "$destdir" in ""|/*) ;; *) echo "uninstall.sh: --destdir must be absolute" >&2; exit 65 ;; esac

rm -f -- "$destdir$prefix/bin/fairsem" "$destdir$prefix/share/man/man1/fairsem.1"
echo "removed FairSem from $destdir$prefix"
