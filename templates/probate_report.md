```markdown
---
title: "Probate / Estate Technical Report Template"
version: "2025-10-25"
notes: "Für Erbschafts‑/Nachlassfälle; juristisch prüfen lassen."
---

# Probate / Estate Technical Report

**Case ID:** {{case_id}}  
**Client / Requester:** {{client}}  
**Operator:** {{operator}}  
**Created:** {{created_at}}

## 1. Auftrag & Scope
- Auftraggeber / Antrag: ____________________  
- Ziel: Forensische Sicherung, Dokumentation und technische Befunderstattung für Nachlassregelung.  
- Einschränkungen: z. B. keine Entschlüsselung ohne gerichtliche Anordnung / zusätzliche Freigabe.

## 2. Identitäts‑ & Übergabe‑Belege
- ID‑Prüfung: Methode, Name, ID‑Nr.  
- Fotos: archives/photos/*.jpg (Device condition)  
- Witness log: archives/witness_log.md

## 3. Imaging & Integrität
- Imaging tool & command: dd if=/dev/sdX of=case_dir/image.dd bs=4M conv=sync,noerror status=progress  
- Image SHA256: `<sha256hex>` (Datei: image.dd.sha256)  
- Storage: verschlüsselt (ja/nein), Methode: [LUKS / GPG]  
- Chain of Custody: chain_of_custody.txt

## 4. Methodik & Tools
- Tools: rustscanner vX.Y, python scanner vX.Y, bulk_extractor (opt.), yara (opt.)  
- Scan modes: filename / head / deep / carving (siehe Appendix)  
- Masking policy angewendet (siehe Anhang)

## 5. Timeline (Kurz)
- Received: YYYY‑MM‑DD HH:MM — von: [Name]  
- Imaging: start/end Zeitstempel  
- Analysis: start/end Zeitstempel

## 6. Findings (Masked)
- Finding 1:
  - Pfad: `relative/path`
  - Größe: N bytes
  - SHA256: `<sha256>`  
  - Heuristik: filename/content/yara
  - Snippet (masked): `[...]`
  - Sensitivity: high/medium/low
  - Empfehlung: weitere rechtliche Klärung / autorisierte Extraktion
- (weitere Findings...)

## 7. Evidence Package
- archives/probate_package_*.tar.gz (enthält manifest + signed manifest + consent + affidavit)  
- manifest: manifest.txt (sha256 + relative paths)  
- signatures: manifest.txt.sig (GPG detached)

## 8. Limitationen
- Dinge, die NICHT geprüft wurden (z. B. verschlüsselte Partitionen ohne Schlüssel).  
- Hinweis zu möglichen False Positives/Negatives.

## 9. Appendix
- Tool‑Versionen & CLI‑Invocations (vollständig)  
- chain_of_custody.txt (vollständiger Auszug)  
- logs/process.log (Snapshot)  
- Operator CV / Qualifications

---

**Erklärung**  
Ich bestätige, dass die oben beschriebenen Maßnahmen nach forensischen Standards durchgeführt wurden.

Operator (Name): ____________________  Datum: ___________  
GPG Fingerprint (operator): ____________________
```