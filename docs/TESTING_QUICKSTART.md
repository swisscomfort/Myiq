# Testing Quick Start Guide

This guide provides a fast path to running tests and validating the scanner functionality.

## Quick Test Commands

### Run All Tests
```bash
make test
```

### Run Specific Test Suites
```bash
# Scanner unit tests only
make test-scanner

# GUI integration tests only (requires xvfb for headless)
make test-gui

# Shell script validation
make test-shell

# With coverage report
make test-coverage
```

### Run Tests Without Make
```bash
# All tests
python3 -m unittest discover -s tests -p 'test_*.py' -v

# Scanner tests only
python3 tests/test_scanner.py -v

# GUI tests only
python3 tests/test_gui.py -v
```

## Generate Test Data

Create realistic test files for scanner validation:

```bash
# Generate test files in /tmp
python3 tests/create_test_data.py /tmp/test_scan_data

# Generate with disk image (requires root for losetup)
python3 tests/create_test_data.py /tmp/test_scan_data --disk-image --size 50
```

## Test Scanner with Generated Data

### Quick Scanner Test
```bash
# 1. Generate test data
python3 tests/create_test_data.py /tmp/test_scan_data

# 2. Run scanner
python3 tools/modules/search.py --root /tmp/test_scan_data --outdir /tmp/test_output

# 3. Check results
cat /tmp/test_output/scan_results_*.json | python3 -m json.tool | less

# 4. Verify masking (sensitive data should be REDACTED)
grep -i "sensitive" /tmp/test_output/scan_results_*.json
grep "REDACTED" /tmp/test_output/scan_results_*.json

# 5. Clean up
rm -rf /tmp/test_scan_data /tmp/test_output
```

### Full Workflow Test
```bash
# 1. Create test case structure
./scripts/auto_case_setup.sh "Test Client" /tmp/test_case

# 2. Generate test data in case directory
python3 tests/create_test_data.py /tmp/test_case/test_data

# 3. Scan test data
python3 tools/modules/search.py \
    --root /tmp/test_case/test_data \
    --outdir /tmp/test_case/reports

# 4. Check reports
ls -lh /tmp/test_case/reports/

# 5. Clean up
rm -rf /tmp/test_case
```

## GUI Testing

### Manual GUI Test
```bash
# Launch GUI (requires X11 or xvfb)
python3 tools/gui/gui.py

# Test Scanner Tab:
# 1. Select image file: Click "Browse Image" → select .dd file
# 2. Select directory: Click "Browse Directory" → select test_data folder
# 3. Click "Start Scan" → verify output in text area
```

### Headless GUI Test (CI/CD)
```bash
# Install xvfb if needed
sudo apt-get install -y xvfb

# Run GUI tests headless
xvfb-run -a python3 tests/test_gui.py -v
```

## Expected Test Results

### All Tests Should Pass
```
Ran 21 tests in 0.XXXs

OK
```

### Scanner Test Coverage
- ✅ Pattern matching (filenames and content)
- ✅ Hex/mnemonic/text masking
- ✅ File scanning with sensitivity detection
- ✅ Large file handling
- ✅ CLI integration

### GUI Test Coverage
- ✅ Case structure validation
- ✅ Metadata parsing
- ✅ Import validation
- ✅ Scanner script existence
- ✅ File extension validation
- ✅ Helper script checks

## Continuous Integration

Tests run automatically on GitHub Actions for:
- Python 3.8, 3.9, 3.10, 3.11
- Code formatting (black)
- Linting (pylint)
- Shell script validation
- Security scanning

## Troubleshooting

### ModuleNotFoundError
```bash
# Ensure you're in project root
cd /path/to/project

# Install dependencies
pip3 install -r requirements.txt
```

### GUI Tests Fail on Headless System
```bash
# Install and use xvfb
sudo apt-get install xvfb
xvfb-run -a python3 tests/test_gui.py
```

### Test Data Not Found
```bash
# Regenerate test data
python3 tests/create_test_data.py /tmp/test_scan_data
```

### Permission Denied for Disk Image Creation
```bash
# Disk image creation requires root (uses losetup)
sudo python3 tests/create_test_data.py /tmp/test_scan_data --disk-image
```

## Performance Benchmarks

Typical test execution times:
- Unit tests (scanner): ~0.1s
- Integration tests (GUI): ~0.5s
- Full test suite: ~0.6s
- Scanner on 1000 files: ~2-5s (depends on file sizes)

## Next Steps

After validating tests:
1. Review test coverage: `make test-coverage`
2. Check code formatting: `make format`
3. Run linting: `make lint`
4. Review documentation: `docs/TESTING.md`
5. Explore GUI scanner: `docs/GUI_SCANNER_GUIDE.md`

## Additional Resources

- **Comprehensive Testing Guide**: `docs/TESTING.md`
- **Test Suite Documentation**: `tests/README.md`
- **GUI Scanner Guide**: `docs/GUI_SCANNER_GUIDE.md`
- **Operators Guide**: `docs/OPERATORS_GUIDE.md`
- **API Reference**: `docs/API_REFERENCE.md`

---
Last updated: 2025-10-25
