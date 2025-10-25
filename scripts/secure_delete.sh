#!/usr/bin/env bash
# Securely delete files (shred fallback). Use carefully.
# Usage: ./secure_delete.sh /path/to/file_or_dir
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /path/to/file_or_dir"
  exit 2
fi

TARGET="$1"

if [ -d "$TARGET" ]; then
  # find files and shred, then remove dirs
  find "$TARGET" -type f -print0 | while IFS= read -r -d '' f; do
    echo "Shredding $f"
    shred -u -v -n 3 "$f" || rm -f "$f"
  done
  # attempt to remove empty dirs
  find "$TARGET" -type d -empty -delete || true
else
  echo "Shredding $TARGET"
  shred -u -v -n 3 "$TARGET" || rm -f "$TARGET"
fi

echo "Secure delete attempted for $TARGET"