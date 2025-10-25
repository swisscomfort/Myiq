```markdown
---
title: "Einverständnis‑ und Ablaufbestätigung (Detailliert)"
version: "2025-10-25"
notes: "Vor Veröffentlichung juristisch prüfen"
---

# Einverständnis‑ und Ablaufbestätigung (Detaillierte Version)

Hinweis: Jede Checkbox ist mit Initialen zu bestätigen (Initials: ____). Vor der Analyse muss das Formular vollständig ausgefüllt und unterschrieben vorliegen.

## Fall‑Metadaten
- Case ID: ______________________
- Client (Name, Kontakt): ______________________
- Gerät(e): ______________________ (Typ, Hersteller, Seriennr.)
- Übergabeort: ______________________
- Datum / Uhrzeit: ______________________
- Operator (Vorname Nachname): ______________________

## Identitätsprüfung (Pflicht)
[ ] Identitätsprüfung durchgeführt (Ausweis/Reisepass vorgelegt). Initials: ____
- Prüfmethode / ID‑Nr.: ______________________
- Kopie des Ausweises gesichert: (ja / nein) ______  (falls ja: Ablageort) __________

## Scope / Zweck der Verarbeitung (ankreuzen)
[ ] Forensisches Imaging (bit‑genaue Kopie) des Datenträgers. Initials: ____
[ ] Automatisierte Suche nach wallet‑Artefakten (Dateinamen, Keystore‑JSON, Mnemonic‑Heuristiken). Initials: ____
[ ] Owner‑Report (laienverständlich). Initials: ____
[ ] Court‑Report (technisch) — nur mit expliziter Zusatz‑Einwilligung. Initials: ____
[ ] Manuelle Schlüssel‑Extraktion / Übermittlung von Klartext (nur nach separater, schriftlicher Freigabe). Initials: ____

## Technische Kurzbeschreibung (für Auftraggeber)
1) Imaging:
   - Tool: dd (oder guymager/dcfldd) — bit‑genaue Kopie.
   - Hash: SHA‑256 (Datei: image.dd.sha256).
   - Speicherung: verschlüsselt (GPG asymm. oder LUKS) oder ggf. nach Absprache.
   Initials: ____

2) Analyse:
   - Tools/Heuristiken: rustscanner (filename/head/deep), yara (optional), bulk_extractor (optional), Python‑Scanner (Masking).
   - Output: maskierte Treffer (JSONL/CSV). Keine automatische Offenlegung von seed/private keys ohne Extra‑Consent.
   Initials: ____

3) Berichterstellung:
   - Owner‑Report (Markdown/HTML), Court‑Report (technisch, nur mit Consent).
   - Signatur: GPG detached/clearsign durch Operator möglich.
   Initials: ____

## Aufbewahrung & Löschung
- Aufbewahrungsfrist (Retention): _____ Tage (Standard: 30). Initials: ____
- Nach Ablauf: sichere Löschung mittels secure_delete (shred/overwrite) oder Rückgabe gem. Vereinbarung. Initials: ____
- Verschlüsselung: [ ] GPG (asymm)  [ ] GPG (symm)  [ ] LUKS. Initials: ____

## Übergabe / Handover
- Übergabe sensitiver Daten (nur bei Zusatz‑Freigabe): [ ] persönlich mit Empfangsbestätigung  [ ] verschlüsselt per GPG an bekannte Key‑ID. Initials: ____
- Empfangsbestätigung wird im Case‑Archiv abgelegt. Initials: ____

## Widerruf & Betroffenenrechte (DSGVO)
- Widerruf: Schriftlich möglich; bereits erfolgte legitime Verarbeitung bleibt unberührt.
- Auskunft, Löschung, Einschränkung: richten an: [DPO / Kontakt].
Initials: ____

## Haftung & Zusatz
- Verarbeitung nach bestem Wissen; Haftungsregelungen im DPA geregelt. Private Schlüssel nur nach separatem schriftlichem Einverständnis offengelegt. Initials: ____

---

### Unterschriften
Ich bestätige, die oben genannten Punkte gelesen, verstanden und akzeptiert zu haben.

Client (Name in Blockschrift): ______________________  
Unterschrift Client: ______________________   Datum: ______________

Operator (Name in Blockschrift): ______________________  
Unterschrift Operator: ____________________  Datum: ______________

---

### Technische Anlage (transparente Beispiele)
- Imaging‑Beispiel: dd if=/dev/sdX of=/case/path/image.dd bs=4M conv=sync,noerror status=progress  
- Hash‑Beispiel: sha256sum image.dd > image.dd.sha256  
- Signatur‑Beispiel (Operator): gpg --armor --detach-sign image.dd.sha256

```