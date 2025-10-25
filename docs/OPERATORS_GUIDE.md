# Operators Guide

Comprehensive guide for running investigations, managing cases, and troubleshooting.

## Table of Contents

1. [Pre-Investigation Checklist](#pre-investigation-checklist)
2. [Running an Investigation](#running-an-investigation)
3. [Case Management](#case-management)
4. [Report Generation & Review](#report-generation--review)
5. [Troubleshooting](#troubleshooting)

---

## Pre-Investigation Checklist

### System Verification

- [ ] Operating system is Debian/Ubuntu
- [ ] Have sudo/root access on forensic workstation
- [ ] Disk has at least 20% free space
- [ ] All required tools installed: `bash`, `python3`, `gnupg`, etc.
- [ ] GPG key configured: `gpg --list-keys`
- [ ] Network is **disconnected** (air-gap recommended)

### Legal & Compliance

- [ ] Written consent obtained from evidence owner
- [ ] Consent form signed and stored (see `templates/consent_form.txt`)
- [ ] Case identifier assigned and documented
- [ ] Chain of custody template prepared (see `templates/chain_of_custody.txt`)
- [ ] Legal reviewer informed of investigation

### Evidence Preparation

- [ ] Source device physically isolated
- [ ] Write-blocker connected (if using hardware)
- [ ] Device connectivity verified
- [ ] Device name/serial documented in chain of custody

---

## Running an Investigation

### Step 1: Create a Case

```bash
# Full workflow: imaging + analysis
sudo ./start.sh /dev/sdX ./cases "Client Name"

# This automatically:
# 1. Creates case_YYYYMMDDTHHMMSSZ/ directory
# 2. Images device to image.dd
# 3. Verifies SHA-256 checksum
# 4. Mounts image read-only
# 5. Runs Python scanner + optional Rust/YARA
# 6. Generates masked reports
# 7. Encrypts if configured (auto_encrypt = yes)
```

### Step 2: Monitor Analysis Progress

**Option A: Check Log Files**

```bash
# View real-time analysis log
tail -f ./cases/case_*/logs/analysis.log

# View all events
cat ./cases/case_*/logs/events.jsonl
```

**Option B: Use GUI Monitor**

```bash
# Start live GUI monitor
python3 tools/gui/gui.py --case-dir ./cases/case_YYYYMMDDTHHMMSSZ

# Monitor shows:
# - Real-time progress bar
# - Live findings (masked)
# - Event log
# - Case metadata
```

### Step 3: Review Findings

```bash
# View masked findings (safe to share)
cat ./cases/case_*/reports/findings_masked.txt

# View detailed masked report
cat ./cases/case_*/reports/report_masked.md

# Check metadata
cat ./cases/case_*/metadata.txt

# Verify image integrity
cat ./cases/case_*/image.dd.sha256
```

---

## Case Management

### Directory Structure

```
cases/case_2025MMDDTHHMMSSZ/
├── image.dd                    # Forensic image
├── image.dd.sha256            # SHA-256 hash for verification
├── metadata.txt               # Case information
├── config.ini                 # Case configuration
├── manifest.txt               # File manifest
├── manifest.txt.asc           # GPG signature
├── logs/
│   ├── analysis.log          # Analysis output
│   ├── events.jsonl          # Structured events
│   └── errors.log            # Error log (if any)
├── reports/
│   ├── findings_masked.txt    # Masked findings (SAFE to share)
│   ├── findings_unmasked.txt  # Unmasked findings (ENCRYPTED)
│   ├── report_masked.md       # Masked report (SAFE to share)
│   └── report_unmasked.md     # Unmasked report (ENCRYPTED)
├── archives/
│   └── consent_*.asc          # Signed consent (if available)
└── templates/
    ├── consent_form.txt
    └── chain_of_custody.txt
```

### Archive a Case

```bash
# Compress case for storage
tar -czf ./archive/case_2025MMDDTHHMMSSZ.tar.gz \
    ./cases/case_2025MMDDTHHMMSSZ/

# Verify archive integrity
tar -tzf ./archive/case_2025MMDDTHHMMSSZ.tar.gz | head
```

### Securely Delete Sensitive Data

```bash
# Review retention policy first
cat ./cases/case_*/config.ini | grep -i retention

# Securely delete old cases (configured retention days)
./scripts/retention_manager.sh ./cases

# Manually delete a case
./scripts/secure_delete.sh ./cases/case_2025MMDDTHHMMSSZ
```

---

## Report Generation & Review

### View Masked Reports

**Safe to share with clients:**

```bash
# Short summary
cat ./cases/case_*/reports/findings_masked.txt

# Full report (Markdown)
cat ./cases/case_*/reports/report_masked.md

# Convert to HTML (if pandoc installed)
pandoc ./cases/case_*/reports/report_masked.md \
    -o ./report.html
```

### Generate Custom Reports

```bash
# Use GUI to generate reports interactively
python3 tools/gui/gui.py --case-dir ./cases/case_*

# Or use command-line report generator
python3 tools/modules/search.py \
    --root ./cases/case_*/mnt \
    --outdir ./cases/case_*/reports \
    --report-type owner
```

### Package for Legal Delivery

```bash
# 1. Validate case
./scripts/validate_case_before_packaging.sh \
    ./cases/case_2025MMDDTHHMMSSZ

# 2. Create legal package (strict validation)
./scripts/package_for_legal_strict.sh \
    ./cases/case_2025MMDDTHHMMSSZ \
    ./legal_delivery.tar.gz

# 3. Verify GPG signature
gpg --verify legal_delivery.tar.gz.asc legal_delivery.tar.gz

# 4. For probate/estate cases
./scripts/create_probate_package.sh \
    ./cases/case_2025MMDDTHHMMSSZ \
    ./probate_delivery.tar.gz
```

---

## Troubleshooting

### Common Issues

#### Issue: "Permission denied" when running start.sh

```bash
# Solution: Use sudo for privileged operations
sudo ./start.sh /dev/sdX ./cases "Name"

# Verify sudo access
sudo -l | grep start.sh
```

#### Issue: Device not found

```bash
# List available devices
lsblk
sudo fdisk -l

# Check device permissions
ls -l /dev/sd*

# Solution: Use correct device name
sudo ./start.sh /dev/sdb ./cases "Name"  # not /dev/sdb1
```

#### Issue: Insufficient disk space

```bash
# Check available space
df -h

# Solution: Free up space or use external drive
sudo ./start.sh /dev/sdX /mnt/external/cases "Name"
```

#### Issue: Analysis hangs or is slow

```bash
# Monitor resource usage
watch -n1 'top -b | head -n 15'

# Check if process is still running
ps aux | grep -E 'search\.py|rustscanner'

# Solution: Adjust thread count in scripts or wait
# For faster analysis, ensure no other heavy processes running
```

#### Issue: GPG signature verification fails

```bash
# Verify GPG key is available
gpg --list-keys

# Check signature
gpg --verify case_manifest.txt.asc

# Solution: Import operator's public key
gpg --import operator_pubkey.asc
gpg --verify case_manifest.txt.asc
```

#### Issue: Reports are empty

```bash
# Check analysis log
cat ./cases/case_*/logs/analysis.log

# Check for errors
cat ./cases/case_*/logs/errors.log

# Verify image file
ls -lah ./cases/case_*/image.dd

# Solution: Rerun analysis
./scripts/analyze.sh ./cases/case_*/image.dd ./cases/case_*
```

### Advanced Troubleshooting

#### Enable Debug Logging

```bash
# Edit analyze.sh and add:
# set -x  # Enable debug output

# Or run with debug flag
bash -x ./scripts/analyze.sh image.dd case_dir
```

#### Check Loop Device Issues

```bash
# List active loop devices
losetup -l

# Check if loop device is mounted
mount | grep loop

# If stuck, force cleanup
sudo losetup -d /dev/loop0  # Use with caution!
```

#### Validate Python Environment

```bash
# Check Python version
python3 --version  # Should be 3.8+

# Test import
python3 -c "from tools.modules.search import *"

# Run syntax check
python3 -m py_compile tools/modules/search.py
```

#### Validate Rust Scanner

```bash
# Check if binary exists
ls -la ./A_rustscanner/target/release/rustscanner

# Test binary
./A_rustscanner/target/release/rustscanner --help

# Rebuild if needed
cd A_rustscanner
cargo build --release
cd ..
```

---

## Best Practices

### Operational Security

1. **Air-Gap:** Run on a dedicated, disconnected forensic workstation
2. **Logging:** Enable audit logging in config.ini
3. **Encryption:** Set `auto_encrypt = yes` for sensitive cases
4. **Backups:** Store case archives with proper retention policy
5. **Access Control:** Restrict file permissions: `chmod 700 ./cases`

### Evidence Integrity

1. **Verify Checksums:** Always check SHA-256 hashes
2. **Sign Reports:** Use GPG signatures for legal handoff
3. **Chain of Custody:** Maintain complete documentation
4. **Write-Blockers:** Always use for physical devices
5. **Copies Only:** Work only on image copies

### Legal Compliance

1. **Consent:** Obtain written consent before analysis
2. **DPA:** Use Data Processing Agreement if applicable
3. **Retention:** Follow configured retention policy
4. **Masking:** Use masked reports for sharing
5. **Audit Trail:** Maintain complete logs

---

## Getting Help

- **Quick Reference:** See `training/cheatsheet.md`
- **Full Training:** See `training/` modules
- **Legal Issues:** See `README_GDPR.md` and templates
- **Security Issues:** See `SECURITY.md`
