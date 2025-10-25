#!/usr/bin/env bash
# Mount image read-only using loop device and run Python scanner.
# At the end, optionally call encrypt_reports.sh if auto_encrypt is enabled in config.
# Usage: ./analyze.sh /path/to/image.dd /path/to/case_dir
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 /path/to/image.dd /path/to/case_dir"
  exit 2
fi

IMAGE="$1"
CASE_DIR="$2"
MOUNT_DIR="$CASE_DIR/mount"
REPORT_DIR="$CASE_DIR/reports"
mkdir -p "$MOUNT_DIR" "$REPORT_DIR"

# Set up loop device (with partitions if present)
LOOP=$(losetup --show -fP "$IMAGE")
trap 'losetup -d "$LOOP" || true' EXIT

echo "Loop device: $LOOP"

# Try to mount first partition if exists, else mount whole loop device read-only
if [ -b "${LOOP}p1" ]; then
  echo "Mounting first partition ${LOOP}p1 read-only..."
  mount -o ro "${LOOP}p1" "$MOUNT_DIR" || { echo "Mount failed"; exit 1; }
else
  echo "Mounting whole device $LOOP read-only..."
  mount -o ro "$LOOP" "$MOUNT_DIR" || { echo "Mount failed"; exit 1; }
fi

echo "Mounted at $MOUNT_DIR"

# Optional tools
if command -v bulk_extractor >/dev/null 2>&1; then
  echo "Running bulk_extractor (optional)..."
  bulk_extractor -o "$REPORT_DIR/bulk_extractor" "$IMAGE" || true
else
  echo "bulk_extractor not found; skipping."
fi

if command -v yara >/dev/null 2>&1 && [ -d "yara_rules" ]; then
  echo "Running yara rules..."
  yara -r yara_rules/wallet_candidates.yar "$MOUNT_DIR" > "$REPORT_DIR/yara_matches.txt" || true
else
  echo "yara not found or rules missing; skipping yara."
fi

# Run Python scanner (walks filesystem, produces JSON + CSV)
python3 tools/modules/search.py --root "$MOUNT_DIR" --outdir "$REPORT_DIR"

# Unmount
umount "$MOUNT_DIR" || true
echo "Analyse abgeschlossen. Reports in $REPORT_DIR"

# Optionally verify integrity if image.sha256 exists next to image
if [ -f "${IMAGE}.sha256" ]; then
  echo "Verifying image integrity..."
  bash scripts/verify_integrity.sh "$IMAGE" "${IMAGE}.sha256" || echo "Warning: integrity check failed"
fi

# Read config to decide on auto encryption
CFG="${CASE_DIR}/config.ini"
AUTO_ENCRYPT="no"
if [ -f "$CFG" ]; then
  AUTO_ENCRYPT=$(awk -F'=' '/^auto_encrypt/ {gsub(/ /,"",$2); print tolower($2)}' "$CFG" | head -n1 || echo "no")
fi

if [ "$AUTO_ENCRYPT" = "yes" ]; then
  echo "Auto-encrypt enabled in config. Running encrypt_reports.sh..."
  bash scripts/encrypt_reports.sh "$CASE_DIR"
else
  echo "Auto-encrypt disabled. Run scripts/encrypt_reports.sh manually to encrypt."
fi