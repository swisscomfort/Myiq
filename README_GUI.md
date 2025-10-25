# GUI: Live-Monitor & Scanner für Fälle

## Überblick

Die GUI bietet:
- **Scanner-Tab**: Disk-Images oder Verzeichnisse auswählen und scannen
- **Monitor-Tab**: Live-Log, Ereignisstand und Fortschritt anzeigen
- **Findings-Tab**: Maskierte Treffer durchsuchen
- **Reports-Tab**: Owner/Court Reports generieren und signieren

Offline-fähig; kann lokal genutzt werden, z.B. vor Ort beim Kunden.

## Abhängigkeiten

- python3 (bereits benötigt)
- python3-tk (Tkinter): `sudo apt install python3-tk`

## Installation

1. GUI-Dateien sind bereits im Repository: `tools/gui/gui.py`
2. Script ausführbar machen: `chmod +x tools/gui/gui.py`
3. Log-Helper: `chmod +x scripts/log_event.sh`

## Neue Funktion: Scanner-Tab

Der Scanner-Tab ermöglicht das direkte Scannen aus der GUI:

### Disk-Image scannen
1. GUI öffnen: `python3 tools/gui/gui.py --case-dir ./cases/case_YYYYMMDDTHHMMSSZ`
2. Tab "Scanner" auswählen
3. "Browse Image..." klicken und .dd/.img/.raw/.E01 Datei auswählen
4. "Start Scan" klicken

**Hinweis:** Nutzt `scripts/analyze.sh` (mount → scan → unmount)

### Verzeichnis scannen
1. GUI öffnen
2. Tab "Scanner" auswählen
3. "Browse Directory..." klicken und Ordner auswählen (z.B. gemounteter USB-Stick)
4. "Start Scan" klicken

**Vorteil:** Direkter Scan ohne Image-Erstellung, nutzt `tools/modules/search.py`

### Unterstützte Formate
- **Images**: `.dd`, `.img`, `.raw`, `.E01`
- **Verzeichnisse**: Beliebige Ordner-Strukturen

**Siehe auch:** Detaillierte Anleitung in [GUI Scanner Guide](docs/GUI_SCANNER_GUIDE.md)

## Integration mit Workflow

Füge in `start.sh` und `analyze.sh` an wichtigen Stellen Aufrufe zu `scripts/log_event.sh` ein:
```bash
bash scripts/log_event.sh "$case_dir" info "Imaging started" 5
bash scripts/log_event.sh "$case_dir" info "Imaging completed" 20
bash scripts/log_event.sh "$case_dir" info "Analysis started" 30
bash scripts/log_event.sh "$case_dir" info "Reports generated" 80
bash scripts/log_event.sh "$case_dir" info "Case finished" 100
```

## GUI Starten

```bash
# Während oder nach der Analyse
python3 tools/gui/gui.py --case-dir ./cases/case_2025...

# Mit sudo (falls Loop-Devices für Image-Scan benötigt)
sudo python3 tools/gui/gui.py --case-dir ./cases/...
```

## GUI-Tabs Übersicht

### 1. Scanner-Tab (NEU!)
- Disk-Images oder Verzeichnisse auswählen
- Scan-Prozess starten und überwachen
- Live-Output während des Scans
- Automatische Findings-Aktualisierung nach Scan

### 2. Monitor / Log-Tab
- Live-Log-Anzeige
- Letzter Ereignisstand
- Fortschrittsbalken (0-100%)

### 3. Masked Findings-Tab
- Treeview mit maskierten Treffern
- Sortierbar nach Datei, Snippet, Größe
- "Refresh findings" Button

### 4. Reports / Export-Tab
- Owner Report generieren
- Court Report generieren (benötigt Consent)
- GPG-Signierung
- Legal/Probate Package erstellen
- Affidavit Editor

## Datenschutz / DSGVO Hinweis

⚠️ **Wichtig:**
- GUI zeigt nur maskierte Snippets aus Reports
- Keine Schlüssel werden entschlüsselt oder im Klartext angezeigt
- Scanner arbeitet read-only (keine Modifikation von Quellen)
- Zeige das GUI dem Kunden nur nach unterschriebener Einwilligung und ggf. DPA

## Troubleshooting

### GUI startet nicht
```bash
# Tkinter installieren
sudo apt install python3-tk

# Python-Version prüfen (>= 3.8)
python3 --version
```

### "ModuleNotFoundError: No module named 'tools'"
```bash
# GUI muss aus Repository-Hauptverzeichnis gestartet werden
cd /path/to/crypto-recovery-toolkit
python3 tools/gui/gui.py --case-dir ./cases/...
```

### Image-Scan schlägt fehl
```bash
# Loop-Device-Operationen benötigen oft root
sudo python3 tools/gui/gui.py --case-dir ./cases/...
```

### Filedialog öffnet nicht
- X11-Forwarding aktivieren (bei SSH): `ssh -X user@host`
- Oder: Lokal auf dem System mit GUI ausführen

## Siehe auch

- [GUI Scanner Guide](docs/GUI_SCANNER_GUIDE.md) - Detaillierte Scanner-Anleitung
- [Operators Guide](docs/OPERATORS_GUIDE.md) - Komplette Workflow-Dokumentation
- [Quick Start](docs/QUICK_START.md) - Schnelleinstieg

---

**Version:** 1.1.0 (mit Scanner-Tab)
**Letzte Aktualisierung:** 2025-10-25
```