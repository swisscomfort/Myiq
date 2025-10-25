#!/usr/bin/env bash
# Create a forensic image using dd and compute sha256
# Usage: ./image_disk.sh /dev/sdX /path/to/output/image.dd
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 /dev/sdX /path/to/output/image.dd"
  exit 2
fi

DEVICE="$1"
IMAGE="$2"
DIR=$(dirname "$IMAGE")
mkdir -p "$DIR"

echo "Creating image of $DEVICE -> $IMAGE"
# Basic dd imaging. For better forensic logs consider dcfldd or guymager.
# bs=4M for reasonable speed; adjust if needed.
dd if="$DEVICE" of="$IMAGE" bs=4M conv=sync,noerror status=progress

echo "Computing sha256..."
sha256sum "$IMAGE" > "${IMAGE}.sha256"

echo "Image and checksum created."