#!/usr/bin/env python3
"""
Normalize Obsidian daily notes.

For every file named "YYYY-MM-DD.md" or "YYYY-MM-DD Some title.md":
    1. Ensure the frontmatter has a `title` property (adds one if missing).
    2. If the filename has a title after the date, move it into `title`
        and rename the file to just "YYYY-MM-DD.md".

Usage:
    python3 fix_daily_notes.py "/path/to/Daily Notes"            # dry run (default)
    python3 fix_daily_notes.py "/path/to/Daily Notes" --apply    # make changes

Notes:
  * Never overwrites an existing non-empty `title` that differs from the
    filename suffix, and never overwrites an existing date-only file.
    These are reported as CONFLICT and left untouched.
  * Renaming outside Obsidian does NOT update [[wikilinks]] that point at the
    old filename. Close Obsidian first, or use the Obsidian CLI version if
    other notes link to these ones.
  * Back up the folder before using --apply.
"""
import argparse
import re
import sys
from pathlib import Path

NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:\s+(.+))?$")
TITLE_LINE = re.compile(r"^title\s*:\s*(.*?)\s*$")
LEADING_JUNK = " -\u2013\u2014:_"  # space, hyphen, en dash, em dash, colon, underscore


def yaml_scalar(text: str) -> str:
    """Plain scalar when safe, double-quoted when YAML would misread it."""
    needs_quotes = (
        re.search(r":\s|\s#|:$", text)
        or re.match(r"""^[\[\]{}&*!|>'"%@`?-]""", text)
        or text.lower() in {"yes", "no", "true", "false", "null", "~", "on", "off"}
    )
    if needs_quotes:
        return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return text


def unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def process(path: Path, apply: bool) -> None:
    m = NAME.match(path.stem)
    if not m:
        print(f"SKIP      {path.name} (not a daily note name)")
        return

    date, suffix = m.group(1), (m.group(2) or "").strip(LEADING_JUNK).strip()

    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.splitlines(keepends=True)

    fm_end = None
    has_fm = bool(lines) and lines[0].rstrip("\r\n") == "---"
    if has_fm:
        for i in range(1, len(lines)):
            if lines[i].rstrip("\r\n") in ("---", "..."):
                fm_end = i
                break
        if fm_end is None:
            print(f"SKIP      {path.name} (frontmatter never closes, fix by hand)")
            return

    new_line = f"title: {yaml_scalar(suffix)}".rstrip() + nl
    changed_text = False

    if not has_fm:
        lines = ["---" + nl, new_line, "---" + nl] + lines
        changed_text = True
        action = "added frontmatter + title"
    else:
        idx = None
        existing = ""
        for i in range(1, fm_end):
            tm = TITLE_LINE.match(lines[i].rstrip("\r\n"))
            if tm:
                idx, existing = i, unquote(tm.group(1))
                break

        if idx is None:
            lines.insert(fm_end, new_line)
            changed_text = True
            action = "added title"
        elif existing == "" and suffix:
            lines[idx] = new_line
            changed_text = True
            action = "filled empty title"
        elif existing and suffix and existing != suffix:
            print(f"CONFLICT  {path.name}: title is already '{existing}', left untouched")
            return
        else:
            action = "title already present"

    target = path.with_name(f"{date}.md")
    will_rename = bool(suffix) and path.name != target.name
    if will_rename and target.exists():
        print(f"CONFLICT  {path.name}: {target.name} already exists, left untouched")
        return

    if not changed_text and not will_rename:
        print(f"OK        {path.name} ({action})")
        return

    parts = [action]
    if will_rename:
        parts.append(f"rename -> {target.name}")
    print(f"{'CHANGE' if apply else 'WOULD'}    {path.name}: " + "; ".join(parts))

    if apply:
        if changed_text:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write("".join(lines))
        if will_rename:
            path.rename(target)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", type=Path)
    ap.add_argument("--apply", action="store_true", help="write changes (default is a dry run)")
    args = ap.parse_args()

    if not args.folder.is_dir():
        print(f"Not a folder: {args.folder}", file=sys.stderr)
        return 2

    for path in sorted(args.folder.glob("*.md")):
        process(path, args.apply)

    if not args.apply:
        print("\nDry run only. Re-run with --apply to make these changes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())