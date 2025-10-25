# API Reference

Technical reference for integrating with the Crypto Recovery Toolkit.

## Table of Contents

1. [Rust Scanner JSONL Output](#rust-scanner-jsonl-output)
2. [Python Scanner Module](#python-scanner-module)
3. [Configuration Schema](#configuration-schema)
4. [File Formats](#file-formats)

---

## Rust Scanner JSONL Output

### Schema

The Rust scanner emits JSONL (JSON Lines) format, one complete JSON object per line.

```json
{
  "case": "string (case ID or root path)",
  "path": "string (absolute file path)",
  "filesize": 12345,
  "pattern": "string (pattern that matched)",
  "snippet": "string (masked or truncated content)",
  "sha256": "string (hex-encoded SHA-256 hash)",
  "timestamp": "string (RFC 3339 timestamp)",
  "scanner_version": "string (e.g., '0.1.0')"
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `case` | string | Unique case identifier or root path for analysis |
| `path` | string | Absolute filesystem path to the matched file |
| `filesize` | integer | File size in bytes |
| `pattern` | string | Pattern that matched, e.g., `"filename:(?i)wallet"` or `"content:hex:.*deadbeef.*"` |
| `snippet` | string | Matched content (masked/truncated for security) or `"[FILENAME MATCH]"` |
| `sha256` | string | SHA-256 hash of the entire file (lowercase hex) |
| `timestamp` | string | UTC timestamp in RFC 3339 format: `"2025-10-25T14:30:00Z"` |
| `scanner_version` | string | Version of the scanner that produced this output |

### Example Output

```jsonl
{"case": "case_20251025T143000Z", "path": "/mnt/wallet_backup.json", "filesize": 2048, "pattern": "filename:(?i)wallet", "snippet": "[FILENAME MATCH]", "sha256": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6", "timestamp": "2025-10-25T14:30:15Z", "scanner_version": "0.1.0"}
{"case": "case_20251025T143000Z", "path": "/mnt/documents/keys.txt", "filesize": 512, "pattern": "content:mnemonic", "snippet": "[MNEMONIC PATTERN - MASKED]", "sha256": "b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7", "timestamp": "2025-10-25T14:30:16Z", "scanner_version": "0.1.0"}
```

### Consuming JSONL Output

**Python example:**

```python
import json

def process_hits(jsonl_file):
    """Process Rust scanner JSONL output."""
    hits = []
    with open(jsonl_file, 'r') as f:
        for line in f:
            if line.strip():
                hit = json.loads(line)
                hits.append(hit)
    return hits

hits = process_hits('scan_results.jsonl')
for hit in hits:
    print(f"{hit['path']}: {hit['snippet']}")
```

**Bash example:**

```bash
# Count total hits
cat scan_results.jsonl | wc -l

# Extract paths only
cat scan_results.jsonl | jq -r '.path'

# Filter by pattern
cat scan_results.jsonl | jq 'select(.pattern | contains("wallet"))'
```

---

## Python Scanner Module

### Module: `tools/modules/search.py`

#### Class: `FileScanner`

High-level interface for scanning filesystems.

**Constructor:**

```python
from tools.modules.search import FileScanner

scanner = FileScanner(
    root_dir="/mnt/case_mount",
    patterns=None,  # Use default patterns
    mask_sensitive=True,
    max_filesize=None
)
```

**Methods:**

| Method | Signature | Description |
|--------|-----------|-------------|
| `scan()` | `scan() -> List[Dict]` | Scan root directory, return list of hits |
| `scan_file()` | `scan_file(path: str) -> List[Dict]` | Scan single file |
| `get_findings()` | `get_findings() -> List[Dict]` | Get all findings accumulated so far |

#### Example Usage

```python
from tools.modules.search import FileScanner

# Create scanner
scanner = FileScanner(
    root_dir="/mnt/image",
    mask_sensitive=True
)

# Run scan
findings = scanner.scan()

# Process findings
for finding in findings:
    print(f"Found: {finding['path']}")
    print(f"  Pattern: {finding['pattern']}")
    print(f"  Snippet: {finding['snippet']}")
    print(f"  Hash: {finding['sha256']}")
```

### Command-Line Usage

```bash
# Basic scan
python3 tools/modules/search.py --root /mnt/image --outdir ./reports

# With custom patterns
python3 tools/modules/search.py \
    --root /mnt/image \
    --outdir ./reports \
    --patterns ./custom_patterns.txt

# Without masking (for technical review)
python3 tools/modules/search.py \
    --root /mnt/image \
    --outdir ./reports \
    --no-mask

# See all options
python3 tools/modules/search.py --help
```

---

## Configuration Schema

### File: `config/case_policy.ini`

**Format:** INI (standard UNIX configuration format)

**Sections & Keys:**

```ini
[forensics]
# Enable/disable scanner components
enable_rust_scanner = yes
enable_python_scanner = yes
enable_yara = yes
enable_bulk_extractor = no

# Masking and reporting
mask_sensitive_data = yes
mask_hex_keys = yes
mask_mnemonics = yes

# Report format
report_formats = markdown,html
include_signed_reports = yes

[encryption]
# GPG encryption of sensitive reports
auto_encrypt = yes
recipient_email = operator@example.com

[retention]
# Automatic case deletion policy
enable_retention = yes
retention_days = 30

[logging]
# Audit logging
log_level = info
log_format = jsonl
```

**Example Configuration:**

```ini
[forensics]
enable_rust_scanner = yes
enable_python_scanner = yes
enable_yara = yes
mask_sensitive_data = yes
report_formats = markdown

[encryption]
auto_encrypt = yes
recipient_email = investigator@forensics.local

[retention]
enable_retention = yes
retention_days = 90
```

### Using Configuration

Configurations are copied to each case directory:

```bash
cp config/case_policy.ini ./cases/case_*/config.ini
```

Modify per-case configuration:

```bash
# Enable additional tools for specific case
sed -i 's/enable_rust_scanner = no/enable_rust_scanner = yes/' \
    ./cases/case_*/config.ini
```

---

## File Formats

### Case Manifest: `manifest.txt`

Lists all files in case directory with hashes.

**Format:**

```
SHA256(image.dd)=<hash>
SHA256(reports/report.md)=<hash>
...
```

**Example:**

```
SHA256(image.dd)=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d
SHA256(reports/report_masked.md)=b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9
```

### Event Log: `logs/events.jsonl`

Structured audit log of case operations.

**Format:** JSONL (one JSON object per line)

**Schema:**

```json
{
  "timestamp": "2025-10-25T14:30:00Z",
  "event_type": "string (e.g., 'imaging_started', 'analysis_complete')",
  "level": "string (info, warning, error)",
  "message": "string (human-readable message)",
  "metadata": {
    "case_id": "string",
    "component": "string (e.g., 'python_scanner', 'rust_scanner')",
    "details": {}
  }
}
```

**Example:**

```jsonl
{"timestamp": "2025-10-25T14:30:00Z", "event_type": "imaging_started", "level": "info", "message": "Imaging started for device /dev/sdb", "metadata": {"case_id": "case_20251025T143000Z", "component": "orchestration"}}
{"timestamp": "2025-10-25T14:35:00Z", "event_type": "imaging_complete", "level": "info", "message": "Imaging complete. Image size: 500 GB", "metadata": {"case_id": "case_20251025T143000Z", "component": "imaging"}}
```

### Report Format: `report_masked.md`

Markdown report with masked sensitive data.

**Structure:**

```markdown
# Forensic Report — Case: case_ID

**Generated:** 2025-10-25
**Examiner:** Investigator Name
**Case:** John Doe Estate Recovery

## Summary

Total files scanned: 50,000
Findings: 23

## Findings

### Finding 1: Wallet File Detected
**Location:** /home/user/wallet.json
**Pattern:** Filename match
**Content Snippet:** [SENSITIVE DATA - MASKED]
**File Hash:** a1b2c3d4...

...

## Technical Details

### Scan Patterns Used
- Filenames: wallet, key, seed, mnemonic
- Content: BIP-39 mnemonics, hex patterns
- Formats: JSON, TXT, DAT files

### Integrity
- Image Hash: SHA-256: ...
- Report Signed: Yes (GPG)
- Encryption: Yes (GPG)
```

---

## Integration Points

### Running Rust Scanner Standalone

```bash
cd A_rustscanner

# Build
cargo build --release

# Run
./target/release/rustscanner \
    --root /path/to/scan \
    --head-size 200000 \
    --threads 4 \
    > output.jsonl

# Consume output
python3 ../B_python_reader/scripts/rustscanner_reader.py \
    --jsonl output.jsonl \
    --outdir reports/
```

### Writing Custom Pattern Matchers

Create custom patterns in `tools/modules/search.py`:

```python
# Add to patterns list
CUSTOM_PATTERNS = [
    {
        'name': 'custom_wallet_pattern',
        'type': 'regex',
        'pattern': r'CustomWallet\{.*\}',
        'mask_in_snippet': True
    }
]
```

---

## Version History

- **v0.1.0** (2025-10-25): Initial PoC release
  - JSONL format with basic Hit struct
  - Python scanner with masking
  - Configuration INI schema
