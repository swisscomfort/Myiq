```markdown
# GUI Integration: Packaging & Probate Buttons — Kurzanleitung (Deutsch)

Diese Anleitung beschreibt die neuen GUI‑Funktionen (Validate, Create Legal Package, Create Probate Package) und wie du sie sicher verwendest.

Voraussetzungen
- Python3 + tkinter: sudo apt install python3-tk
- Die folgenden Skripte müssen vorhanden und ausführbar sein:
  - scripts/validate_case_before_packaging.sh
  - scripts/package_for_legal_strict.sh
  - scripts/create_probate_package.sh
- Optional: scripts/log_event.sh (GUI ruft dieses Script, falls vorhanden, zur Protokollierung auf)
- GPG (zum Signieren) falls du Signaturen erzeugen willst

Installation
1. Kopiere die Datei tools/gui/gui.py in dein Repo (ersetzt vorhandene GUI).
2. Mach die Datei ausführbar:
   chmod +x tools/gui/gui.py
3. Stelle sicher, dass alle Scripts ausführbar sind:
   chmod +x scripts/*.sh

Benutzung (kurz)
- Starte GUI:
  python3 tools/gui/gui.py --case-dir ./cases/case_YYYY...
- Im Tab "Reports / Export" findest du jetzt:
  - Validate Case (ruft scripts/validate_case_before_packaging.sh auf)
  - Create Legal Package (ruft scripts/package_for_legal_strict.sh auf und fragt nach Speicherort)
  - Create Probate Package (ruft scripts/create_probate_package.sh auf und fragt nach Speicherort)
- Während der Ausführung öffnet sich ein Fenster mit laufendem Output; Buttons sind deaktiviert bis Abschluss.

Sicherheitshinweise
- Die GUI zeigt und speichert only das, was die Scripts ausgeben. Sensible Daten werden nicht automatisch entschlüsselt.
- Prüfe Scripts und Pfade vor produktivem Einsatz; juristische Vorlagen vor Veröffentlichung juristisch prüfen.

Fehlerbehandlung
- Wenn ein Script fehlt oder nicht ausführbar, zeigt die GUI eine Warnung.
- Prüfe logs/process.log im Case‑Verzeichnis für detaillierte Protokolle.