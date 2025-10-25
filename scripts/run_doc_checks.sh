#!/usr/bin/env bash
# Wrapper to run the document quality check and print a short summary.
# Usage: ./scripts/run_doc_checks.sh /path/to/repo
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /path/to/repo" >&2
  exit 2
fi

REPO_ROOT="$1"

if [ ! -d "$REPO_ROOT" ]; then
  echo "Repo path not found: $REPO_ROOT" >&2
  exit 3
fi

PY=$(command -v python3 || true)
if [ -z "$PY" ]; then
  echo "python3 not found in PATH. Install Python 3." >&2
  exit 4
fi

"$PY" "$(dirname "$0")/doc_quality_check.py" "$REPO_ROOT"
RC=$?
if [ "$RC" -ne 0 ]; then
  echo "Doc quality check exited with code $RC" >&2
fi
exit $RC