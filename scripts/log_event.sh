#!/usr/bin/env bash
# Simple structured logger for the toolkit.
# Usage: ./scripts/log_event.sh /path/to/case_dir LEVEL "message" [progress]
# LEVEL examples: info, warn, error
# progress optional: integer 0-100
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "Usage: $0 /path/to/case_dir LEVEL \"message\" [progress]" >&2
  exit 2
fi

CASE_DIR="$1"; shift
LEVEL="$1"; shift
MESSAGE="$1"; shift
PROGRESS="${1:-}"

LOG_DIR="$CASE_DIR/logs"
mkdir -p "$LOG_DIR"

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
# Escape double quotes in message
ESC_MSG=$(printf "%s" "$MESSAGE" | sed 's/"/\\"/g')

# Compose JSON entry
if [ -n "$PROGRESS" ]; then
  ENTRY="{\"timestamp\":\"$TS\",\"level\":\"$LEVEL\",\"message\":\"$ESC_MSG\",\"progress\":$PROGRESS}"
else
  ENTRY="{\"timestamp\":\"$TS\",\"level\":\"$LEVEL\",\"message\":\"$ESC_MSG\"}"
fi

# Append to process.log (newline separated JSON objects)
echo "$ENTRY" >> "$LOG_DIR/process.log"

# Update status.json with summary (overwrite)
if [ -n "$PROGRESS" ]; then
  cat > "$LOG_DIR/status.json" <<EOF
{"last_event":"$ESC_MSG","level":"$LEVEL","timestamp":"$TS","progress":$PROGRESS}
EOF
else
  cat > "$LOG_DIR/status.json" <<EOF
{"last_event":"$ESC_MSG","level":"$LEVEL","timestamp":"$TS","progress":null}
EOF
fi

# Also write a human-readable text log for convenience
echo "[$TS] $LEVEL: $MESSAGE" >> "$LOG_DIR/process.txt"

# Print entry on stdout for interoperability
printf "%s\n" "$ENTRY"