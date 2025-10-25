```markdown
---
title: "Expert Affidavit / Eidesstattliche Erklärung"
version: "2025-10-25"
---

# Eidesstattliche Erklärung (Expert Affidavit) — Sachverständiger

Ich, ______________________ (Name des Experten), geboren am ____, wohnhaft in ____, erkläre an Eides statt:

1. Qualifikation  
- Tätigkeit: IT‑Forensiker / Digital Forensics Specialist  
- Qualifikationen / Zertifikate: (Kurzaufzählung)

2. Auftrag & Befugnis  
- Auftraggeber: __________________  
- Case ID: __________________  
- Umfang: Forensische Sicherung, Analyse und Berichterstattung (keine Extraktion von Klartext‑Schlüsseln ohne Zusatz‑Freigabe).

3. Methodik (Sachverhalt)
- Imaging: Tool, Datum, Uhrzeit, Kommando (z. B. dd if=/dev/sdX of=case_dir/image.dd bs=4M conv=sync,noerror)  
- Hashing: SHA‑256: `<sha256hex>` (siehe image.dd.sha256)  
- Analyse: rustscanner (args), yara rules (falls verwendet), bulk_extractor (falls verwendet).  
- Masking: Snippets in Reports wurden gemäss Masking‑Policy redigiert.

4. Feststellungen (Kurz, faktisch)
- Zusammenfassung der technischen Befunde (maskiert) — siehe Probate Report.

5. Beweiskraft & Aussagebereitschaft
- Ich bestätige, dass die Integrität der Kopien nachweisbar ist und erkläre mich bereit, meine Methodik und Ergebnisse gerichtlich auszusagen.

Ort / Datum: __________________  
Unterschrift Sachverständiger: __________________  
GPG Fingerprint (optional): __________________

(Notary / Beglaubigung falls erforderlich — Abschnitt für Notar)
```