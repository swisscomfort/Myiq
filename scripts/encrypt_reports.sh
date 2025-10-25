#!/usr/bin/env bash
# Encrypt case reports/images using GPG.
# Reads config from case_dir/config.ini or repo config/case_policy.ini
# Usage: ./encrypt_reports.sh /path/to/case_dir
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /path/to/case_dir"
  exit 2
fi

CASE_DIR="$1"
if [ ! -d "$CASE_DIR" ]; then
  echo "Case dir not found: $CASE_DIR"
  exit 3
fi

CONFIG="${CASE_DIR}/config.ini"
if [ ! -f "$CONFIG" ]; then
  CONFIG="config/case_policy.ini"
fi

if ! command -v gpg >/dev/null 2>&1; then
  echo "gpg not found. Install gnupg."
  exit 4
fi

# Simple ini reader: get value for a key
get_cfg() {
  local key="$1"
  awk -F'=' -v k="$key" '$1~k {gsub(/ /,"",$2); print $2; exit}' "$CONFIG" || true
}

ENCRYPTION_MODE=$(get_cfg "encryption_mode")
GPG_RECIPIENT=$(get_cfg "gpg_recipient")
GPG_SYMMETRIC_FLAG=$(get_cfg "gpg_symmetric" || true)

OUTDIR="${CASE_DIR}/encrypted"
mkdir -p "$OUTDIR"

# Determine files to encrypt (images + reports)
find "$CASE_DIR" -type f \( -name "*.dd" -o -path "*/reports/*" -o -name "*.sha256" \) | while read -r file; do
  base=$(basename "$file")
  out="$OUTDIR/${base}.gpg"
  if [ "$ENCRYPTION_MODE" = "gpg-symmetric" ] || [ "${GPG_SYMMETRIC:-0}" = "1" ] || [ "$GPG_SYMMETRIC_FLAG" = "1" ]; then
    if [ -z "${GPG_PASSPHRASE:-}" ]; then
      echo "GPG_PASSPHRASE not set for symmetric encryption. Aborting $file."
      continue
    fi
    echo "Symmetric encrypting $file -> $out"
    gpg --yes --batch --pinentry-mode loopback --symmetric --cipher-algo AES256 --passphrase "$GPG_PASSPHRASE" -o "$out" "$file"
  else
    if [ -z "$GPG_RECIPIENT" ]; then
      echo "GPG_RECIPIENT not set. Skipping asymmetric encryption for $file."
      continue
    fi
    echo "Asymmetric encrypting $file -> $out (recipient: $GPG_RECIPIENT)"
    gpg --yes --batch --recipient "$GPG_RECIPIENT" --encrypt --output "$out" "$file"
  fi
done

echo "Encryption complete. Encrypted files in: $OUTDIR"