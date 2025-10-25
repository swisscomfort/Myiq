# Tests

Dieses Verzeichnis enthält automatisierte Tests für das Crypto Recovery Toolkit.

## Test-Dateien

- `test_scanner.py` - Unit-Tests für den Python-Scanner (`tools/modules/search.py`)
- `test_gui.py` - Tests für GUI-Funktionen und Integration

## Tests ausführen

### Alle Tests ausführen

```bash
# Mit unittest (Python Standard Library)
python3 -m unittest discover tests/

# Mit pytest (falls installiert)
python3 -m pytest tests/ -v

# Via Makefile
make test
```

### Einzelne Test-Dateien ausführen

```bash
# Scanner-Tests
python3 tests/test_scanner.py

# GUI-Tests
python3 tests/test_gui.py

# Mit pytest
python3 -m pytest tests/test_scanner.py -v
```

### Mit Coverage

```bash
# Installiere pytest-cov
pip3 install pytest pytest-cov

# Tests mit Coverage ausführen
python3 -m pytest tests/ --cov=tools --cov-report=html --cov-report=term

# HTML-Report öffnen
xdg-open htmlcov/index.html
```

## Test-Kategorien

### Scanner-Tests (`test_scanner.py`)

**Pattern Matching Tests:**
- `test_filename_patterns` - Testet Dateinamen-Erkennung (wallet.dat, keystore.json, etc.)
- `test_content_patterns` - Testet Content-Pattern-Matching (JSON-Keystores, Hex, Mnemonics)

**Masking Tests:**
- `test_mask_hex` - Testet Hex-String-Maskierung
- `test_mask_mnemonic` - Testet Mnemonic-Phrase-Maskierung
- `test_mask_text` - Testet allgemeine Text-Maskierung

**Scanner Funktionalität:**
- `test_scan_finds_wallet_files` - Prüft ob Wallet-Dateien gefunden werden
- `test_scan_masks_sensitive_data` - Prüft ob Daten maskiert werden
- `test_scan_respects_file_size_limit` - Prüft Handling von großen Dateien
- `test_file_sha256` - Testet SHA-256 Hash-Berechnung

**Integration Tests:**
- `test_command_line_execution` - Testet CLI-Ausführung

### GUI-Tests (`test_gui.py`)

**GUI Funktionen:**
- `test_case_directory_structure` - Prüft Case-Verzeichnis-Struktur
- `test_metadata_parsing` - Testet Metadata-Parsing
- `test_gui_imports` - Testet ob GUI-Module importiert werden können

**Scanner Integration:**
- `test_scanner_script_exists` - Prüft ob Scanner-Script existiert
- `test_analyze_script_exists` - Prüft ob analyze.sh existiert
- `test_directory_scan_simulation` - Simuliert Verzeichnis-Scan

**Validierung:**
- `test_image_file_extensions` - Testet Image-Dateiformat-Validierung
- `test_path_validation` - Testet Pfad-Validierung

**Helper Scripts:**
- `test_log_event_script_exists` - Prüft log_event.sh
- `test_validation_scripts_exist` - Prüft Validierungs-Scripts

## CI/CD Integration

Tests werden automatisch via GitHub Actions ausgeführt:

- **Python Workflow** (`.github/workflows/python.yml`)
  - Läuft bei jedem Push/PR auf `main` und `develop`
  - Testet Python 3.8, 3.9, 3.10, 3.11
  - Führt Linting (pylint, black) aus
  - Führt alle Tests aus
  - Generiert Coverage-Report
  - GUI-Tests laufen mit xvfb (headless)

- **Shell Workflow** (`.github/workflows/shell.yml`)
  - Validiert alle Shell-Scripts mit shellcheck

- **Security Workflow** (`.github/workflows/security.yml`)
  - Security-Scans

## Test-Daten

Tests erstellen temporäre Verzeichnisse mit Test-Dateien:
- Temporäre Verzeichnisse werden mit `tempfile.mkdtemp()` erstellt
- Automatische Bereinigung in `tearDown()` Methoden
- Keine persistenten Test-Daten im Repository

## Neue Tests hinzufügen

### 1. Test-Datei erstellen

```python
#!/usr/bin/env python3
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestNeueFeature(unittest.TestCase):
    def test_beispiel(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
```

### 2. Test zu GitHub Actions hinzufügen

Die Tests werden automatisch erkannt wenn sie:
- Im `tests/` Verzeichnis liegen
- Mit `test_` beginnen
- `unittest.TestCase` erben

### 3. Test lokal ausführen

```bash
python3 tests/test_neue_feature.py
```

## Troubleshooting

### ImportError: No module named 'pytest'

**Lösung:**
```bash
pip3 install pytest pytest-cov
```

Oder nutze unittest (keine Installation nötig):
```bash
python3 -m unittest discover tests/
```

### GUI-Tests schlagen fehl (Display-Fehler)

**Lösung:** Nutze xvfb für headless-Testing:
```bash
sudo apt-get install xvfb
xvfb-run python3 tests/test_gui.py
```

### Tests finden Module nicht

**Lösung:** Tests müssen aus Repository-Root ausgeführt werden:
```bash
cd /path/to/crypto-recovery-toolkit
python3 tests/test_scanner.py
```

## Best Practices

1. **Isolierte Tests**: Jeder Test sollte unabhängig laufen können
2. **Cleanup**: `tearDown()` sollte immer temp-Dateien aufräumen
3. **Mocking**: Externe Dependencies (GPG, Disk-Operationen) sollten gemockt werden
4. **Fast Tests**: Tests sollten schnell sein (<5 Sekunden pro Test)
5. **Aussagekräftige Namen**: Test-Namen beschreiben was getestet wird
6. **Dokumentation**: Docstrings erklären den Test-Zweck

## Coverage-Ziele

- **Scanner (`tools/modules/search.py`)**: >80% Code-Coverage
- **GUI (`tools/gui/*.py`)**: >60% Code-Coverage (GUI ist schwer zu testen)
- **Report Generator**: >70% Code-Coverage

Aktuellen Coverage-Report anzeigen:
```bash
python3 -m pytest tests/ --cov=tools --cov-report=term
```

## Siehe auch

- [DEVELOPMENT.md](../DEVELOPMENT.md) - Entwicklungs-Guide
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution-Guidelines
- [.github/workflows/](../.github/workflows/) - CI/CD Konfiguration
