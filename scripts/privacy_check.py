#!/usr/bin/env python3
"""
Privacy check — scans Quartz `content/` for Amazon-confidential patterns.

Exits non-zero if any banned pattern is found. Must pass before
`npx quartz build`, before any `git push`, and before any deploy.

Usage:
    python3 scripts/privacy_check.py              # scan content/
    python3 scripts/privacy_check.py --path X     # scan X
    python3 scripts/privacy_check.py --strict     # also scan .md in repo root

Banned patterns live in .privacy/patterns.txt (one per line, case-insensitive).
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATTERNS_FILE = ROOT / ".privacy" / "patterns.txt"


def load_patterns():
    patterns = []
    for raw in PATTERNS_FILE.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append(line)
    return patterns


def scan_file(path: Path, patterns: list[str]) -> list[tuple[int, str, str]]:
    hits = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return hits
    for i, line in enumerate(text.splitlines(), start=1):
        for pat in patterns:
            # Use word boundaries for short (<=6 char) alphanumeric patterns to avoid
            # substring false positives (e.g. "PAP" matching "paper"). Longer patterns
            # and patterns with non-word characters match literally.
            if len(pat) <= 6 and pat.replace("_", "").isalnum():
                regex = r"\b" + re.escape(pat) + r"\b"
            else:
                regex = re.escape(pat)
            if re.search(regex, line, re.IGNORECASE):
                hits.append((i, pat, line.strip()[:200]))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default="content", help="directory to scan")
    ap.add_argument("--strict", action="store_true", help="also scan markdown in repo root")
    args = ap.parse_args()

    patterns = load_patterns()
    scan_root = ROOT / args.path
    files = list(scan_root.rglob("*.md")) + list(scan_root.rglob("*.html"))
    if args.strict:
        files += [p for p in ROOT.glob("*.md")]

    total_hits = 0
    for f in files:
        hits = scan_file(f, patterns)
        if hits:
            rel = f.relative_to(ROOT)
            print(f"\n❌ {rel}")
            for line_no, pat, line in hits:
                print(f"   L{line_no}  [{pat}]  {line}")
            total_hits += len(hits)

    if total_hits == 0:
        print(f"✅ Privacy check passed — scanned {len(files)} file(s) against "
              f"{len(patterns)} banned pattern(s).")
        return 0

    print(f"\n❌ Privacy check FAILED — {total_hits} hit(s) across banned patterns.")
    print("   Remove or rewrite flagged content before building or deploying.")
    print("   Amazon-confidential references MUST NOT appear on the public site.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
