```markdown
---
title: "DPIA‑Template (Data Protection Impact Assessment)"
version: "2025-10-25"
notes: "Vorlage für Datenschutz‑Risikoanalyse; lokal ausfüllen und DPO prüfen."
---

# DPIA‑Template — Crypto Wallet Recovery (On‑Site)

## 1. Projektbeschreibung
- Projektname: Crypto Wallet Recovery — On‑Site Service  
- Kurzbeschreibung: Vor‑Ort Imaging, automatisierte Suche nach wallet‑Artefakten, Berichtserstellung, optionale extrahierte Übergabe bei ausdrücklicher Zustimmung.

## 2. Verantwortliche & Rollen
- Data Controller: [Name, Kontakt]  
- Data Processor (Operator): [Name, Kontakt]  
- DPO: [Name, Kontakt]

## 3. Verarbeitungsaktivitäten & Datenkategorien
- Auflistung: Aufnahme (Intake), Imaging, Scanning, Reporting, Archivierung, Löschung.
- Kategorien: Gerätedaten, Dateiinhalte (möglicherweise personenbezogen), Logdaten, consent‑Dokumente.

## 4. Notwendigkeit & Verhältnismäßigkeit
- Zweckbindung: Nur Wiederherstellung von Zugängen / Auffinden relevanter Artefakte.
- Minimierung: Standardmäßig Masking, keine Extraktion ohne Zusatz‑Consent.

## 5. Risiken für Betroffene
- Unautorisierte Offenlegung sensitiver Daten (Seeds, private keys).
- Verlust / Diebstahl von Images.
- Unbeabsichtigte Weitergabe an Dritte / Ausland.

## 6. Maßnahmen zur Risikominderung
- Consent gating, Masking policy, Retention policy, Verschlüsselung at rest, HSM/Token‑basierte Key‑Storage, Audit logs und signierte Manifeste.

## 7. Rest‑Risiko & Entscheidung
- Bewertung (niedrig/mittel/hoch) je Maßnahme; Verantwortliche benennen (DPO / Geschäftsleitung).

## 8. Monitoring & Review
- Review‑Intervall: mindestens einmal jährlich oder bei Prozessänderung.
- Dokumentation: Änderungsverlauf, Review‑Protokolle.

## Anlagen
- Links zu Consent, DPA, chain_of_custody, technical runbooks.

```