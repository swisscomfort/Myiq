```markdown
---
title: "Betriebsablauf — Nachlass / Erbschafts‑Fälle"
version: "2025-10-25"
---

# Betriebsablauf für Nachlass‑/Erbschafts‑Fälle (Kurz, gerichtsfest)

## Ziel
Lückenloser, gerichtsfester Ablauf von Intake bis Probate‑Package.

## 1) Intake & Vorprüfung
- Remote Intake: Erste Infos (Wer, welches Recht, Vollmacht?).  
- Consent‑Vorlage vorbereiten und zur Unterschrift mitbringen.

## 2) On‑Site Entgegennahme
- ID‑Prüfung & Photo‑Protokoll (archives/photos).  
- Ausfüllen client_acknowledgement_form.md mit Zeugen.  
- Witness log erstellen (archives/witness_log.md).

## 3) Imaging
- Hardware Write‑blocker verwenden (falls verfügbar).  
- dd → image.dd; sha256sum → image.dd.sha256.  
- logs/process.log und process.txt aktualisieren.

## 4) Analyse
- Nur nach unterschriebenem Consent / gerichtlicher Anordnung: rustscanner / deeper scans.  
- Masking strikt anwenden; sensitive hits nur markieren, nicht automatisch extrahieren.

## 5) Reporting
- Owner Report (live vor Ort besprechen).  
- Court / Probate Report nach Bedarf; Affidavit erstellen und signieren.

## 6) Probate‑Package
- create_probate_package.sh erzeugt probate_package tar.gz mit manifest + signatures.  
- Übergabe an Notar / Gericht: gedruckte, signierte/ ggf. beglaubigte Unterlagen.

## 7) Retention und Löschung
- Retention gem. config (Default 30 Tage).  
- Nach Frist: secure_delete.sh ausführen und signed deletion manifest erzeugen.

## 8) Nachbereitung
- Operator‑Vorbereitung für Zeugenaussage: Methodik, CLI‑Belege, Timeline.
```