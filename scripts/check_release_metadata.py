#!/usr/bin/env python3
"""Fail when public version/checksum metadata drifts across release surfaces."""

from __future__ import annotations

import argparse
import hashlib
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def require(text: str, expected: str, surface: str) -> None:
    if expected not in text:
        raise SystemExit(f"release metadata mismatch in {surface}: missing {expected!r}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check FairSem version, archive, and published release metadata."
    )
    parser.add_argument(
        "--skip-published-formula-checksum",
        action="store_true",
        help=(
            "validate the candidate archive without requiring it to match the "
            "already-published Homebrew formula"
        ),
    )
    args = parser.parse_args()
    binary = read("bin/fairsem")
    match = re.search(r'^VERSION = "([0-9]+\.[0-9]+\.[0-9]+)"$', binary, re.MULTILINE)
    if match is None:
        raise SystemExit("cannot find semantic VERSION in bin/fairsem")
    version = match.group(1)
    archive_name = f"fairsem-v{version}.tar.gz"

    build_script = read("scripts/build_release.py")
    require(build_script, f'VERSION = "{version}"', "build script")
    require(read("scripts/rehearse_release.sh"), archive_name, "rehearsal script")
    require(read("man/fairsem.1"), f'"fairsem {version}"', "man page")
    formula = read("Formula/fairsem.rb")
    require(formula, f"/v{version}/{archive_name}", "Homebrew formula URL")
    require(formula, f'fairsem {version}', "Homebrew formula test")
    require(read("CHANGELOG.md"), f"## [{version}]", "changelog")
    if not (ROOT / f"docs/RELEASE_NOTES_v{version}.md").is_file():
        raise SystemExit(f"missing release notes for v{version}")

    svg_relative = "docs/assets/social-preview.svg"
    png_relative = "docs/assets/social-preview.png"
    require(read("README.md"), f"]({svg_relative})", "README hero")
    require(build_script, f'"{svg_relative}"', "build script")
    require(build_script, f'"{png_relative}"', "build script")
    svg = read(svg_relative)
    require(svg, 'width="1280" height="640"', "social preview SVG dimensions")
    require(svg, "<title", "social preview SVG accessibility")
    require(svg, "<desc", "social preview SVG accessibility")
    png = (ROOT / png_relative).read_bytes()
    if not png.startswith(b"\x89PNG\r\n\x1a\n") or len(png) < 24:
        raise SystemExit("social preview PNG is missing or invalid")
    if struct.unpack(">II", png[16:24]) != (1280, 640):
        raise SystemExit("social preview PNG must be exactly 1280x640")

    archive = ROOT / "dist" / archive_name
    sums = ROOT / "dist" / "SHA256SUMS"
    if archive.is_file() and sums.is_file():
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        expected_line = f"{digest}  {archive_name}\n"
        if sums.read_text(encoding="ascii") != expected_line:
            raise SystemExit("SHA256SUMS does not match the built archive")
        if not args.skip_published_formula_checksum:
            require(formula, f'sha256 "{digest}"', "Homebrew formula checksum")

    print(f"release metadata is consistent for v{version}")


if __name__ == "__main__":
    main()
