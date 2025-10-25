```markdown
# GUI: Live-Monitor für Fälle (Kurz)

Zweck
- Zeigt Live‑Log, letzten Ereignisstand, Fortschritt und maskierte Treffer für einen Case.
- Offline‑fähig; lokal anzeigen, z. B. dem Kunden vor Ort.

Abhängigkeiten
- python3 (bereits benötigt)
- python3-tk (Tkinter): sudo apt install python3-tk

Installation
1. Datei in repo ablegen: tools/gui/gui.py
2. script ausführbar machen: chmod +x tools/gui/gui.py
3. log_event helper: chmod +x scripts/log_event.sh

Integration (kurzer Vorschlag)
- Füge in start.sh und analyze.sh an wichtigen Stellen Aufrufe zu scripts/log_event.sh ein, z. B.:
  bash scripts/log_event.sh "$case_dir" info "Imaging started" 5
  bash scripts/log_event.sh "$case_dir" info "Imaging completed" 20
  bash scripts/log_event.sh "$case_dir" info "Analysis started" 30
  bash scripts/log_event.sh "$case_dir" info "Reports generated" 80
  bash scripts/log_event.sh "$case_dir" info "Case finished" 100

Starten des GUI
- Während der Analyse (oder danach) lokal öffnen:
  python3 tools/gui/gui.py --case-dir ./cases/case_2025...

Datenschutz / DSGVO Hinweis
- GUI zeigt nur maskierte Snippets aus Reports; keine Schlüssel werden entschlüsselt oder im Klartext angezeigt.
- Zeige das GUI dem Kunden nur nach unterschriebener Einwilligung und ggf. DPA.
```