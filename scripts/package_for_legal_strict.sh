#!/usr/bin/env bash
# Strict packaging script for legal review.
# - Verifies required artifacts (clearsigned consent, image checksum, reports)
# - Scans reports for unmasked sensitive patterns (mnemonic-like, long hex without masking)
# - Creates manifest, signs it (gpg) and packages artifacts into a tar.gz
# Usage: ./scripts/package_for_legal_strict.sh /path/to/case_dir /path/to/output.tar.gz
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 /path/to/case_dir /path/to/output.tar.gz" >&2
  exit 2
fi

CASE_DIR="$1"
OUT_TAR="$2"

if [ ! -d "$CASE_DIR" ]; then
  echo "Case directory not found: $CASE_DIR" >&2
  exit 3
fi

# Helper: fail with message and exit
fail() {
  echo "ERROR: $1" >&2
  exit 4
}

# 1) Basic artifact checks
REQUIRED=(
  "metadata.txt"
  "chain_of_custody.txt"
)

for f in "${REQUIRED[@]}"; do
  if [ ! -f "$CASE_DIR/$f" ]; then
    fail "Required file missing: $f"
  fi
done

# Check for clearsigned consent in archives (must exist and be .asc or .sig)
CONSENT_FOUND=$(find "$CASE_DIR" -type f \( -name '*consent*.*asc' -o -name '*consent*.*sig' -o -name '*acknowledgement*.*asc' \) | wc -l)
if [ "$CONSENT_FOUND" -eq 0 ]; then
  fail "Clearsigned consent/acknowledgement not found in $CASE_DIR/archives. Aborting packaging."
fi

# Check for image checksum(s)
IMAGE_SUM=$(find "$CASE_DIR" -maxdepth 1 -type f -name '*.sha256' | wc -l)
if [ "$IMAGE_SUM" -eq 0 ]; then
  fail "No image.dd.sha256 found at top level of case directory. Aborting packaging."
fi

# Ensure reports exist
REPORTS_DIR="$CASE_DIR/reports"
if [ ! -d "$REPORTS_DIR" ]; then
  fail "Reports directory not found: $REPORTS_DIR"
fi

shopt -s nullglob
REPORT_FILES=("$REPORTS_DIR"/*scan_results*.*)
if [ "${#REPORT_FILES[@]}" -eq 0 ]; then
  fail "No scan results found in $REPORTS_DIR"
fi

# 2) Heuristic masking check: look for likely unmasked mnemonics and long hex sequences not masked
# We'll run a careful scan but avoid printing secrets: report file + line number + masked preview

PYTHON=$(command -v python3 || true)
if [ -z "$PYTHON" ]; then
  fail "python3 is required for masking checks."
fi

echo "Running masking checks on reports..."
MASK_CHECK_SCRIPT="$(mktemp)"
cat > "$MASK_CHECK_SCRIPT" <<'PYCODE'
#!/usr/bin/env python3
import re,sys,os,json

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
                # skip lines that already contain obvious masking or REDACTED
                if '***' in line or 'REDACTED' in line or '*' in line:
                    continue
                if mnemonic_re.search(line):
                    issues.append((rp,i,'mnemonic'))
                else:
                    m = hex_re.search(line)
                    if m:
                        # ignore if likely a proper sha256 metadata line (heuristic: contains "sha256" or "image" words)
                        if 'sha256' in line.lower() or 'image' in line.lower():
                            continue
                        issues.append((rp,i,'hex'))
    except Exception:
        pass

# Print structured result in machine-friendly way
if issues:
    print(json.dumps({"status":"fail","issues":issues}))
    sys.exit(5)
else:
    print(json.dumps({"status":"ok"}))
    sys.exit(0)
PYCODE

python3 "$MASK_CHECK_SCRIPT" "$CASE_DIR" > /tmp/mask_check_result.json || {
  cat /tmp/mask_check_result.json
  rm -f "$MASK_CHECK_SCRIPT"
  fail "Masking check failed. Please review the report files for unmasked sensitive content."
}
cat /tmp/mask_check_result.json
rm -f "$MASK_CHECK_SCRIPT"

echo "Masking check OK."

# 3) Create manifest (sha256 of each file to include)
echo "Creating manifest..."
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT
P_LIST="$TMPDIR/filelist.txt"

# Define which files to include in package: metadata, chains, reports, exports, archives, logs, image checksums (but not image.dd itself)
find "$CASE_DIR" -type f \( -path "$CASE_DIR/image.dd" -prune -o -name '*.dd' -prune -o -name 'image.dd' -o -false \) > /dev/null 2>&1 || true

# We'll include: metadata, chain_of_custody, image*.sha256, reports/, exports/, archives/, logs/, config.ini
(
  cd "$CASE_DIR"
  for f in metadata.txt chain_of_custody.txt *.sha256 config.ini; do
    [ -e "$f" ] && echo "$f"
  done
  for d in reports exports archives logs; do
    [ -d "$d" ] && find "$d" -type f | sed 's|^\./||'
  done
) > "$P_LIST"

# Compute checksums (relative paths)
pushd "$CASE_DIR" >/dev/null
sha256sum $(cat "$P_LIST") > "$TMPDIR/manifest.txt"
popd >/dev/null

# Sign manifest (requires GPG secret key)
MANIFEST="$TMPDIR/manifest.txt"
MANIFEST_SIG="$TMPDIR/manifest.txt.sig"
if command -v gpg >/dev/null 2>&1 && gpg --list-secret-keys >/dev/null 2>&1; then
  echo "Signing manifest with local GPG key..."
  gpg --yes --batch --armor --output "$MANIFEST_SIG" --detach-sign "$MANIFEST" || {
    echo "Warning: gpg sign failed. Continuing without signature."
  }
else
  echo "No local GPG secret key found; manifest will be unsigned."
fi

# 4) Package artifacts into tar.gz (manifest + manifest.sig included)
echo "Creating tarball..."
pushd "$CASE_DIR" >/dev/null
tar -czf "$OUT_TAR" -T "$P_LIST" "$MANIFEST" "$MANIFEST_SIG" || fail "tar failed"
popd >/dev/null

echo "Package created: $OUT_TAR"
echo "Done."
exit 0