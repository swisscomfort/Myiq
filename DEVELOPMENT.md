# Development Guide

Welcome! This guide helps you set up a development environment and contribute to the Crypto Recovery Toolkit.

## Table of Contents

1. [Quick Setup](#quick-setup)
2. [Development Workflow](#development-workflow)
3. [Code Standards](#code-standards)
4. [Testing](#testing)
5. [Building & Releasing](#building--releasing)

---

## Quick Setup

### Prerequisites

- **OS**: Debian/Ubuntu Linux
- **Tools**: bash, python3, git
- **Permissions**: sudo access for optional tool installation

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/crypto-recovery-toolkit.git
cd crypto-recovery-toolkit

# Install development dependencies
make install-dev

# Verify installation
python3 tools/modules/search.py --help
```

### Recommended IDEs/Editors

- **VS Code** with extensions:
  - Python (for Python development)
  - ShellFormat (for shell scripts)
  - EditorConfig (for consistent formatting)
- **PyCharm** (Python-focused)
- **Sublime Text** or **vim** (lightweight)

---

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` — new features or enhancements
- `bugfix/` — bug fixes
- `docs/` — documentation improvements
- `refactor/` — code refactoring
- `chore/` — maintenance tasks

### 2. Make Changes

Follow the code standards below. Make atomic, logical commits:

```bash
git add <files>
git commit -m "descriptive commit message"
```

### 3. Run Tests & Linters

Before committing, verify code quality:

```bash
# Format code
make format

# Run linters
make lint

# Run tests (if applicable)
make test
```

### 4. Open a Pull Request

Push your branch and open a PR on GitHub:

```bash
git push origin feature/your-feature-name
```

In the PR description, explain:
- **What** you changed
- **Why** you made the change
- **How** to test it

---

## Code Standards

### Python

**Style:**
- Follow PEP 8 using `black` formatter
- Use 4-space indentation
- Type hints are encouraged (Python 3.8+)

**Dependencies:**
- Core scripts use **only Python standard library** (no external PyPI packages)
- GUI may use Tkinter (usually pre-installed)
- Development/testing can use external tools (pytest, pylint, black)

**Example:**

```python
#!/usr/bin/env python3
"""Module docstring describing the module's purpose."""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional


def process_findings(
    input_file: str, output_dir: str, mask: bool = True
) -> Dict[str, List[str]]:
    """
    Process forensic findings from input file.

    Args:
        input_file: Path to input JSON file
        output_dir: Directory for output reports
        mask: Whether to mask sensitive data

    Returns:
        Dictionary of processed findings
    """
    result = {}
    # Implementation...
    return result


if __name__ == "__main__":
    # Main execution
    pass
```

Format and validate:

```bash
black your_file.py
pylint your_file.py
```

### Shell Scripts

**Style:**
- Use `#!/usr/bin/env bash` shebang
- Always use `set -euo pipefail` at the start
- Quote variables: `"$VAR"` not `$VAR`
- Use meaningful variable names
- Add comments for complex logic

**Example:**

```bash
#!/usr/bin/env bash
set -euo pipefail

# Description of script purpose

main() {
    local input_file="$1"
    local output_dir="$2"

    if [[ ! -f "$input_file" ]]; then
        echo "Error: Input file not found: $input_file" >&2
        return 1
    fi

    # Implementation...
    echo "Processing complete: $output_dir"
}

main "$@"
```

Validate:

```bash
bash -n your_script.sh
shellcheck your_script.sh
```

---

## Testing

### Python Tests

Create test files in `tests/` directory:

```bash
# tests/test_search.py
import unittest
from tools.modules.search import process_findings


class TestSearch(unittest.TestCase):
    def test_process_findings(self):
        result = process_findings("test_input.json", "./output")
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
```

Run tests:

```bash
python3 -m pytest tests/ -v
# or
make test
```

### Test Coverage

Check test coverage:

```bash
make test-coverage
```

Run specific test suites:

```bash
make test-scanner  # Scanner unit tests only
make test-gui      # GUI integration tests only
make benchmark     # Performance benchmarks
```

### Manual Testing

For workflow changes, test the complete workflow:

```bash
# Create a test image (see training/exercises.md)
dd if=/dev/zero of=test_image.dd bs=1M count=100

# Run analysis
./scripts/analyze.sh ./test_image.dd ./test_case

# Verify reports
ls test_case/reports/
```

---

## Building & Releasing

### Building for Release

```bash
# Create distribution package
tar -czf crypto-recovery-toolkit-v1.0.0.tar.gz \
    --exclude='.git' \
    --exclude='__pycache__' \
    .
```

### Version Management

This project follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes (e.g., incompatible report schema change)
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

Update version in:
1. `CHANGELOG.md` — Add new section with release date
2. Git tag: `git tag -a vX.Y.Z -m "Release version X.Y.Z"`

### Creating a Release

```bash
# Update versions
# Update CHANGELOG.md
git add .
git commit -m "Release version X.Y.Z"

# Tag the release
git tag -a vX.Y.Z -m "Release version X.Y.Z"

# Push to GitHub
git push origin main
git push origin vX.Y.Z

# Create release on GitHub (manual or via CLI)
gh release create vX.Y.Z --generate-notes
```

---

## Security Considerations

### Code Review Checklist

Before submitting code, verify:

- [ ] No hardcoded secrets, API keys, or credentials
- [ ] No real forensic data or case information
- [ ] Input validation for all external inputs
- [ ] Error messages don't leak sensitive information
- [ ] File paths are properly quoted and validated
- [ ] Dependencies are minimal and vetted
- [ ] Comments clarify security-critical sections

### Reporting Security Issues

Please see `SECURITY.md` for responsible disclosure procedures.

---

## Troubleshooting

### Common Issues

**Python import errors:**

```bash
# Verify Python version
python3 --version  # Should be 3.8+

# Test import
python3 -c "from tools.modules.search import *"
```

**Shell script permission denied:**

```bash
chmod +x scripts/*.sh start.sh tools/gui/*.py
```

**Git merge conflicts:**

```bash
# Check conflicts
git status

# Resolve manually, then:
git add <resolved_files>
git commit -m "Resolve merge conflicts"
```

---

## Getting Help

- **Documentation**: See `docs/` and `training/` directories
- **Issues**: Check GitHub Issues for known problems
- **Contact**: See `SECURITY.md` for security issues; use GitHub Discussions for general questions

Thank you for contributing! 🙌
