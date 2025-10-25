# Testing Guide

Dieses Dokument beschreibt wie der Scanner und die GUI getestet werden.

## Überblick

Das Projekt nutzt:
- **Python unittest** - Standard-Testing-Framework (keine Installation nötig)
- **pytest** - Optional für erweiterte Features (Coverage, Fixtures)
- **GitHub Actions** - Automatisierte CI/CD-Tests bei jedem Push/PR

## Schnellstart

```bash
# Alle Tests ausführen
make test

# Scanner-Tests nur
make test-scanner

# GUI-Tests nur
make test-gui

# Mit Coverage-Report
make test-coverage

# Shell-Script Validierung
make test-shell
```

## Test-Struktur

```
tests/
├── README.md              # Test-Dokumentation
├── test_scanner.py        # Scanner Unit-Tests (10 Tests)
└── test_gui.py           # GUI Integration-Tests (11 Tests)
```

### Test-Coverage

**Scanner Tests (`test_scanner.py`):**
- ✅ Pattern Matching (Dateinamen, Content)
- ✅ Masking (Hex, Mnemonics, Text)
- ✅ File Scanning (Wallet-Erkennung, Sensitive-Data-Maskierung)
- ✅ SHA-256 Hash-Berechnung
- ✅ CLI-Integration

**GUI Tests (`test_gui.py`):**
- ✅ Case-Struktur-Validierung
- ✅ Metadata-Parsing
- ✅ Scanner-Integration
- ✅ File-Format-Validierung
- ✅ Helper-Scripts-Existenz

## Lokales Testen

### Mit unittest (empfohlen - keine Installation nötig)

```bash
# Alle Tests
python3 -m unittest discover tests/ -v

# Einzelner Test
python3 tests/test_scanner.py

# Spezifischer Test
python3 -m unittest tests.test_scanner.TestScanner.test_scan_finds_wallet_files
```

### Mit pytest (optional - erweiterte Features)

```bash
# Installation
pip3 install pytest pytest-cov

# Alle Tests mit Ausgabe
python3 -m pytest tests/ -v

# Mit Coverage
python3 -m pytest tests/ --cov=tools --cov-report=html

# Nur fehlgeschlagene Tests erneut ausführen
python3 -m pytest tests/ --lf

# Stoppe bei erstem Fehler
python3 -m pytest tests/ -x
```

### Shell-Script Tests

```bash
# Syntax-Validierung
make test-shell

# Oder manuell
bash -n scripts/analyze.sh
bash -n start.sh
shellcheck scripts/*.sh
```

## GitHub Actions (CI/CD)

Tests laufen automatisch bei:
- Push auf `main` oder `develop` Branch
- Pull Requests zu `main` oder `develop`

### Workflows

**`.github/workflows/python.yml`** - Python Testing
- Matrix: Python 3.8, 3.9, 3.10, 3.11
- Schritte:
  1. Code Checkout
  2. Python Setup
  3. Dependencies Installation (inkl. xvfb für GUI)
  4. Black Formatting Check
  5. Pylint Linting
  6. Syntax Check
  7. **Scanner Tests**
  8. **GUI Tests (headless mit xvfb)**
  9. Coverage Report
  10. Coverage Upload (nur Python 3.11)

**`.github/workflows/shell.yml`** - Shell Script Validation
- Shellcheck für alle `.sh` Dateien
- Syntax-Validierung mit `bash -n`

**`.github/workflows/security.yml`** - Security Scans

### Workflow lokal nachstellen

```bash
# Wie GitHub Actions
python3 -m pip install pylint black pytest pytest-cov
black --check tools/ tests/
pylint tools/**/*.py tests/**/*.py || true
python3 -m pytest tests/ -v --cov=tools
```

## Test-Daten & Fixtures

### Temporäre Test-Verzeichnisse

Tests erstellen temporäre Verzeichnisse:

```python
import tempfile
import shutil

def setUp(self):
    self.test_dir = tempfile.mkdtemp(prefix="test_")

def tearDown(self):
    shutil.rmtree(self.test_dir, ignore_errors=True)
```

### Test-Dateien

Scanner-Tests erstellen Test-Wallet-Dateien:

```python
test_files = {
    "wallet.dat": "wallet content",
    "keystore.json": '{"crypto": {...}}',
    "mnemonic.txt": "abandon ability able...",
}
```

## Neue Tests hinzufügen

### 1. Test-Datei erstellen

```python
#!/usr/bin/env python3
import unittest
import sys
import os

# Import-Path Setup
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.modules import search

class TestNeueFeature(unittest.TestCase):
    def setUp(self):
        """Setup vor jedem Test"""
        pass

    def tearDown(self):
        """Cleanup nach jedem Test"""
        pass

    def test_beispiel(self):
        """Test-Beschreibung"""
        result = search.some_function()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
```

### 2. Test ausführen

```bash
python3 tests/test_neue_feature.py
```

### 3. GitHub Actions anpassen (optional)

Tests im `tests/` Verzeichnis werden automatisch erkannt.
Nur bei speziellen Requirements `.github/workflows/python.yml` anpassen.

## Test-Best-Practices

### 1. Test-Isolation
```python
# Gut: Jeder Test ist unabhängig
def test_feature_a(self):
    data = create_test_data()
    result = process(data)
    self.assertEqual(result, expected)

# Schlecht: Tests teilen sich State
class_var = None  # Shared state!
def test_feature_a(self):
    self.class_var = "data"
```

### 2. Cleanup
```python
def tearDown(self):
    # IMMER temp-Dateien aufräumen
    if hasattr(self, 'test_dir') and os.path.exists(self.test_dir):
        shutil.rmtree(self.test_dir, ignore_errors=True)
```

### 3. Aussagekräftige Assertions
```python
# Gut
self.assertEqual(len(findings), 3,
                f"Expected 3 findings, got {len(findings)}")

# Schlecht
self.assertEqual(len(findings), 3)
```

### 4. Mock externe Dependencies
```python
import unittest.mock as mock

@mock.patch('subprocess.run')
def test_with_mock(self, mock_run):
    mock_run.return_value = mock.Mock(returncode=0)
    result = run_scanner()
    self.assertTrue(result)
```

## Troubleshooting

### Tests schlagen fehl: "No module named 'tools'"

**Problem:** Python findet Module nicht

**Lösung:**
```bash
# Aus Repository-Root ausführen
cd /path/to/crypto-recovery-toolkit
python3 tests/test_scanner.py
```

### GUI-Tests schlagen fehl: "no display name"

**Problem:** Kein X11-Display verfügbar

**Lösung:**
```bash
# Installiere xvfb
sudo apt-get install xvfb

# Führe mit xvfb aus
xvfb-run python3 tests/test_gui.py
```

### ImportError bei pytest

**Problem:** pytest nicht installiert

**Lösung:**
```bash
# Nutze unittest (keine Installation nötig)
python3 -m unittest discover tests/

# Oder installiere pytest
pip3 install pytest pytest-cov
```

### Coverage-Report fehlt

**Problem:** pytest-cov nicht installiert

**Lösung:**
```bash
pip3 install pytest-cov
python3 -m pytest tests/ --cov=tools --cov-report=html
```

## Coverage-Ziele

| Komponente | Target | Aktuell |
|-----------|--------|---------|
| `tools/modules/search.py` | 80% | ✅ ~85% |
| `tools/gui/gui.py` | 60% | ✅ ~65% |
| `tools/gui/report_generator.py` | 70% | 🔄 In Arbeit |

Coverage-Report anzeigen:
```bash
make test-coverage
xdg-open htmlcov/index.html
```

## Continuous Testing während Entwicklung

### Watch-Mode (mit pytest-watch)

```bash
# Installation
pip3 install pytest-watch

# Auto-Run bei Datei-Änderungen
ptw tests/ -- -v
```

### VS Code Integration

`.vscode/settings.json`:
```json
{
    "python.testing.unittestEnabled": true,
    "python.testing.unittestArgs": [
        "-v",
        "-s",
        "./tests",
        "-p",
        "test_*.py"
    ],
    "python.testing.pytestEnabled": false
}
```

## Performance Testing

Für Performance-Tests:

```python
import time

def test_scanner_performance(self):
    start = time.time()
    search.scan(large_directory, output_dir)
    duration = time.time() - start
    self.assertLess(duration, 60, "Scan should complete in <60s")
```

## Siehe auch

- [tests/README.md](../tests/README.md) - Detaillierte Test-Dokumentation
- [DEVELOPMENT.md](../DEVELOPMENT.md) - Entwicklungs-Guide
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution-Guidelines
- [.github/workflows/](../.github/workflows/) - CI/CD Konfiguration
