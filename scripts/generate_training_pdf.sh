#!/usr/bin/env bash
# Generate a single PDF from training/*.md using pandoc if available.
# Usage: ./scripts/generate_training_pdf.sh /path/to/repo/output.pdf
# English comments: minimal, clear behaviour.
set -euo pipefail

OUTFILE="${1:-./training_package.pdf}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TRAINING_DIR="$REPO_ROOT/training"

if [ ! -d "$TRAINING_DIR" ]; then
  echo "Training directory not found: $TRAINING_DIR" >&2
  exit 2
fi

# Check for pandoc
if ! command -v pandoc >/dev/null 2>&1; then
  cat <<EOF
pandoc is not installed. To produce a PDF install pandoc and a LaTeX engine.
On Debian/Ubuntu:
  sudo apt update
  sudo apt install -y pandoc texlive-xetex
Then re-run this script.
This script will still produce a concatenated Markdown file at ./training_combined.md if pandoc is not available.
EOF
  # Create combined markdown as fallback
  COMBINED="./training_combined.md"
  echo "Creating combined markdown at $COMBINED"
  rm -f "$COMBINED"
  for f in "$TRAINING_DIR"/*.md; do
    echo -e "\n\n<!-- START $f -->\n\n" >> "$COMBINED"
    sed '' "$f" >> "$COMBINED"
  done
  echo "Combined markdown created. Install pandoc to render PDF."
  exit 0
fi

# Create a temporary ordered list of files: README_TRAINING first if exists, then modules sorted
TMPMD="$(mktemp --suffix=.md)"
trap 'rm -f "$TMPMD"' EXIT

# Ensure README_TRAINING first if present
if [ -f "$TRAINING_DIR/README_TRAINING.md" ]; then
  echo "" > "$TMPMD"
  sed '' "$TRAINING_DIR/README_TRAINING.md" >> "$TMPMD"
fi

for f in "$TRAINING_DIR"/*.md; do
  # skip README if already added
  if [ "$(basename "$f")" = "README_TRAINING.md" ]; then
    continue
  fi
  echo -e "\n\n<!-- START $(basename "$f") -->\n\n" >> "$TMPMD"
  sed '' "$f" >> "$TMPMD"
done

echo "Generating PDF with pandoc -> $OUTFILE"
pandoc "$TMPMD" -o "$OUTFILE" --pdf-engine=xelatex --metadata title="Training & Betriebsanleitung" \
  -V geometry:margin=1in -V mainfont="DejaVu Serif" || {
    echo "pandoc failed to generate PDF. Check pandoc/xelatex installation." >&2
    exit 3
  }

echo "PDF created: $OUTFILE"