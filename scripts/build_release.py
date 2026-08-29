#!/usr/bin/env python3
"""Build a byte-reproducible source/install archive and SHA-256 manifest."""

from __future__ import annotations

import gzip
import hashlib
import io
import tarfile
from pathlib import Path

VERSION = "0.1.1"
ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ARCHIVE = DIST / f"fairsem-v{VERSION}.tar.gz"
PREFIX = f"fairsem-v{VERSION}"
FILES = [
    "bin/fairsem",
    "man/fairsem.1",
    "docs/CONTRACT.md",
    "docs/COMPETITORS.md",
    "docs/RELEASE_NOTES_v0.1.1.md",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "install.sh",
    "uninstall.sh",
]
EXECUTABLES = {"bin/fairsem", "install.sh", "uninstall.sh"}


def build() -> None:
    DIST.mkdir(exist_ok=True)
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for relative in sorted(FILES):
            source = ROOT / relative
            payload = source.read_bytes()
            info = tarfile.TarInfo(f"{PREFIX}/{relative}")
            info.size = len(payload)
            info.mtime = 0
            info.uid = info.gid = 0
            info.uname = info.gname = "root"
            info.mode = 0o755 if relative in EXECUTABLES else 0o644
            archive.addfile(info, io.BytesIO(payload))
    with ARCHIVE.open("wb") as raw, gzip.GzipFile(
        filename="", mode="wb", fileobj=raw, mtime=0
    ) as compressed:
        compressed.write(buffer.getvalue())
    digest = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
    (DIST / "SHA256SUMS").write_text(f"{digest}  {ARCHIVE.name}\n", encoding="ascii")
    print(ARCHIVE)
    print(DIST / "SHA256SUMS")


if __name__ == "__main__":
    build()
