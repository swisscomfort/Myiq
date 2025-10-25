# GitHub Manifest

Metadata file for GitHub repository configuration.

**Repository:** crypto-recovery-toolkit
**Description:** Professional offline forensic toolkit for legally compliant crypto-asset recovery
**Language:** Python, Rust, Shell
**License:** MIT
**Status:** Production Ready

## Topics

- forensics
- cryptocurrency
- recovery
- gdpr
- compliance
- linux
- python
- rust
- security
- legal

## Repository Settings Recommendations

### General
- **Description:** Professional offline forensic toolkit for legally compliant crypto-asset recovery with GDPR compliance, dual-scanner architecture, and chain-of-custody tracking
- **Homepage:** (optional: https://...)
- **Visibility:** Public
- **Default Branch:** main

### Features
- ✅ Issues
- ✅ Discussions (enable for Q&A)
- ✅ Wiki (enable for documentation)
- ❌ Projects (optional)

### Security
- ✅ Enable branch protection on `main`
- ✅ Require pull request reviews (min 1)
- ✅ Require status checks to pass
- ✅ Include administrators in restrictions
- ✅ Dismiss stale pull request approvals

### Merge Strategy
- Prefer: "Squash and merge"
- Allow merge commits: Yes
- Allow rebase merge: Yes

## Branch Protection Rules

### Main Branch (`main`)
- Require pull request reviews before merging (1 reviewer)
- Require status checks to pass:
  - `build` (all jobs must pass)
  - `lint` (all jobs must pass)
  - `security` (optional)
- Require branches to be up to date before merging
- Include administrators in restrictions
- Dismiss stale pull request approvals

### Develop Branch (`develop`)
- Similar to main but optional reviewer for faster iteration

## Labels

```yaml
- bug: ff0000 (Red)
- enhancement: 0366d6 (Blue)
- documentation: 0075ca (Dark Blue)
- security: d73a4a (Dark Red)
- good first issue: 7057ff (Purple)
- help wanted: 008672 (Teal)
- wontfix: ffffff (White)
- dependencies: 0366d6 (Blue)
- legal-review: ffb300 (Orange)
```

## Milestones

- v1.0.0 (Initial Release)
- v1.1.0 (Enhancements)
- v2.0.0 (Major Features)

## Release Template

```markdown
## What's New in vX.Y.Z

### Features
- List new features

### Bug Fixes
- List fixed bugs

### Security
- List security improvements

### Breaking Changes
- List any breaking changes

### Installation

\`\`\`bash
git clone https://github.com/YOUR_USERNAME/crypto-recovery-toolkit.git
cd crypto-recovery-toolkit
git checkout vX.Y.Z
\`\`\`

### Contributors
- List contributors
```
