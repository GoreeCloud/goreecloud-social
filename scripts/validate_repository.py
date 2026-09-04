#!/usr/bin/env python3
"""Validate the GoreeCloud Social Development repository foundation."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_ROOT_FILES = {"README.md", "SPECIFICATIONS.md", "FEATURES.md", "BENEFITS.md", "COMPETITIVE-OBJECTIVES.md", "BRANDING.md", "USER-MANUAL.md", "VERSION", "goreecloud.platform.yaml"}


def main() -> int:
    failures: list[str] = []
    for name in sorted(REQUIRED_ROOT_FILES):
        path = ROOT / name
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            failures.append(f"missing or empty required root file: {name}")
    forbidden = [path.relative_to(ROOT).as_posix() for path in ROOT.rglob(".env*") if path.name not in {".env.example", ".env.template"}]
    if forbidden:
        failures.append("forbidden environment files present: " + ", ".join(forbidden))
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").is_file() else ""
    package = (ROOT / "src/goreecloud_social/__init__.py").read_text(encoding="utf-8") if (ROOT / "src/goreecloud_social/__init__.py").is_file() else ""
    if version and f'__version__ = "{version}"' not in package:
        failures.append("VERSION does not match goreecloud_social.__version__")
    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        return 1
    print("GoreeCloud Social repository structure validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
