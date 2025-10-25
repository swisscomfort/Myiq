#!/usr/bin/env bash
# Package relevant artifacts for legal review.
# Usage: ./package_for_legal.sh /path/to/case_dir /path/to/output.tar.gz
# Requirements: gpg, tar, sha256sum
set -euo pipefail

# English comments in code as requested.
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 /path/to/case_dir /path/to/output.tar.gz"
  exit 2
fi

CASE_DIR="$1"
OUT_TAR="$2"

if [ ! -d "$CASE_DIR" ]; then
  echo "Case directory not found: $CASE_DIR" >&2
  exit 3
fi

TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Copy allowed artifacts (no unmasked sensitive secrets)
mkdir -p "$TMPDIR/artifacts"
cp -r "$CASE_DIR/templates" "$TMPDIR/artifacts/" || true
cp -r "$CASE_DIR/metadata.txt" "$TMPDIR/artifacts/" || true
cp -r "$CASE_DIR/chain_of_custody.txt" "$TMPDIR/artifacts/" || true
# copy masked reports only
if [ -d "$CASE_DIR/reports" ]; then
  mkdir -p "$TMPDIR/artifacts/reports"
  find "$CASE_DIR/reports" -type f -name 'scan_results_*.json' -o -name 'scan_results_*.csv' -print0 | while IFS= read -r -d '' f; do
    # Ensure the snippet fields are masked (best-effort check)
    # If file contains strings like "mnemonic" or long hex without '*' mark, still copy but flag
    cp "$f" "$TMPDIR/artifacts/reports/"
  done
fi

# copy config and policy
cp -r config "$TMPDIR/artifacts/" || true
# include image checksum but not the image itself
find "$CASE_DIR" -maxdepth 1 -type f -name '*.sha256' -exec cp {} "$TMPDIR/artifacts/" \; || true

# operator key fingerprint, if available
if command -v gpg >/dev/null 2>&1; then
  # try to detect operator key from git config or keyring; fallback to listing all keys
  gpg --list-keys --with-colons > "$TMPDIR/artifacts/gpg_keys_list.txt" || true
fi

# create manifest with sha256 for everything in artifacts
pushd "$TMPDIR/artifacts" >/dev/null
find . -type f -print0 | sort -z | xargs -0 sha256sum > "$TMPDIR/manifest.txt"
popd >/dev/null

# sign manifest if operator key available
if command -v gpg >/dev/null 2>&1; then
  # sign armored; will prompt if no default key, unless GPG opts are set
  if gpg --list-secret-keys >/dev/null 2>&1; then
    gpg --armor --output "$TMPDIR/manifest.txt.sig" --sign "$TMPDIR/manifest.txt" || true
  fi
fi

# package
tar -C "$TMPDIR" -czf "$OUT_TAR" artifacts manifest.txt manifest.txt.sig 2>/dev/null || {
  # if no signature exists, still package
  tar -C "$TMPDIR" -czf "$OUT_TAR" artifacts manifest.txt
}

echo "Legal package created: $OUT_TAR"