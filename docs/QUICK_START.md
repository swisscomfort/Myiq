# Quick Start Guide

Get started with the Crypto Recovery Toolkit in 5 minutes!

## Prerequisites

**System Requirements:**
- Debian/Ubuntu Linux (other distributions may work but are untested)
- sudo access
- ~5 GB free disk space (minimum)

**Install Dependencies:**

```bash
# Update package list
sudo apt update

# Install core tools
sudo apt install -y \
    bash coreutils util-linux python3 python3-tk gnupg git

# Optional but recommended for enhanced functionality
sudo apt install -y \
    bulk-extractor yara cargo rustc
```

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/crypto-recovery-toolkit.git
cd crypto-recovery-toolkit

# 2. Make scripts executable
chmod +x scripts/*.sh tools/gui/*.py start.sh

# 3. Build Rust scanner (optional, for performance)
cd A_rustscanner
cargo build --release
cd ..

# 4. Create GPG signing key (if you don't have one)
gpg --full-generate-key
```

## Basic Workflow

### 1. Create a New Case

This is the main entry point. It handles disk imaging, analysis, and report generation:

```bash
# Syntax: ./start.sh <device> <output_dir> <client_name>
sudo ./start.sh /dev/sdX ./cases "John Doe"
```

**What happens:**
- Creates a case directory: `case_2025MMDDTHHMMSSZ/`
- Images the device to `image.dd` with SHA-256 verification
- Mounts the image read-only
- Runs both scanners (Python + optional Rust/YARA)
- Generates masked reports in `reports/`
- Optionally encrypts results

**⏱️ Duration:** 5 minutes to several hours (depends on device size)

### 2. Work with an Existing Image

If you already have a forensic image, analyze it directly:

```bash
# Syntax: ./scripts/analyze.sh <image_path> <case_dir>
./scripts/analyze.sh ./cases/case_2025.../image.dd ./cases/case_2025...
```

### 3. Review Reports

Check the generated findings:

```bash
# List available reports
ls ./cases/case_2025.../reports/

# View masked findings (safe to share with client)
cat ./cases/case_2025.../reports/findings_masked.txt
```

### 4. Use the GUI Monitor (Optional)

For visual progress tracking:

```bash
# Start GUI monitor for a case
python3 tools/gui/gui.py --case-dir ./cases/case_2025...
```

### 5. Package for Legal Handoff

When analysis is complete, create a legal package:

```bash
# Validate case integrity
./scripts/validate_case_before_packaging.sh ./cases/case_2025...

# Create legal-grade package (strict validation)
./scripts/package_for_legal_strict.sh ./cases/case_2025... ./legal_package.tar.gz

# For probate/estate cases (includes affidavit)
./scripts/create_probate_package.sh ./cases/case_2025... ./probate_package.tar.gz
```

---

## Example Workflow

```bash
# 1. Set up case
sudo ./start.sh /dev/sdb ./cases "Jane Smith"

# 2. When analysis completes, check reports
cat ./cases/case_*/reports/findings_masked.txt

# 3. Package results
./scripts/validate_case_before_packaging.sh ./cases/case_*
./scripts/package_for_legal_strict.sh ./cases/case_* ./jane_smith_package.tar.gz

# 4. Verify signature (recipient's side)
gpg --verify ./jane_smith_package.tar.gz.asc ./jane_smith_package.tar.gz
```

---

## Important Notes

### Security

⚠️ **Always work on IMAGE COPIES, never on original evidence!**

- The toolkit uses read-only mounting to prevent accidental modification
- All operations are logged (see `cases/case_*/logs/`)
- Verify GPG signatures on all reports

### Privacy & Compliance

✅ **GDPR/DSGVO built-in**

- Sensitive data is automatically masked (hex keys, mnemonics)
- Masked snippets are safe to share with clients
- Unencrypted keys never appear in reports
- Consent management templates provided

### Troubleshooting

**Device not accessible:**
```bash
# Check available devices
lsblk
sudo fdisk -l

# Verify permissions (usually need sudo)
sudo ./start.sh /dev/sdX ./cases "Name"
```

**Insufficient permissions:**
```bash
# Make sure scripts are executable
chmod +x scripts/*.sh start.sh tools/gui/*.py

# Ensure sudo access for privileged operations
sudo -l
```

**Memory/CPU issues:**
```bash
# Reduce parallelism in analysis (edit analyze.sh or scripts)
# Monitor system during analysis:
watch -n1 'ps aux | grep python3'
```

---

## Next Steps

1. **Learn more:** See [DEVELOPMENT.md](../DEVELOPMENT.md) for development setup
2. **Training:** Complete [training modules](../training/) for in-depth knowledge
3. **Legal:** Review [GDPR guide](../README_GDPR.md) and [legal templates](../templates/)
4. **Help:** Check [troubleshooting](../training/cheatsheet.md) or [FAQ](../docs/)

---

## Support

- **Documentation:** See `docs/` directory
- **Issues:** Check GitHub Issues or open a new one
- **Security:** Report vulnerabilities via `SECURITY.md`
- **Training:** See `training/` modules
