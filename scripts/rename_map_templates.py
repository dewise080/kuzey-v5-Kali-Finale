#!/usr/bin/env python3
"""
Rename all HTML templates in templates/newfrontend/maps by appending '_map_only'
before the .html extension. Skips files that already end with _map_only.html.

Usage:
  python scripts/rename_map_templates.py           # perform rename
  python scripts/rename_map_templates.py --dry-run # preview changes only

Notes:
  - Works recursively if you pass --recursive, otherwise only the top-level
    files in templates/newfrontend/maps are processed.
  - If the destination filename already exists, the file is skipped.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path


def find_maps_dir(start: Path) -> Path:
    """Return the maps directory path, or raise if not found."""
    candidate = (start / 'templates' / 'newfrontend' / 'maps').resolve()
    if candidate.exists() and candidate.is_dir():
        return candidate
    # Try relative to this script (in case cwd differs)
    here = Path(__file__).resolve().parent
    candidate = (here.parent / 'templates' / 'newfrontend' / 'maps').resolve()
    if candidate.exists() and candidate.is_dir():
        return candidate
    raise SystemExit("templates/newfrontend/maps directory not found from current location")


def plan_renames(maps_dir: Path, recursive: bool = False):
    pattern = '**/*.html' if recursive else '*.html'
    for p in maps_dir.glob(pattern):
        if not p.is_file():
            continue
        name = p.name
        if name.endswith('_map_only.html'):
            continue
        if not name.endswith('.html'):
            continue
        dest_name = name[:-5] + '_map_only.html'
        dest = p.with_name(dest_name)
        yield p, dest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true', help='Show what would change, do not modify files')
    ap.add_argument('--recursive', action='store_true', help='Rename in subfolders as well')
    args = ap.parse_args()

    maps_dir = find_maps_dir(Path.cwd())
    planned = list(plan_renames(maps_dir, recursive=args.recursive))

    if not planned:
        print('No files to rename.')
        return

    print(f'Target directory: {maps_dir}')
    print(f'Planned renames ({len(planned)}):')
    for src, dst in planned:
        print(f'  - {src.relative_to(maps_dir)} -> {dst.name}')

    if args.dry_run:
        print('Dry-run complete; no files modified.')
        return

    renamed = 0
    skipped = 0
    for src, dst in planned:
        if dst.exists():
            print(f'SKIP (exists): {dst}')
            skipped += 1
            continue
        src.rename(dst)
        print(f'RENAMED: {src.name} -> {dst.name}')
        renamed += 1

    print(f'Done. Renamed: {renamed}, Skipped: {skipped}')


if __name__ == '__main__':
    main()

