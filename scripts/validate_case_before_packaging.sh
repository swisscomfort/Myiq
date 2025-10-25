#!/usr/bin/env bash
# Lightweight validator to run before packaging (prints human-readable guidance)
# Usage: ./scripts/validate_case_before_packaging.sh /path/to/case_dir
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /path/to/case_dir" >&2
  exit 2
fi

CASE_DIR="$1"

if [ ! -d "$CASE_DIR" ]; then
  echo "Case dir not found: $CASE_DIR" >&2
  exit 3
fi

echo "Validating case: $CASE_DIR"
echo "- Checking presence of required files..."

MISSING=0
for f in metadata.txt chain_of_custody.txt; do
  if [ ! -f "$CASE_DIR/$f" ]; then
    echo "  MISSING: $f"
    MISSING=$((MISSING+1))
  else
    echo "  OK: $f"
  fi
done

# Consent
CONSENT=$(find "$CASE_DIR" -type f \( -name '*consent*.*asc' -o -name '*acknowledgement*.*asc' -o -name '*consent*.*sig' \) | wc -l)
if [ "$CONSENT" -eq 0 ]; then
  echo "  MISSING: clearsigned consent/acknowledgement in $CASE_DIR/archives"
  MISSING=$((MISSING+1))
else
  echo "  OK: clearsigned consent present"
fi

# image sha256
if [ -f "$CASE_DIR/image.dd.sha256" ]; then
  echo "  OK: image.dd.sha256 present"
else
  echo "  MISSING: image.dd.sha256 at case root"
  MISSING=$((MISSING+1))
fi

# Reports presence
if [ -d "$CASE_DIR/reports" ] && [ "$(ls -A "$CASE_DIR/reports")" ]; then
  echo "  OK: reports directory non-empty"
else
  echo "  MISSING: reports (empty or absent)"
  MISSING=$((MISSING+1))
fi

if [ "$MISSING" -ne 0 ]; then
  echo ""
  echo "Validation FAILED: $MISSING issues found. Fix before packaging."
  exit 4
fi

echo ""
echo "Quick masking heuristic scan (mnemonic/unmasked hex). This is best-effort and not a proof:"
python3 - "$CASE_DIR" <<'PY'
import sys, re, os, json
case_dir = sys.argv[1]
reports = []
for root,_,files in os.walk(os.path.join(case_dir,'reports')):
    for fn in files:
        if fn.endswith(('.jsonl','.json','.csv','.txt')):
            reports.append(os.path.join(root,fn))

mnemonic_re = re.compile(r'\b([a-z]{2,})(?:\s+[a-z]{2,}){11,24}\b', re.IGNORECASE)
hex_re = re.compile(r'\b([a-f0-9]{20,})\b', re.IGNORECASE)

issues = []
for rp in reports:
    try:
        with open(rp,'r',errors='ignore') as fh:
            for i,line in enumerate(fh, start=1):
                if '***' in line or 'REDACTED' in line or '*' in line:
                    continue
                if mnemonic_re.search(line):
                    issues.append((rp,i,'mnemonic'))
                else:
                    m = hex_re.search(line)
                    if m:
                        if 'sha256' in line.lower() or 'image' in line.lower():
                            continue
                        issues.append((rp,i,'hex'))
    except Exception:
        pass

if issues:
    print("Found potential unmasked sensitive patterns (heuristic):")
    for rp,i,t in issues:
        print(f" - {t} in {rp} at line {i}")
    sys.exit(5)
else:
    print("No obvious unmasked sensitive patterns detected (heuristic).")
    sys.exit(0)
PY

echo ""
echo "Validation PASSED. You may proceed to packaging with package_for_legal_strict.sh"
exit 0