#!/usr/bin/env bash
set -euo pipefail

# Reversible pruner for legacy templates/static not used by the new frontend.
# Default behavior is DRY-RUN (prints what would move). Use --apply to move.
# Use --undo to restore last cleanup from the backup directory.

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
BACKUP_BASE="/home/kali/DEV/depricated"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$BACKUP_BASE/${TIMESTAMP}-cleanup"

MODE="dry"
if [[ "${1:-}" == "--apply" ]]; then MODE="apply"; fi
if [[ "${1:-}" == "--undo" ]]; then MODE="undo"; fi

manifest_path() {
  echo "$1/manifest.txt"
}

latest_backup_dir() {
  ls -1dt "$BACKUP_BASE"/*-cleanup 2>/dev/null | head -n1 || true
}

ensure_backup_dir() {
  mkdir -p "$BACKUP_DIR"
}

record_move() {
  # $1 = src, $2 = dst
  echo "$1 => $2" >> "$(manifest_path "$BACKUP_DIR")"
}

move_preserve_tree() {
  local src="$1"; shift
  local dst_root="$1"; shift
  local dst="$dst_root/$src"
  mkdir -p "$(dirname "$dst")"
  mv "$src" "$dst"
  record_move "$src" "$dst"
}

delete_empty_dirs() {
  find "$1" -type d -empty -delete || true
}

list_template_candidates() {
  # Keep: templates/newfrontend/** and templates/partials/_footer.html
  find templates -type f \
    ! -path 'templates/newfrontend/*' \
    ! -path 'templates/partials/_footer.html'
}

list_static_candidates() {
  local root='coralcity/static'
  # Keep these paths and files that are referenced by the newfrontend
  # - newfront/** assets
  # - flags/** (used by language switcher)
  # - textures/** and jsm/** (three.js demo)
  # - logo.png and loader*.mp4, loader-bg-white.mp4
  # Everything else under coralcity/static is a candidate
  find "$root" -mindepth 1 -maxdepth 1 -print0 | while IFS= read -r -d '' p; do
    base="$(basename "$p")"
    case "$base" in
      newfront|flags|textures|jsm)
        continue ;; # keep
      logo.png|footer-bg.png|footer.mp4|loader-sm.mp4|loader-sm-white-faster.mp4|loader-bg-fast.mp4|loader-bg-white.mp4|logo-wt.jpeg|"Copy of kuzey emlak.png")
        continue ;; # keep these files at root
    esac
    echo "$p"
  done
}

undo_from_manifest() {
  local manifest_file="$1"
  [[ -f "$manifest_file" ]] || { echo "Manifest not found: $manifest_file" >&2; exit 1; }
  # Reverse order to move deeper files first
  tac "$manifest_file" | while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    local src dst
    src="${line%% => *}"
    dst="${line##* => }"
    # Move back to original location
    mkdir -p "$(dirname "$src")"
    mv "$dst" "$src"
  done
  # Optionally remove now-empty backup dir
  rmdir "$(dirname "$manifest_file")" 2>/dev/null || true
}

run_dry() {
  echo "[DRY-RUN] These items would be moved to $BACKUP_DIR" >&2
  echo "-- Templates --"
  list_template_candidates || true
  echo "-- Static --"
  list_static_candidates || true
}

run_apply() {
  ensure_backup_dir
  echo "Backing up to: $BACKUP_DIR"
  : > "$(manifest_path "$BACKUP_DIR")"

  local any=0
  # Templates
  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    if [[ -f "$f" ]]; then
      move_preserve_tree "$f" "$BACKUP_DIR"; any=1
    fi
  done < <(list_template_candidates)

  # Static (top-level dirs/files)
  while IFS= read -r p; do
    [[ -z "$p" ]] && continue
    if [[ -e "$p" ]]; then
      move_preserve_tree "$p" "$BACKUP_DIR"; any=1
    fi
  done < <(list_static_candidates)

  delete_empty_dirs templates || true
  delete_empty_dirs coralcity/static || true

  if [[ "$any" == "0" ]]; then
    echo "Nothing moved."
    rm -f "$(manifest_path "$BACKUP_DIR")"
    rmdir "$BACKUP_DIR" 2>/dev/null || true
  else
    echo "Move complete. Manifest: $(manifest_path "$BACKUP_DIR")"
  fi
}

run_undo() {
  local latest
  latest="$(latest_backup_dir)"
  if [[ -z "$latest" ]]; then
    echo "No backup directories found under $BACKUP_BASE" >&2
    exit 1
  fi
  echo "Restoring from: $latest"
  undo_from_manifest "$(manifest_path "$latest")"
  echo "Restore complete."
}

case "$MODE" in
  dry) run_dry ;;
  apply) run_apply ;;
  undo) run_undo ;;
  *) echo "Usage: $0 [--apply|--undo]" >&2; exit 1 ;;
esac

