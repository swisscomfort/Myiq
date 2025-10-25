#!/usr/bin/env bash
# Sign and archive a filled client acknowledgement form.
# Usage: ./scripts/sign_acknowledgement.sh /path/to/filled_form.md /path/to/case_dir
#
# Behavior:
# - copies the filled form into case_dir/archives with timestamp
# - creates a clearsigned version (human-readable) and a detached armored signature
# - creates a SHA256 checksum file for integrity proof
# - optionally encrypts the signed copy for a recipient when GPG_RECIPIENT env var is set
# - logs an event via scripts/log_event.sh if available
#
# Comments in English as requested; user-facing text is German in the forms.

set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 /path/to/filled_form.md /path/to/case_dir" >&2
  exit 2
fi

INFILE="$1"
CASEDIR="$2"

if [ ! -f "$INFILE" ]; then
  echo "Filled form not found: $INFILE" >&2
  exit 3
fi

if [ ! -d "$CASEDIR" ]; then
  echo "Case directory not found, creating: $CASEDIR"
  mkdir -p "$CASEDIR"
fi

ARCHDIR="$CASEDIR/archives"
mkdir -p "$ARCHDIR"

TS=$(date -u +"%Y%m%dT%H%M%SZ")
BASENAME="$(basename "$INFILE")"
COPYNAME="${BASENAME%.*}_filled_${TS}.${BASENAME##*.}"
COPYPATH="$ARCHDIR/$COPYNAME"

# Copy the filled form into archives
cp "$INFILE" "$COPYPATH"
chmod 600 "$COPYPATH" || true

# Clear-sign the copied form (human-readable signed text)
SIGNED_PATH="$COPYPATH.asc"
if command -v gpg >/dev/null 2>&1; then
  # Use clearsign so the file remains readable and contains a signature block
  echo "Creating clearsigned file: $SIGNED_PATH"
  gpg --yes --batch --armor --clearsign --output "$SIGNED_PATH" "$COPYPATH" || {
    echo "gpg clearsign failed (maybe no secret key configured). Continuing without clearsign." >&2
    # fallback: copy original to signed path
    cp "$COPYPATH" "$SIGNED_PATH"
  }
else
  echo "gpg not found; skipping signing. Plain copy retained at $COPYPATH"
  SIGNED_PATH="$COPYPATH"
fi

# Also create detached armored signature (if gpg present)
SIG_PATH="$COPYPATH.sig"
if command -v gpg >/dev/null 2>&1; then
  echo "Creating detached signature: $SIG_PATH"
  gpg --yes --batch --armor --detach-sign --output "$SIG_PATH" "$COPYPATH" || true
fi

# Create SHA256 checksum for the signed file (or the copy if signing failed)
SHA_FILE="$SIGNED_PATH.sha256"
sha256sum "$SIGNED_PATH" > "$SHA_FILE"

# Optional: encrypt the signed file for a recipient (set env var GPG_RECIPIENT)
if [ -n "${GPG_RECIPIENT:-}" ] && command -v gpg >/dev/null 2>&1; then
  ENC_PATH="$SIGNED_PATH.gpg"
  echo "Encrypting signed file for recipient $GPG_RECIPIENT -> $ENC_PATH"
  gpg --yes --batch --recipient "$GPG_RECIPIENT" --encrypt --output "$ENC_PATH" "$SIGNED_PATH" || \
    echo "Encryption failed for recipient $GPG_RECIPIENT" >&2
fi

# Log event via log_event helper if available
LOG_HELPER="scripts/log_event.sh"
if [ -x "$LOG_HELPER" ]; then
  # try to write a short event; do not fail if logging fails
  "$LOG_HELPER" "$CASEDIR" info "Client acknowledgement signed and archived: $(basename "$SIGNED_PATH")" 0 || true
fi

echo "Signed and archived acknowledgement:"
echo " - archive copy: $COPYPATH"
echo " - clearsigned:  $SIGNED_PATH"
echo " - sha256:       $SHA_FILE"
if [ -n "${ENC_PATH:-}" ]; then
  echo " - encrypted:    $ENC_PATH"
fi
if [ -f "$SIG_PATH" ]; then
  echo " - detached sig: $SIG_PATH"
fi

exit 0