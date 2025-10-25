#!/usr/bin/env bash
# Verify sha256 stored in .sha256 file matches actual image file.
# Usage: ./verify_integrity.sh /path/to/image.dd /path/to/image.dd.sha256
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 /path/to/image.dd /path/to/image.dd.sha256"
  exit 2
fi

IMAGE="$1"
SUMFILE="$2"

if [ ! -f "$IMAGE" ] || [ ! -f "$SUMFILE" ]; then
  echo "Missing image or sumfile."
  exit 3
fi

EXPECTED=$(awk '{print $1}' "$SUMFILE")
ACTUAL=$(sha256sum "$IMAGE" | awk '{print $1}')

if [ "$EXPECTED" = "$ACTUAL" ]; then
  echo "OK: integrity verified."
  exit 0
else
  echo "MISMATCH: expected $EXPECTED but got $ACTUAL"
  exit 4
fi