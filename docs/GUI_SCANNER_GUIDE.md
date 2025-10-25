# GUI Scanner Guide

## Übersicht

Die GUI (`tools/gui/gui.py`) enthält nun einen **Scanner-Tab**, der es ermöglicht, Disk-Images oder Verzeichnisse direkt aus der Oberfläche zu scannen.

## Scanner-Tab Funktionen

### 1. Disk-Image Scannen

**Schritte:**
1. Öffne die GUI mit einem existierenden Case-Verzeichnis:
   ```bash
   python3 tools/gui/gui.py --case-dir ./cases/case_YYYYMMDDTHHMMSSZ
   ```

2. Wechsle zum **"Scanner"** Tab

3. Klicke auf **"Browse Image..."**
   - Wähle ein Disk-Image aus (unterstützte Formate: `.dd`, `.img`, `.raw`, `.E01`)
   - Der Datei-Dialog zeigt nur relevante Dateitypen an

4. Überprüfe das **Output directory** (standardmäßig `case_dir/reports`)
   - Optional: Klicke auf "Change..." um ein anderes Verzeichnis zu wählen

5. Klicke auf **"▶ Start Scan"**
   - Der Scan-Prozess läuft im Hintergrund
   - Fortschritt wird im Output-Bereich angezeigt
   - Nach Abschluss werden die Findings automatisch aktualisiert

**Hinweis:** Beim Scannen eines Images wird `scripts/analyze.sh` ausgeführt, das:
- Das Image als Loop-Device mountet
- Read-only Zugriff sicherstellt
- Den Python-Scanner ausführt
- Optional YARA/bulk_extractor nutzt (falls installiert)

### 2. Verzeichnis Scannen

**Schritte:**
1. Wechsle zum **"Scanner"** Tab

2. Klicke auf **"Browse Directory..."**
   - Wähle ein Verzeichnis aus (z.B. gemountetes Dateisystem, USB-Stick)
   - Das Verzeichnis wird direkt gescannt (kein Mount nötig)

3. Überprüfe das **Output directory**

4. Klicke auf **"▶ Start Scan"**
   - Der Python-Scanner (`tools/modules/search.py`) wird direkt ausgeführt
   - Schneller als Image-Scan (kein Mount/Unmount)

**Vorteil:** Direktes Scannen ohne Image-Erstellung für:
- Bereits gemountete Dateisysteme
- USB-Sticks oder externe Festplatten
- Netzwerk-Freigaben
- Test-Verzeichnisse

### 3. Scan-Optionen

- **Nur EINES wählen:** Entweder Image ODER Verzeichnis (nicht beides)
- **Clear-Buttons:** Setzen die Auswahl zurück
- **Status-Anzeige:** Zeigt "Ready", "Scanning...", "Completed", oder "Failed"
- **Live-Output:** Zeigt den Scan-Fortschritt in Echtzeit

## Unterstützte Dateiformate

### Disk-Images
- `.dd` - RAW disk dump (dd, dcfldd)
- `.img` - Generic disk image
- `.raw` - RAW image format
- `.E01` - EnCase Evidence File (Expert Witness Format)

### Verzeichnisse
- Beliebige Ordner-Struktur
- Empfohlen für bereits gemountete Dateisysteme

## Workflow-Beispiele

### Beispiel 1: Forensisches Image analysieren

```bash
# 1. Case erstellen
./start.sh /dev/sdX ./cases "Client Name"

# 2. GUI öffnen
python3 tools/gui/gui.py --case-dir ./cases/case_YYYYMMDDTHHMMSSZ

# 3. In GUI:
#    - Tab "Scanner" öffnen
#    - "Browse Image..." klicken
#    - case_*/image.dd auswählen
#    - "Start Scan" klicken
```

### Beispiel 2: USB-Stick scannen

```bash
# 1. USB-Stick mounten
sudo mount /dev/sdb1 /mnt/usb

# 2. GUI öffnen
python3 tools/gui/gui.py --case-dir ./cases/case_YYYYMMDDTHHMMSSZ

# 3. In GUI:
#    - Tab "Scanner" öffnen
#    - "Browse Directory..." klicken
#    - /mnt/usb auswählen
#    - "Start Scan" klicken
```

### Beispiel 3: Existing Image neu scannen

```bash
# Wenn analyze.sh bereits gelaufen ist, aber neue Patterns hinzugefügt wurden:

# GUI öffnen
python3 tools/gui/gui.py --case-dir ./cases/case_YYYYMMDDTHHMMSSZ

# In GUI:
#    - Tab "Scanner"
#    - "Browse Image..." → vorhandenes image.dd auswählen
#    - "Start Scan" → Wird erneut gescannt mit aktuellen Patterns
```

## Fehlerbehebung

### Problem: "Script not found: scripts/analyze.sh"
**Lösung:** GUI muss aus dem Repository-Hauptverzeichnis gestartet werden:
```bash
cd /path/to/crypto-recovery-toolkit
python3 tools/gui/gui.py --case-dir ./cases/...
```

### Problem: "Permission denied" beim Image-Scan
**Lösung:** Loop-Device-Operationen erfordern oft root-Rechte:
```bash
sudo python3 tools/gui/gui.py --case-dir ./cases/...
```

### Problem: Filedialog öffnet nicht
**Lösung:** Stelle sicher, dass Python3-Tk installiert ist:
```bash
sudo apt install python3-tk
```

### Problem: Scan bleibt hängen
**Lösung:**
- Große Images können lange dauern (mehrere Stunden)
- Prüfe den Output-Bereich für Fehlermeldungen
- Prüfe `case_dir/logs/process.log` für Details

## Scanner-Tab Features

✅ **File-Browser Integration:**
- Native OS-Datei-Dialoge (via `tkinter.filedialog`)
- Dateitype-Filter für Images
- Recent directories werden gemerkt

✅ **Validierung:**
- Verhindert gleichzeitige Image- und Verzeichnis-Auswahl
- Prüft ob Output-Verzeichnis schreibbar ist
- Warnt bei fehlenden Scripts

✅ **Threading:**
- Scan läuft in separatem Thread
- GUI bleibt responsiv während des Scans
- Live-Output wird gestreamt

✅ **Automatische Integration:**
- Scan-Ergebnisse werden automatisch in "Findings" Tab geladen
- Logs werden in `case_dir/logs/` geschrieben
- Chain-of-Custody wird aktualisiert

## Sicherheitshinweise

⚠️ **Wichtig:**
- Scanne NIE Original-Datenträger direkt (arbeite immer mit Kopien/Images)
- Bei Images: Read-only Mount wird automatisch erzwungen
- Bei Verzeichnissen: Der Scanner liest nur, schreibt nicht
- GPG-Verschlüsselung kann nach dem Scan aktiviert werden (siehe Reports-Tab)

## Siehe auch

- [GUI Manual](../README_GUI.md) - Vollständige GUI-Dokumentation
- [Operators Guide](OPERATORS_GUIDE.md) - Workflow-Anleitungen
- [Quick Start](QUICK_START.md) - Erste Schritte

---

**Version:** 1.1.0 (mit Scanner-Tab)
**Erstellt:** 2025-10-25
**Autor:** Crypto Recovery Toolkit Team
