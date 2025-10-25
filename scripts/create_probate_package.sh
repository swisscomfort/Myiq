#!/usr/bin/env bash
# Create a probate-ready legal package for court/notary (improved).
# Behavior:
# - Validates required artifacts
# - Automatically includes any affidavit files found in case_dir/archives (md, md.asc, .gpg, .sig)
# - Builds manifest, signs manifest if local GPG secret key exists
# - Produces archives/probate_package_<timestamp>.tar.gz and logs action via scripts/log_event.sh if present
#
# Usage: ./scripts/create_probate_package.sh /path/to/case_dir /path/to/output/probate_package.tar.gz

set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 /path/to/case_dir /path/to/output/probate_package.tar.gz" >&2
  exit 2
fi

CASE_DIR="$1"
OUT_TAR="$2"

if [ ! -d "$CASE_DIR" ]; then
  echo "Case directory not found: $CASE_DIR" >&2
  exit 3
fi

LOG_HELPER="scripts/log_event.sh"
log_event() {
  # Invoke log helper if available; do not fail if logging fails.
  if [ -x "$LOG_HELPER" ]; then
    "$LOG_HELPER" "$CASE_DIR" "$1" "$2" "$3" >/dev/null 2>&1 || true
  fi
}

echo "Starting probate package creation for case: $CASE_DIR"

# Basic validations
if [ ! -f "$CASE_DIR/metadata.txt" ] || [ ! -f "$CASE_DIR/chain_of_custody.txt" ]; then
  echo "Required metadata or chain_of_custody missing." >&2
  log_event "error" "Missing metadata/chain_of_custody" 0
  exit 4
fi

# Find clearsigned consent (optional but strongly recommended)
CONSENT_FILE=$(find "$CASE_DIR/archives" -type f \( -iname '*consent*.*asc' -o -iname '*acknowledgement*.*asc' -o -iname '*consent*.*sig' \) | head -n1 || true)
if [ -z "$CONSENT_FILE" ]; then
  echo "Warning: clearsigned consent not found in $CASE_DIR/archives. Proceeding only if court-authorized." >&2
  log_event "warn" "Clearsigned consent not found" 0
else
  echo "Found consent file: $(basename "$CONSENT_FILE")"
  log_event "info" "Consent found: $(basename "$CONSENT_FILE")" 0
fi

# Collect affidavit files (prefer any clearsigned / encrypted variant)
AFFIDAVITS=$(find "$CASE_DIR/archives" -type f \( -iname 'expert_affidavit*' -o -iname '*affidavit*' \) | sort || true)
if [ -z "$AFFIDAVITS" ]; then
  echo "No affidavit files found in archives. Ensure expert affidavit is saved before packaging." >&2
  log_event "warn" "No affidavit found in archives" 0
else
  echo "Affidavit files to include:"
  echo "$AFFIDAVITS"
  log_event "info" "Affidavit files included" 0
fi

# Prepare temp workspace
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT
ART="$TMPDIR/artifacts"
mkdir -p "$ART"

# Copy core artifacts (but do not copy full image.dd unless explicitly authorized)
cp "$CASE_DIR/metadata.txt" "$ART/" || true
cp "$CASE_DIR/chain_of_custody.txt" "$ART/" || true
if [ -f "$CASE_DIR/image.dd.sha256" ]; then
  cp "$CASE_DIR/image.dd.sha256" "$ART/" || true
fi

# Copy directories if present (reports, exports, logs, archives)
for d in reports exports logs; do
  if [ -d "$CASE_DIR/$d" ]; then
    mkdir -p "$ART/$d"
    cp -r "$CASE_DIR/$d/"* "$ART/$d/" 2>/dev/null || true
  fi
done

# Copy the archives (consent, receipts, affidavit etc.), but only files, not large blobs
if [ -d "$CASE_DIR/archives" ]; then
  mkdir -p "$ART/archives"
  # copy all small files; skip any very large files (>200MB) unless authorized
  find "$CASE_DIR/archives" -maxdepth 1 -type f -print0 | while IFS= read -r -d '' f; do
    size=$(stat -c%s "$f" 2>/dev/null || echo 0)
    if [ "$size" -gt $((200*1024*1024)) ]; then
      echo "Skipping large archive file (needs manual review): $(basename "$f")" >&2
      log_event "warn" "Skipping large archive file: $(basename "$f")" 0
      continue
    fi
    cp "$f" "$ART/archives/" || true
  done
fi

# Ensure affidavit files (if present) are included under artifacts/archives/
if [ -n "$AFFIDAVITS" ]; then
  while IFS= read -r af; do
    if [ -f "$af" ]; then
      cp "$af" "$ART/archives/" || true
    fi
  done <<< "$AFFIDAVITS"
fi

# Create manifest (sha256s) for included files
pushd "$ART" >/dev/null
# create a sorted file list and compute sha256
find . -type f -print0 | sort -z | xargs -0 sha256sum > "$TMPDIR/manifest.txt" || true
popd >/dev/null

if [ ! -s "$TMPDIR/manifest.txt" ]; then
  echo "No artifacts collected for manifest; aborting." >&2
  log_event "error" "No artifacts for manifest" 0
  exit 5
fi

# Sign manifest if GPG secret key available
MANIFEST="$TMPDIR/manifest.txt"
MANIFEST_SIG="$TMPDIR/manifest.txt.sig"
if command -v gpg >/dev/null 2>&1 && gpg --list-secret-keys >/dev/null 2>&1; then
  echo "Signing manifest..."
  if gpg --yes --batch --armor --detach-sign --output "$MANIFEST_SIG" "$MANIFEST"; then
    echo "Manifest signed."
    log_event "info" "Manifest signed" 0
  else
    echo "Warning: manifest signing failed." >&2
    log_event "warn" "Manifest signing failed" 0
  fi
else
  echo "No local GPG secret key found; manifest will be unsigned."
  log_event "warn" "No local GPG key for manifest signing" 0
fi

# Create tar.gz package
mkdir -p "$(dirname "$OUT_TAR")"
pushd "$TMPDIR" >/dev/null
# Include artifacts directory and manifest files
if tar -czf "$OUT_TAR" artifacts manifest.txt manifest.txt.sig 2>/dev/null; then
  echo "Probate package created: $OUT_TAR"
  log_event "info" "Probate package created: $(basename "$OUT_TAR")" 100
else
  echo "Tar creation failed." >&2
  log_event "error" "Tar creation failed" 0
  popd >/dev/null
  exit 6
fi
popd >/dev/null

# Move package into case archives for record
mkdir -p "$CASE_DIR/archives"
mv "$OUT_TAR" "$CASE_DIR/archives/" || {
  echo "Warning: failed to move package into case archives; package remains at $OUT_TAR" >&2
  log_event "warn" "Failed to move package to case archives" 0
}
FINAL_PATH="$CASE_DIR/archives/$(basename "$OUT_TAR")"

# Optionally produce a short packaging log file in archives/
PACK_LOG="$CASE_DIR/archives/probate_package_$(date -u +%Y%m%dT%H%M%SZ).log"
{
  echo "probate_package: $(basename "$FINAL_PATH")"
  echo "created_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "manifest_count: $(wc -l < "$MANIFEST" || echo 0)"
  echo "included_affidavit: $( [ -n "$AFFIDAVITS" ] && echo yes || echo no )"
} > "$PACK_LOG" || true
chmod 600 "$PACK_LOG" || true

echo "Probate package stored at: $FINAL_PATH"
echo "Packaging log: $PACK_LOG"
log_event "info" "Probate package stored: $(basename "$FINAL_PATH")" 100

exit 0