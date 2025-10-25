```markdown
# Modul 05 — Betriebs‑ und IT‑Sicherheit (Key‑Management, Storage, Access)

Ziel
----
Betriebssichere Handhabung von Schlüsselmaterial, verschlüsseltem Storage, Log‑Management und Incident Response.

Kernprinzipien
--------------
- Least Privilege: nur notwendige Accounts erhalten Zugriff.
- Keys: private Operator‑Keys niemals in Repo; HSM/USB‑Token empfohlen.
- Encryption at rest: Images/Reports in verschlüsseltem Verzeichnis (LUKS) oder per GPG.
- Backups: nur verschlüsselte Backups; DPA beachten.

Konkrete Maßnahmen
------------------
- GPG: sichere Passphrase, ggf. --pinentry‑mode loopback für automatisierte Prozesse nur in geschützten Umgebungen.
- Access control: separate user für Forensics, 2FA für Admin‑Zugänge, minimaler SSH Zugang.
- Logs & Audit: process.log, process.txt, system journal; regelmäßige Exporte in Legal‑Package.

Incident Response (Kurz)
------------------------
1. Verdacht melden (DPO + legal contact).
2. Sichere betroffene Keys: evtl. Key‑Revocation.
3. Erzzeuge forensic snapshot von beteiligten Systemen.
4. Informiere Kunden (sofern erforderlich) und DPA‑Meldungen prüfen.

Sichere Löschung
----------------
- Verwende scripts/secure_delete.sh (shred fallback).
- Dokumentiere Löschung (who, when, method) im chain_of_custody.

Übung
-----
- Simuliere einen Zugriffstest: erstelle Benutzer mit eingeschränkten Rechten und zeige, dass der Benutzer Reports lesen, aber nicht private Keys exportieren kann.
```