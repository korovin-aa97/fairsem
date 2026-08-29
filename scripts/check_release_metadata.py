#!/usr/bin/env python3
"""Fail when public version/checksum metadata drifts across release surfaces."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require(text: str, expected: str, surface: str) -> None:
    if expected not in text:
        raise SystemExit(f"release metadata mismatch in {surface}: missing {expected!r}")


def main() -> None:
    binary = read("bin/fairsem")
    match = re.search(r'^VERSION = "([0-9]+\.[0-9]+\.[0-9]+)"$', binary, re.MULTILINE)
    if match is None:
        raise SystemExit("cannot find semantic VERSION in bin/fairsem")
    version = match.group(1)
    archive_name = f"fairsem-v{version}.tar.gz"

    require(read("scripts/build_release.py"), f'VERSION = "{version}"', "build script")
    require(read("scripts/rehearse_release.sh"), archive_name, "rehearsal script")
    require(read("man/fairsem.1"), f'"fairsem {version}"', "man page")
    formula = read("Formula/fairsem.rb")
    require(formula, f"/v{version}/{archive_name}", "Homebrew formula URL")
    require(formula, f'fairsem {version}', "Homebrew formula test")
    require(read("CHANGELOG.md"), f"## [{version}]", "changelog")
    if not (ROOT / f"docs/RELEASE_NOTES_v{version}.md").is_file():
        raise SystemExit(f"missing release notes for v{version}")

    archive = ROOT / "dist" / archive_name
    sums = ROOT / "dist" / "SHA256SUMS"
    if archive.is_file() and sums.is_file():
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        expected_line = f"{digest}  {archive_name}\n"
        if sums.read_text(encoding="ascii") != expected_line:
            raise SystemExit("SHA256SUMS does not match the built archive")
        require(formula, f'sha256 "{digest}"', "Homebrew formula checksum")

    print(f"release metadata is consistent for v{version}")


if __name__ == "__main__":
    main()
