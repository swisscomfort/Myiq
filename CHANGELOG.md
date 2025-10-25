# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial public release preparation
- MIT License
- GitHub standard files (CONTRIBUTING, SECURITY, .gitignore)
- Comprehensive documentation structure

## [1.0.0] - 2025-10-25

### Added
- Complete forensic imaging workflow (`start.sh`, `scripts/image_disk.sh`)
- Python-based scanner (`tools/modules/search.py`) with masking and pattern detection
- GDPR-compliant data handling with automatic masking
- Legal compliance framework:
  - Consent forms and DPA templates
  - Chain of custody tracking
  - GPG signature support for all artifacts
- GUI monitor and report generator (`tools/gui/`)
- Packaging scripts for legal handoff:
  - `scripts/package_for_legal_strict.sh`
  - `scripts/create_probate_package.sh`
  - `scripts/validate_case_before_packaging.sh`
- Retention management with systemd timer
- Comprehensive training materials (5 modules + exercises + quiz)
- Support for optional tools: bulk_extractor, YARA
- Automatic encryption support (GPG)
- Multi-report formats: Markdown, HTML, signed variants
- Estate case specialization (probate workflows)
- Wiki framework with taxonomy
- Business and integration planning docs

### Features
- Read-only image mounting with loop devices
- SHA-256 integrity verification
- Pattern-based wallet detection (filename + content)
- Masked snippet generation (hex/mnemonic patterns)
- Affidavit generation for court proceedings
- Witness log templates
- Auto-case setup automation
- Slide generation for training
- Document quality checks

### Security
- No external Python dependencies (standard library only)
- Offline-capable design
- GPG signing and encryption throughout
- Secure deletion support
- Audit logging (JSONL format)
- Air-gap friendly workflows

### Documentation
- German legal templates and READMEs
- English code and technical docs
- DPIA (Data Protection Impact Assessment) template
- Legal evidence checklists
- Installation and compliance guides

### Technical Specifications
- **Languages**: Bash, Python 3.8+
- **Platform**: Debian/Ubuntu Linux
- **Dependencies**: Standard GNU coreutils, GPG, optional YARA
- **Architecture**: Modular shell orchestration + Python scanner
- **Testing**: 21 automated tests (pytest, unittest)
- **Performance**: ~600 files/sec scanning throughput

---

## Release Notes

### v1.0.0 - Initial Public Release

This is the first public release of the Crypto Recovery Toolkit. It has been used internally for estate and forensic cases and is now being released as open source.

**Key Highlights**:
- Production-ready forensic workflows
- Full GDPR/DSGVO compliance features
- Comprehensive legal documentation
- Training materials for operators
- Dual-language support (German templates, English code)

**Known Limitations**:
- Linux-only (Debian/Ubuntu tested)
- No automatic wallet decryption
- Requires manual consent form handling
- No GUI for imaging (CLI only)

**Tested On**:
- Debian 11 (Bullseye)
- Debian 12 (Bookworm)
- Ubuntu 22.04 LTS
- Ubuntu 24.04 LTS

---

[Unreleased]: https://github.com/YOUR_USERNAME/crypto-recovery-toolkit/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/YOUR_USERNAME/crypto-recovery-toolkit/releases/tag/v1.0.0
