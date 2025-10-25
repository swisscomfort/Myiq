```markdown
---
title: "Data Processing Agreement (DPA) — Technische Version"
version: "2025-10-25"
notes: "Dieser DPA‑Entwurf enthält einen technischen Anhang (Anhang A). Juristisch prüfen lassen."
---

# Data Processing Agreement (DPA) — Ausführliche Vorlage

Zwischen:
- Data Controller: [Client Name, Address, Contact]  
- Data Processor: [Your Company / Operator Name, Address, Contact]

## 1. Gegenstand und Dauer
- Gegenstand: Erstellung forensischer Images, Suche nach wallet‑Artefakten, Erstellung von Reports, Speicherung/Archivierung und sichere Löschung gemäß Weisung.
- Dauer: Bis zur Löschung oder Rückgabe gem. Retention Policy oder schriftlicher Weisung des Controllers.

## 2. Kategorien personenbezogener Daten
- Geräte‑ und Metadaten, Dateiinhalte mit personenbezogenen Informationen (z. B. Kontaktinformationen), Logdaten, ggf. sensible Finanzdaten.

## 3. Zwecke der Verarbeitung
- Wiederherstellung oder Auffinden wallet‑bezogener Artefakte; Erstellung von Owner‑ und Court‑Reports; Nachlass‑Support (sofern beauftragt).

## 4. Pflichten des Processors
- Verarbeitung nur auf dokumentierte Weisung des Controllers.
- Technische und organisatorische Maßnahmen gemäß Anhang A sicherstellen.
- Unterstützung des Controllers bei Auskunfts‑/Löschanfragen.

## 5. Subprozessoren
- Subprozessoren nur mit schriftlicher Zustimmung des Controllers; keine grenzüberschreitende Übermittlung ohne schriftliche Einwilligung.

## 6. Löschung & Rückgabe
- Auf Anforderung: Rückgabe oder endgültige, nachgewiesene Löschung (Proof‑of‑Deletion). Proof‑of‑Deletion enthält: Dateiliste, SHA‑256, Zeitstempel, Operator‑Signatur.

## 7. Haftung
- Haftung geregelt in Vertrag; Punkte zu Vorsatz/Grobe Fahrlässigkeit beachten; individuelle Anpassung empfohlen.

---

## Anhang A — Technische Mindestanforderungen (detailliert)

### Artefakte (pro Case)
- metadata.txt (Felder: device, client, created_at, operator)
- chain_of_custody.txt
- image.dd.sha256 (Format: "<sha256hex>  image.dd")
- reports/ (maskierte scan_results JSONL/CSV)
- exports/ (owner_report_*.md, court_report_*.md)
- archives/ (signed consent, receipts)
- logs/process.log (JSONL) & logs/process.txt (human readable)

### Hashing & Manifeste
- Hash‑Algorithmus: SHA‑256.
- Manifest: manifest.txt enthält "<sha256hex>  <relative/path>" pro Zeile.
- Manifest‑Signatur: detached armored GPG signature manifest.txt.sig.

### Verschlüsselung & Schlüsselverwaltung
- Speicherung: LUKS2 oder per‑case asymmetrische GPG‑Verschlüsselung (AES256).
- Operator private keys: HSM/USB‑Token empfohlen; kein Klartext im Repo.
- Key‑Rotation & Revocation‑Prozeduren dokumentieren.

### Masking Policy
- Long hex (>20 hex chars) → partially masked (keep first 6 and last 4 chars).
- Mnemonic sequences (12–24 words) → REDACTED or collapse to first & last word.
- Automatisierte packaging checks müssen vor dem Packaging laufen und bei unmaskierten Mustern scheitern.

### Retention & Deletion Proof
- Default retention: 30 Tage (case‑level override möglich).
- Proof‑of‑Deletion: signed manifest listing deleted files + their last-known sha256 + timestamp + signer.

### Audit & Logs
- Structured logs: timestamp, operator, action, affected_file, sha256 (when applicable).
- Logs sind teil des Legal‑Package und bei Audit vorzulegen; snapshots müssen signiert werden.

### Incident Management
- Notification an Controller und DPO innerhalb 72 Std bei bestätigter Datenpanne.
- Forensische Erhaltung: Image preservation, signed incident manifest.

Unterschriften:
Controller: ______________________   Datum: ______________  
Processor: ______________________    Datum: ______________
```