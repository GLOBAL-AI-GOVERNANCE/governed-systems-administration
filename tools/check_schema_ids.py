#!/usr/bin/env python3
"""Check that every schema $id names this repository's published path.

Each absolute $id must have the form
https://raw.githubusercontent.com/GLOBAL-AI-GOVERNANCE/governed-systems-administration/<ref>/<path>
where <path> is the file's own repository path and <ref> is a release tag
listed in CHANGELOG.md or an allowed branch (main while the alpha has no
release tag). This module does not fetch the network; use
tools/check_schema_ids_online.sh for live resolution.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORG = "GLOBAL-AI-GOVERNANCE"
SOURCES = [("governed-systems-administration", "")]
ALLOWED_BRANCHES = ("main",)
RELEASE_HEADING = re.compile(r"^##\s+\[?v?(\d+\.\d+(?:\.\d+)?(?:-[0-9A-Za-z.]+)?)\]?(?:\s|$)", re.M)


def release_tags() -> set[str]:
    text = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8") if (ROOT / "CHANGELOG.md").exists() else ""
    return {"v" + version for version in RELEASE_HEADING.findall(text)}


def schema_ids() -> list[tuple[Path, str]]:
    found = []
    for path in sorted((ROOT / "schemas").glob("*.json")):
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
        identifier = document.get("$id") if isinstance(document, dict) else None
        if isinstance(identifier, str) and identifier.startswith(("http://", "https://")):
            found.append((path, identifier))
    return found


def offline_errors(items: list[tuple[Path, str]]) -> list[str]:
    refs = release_tags() | set(ALLOWED_BRANCHES)
    errors = []
    for path, identifier in items:
        relative = path.relative_to(ROOT).as_posix()
        for repo, local in SOURCES:
            prefix = f"https://raw.githubusercontent.com/{ORG}/{repo}/"
            if relative.startswith(local) and identifier.startswith(prefix):
                ref, _, id_path = identifier[len(prefix):].partition("/")
                if id_path != relative[len(local):]:
                    errors.append(f"{relative}: $id path {id_path} is not the file path")
                elif ref not in refs:
                    errors.append(f"{relative}: $id ref {ref} is not a CHANGELOG release or allowed branch")
                break
        else:
            errors.append(f"{relative}: $id {identifier} is not a published raw URL for this repository")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.parse_args()
    items = schema_ids()
    errors = offline_errors(items)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print(f"schema $id check passed for {len(items)} schema(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
