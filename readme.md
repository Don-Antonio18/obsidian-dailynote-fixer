# Obsidian Daily Notes Title Fixer

This script converts titled Obsidian daily notes such as:

```text
2026-10-30 Weekend plans.md
```

into the standard daily-note filename:

```text
2026-10-30.md
```

The original filename suffix is preserved in the note's YAML frontmatter as a
`title` property. This keeps Obsidian's date-based daily-note and calendar
workflows working while making the note title available to Bases, Dataview,
searches, and other metadata-driven views.

The script is intentionally conservative:

- It performs a dry run by default.
- It never overwrites an existing non-empty, different `title`.
- It never overwrites an existing date-only note during a rename.
- It skips files with frontmatter that never closes.
- It only processes `.md` files directly inside the folder you provide.

## Requirements

- Python 3.8 or newer
- An Obsidian vault containing the daily-notes folder
- A backup of the folder before applying changes

The script uses only Python's standard library. No packages or virtual
environment are required.

## Installation

### Option 1: Download the script

Save [`fix_obsidian_dailynotes.py`](./fix_obsidian_dailynotes.py) somewhere
convenient, such as a `scripts` folder.

### Option 2: Clone or copy this project

Copy this folder into your preferred development directory. The script can be
run from anywhere; the daily-notes folder is supplied as a command-line
argument.

Verify that Python is available:

```bash
python3 --version
```

On Windows, use `py --version` and replace `python3` with `py` in the commands
below if needed.

## Usage

Open a terminal and run a dry run first:

```bash
python3 /path/to/fix_obsidian_dailynotes.py "/path/to/Your Vault/Daily Notes"
```

The script prints the files it would change. It does not write or rename
anything during a dry run.

After reviewing the output and creating a backup, apply the changes:

```bash
python3 /path/to/fix_obsidian_dailynotes.py \
  "/path/to/Your Vault/Daily Notes" \
  --apply
```

If the script is in your current directory:

```bash
python3 fix_obsidian_dailynotes.py "/path/to/Your Vault/Daily Notes"
python3 fix_obsidian_dailynotes.py "/path/to/Your Vault/Daily Notes" --apply
```

### Windows example

```powershell
py .\fix_obsidian_dailynotes.py "C:\Users\you\Documents\Obsidian\My Vault\Daily Notes"
py .\fix_obsidian_dailynotes.py "C:\Users\you\Documents\Obsidian\My Vault\Daily Notes" --apply
```

Always quote paths that contain spaces.

## What the script changes

For each file whose name matches `YYYY-MM-DD.md` or
`YYYY-MM-DD Some title.md`, the script:

1. Reads the file as UTF-8.
2. Adds YAML frontmatter and a `title` property when the file has no
   frontmatter.
3. Adds `title` to existing frontmatter when it is missing.
4. Fills an empty `title` from the filename suffix.
5. Renames titled files to `YYYY-MM-DD.md`.

For example:

```text
2026-10-30 Weekend plans.md
```

becomes:

```markdown
---
title: Weekend plans
---

Notes for the day...
```

saved as `2026-10-30.md`.

Leading spaces, hyphens, en dashes, em dashes, colons, and underscores in the
filename suffix are removed before the title is written. Values that could be
misread by YAML are automatically quoted.

## Conflict and skip messages

The output uses these statuses:

- `WOULD`: a change would be made during a dry run.
- `CHANGE`: a change was made with `--apply`.
- `OK`: no change was needed.
- `CONFLICT`: the file was left untouched because applying the change could
  overwrite information or a destination file.
- `SKIP`: the filename or frontmatter could not be safely processed.

Resolve `CONFLICT` and `SKIP` messages manually, then run the script again.

## Recommended workflow

1. Close Obsidian, or at least avoid editing the affected notes while the
   script runs.
2. Back up the daily-notes folder or commit it to version control.
3. Run the script without `--apply`.
4. Review every proposed change.
5. Run it with `--apply`.
6. Reopen Obsidian and verify the daily-notes calendar, links, and metadata
   views.

## Important limitations

- The script does not recursively scan subfolders.
- It does not update `[[wikilinks]]`, Markdown links, embeds, or plugins that
  refer to the old filename. Renaming a note outside Obsidian may leave those
  references stale. Use Obsidian's own rename handling or update affected
  links separately.
- It does not parse or reformat arbitrary YAML. Existing frontmatter should
  be valid and must close with `---` or `...`.
- It does not replace a non-empty `title` that differs from the filename
  suffix. This protects existing metadata; resolve such files manually.
- Files with names that do not begin with a valid date in `YYYY-MM-DD` format
  are ignored.

## Troubleshooting

### `Not a folder`

Check the path and quote it if it contains spaces:

```bash
python3 fix_obsidian_dailynotes.py "/Users/you/Documents/My Vault/Daily Notes"
```

### `frontmatter never closes`

Open the reported note and add the missing closing `---` or `...` line, then
run the dry run again.

### `target already exists`

The date-only destination already exists. Compare the two notes and decide
which content should be kept before running the script again.

### `title is already ...`

The note already has a different non-empty title. Review it manually rather
than allowing an automated rename to change its metadata.

## License

Uses MIT license.
