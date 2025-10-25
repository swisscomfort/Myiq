```markdown
# Slides / Präsentation — Offline Slideshow Generator

Kurz:
- Das Skript `tools/slides/generate_slides.py` erstellt eine einfache, offline‑fähige HTML‑Slideshow aus allen Markdown‑Dateien im Ordner `training/`.
- Ausgabe: `tools/slides/output/presentation.html`

Voraussetzungen:
- Python 3 (standard library only)
- Keine weiteren Abhängigkeiten

Benutzung:
1. Von Projekt‑Root aus ausführen:
   python3 tools/slides/generate_slides.py /pfad/zum/repo

2. Öffne die erzeugte Datei:
   xdg-open tools/slides/output/presentation.html

Navigation:
- Pfeiltasten links/rechts oder Buttons "Prev"/"Next".
- Keine externe JS/CSS Bibliothek wird geladen — offline‑fähig.

Hinweis:
- Die Markdown→HTML Konvertierung ist bewusst minimalistisch (Headings, Listen, Codeblocks, einfache Absätze).
- Für komplexere Slides (Bilder, Tabellen) kannst du die erzeugte HTML manuell anpassen oder einen Markdown‑zu‑HTML Konverter (pandoc) verwenden.