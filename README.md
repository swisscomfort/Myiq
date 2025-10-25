# Offline Forensic Toolkit for Crypto-Recovery# 🔐 Crypto Recovery Toolkit



This repository contains a suite of specialized tools for offline forensic analysis, specifically designed for crypto-recovery workflows. It provides a command-line-driven process to image storage devices, scan for cryptocurrency wallet artifacts, and generate reports.[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Platform](https://img.shields.io/badge/Platform-Linux-blue.svg)](https://www.linux.org/)

## Core Features[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)

[![Rust](https://img.shields.io/badge/Rust-2021-orange.svg)](https://www.rust-lang.org/)

- **Disk Imaging:** Safely create bit-for-bit copies of storage media using `dd`.

- **High-Speed Scanning:** A parallelized scanner written in Rust (`A_rustscanner`) searches for wallet files and other artifacts based on predefined patterns.**Professional offline forensic toolkit for legally compliant crypto-asset recovery.**

- **Flexible Analysis:** An alternative Python-based scanner (`tools/modules/search.py`) allows for easy customization and portability.

- **Orchestration:** A top-level shell script (`start.sh`) automates the entire workflow, from case creation to analysis.Designed for estate executors, forensic investigators, and legal professionals handling crypto asset recovery in probate cases, authorized investigations, and owner recovery scenarios. Fully GDPR/DSGVO compliant with automated masking, chain-of-custody tracking, and GPG-signed reports.

- **Reporting:** Tools to generate masked reports from scan results, ready for legal and evidentiary use.

---

## Architecture Overview

## 🎯 Features

The toolkit is designed as a modular system:

### 🔍 Forensic Imaging & Analysis

1.  **Orchestration (`start.sh`, `scripts/`):** Bash scripts manage the high-level workflow. `start.sh` creates a case directory, calls `scripts/image_disk.sh` to create an image, and runs `scripts/analyze.sh` to perform the analysis.- **Forensic disk imaging** with SHA-256 verification

2.  **Scanners (`A_rustscanner/`, `tools/modules/search.py`):**- **Read-only mounting** via loop devices (prevents evidence contamination)

    *   The **Rust scanner** is optimized for performance, walking the filesystem in parallel and emitting findings as JSONL.- **Dual-scanner architecture**:

    *   The **Python scanner** provides a more portable alternative that integrates directly into the `analyze.sh` script.  - 🦀 **Rust scanner**: High-performance parallel scanner with JSONL output

3.  **Reporting (`D_reports/`, `tools/gui/`):** Scan outputs (JSONL) are processed to generate human-readable and masked reports. A Tkinter-based GUI provides helpers for report generation and signing.  - 🐍 **Python scanner**: Portable scanner with built-in masking

- **Pattern-based detection**: Filenames, JSON keystores, hex patterns, mnemonics

## Quick Start: Analyzing a Disk Image- **Optional integrations**: bulk_extractor, YARA rules



This example demonstrates how to analyze an existing disk image.### 🔒 Privacy & Compliance

- ✅ **GDPR/DSGVO compliant** by design

**Prerequisites:**- ✅ **Automatic data masking** (hex keys, mnemonic phrases)

- A Linux environment with standard utilities (`bash`, `losetup`, `mount`).- ✅ **Consent management** (templates provided)

- Python 3.- ✅ **Data Processing Agreements** (DPA templates)

- Rust and Cargo (for building the Rust scanner).- ✅ **Chain of Custody** tracking

- ✅ **GPG signatures** for all artifacts

**Steps:**- ✅ **Retention management** (automated deletion)

- ✅ **Audit logging** (JSONL format)

1.  **Clone the repository:**

    ```bash### 📊 Reporting & Packaging

    git clone https://github.com/swisscomfort/Myiq.git- **Multi-format reports**: Markdown, HTML

    cd Myiq- **Owner reports** (non-technical, client-friendly)

    ```- **Court reports** (technical, evidence-grade)

- **Probate packages** with affidavits

2.  **Build the Rust Scanner:**- **GPG signing** for legal handoff

    ```bash- **Automated validation** before packaging

    cd A_rustscanner

    cargo build --release### 🎓 Training & Documentation

    cd ..- **5 comprehensive training modules**

    ```- **Practical exercises** and quizzes

- **Legal compliance guides**

3.  **Run the Analysis Script:**- **Template library** (12+ legal documents)

    The `analyze.sh` script automates mounting the image and running the scanners.- **Cheat sheets** for operators



    *   **`<path/to/image.dd>`**: The path to your disk image file.---

    *   **`<path/to/case_dir>`**: A directory where reports and metadata will be stored.

## 🚀 Quick Start

    ```bash

    ./scripts/analyze.sh /path/to/image.dd ./cases/my_case_01### Prerequisites

    ``````bash

    The script will:# Debian/Ubuntu

    - Set up a loop device for the image.sudo apt update

    - Mount the primary partition read-only.sudo apt install -y bash coreutils util-linux python3 python3-tk gnupg

    - Run the Python scanner on the mounted filesystem.

    - Store masked findings in `./cases/my_case_01/reports/`.# Optional but recommended

sudo apt install -y bulk-extractor yara cargo rustc

4.  **Review the Results:**```

    Scan results are located in the `reports/` subdirectory of your case folder.

### Installation

## Development```bash

# Clone repository

For details on the architecture, developer workflows, and project-specific conventions, please see the [AI agent instructions](/.github/copilot-instructions.md).git clone https://github.com/YOUR_USERNAME/crypto-recovery-toolkit.git

cd crypto-recovery-toolkit

## License

# Make scripts executable

This project is licensed under the terms of the LICENSE file.chmod +x scripts/*.sh tools/gui/*.py start.sh


# Build Rust scanner (optional, for performance)
cd A_rustscanner
cargo build --release
cd ..

# Generate GPG key for signing (if not already present)
gpg --full-generate-key
```

### Basic Usage

#### 1️⃣ Create a Case
```bash
# Full workflow: imaging + analysis
sudo ./start.sh /dev/sdX ./cases "Client Name"

# This will:
# - Create case_YYYYMMDDTHHMMSSZ/ directory
# - Image the device to case_*/image.dd
# - Compute SHA-256 checksum
# - Mount image read-only
# - Run scanners (Python + optional Rust/YARA/bulk_extractor)
# - Generate masked reports in case_*/reports/
# - Auto-encrypt if configured
```

#### 2️⃣ Analyze Existing Image
```bash
# If you already have a disk image
./scripts/analyze.sh /path/to/image.dd /path/to/case_dir
```

#### 3️⃣ Generate Reports
```bash
# GUI for report generation and packaging
python3 tools/gui/gui.py --case-dir ./cases/case_YYYYMMDDTHHMMSSZ
```

#### 4️⃣ Package for Legal Handoff
```bash
# Validate case integrity first
./scripts/validate_case_before_packaging.sh ./cases/case_YYYYMMDDTHHMMSSZ

# Create legal package (strict validation)
./scripts/package_for_legal_strict.sh ./cases/case_YYYYMMDDTHHMMSSZ ./legal_package.tar.gz

# For probate/estate cases (includes affidavit)
./scripts/create_probate_package.sh ./cases/case_YYYYMMDDTHHMMSSZ ./probate_package.tar.gz
```

---

## 📁 Project Structure

```
crypto-recovery-toolkit/
├── start.sh                      # Main orchestrator
├── scripts/                      # 17 workflow scripts
│   ├── image_disk.sh            # Forensic imaging
│   ├── analyze.sh               # Image analysis
│   ├── package_for_legal_strict.sh
│   ├── create_probate_package.sh
│   └── ...
├── A_rustscanner/               # Rust parallel scanner (PoC)
│   └── src/main.rs
├── B_python_reader/             # JSONL reader utilities
├── tools/
│   ├── gui/                     # Tkinter GUI (monitor + reports)
│   │   ├── gui.py
│   │   └── report_generator.py
│   ├── modules/
│   │   └── search.py            # Python scanner with masking
│   └── slides/                  # Training slide generator
├── templates/                   # 12 legal document templates
│   ├── consent_form.txt
│   ├── chain_of_custody.txt
│   ├── data_processing_agreement.md
│   ├── expert_affidavit.md
│   └── ...
├── training/                    # Training materials
│   ├── module_01_legal.md
│   ├── module_02_imaging.md
│   ├── exercises.md
│   └── quiz.md
├── docs/                        # Technical documentation
├── config/
│   └── case_policy.ini          # Default case configuration
└── yara_rules/                  # YARA signatures
```

---

## 🛡️ Security & Legal

### ⚠️ Critical Warnings

1. **AUTHORIZATION REQUIRED**: Only use with written consent from the asset owner or legal authority
2. **WORK ON COPIES**: Never analyze original storage devices
3. **PRIVACY LAWS**: Ensure compliance with GDPR/DSGVO and local laws
4. **NO AUTO-DECRYPTION**: This toolkit does NOT decrypt wallets automatically
5. **ETHICAL USE ONLY**: For legitimate forensic recovery only

### Security Features

- 🔐 **Offline-capable**: No internet required (air-gap friendly)
- 🔐 **No external Python deps**: Uses only standard library (supply chain security)
- 🔐 **GPG encryption**: Reports can be auto-encrypted
- 🔐 **Secure deletion**: Uses shred/srm for case cleanup
- 🔐 **Read-only mounts**: Prevents accidental evidence modification
- 🔐 **Audit trails**: All actions logged with timestamps

### Legal Compliance

See detailed guides:
- 📄 **GDPR/DSGVO**: `README_GDPR.md`
- 📄 **Legal Evidence**: `docs/legal_readme.md`
- 📄 **Installation & Compliance**: `README_INSTALL_LEGAL.md`
- 📄 **DPIA Template**: `docs/DPIA_template.md`

---

## 🎓 Training

Comprehensive training modules included:

1. **Legal Foundations** (`training/module_01_legal.md`)
   - GDPR compliance, consent, DPA
2. **Imaging** (`training/module_02_imaging.md`)
   - Forensic imaging, hash verification
3. **Analysis** (`training/module_03_analysis.md`)
   - Scanner usage, pattern recognition
4. **Reporting** (`training/module_04_reporting.md`)
   - Report generation, signing, packaging
5. **Operational Security** (`training/module_05_ops_security.md`)
   - Chain of custody, retention, secure deletion

**Exercises**: `training/exercises.md`
**Quiz**: `training/quiz.md`
**Cheat Sheet**: `training/cheatsheet.md`

---

## 🔧 Advanced Configuration

### Case Policy (`config/case_policy.ini`)

```ini
[case]
retention_days = 30              # Auto-delete after X days
encryption_mode = gpg-recipient  # or 'gpg-symmetric'
gpg_recipient = user@example.com # Your GPG key
auto_encrypt = yes               # Encrypt reports automatically
```

### Rust Scanner (High Performance)

```bash
cd A_rustscanner
cargo build --release

# Scan with custom parameters
./target/release/rustscanner \
  --root /mnt/case_mount \
  --head-size 200000 \
  --threads 8 > hits.jsonl

# Process results
python3 B_python_reader/scripts/rustscanner_reader.py \
  --case-dir ./cases/case_XYZ \
  --jsonl hits.jsonl
```

### YARA Rules

Add custom patterns in `yara_rules/wallet_candidates.yar`:

```yara
rule ethereum_keystore {
  strings:
    $json = "\"crypto\""
    $address = "\"address\""
  condition:
    all of them
}
```

---

## 📚 Documentation

- **Installation**: `README_INSTALL_LEGAL.md`
- **GDPR Compliance**: `README_GDPR.md`
- **GUI Usage**: `README_GUI.md`
- **Additional Instructions**: `README_ADDITIONAL_INSTRUCTIONS.md`
- **Architecture**: `.github/copilot-instructions.md`
- **Legal Guides**: `docs/legal_readme.md`
- **API Spec**: `C_api_spec/docs/api_spec.md`

---

## 🤝 Contributing

Contributions welcome! See `CONTRIBUTING.md` for:
- Code standards (Bash, Python, Rust)
- Security requirements
- Testing procedures
- Pull request process

**Please read `SECURITY.md` before contributing** — this is a sensitive forensic toolkit.

---

## 📄 License

MIT License - see `LICENSE` file for details.

**Important**: While the software is open source, you are responsible for:
- Obtaining proper authorization before use
- Compliance with local laws (GDPR, computer fraud laws, etc.)
- Ethical use in legitimate recovery scenarios only

---

## 🌟 Use Cases

### ✅ Legitimate Uses
- **Estate/Probate**: Recovering crypto assets for heirs
- **Owner Recovery**: Authorized recovery of own lost wallets
- **Legal Investigations**: With proper court authorization
- **Corporate Recovery**: With written company authorization

### ❌ Prohibited Uses
- Unauthorized access to others' systems
- Theft or fraud
- Privacy violations without consent
- Circumventing security without authorization

---

## 🔗 Related Projects

- [bulk_extractor](https://github.com/simsong/bulk_extractor) - Forensic tool for extracting features
- [YARA](https://virustotal.github.io/yara/) - Pattern matching tool
- [Autopsy](https://www.autopsy.com/) - Digital forensics platform

---

## 📞 Support & Contact

- **Issues**: Open GitHub issues for bugs/features
- **Security**: See `SECURITY.md` for vulnerability reporting
- **Discussions**: Use GitHub Discussions for questions

---

## 🙏 Credits

Developed for the forensic and legal communities handling crypto asset recovery in estate and authorized recovery cases.

**Contributors**: See `git log` and GitHub contributors page

---

**⚖️ Remember: With great power comes great responsibility. Use ethically and legally.**