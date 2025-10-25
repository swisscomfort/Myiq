#!/usr/bin/env bash
# Orchestrator: create image, run analysis, optionally encrypt results.
# Usage: ./start.sh /dev/sdX /path/to/output "Client Name"
set -euo pipefail

if [ "$#" -ne 3 ]; then
  echo "Usage: $0 /dev/sdX /path/to/output \"Client Name\""
  exit 2
fi

DEVICE="$1"
OUTDIR="$2"
CLIENT="$3"
TIMESTAMP=$(date -u +"%Y%m%dT%H%M%SZ")

mkdir -p "$OUTDIR"
case_dir="$OUTDIR/case_${TIMESTAMP}"
mkdir -p "$case_dir"
echo "Case directory: $case_dir"

# Copy templates and record metadata
cp -r templates "$case_dir/" || true
cp config/case_policy.ini "$case_dir/config.ini" || true
echo "device: $DEVICE" > "$case_dir/metadata.txt"
echo "client: $CLIENT" >> "$case_dir/metadata.txt"
echo "created_at: $TIMESTAMP" >> "$case_dir/metadata.txt"
echo "operator: $(whoami)@$(hostname)" >> "$case_dir/metadata.txt"

# Create image (calls scripts/image_disk.sh)
bash scripts/image_disk.sh "$DEVICE" "$case_dir/image.dd"

# Run analysis (analyze.sh may call encrypt_reports.sh depending on config)
bash scripts/analyze.sh "$case_dir/image.dd" "$case_dir"

echo "Fertig. Ergebnisse liegen in: $case_dir"