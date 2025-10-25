# Documentation Index

Welcome to the **Crypto Recovery Toolkit** documentation. This index helps you find what you need.

---

## � Getting Started

- **[Quick Start](QUICK_START.md)** — Installation and basic usage (5 minutes)
- **[Installation & Legal Guide](../README_INSTALL_LEGAL.md)** — Detailed setup and compliance checklist

## 👨‍💻 Development

- **[DEVELOPMENT.md](../DEVELOPMENT.md)** — Development setup, code standards, testing, and contributing guide
- **[API Reference](API_REFERENCE.md)** — Python module documentation and JSON schemas

## 🏛️ Legal & Compliance

- **[GDPR/DSGVO Guide](../README_GDPR.md)** — GDPR compliance requirements and technical measures
- **[DPIA Template](DPIA_template.md)** — Data Protection Impact Assessment template
- **[Legal Evidence Guide](legal_readme.md)** — Required artifacts and verification
- **[Legal Templates](../templates/)** — Consent forms, DPA, chain of custody, affidavits

## 📊 Operations

- **[GUI Manual](../README_GUI.md)** — Using the live monitor and report generator
- **[Operators Guide](OPERATORS_GUIDE.md)** — Running investigations, managing cases, troubleshooting

## 🎓 Training

- **[Training Overview](../training/README_TRAINING.md)** — 5 comprehensive modules + exercises
- **[Estate Cases Guide](estate_case_flow.md)** — Specialized probate workflows
- **[Troubleshooting](../training/cheatsheet.md)** — Common issues and solutions

## 🏢 Business & Integration

- **[Integration Plan](../E_integration/docs/integration_plan.md)** — System integration guidance
- **[Business Plan](../F_business/docs/business_plan_on_site.md)** — On-site service considerations

## 🔒 Security

- **[Security Policy](../SECURITY.md)** — Vulnerability reporting and security best practices

## 📋 Project Information

- **[README](../README.md)** — Project overview and features
- **[CHANGELOG](../CHANGELOG.md)** — Version history and release notes
- **[CONTRIBUTING](../CONTRIBUTING.md)** — How to contribute
- **[CODE OF CONDUCT](../CODE_OF_CONDUCT.md)** — Community standards

---

## � Quick Links by Role

### For End Users / Operators
1. Read: **[Quick Start](QUICK_START.md)**
2. Read: **[Operators Guide](OPERATORS_GUIDE.md)**
3. Reference: **[GUI Manual](../README_GUI.md)**, **[Legal Templates](../templates/)**

### For Developers / Contributors
1. Read: **[DEVELOPMENT.md](../DEVELOPMENT.md)**
2. Read: **[API Reference](API_REFERENCE.md)**
3. Reference: **Code in tools/modules/**

### For Legal / Compliance Officers
1. Read: **[GDPR/DSGVO Guide](../README_GDPR.md)**
2. Read: **[Legal Templates](../templates/)**
3. Use: **[DPIA Template](DPIA_template.md)**

### For Trainers / Educators
1. Reference: **[Training Modules](../training/)**
2. Use: **[Exercises & Quiz](../training/exercises.md)**
3. Adapt: **[Templates & Slides](../tools/slides/)**

---

## 📖 Documentation by Role

### For Estate Executors / Legal Professionals
1. [Legal Evidence Guide](legal_readme.md) — What artifacts you'll receive
2. [GDPR Compliance](../README_GDPR.md) — Privacy obligations
3. [Estate Case Workflow](estate_case_flow.md) — Step-by-step process
4. [Training Module 01: Legal](../training/module_01_legal.md) — Legal foundations

### For Forensic Operators
1. [Installation Guide](../README_INSTALL_LEGAL.md) — Setup instructions
2. [Training Modules](../training/) — Complete training program
3. [Cheat Sheet](../training/cheatsheet.md) — Quick reference
4. [GUI Guide](../README_GUI.md) — Interface walkthrough

### For Developers
1. [Architecture](.github/copilot-instructions.md) — System design
2. [Contributing Guide](../CONTRIBUTING.md) — Development standards
3. [API Spec](../C_api_spec/docs/api_spec.md) — Integration points

---

## 🗂️ Document Categories

### Legal Templates (`../templates/`)
- `consent_form.txt` — Client consent
- `data_processing_agreement.md` — DPA for processors
- `chain_of_custody.txt` — Evidence tracking
- `expert_affidavit.md` — Court affidavit
- `witness_log.md` — Witness documentation
- `probate_report.md` — Estate report template
- `notarization_checklist.md` — Notary requirements
- `legal_evidence_checklist.txt` — Evidence validation

### Training Materials (`../training/`)
- `module_01_legal.md` — Legal foundations
- `module_02_imaging.md` — Forensic imaging
- `module_03_analysis.md` — Analysis techniques
- `module_04_reporting.md` — Report generation
- `module_05_ops_security.md` — Operational security
- `module_estate_cases.md` — Estate specialization
- `exercises.md` — Practical exercises
- `quiz.md` — Knowledge assessment
- `cheatsheet.md` — Quick reference

### Scripts Documentation
See inline documentation in each script:
- `scripts/image_disk.sh` — Imaging
- `scripts/analyze.sh` — Analysis
- `scripts/package_for_legal_strict.sh` — Legal packaging
- `scripts/create_probate_package.sh` — Probate packaging
- `scripts/validate_case_before_packaging.sh` — Validation
- And 12 more in `scripts/`

---

## 🔍 Search Tips

### Finding Information
```bash
# Search all documentation
grep -r "keyword" docs/ training/ *.md

# Find specific template
ls templates/ | grep -i consent

# List all training modules
ls training/module_*.md
```

### Common Questions

**Q: How do I image a disk?**
A: See [Training Module 02](../training/module_02_imaging.md) and `scripts/image_disk.sh`

**Q: What legal documents do I need?**
A: See [Legal Evidence Guide](legal_readme.md) and `templates/`

**Q: How do I generate reports?**
A: See [GUI Guide](../README_GUI.md) or [Training Module 04](../training/module_04_reporting.md)

**Q: Is this GDPR compliant?**
A: Yes, see [GDPR Guide](../README_GDPR.md) and [DPIA Template](DPIA_template.md)

**Q: How do I contribute?**
A: See [Contributing Guidelines](../CONTRIBUTING.md)

---

## 📞 Support

- 🐛 **Bug Reports**: GitHub Issues
- 💡 **Feature Requests**: GitHub Issues
- 🔒 **Security Issues**: See [SECURITY.md](../SECURITY.md)
- 💬 **General Questions**: GitHub Discussions

---

## 📄 License

All documentation is licensed under MIT License (see [LICENSE](../LICENSE)).

Legal templates are provided as-is and should be reviewed by qualified legal counsel before use.

---

**Last Updated**: 2025-10-25