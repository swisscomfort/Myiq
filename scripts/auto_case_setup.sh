#!/usr/bin/env bash
# Auto-create a new case directory and populate blank forms/configs.
# Usage: ./scripts/auto_case_setup.sh /path/to/cases_parent_dir "Client Name" "DeviceID(optional)"
# Non-interactive: all params required. Comments in English.
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 /path/to/cases_parent_dir \"Client Name\" [DeviceID]" >&2
  exit 2
fi

CASES_ROOT="$1"
CLIENT_NAME="$2"
DEVICE_ID="${3:-unknown}"
TIMESTAMP=$(date -u +"%Y%m%dT%H%M%SZ")
CASE_DIR="$CASES_ROOT/case_${TIMESTAMP}"

mkdir -p "$CASE_DIR"
mkdir -p "$CASE_DIR/forms" "$CASE_DIR/reports" "$CASE_DIR/logs" "$CASE_DIR/archives" "$CASE_DIR/exports"

# Copy templates (if present in repo)
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [ -d "$REPO_ROOT/templates" ]; then
  cp -r "$REPO_ROOT/templates/"* "$CASE_DIR/forms/" 2>/dev/null || true
fi

# Copy config defaults
if [ -f "$REPO_ROOT/config/case_policy.ini" ]; then
  cp "$REPO_ROOT/config/case_policy.ini" "$CASE_DIR/config.ini" || true
fi

# create basic metadata and chain_of_custody placeholder
cat > "$CASE_DIR/metadata.txt" <<EOF
device: $DEVICE_ID
client: $CLIENT_NAME
created_at: $TIMESTAMP
operator: $(whoami)@$(hostname)
EOF

cat > "$CASE_DIR/chain_of_custody.txt" <<'EOF'
Chain of Custody Log
---------------------
(Please fill in details during acceptance and transfers)
Case ID: ____________________
Device ID: __________________
Collected by: _______________
Received from: ______________
Date & Time Received: _______

Actions:
- Imaging performed: (yes/no)  Path to image: ___________________
- Hash (sha256) of image: ___________________
- Analysis performed by: ____________________
- Reports produced: ________________________

Transfer history:
- From ______________ to ______________ at ______________ (signature)
EOF

# Touch initial log files
touch "$CASE_DIR/logs/process.log" "$CASE_DIR/logs/process.txt" "$CASE_DIR/logs/status.json"

# Attempt to log event using scripts/log_event.sh if available
LOG_HELPER="$REPO_ROOT/scripts/log_event.sh"
if [ -x "$LOG_HELPER" ]; then
  "$LOG_HELPER" "$CASE_DIR" info "Case directory created and blank forms copied" 0 || true
fi

echo "Case created: $CASE_DIR"
echo "Forms copied to: $CASE_DIR/forms"
echo "Please have the client fill and sign the form located in $CASE_DIR/forms (client_acknowledgement_form.md)."
echo "After signing, run scripts/sign_acknowledgement.sh /path/to/filled_form.md $CASE_DIR"