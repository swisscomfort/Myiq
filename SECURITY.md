# Security Policy

## Reporting Security Vulnerabilities

This is a forensic toolkit designed for legally compliant crypto-asset recovery. Security is paramount.

### How to Report

**DO NOT** create public GitHub issues for security vulnerabilities.

Instead:
1. Email the maintainers directly (see AUTHORS or package.json if added)
2. Encrypt your message with GPG if possible
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Critical issues within 14 days, others within 30 days

## Security Best Practices for Users

### ⚠️ Critical Reminders

1. **Always work on IMAGE COPIES**, never on original evidence
2. **Verify GPG signatures** of all reports and manifests
3. **Obtain written consent** before any analysis (templates in `templates/`)
4. **Encrypt sensitive data** at rest (use `auto_encrypt = yes` in config)
5. **Secure deletion** of old cases using `scripts/secure_delete.sh`
6. **Air-gapped operation** recommended for highest security

### System Security

- Run on **dedicated forensic workstation** (ideally air-gapped)
- Use **full-disk encryption** (LUKS recommended)
- **Minimal software** installed (reduce attack surface)
- **Regular security updates** of OS and dependencies
- **GPG key protection**: Use hardware tokens (YubiKey) for signing keys

### Data Handling

- **Chain of Custody**: Always maintain (template in `templates/chain_of_custody.txt`)
- **Access Logs**: Enable and review regularly (`logs/`)
- **Retention Policy**: Follow configured retention (default 30 days)
- **Secure Transfer**: Use encrypted channels only (GPG, SFTP, physical media)

### Legal Compliance

- **GDPR/DSGVO**: Follow guidelines in `README_GDPR.md`
- **Consent Forms**: Mandatory before analysis (`templates/consent_form.txt`)
- **Data Processing Agreement**: For third-party processing (`templates/data_processing_agreement.md`)
- **Jurisdiction**: Ensure compliance with local laws

## Known Limitations

1. **No automatic wallet decryption** — requires client-provided passphrases
2. **Heuristic scanning** — may have false positives/negatives
3. **Linux-only** — Debian/Ubuntu tested; other distros may need adjustments
4. **Root/sudo required** for imaging and loop device mounting
5. **GPG dependency** — proper key management required

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| < 1.0   | :x:                |

## Security Contacts

- For sensitive security reports, use encrypted email
- Public key available in `docs/` or keyserver
- Response guaranteed within 48 hours

---

**Last Updated**: 2025-10-25
