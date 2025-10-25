#!/usr/bin/env bash
# Find cases under a given parent dir and securely delete ones older than retention_days.
# Usage: ./retention_manager.sh /path/to/cases_parent_dir
# This script uses config/case_policy.ini as default, case-level config.ini can override retention_days.
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /path/to/cases_parent_dir"
  exit 2
fi

CASES_ROOT="$1"
GLOBAL_CFG="config/case_policy.ini"
DEFAULT_RETENTION=$(awk -F'=' '/^retention_days/ {gsub(/ /,"",$2); print $2; exit}' "$GLOBAL_CFG" || echo "30")

# for each case_* directory
find "$CASES_ROOT" -maxdepth 1 -type d -name 'case_*' | while read -r case; do
  # choose retention: case override or default
  CASE_CFG="$case/config.ini"
  if [ -f "$CASE_CFG" ]; then
    RET=$(awk -F'=' '/^retention_days/ {gsub(/ /,"",$2); print $2; exit}' "$CASE_CFG" || echo "$DEFAULT_RETENTION")
  else
    RET="$DEFAULT_RETENTION"
  fi
  # compute age in days
  created=$(awk -F': ' '/^created_at:/ {print $2; exit}' "$case/metadata.txt" || echo "")
  if [ -n "$created" ]; then
    # created is ISO timestamp YYYYMMDDTHHMMSSZ
    created_ts=$(date -u -d "${created}" +"%s" 2>/dev/null || date -u -d "$(echo "$created" | sed -E 's/(....)(..)(..).*/\1-\2-\3/')" +"%s" 2>/dev/null || 0)
  else
    # fallback to directory mtime
    created_ts=$(stat -c %Y "$case")
  fi
  now_ts=$(date -u +"%s")
  age_days=$(( (now_ts - created_ts) / 86400 ))
  if [ "$age_days" -ge "$RET" ]; then
    echo "Case $case is $age_days days old (retention $RET). Secure deleting..."
    # Call secure_delete.sh (must be present)
    if [ -x "scripts/secure_delete.sh" ]; then
      bash scripts/secure_delete.sh "$case" || echo "Warning: secure delete had issues for $case"
    else
      echo "scripts/secure_delete.sh not found or not executable; removing files unsafely."
      rm -rf "$case" || true
    fi
  else
    echo "Case $case is $age_days days old (retention $RET). Keeping."
  fi
done

echo "Retention pass complete."