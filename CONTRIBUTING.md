# Contributing to Crypto Recovery Toolkit

Thank you for considering contributing! This is a sensitive forensic toolkit, so contributions must meet high standards.

## 🎯 Contribution Areas

- **Bug fixes** in scripts or scanners
- **Documentation** improvements (especially translations)
- **Legal templates** (jurisdiction-specific)
- **Scanner patterns** (new wallet types)
- **Training materials** (case studies, exercises)
- **Testing** (unit tests, integration tests)

## 📋 Before You Start

1. **Check existing issues** — someone may already be working on it
2. **Open an issue** to discuss major changes before coding
3. **Read SECURITY.md** — understand security implications
4. **Review legal docs** — familiarize yourself with GDPR/compliance requirements

## 🔧 Development Setup

### Prerequisites
```bash
# Debian/Ubuntu
sudo apt update
sudo apt install -y git bash python3 python3-tk gnupg coreutils util-linux

# Clone repo
git clone https://github.com/YOUR_USERNAME/crypto-recovery-toolkit.git
cd crypto-recovery-toolkit

# Make scripts executable
chmod +x scripts/*.sh tools/gui/*.py start.sh
```

### Testing
```bash
# Test Python scanner
python3 tools/modules/search.py --root ./test_data --outdir ./test_output

# Validate shell scripts (optional)
shellcheck scripts/*.sh
```

## 📝 Coding Standards

### Shell Scripts
- Use `#!/usr/bin/env bash`
- Always `set -euo pipefail`
- Quote variables: `"$VAR"` not `$VAR`
- Use shellcheck for validation
- Add usage instructions in comments

### Python
- Python 3.8+ compatible
- **Use standard library only** (no external deps for core scripts)
- PEP 8 style (use `black` formatter)
- Type hints encouraged
- Docstrings for functions

### Shell Scripts
- Use `#!/usr/bin/env bash`
- Always include `set -euo pipefail`
- Quote all variables
- Use ShellCheck for linting

## 🔒 Security Requirements

### Critical Rules
1. **Never commit**:
   - Real case data
   - Private keys
   - Actual wallet files
   - Personal information

2. **Sanitize examples**:
   - Use fake/generated data only
   - Mask all sensitive patterns
   - Document clearly as "EXAMPLE ONLY"

3. **Review for**:
   - Injection vulnerabilities (shell, SQL)
   - Path traversal
   - Information leakage
   - Weak cryptography

### Code Review Checklist
- [ ] No hardcoded secrets/keys
- [ ] Input validation present
- [ ] Error messages don't leak sensitive info
- [ ] File operations use safe paths
- [ ] Subprocess calls avoid shell injection
- [ ] GPG operations properly error-handled

## 📄 Documentation

- **Code comments**: Explain *why*, not *what*
- **README updates**: For new features
- **Templates**: Keep legal docs accurate and up-to-date
- **Training materials**: Add exercises for new workflows
- **Changelog**: Update CHANGELOG.md with changes

## 🌍 Translations

We welcome translations! Priority areas:
- German ↔ English for documentation
- Legal templates for other jurisdictions
- Training materials in other languages

## 🧪 Testing

### Manual Testing
```bash
# Create a minimal test case
mkdir -p test_case
echo "test wallet data" > test_case/wallet.dat
./scripts/analyze.sh test_case/test.img test_case
```

### Automated Testing (Future)
- Unit tests in `tests/` directory
- Integration tests in CI/CD
- Coverage reports

## 📤 Pull Request Process

1. **Fork** the repository
2. **Create a branch**: `feature/your-feature-name` or `fix/issue-number`
3. **Make changes**:
   - Follow coding standards
   - Add tests if applicable
   - Update documentation
4. **Test thoroughly**:
   - Run existing tests
   - Test on clean Debian/Ubuntu VM
5. **Commit**:
   - Clear commit messages
   - Reference issues: "Fixes #123"
   - Sign commits (GPG) if possible
6. **Push** and create Pull Request
7. **Describe** your changes:
   - What problem does it solve?
   - How did you test it?
   - Any breaking changes?

## 📋 PR Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings/errors
- [ ] Tested on clean environment
- [ ] CHANGELOG.md updated
- [ ] Security implications considered

## 🎓 Learning Resources

- **Forensic Tools**: SANS SIFT Workstation, Autopsy
- **GDPR Compliance**: Official EU GDPR portal
- **Crypto Wallets**: Bitcoin Developer Guide, Ethereum docs
- **Shell Scripting**: GNU Bash manual
- **Python Forensics**: "Violent Python", "Black Hat Python"

## ⚖️ Legal Considerations

### Contributor Agreement
By contributing, you agree:
- Your contributions are your own work
- You have rights to submit under MIT license
- You understand the legal/ethical implications
- You won't contribute patterns/code for illegal purposes

### Ethical Use
This toolkit is for **legitimate forensic recovery only**:
- Estate/probate cases
- Authorized owner recovery
- Legal investigations with consent

**NOT for**:
- Unauthorized access
- Theft or fraud
- Privacy violations

## 🤝 Community

- **Be respectful**: Constructive feedback only
- **Be patient**: Maintainers are volunteers
- **Be helpful**: Share knowledge with others
- **Be ethical**: Remember the legal/security context

## 📞 Questions?

- Open a GitHub Discussion
- Check existing documentation in `docs/`
- Review training materials in `training/`

---

**Thank you for contributing to secure, ethical forensic recovery!** 🙏
