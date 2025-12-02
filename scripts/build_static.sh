#!/usr/bin/env bash
set -euo pipefail

# Build a static export of the site into distill_output/ using django-distill.
# - Creates/uses a local virtualenv (default: .venv)
# - Installs Python requirements
# - Runs collectstatic into distill_output/static (per settings.py override)
# - Runs distill-local to render pages
# - Copies media/ into distill_output/media for a self-contained artifact
# - Optionally zips the result (use --zip)

usage() {
  cat <<EOF
Usage: $0 [--venv <path>] [--zip]

Options:
  --venv <path>   Virtualenv directory to use/create (default: .venv)
  --zip           Create static-site-<timestamp>.zip from distill_output
EOF
}

VENV_DIR=".venv"
MAKE_ZIP=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --venv) VENV_DIR="$2"; shift 2 ;;
    --zip) MAKE_ZIP=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 1 ;;
  esac
done

PYTHON_BIN="python3"
command -v "$PYTHON_BIN" >/dev/null 2>&1 || { echo "python3 not found in PATH" >&2; exit 1; }

if [[ ! -x "$VENV_DIR/bin/python" ]]; then
  echo "Creating virtualenv at $VENV_DIR"
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
python -m pip install -U pip wheel >/dev/null
echo "Installing requirements..."
pip install -r requirements.txt

echo "Running static build (django-distill)..."
# Ensure whitenoise manifest storage has a fresh manifest
python manage.py collectstatic --noinput
python manage.py distill-local --force

echo "Copying media into distill_output/media ..."
mkdir -p distill_output/media
rsync -a --delete media/ distill_output/media/ || true

if [[ "$MAKE_ZIP" -eq 1 ]]; then
  TS=$(date +%Y%m%d-%H%M%S)
  ARCHIVE="static-site-${TS}.zip"
  echo "Creating archive: $ARCHIVE"
  (cd distill_output && zip -qr "../$ARCHIVE" .)
  echo "Archive created at: $ARCHIVE"
fi

echo "Done. Static site is in distill_output/"

