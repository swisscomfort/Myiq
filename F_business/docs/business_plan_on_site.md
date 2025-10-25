```markdown
# Business‑Plan: Vor‑Ort Crypto Wallet Recovery Service (Diskret & DSGVO‑konform)

Kurzbeschreibung
----------------
Wir bieten diskrete, professionelle Vor‑Ort Wiederherstellung von Kryptowährungs‑Wallets und zugehörigen Artefakten. Kernversprechen: keine Geräteversendung ins Ausland, unmittelbare Betreuung vor Ort, vollständige Dokumentation und DSGVO‑Konformität.

USP (Unique Selling Points)
---------------------------
- Vor‑Ort‑Service: Gerät bleibt beim Kunden; Arbeit findet lokal statt.
- Diskretion & Datenschutz: keine Versendung von Hardware; Daten bleiben physisch unter Kontrolle.
- Vollständige Beweiskette: Imaging, SHA256, Chain‑of‑Custody, signierte Reports.
- Fachliche Expertise: forensische Methodik + verständliche Owner‑Reports + Court‑Reports.
- Schnell: Onsite‑Triage und Recovery starten innerhalb definierter SLA.

Zielkunden & Markt
------------------
- Privatpersonen mit verlorenem Zugang zu Krypto‑Wallets
- Anwälte / Nachlassverwalter
- KMU mit Krypto‑Beständen
- Forensische Dienstleister, die Sub‑Aufträge vergeben möchten

Dienstleistungs‑Portfolio
------------------------
1) Triage & Erstbewertung (Onsite)
   - Sichtprüfung, Identitätsprüfung, Consent, Foto‑Protokoll, Risikoeinschätzung.
2) Imaging & Analyse (Vor Ort)
   - Forensisches Image, SHA256, Live‑Scan mit rustscanner, Masked Report.
3) Recovery & Handover (mit Einwilligung)
   - Schrittweise, dokumentierte Extraktion (nur nach schriftlicher Zusatzfreigabe).
4) Reporting & Legal Package
   - Owner‑Report, Court‑Report, signed manifest, legal package.
5) Retention & Secure Deletion
   - Verschlüsselte Aufbewahrung, definierte Retention, sichere Löschung auf Anfrage.

Preismodell (Beispiel)
----------------------
- Ersttermin / Triage: Pauschal 150–300 EUR (inkl. 30–60 min vor Ort)
- Imaging & Basis-Analyse: Pauschal 350–800 EUR (je nach Gerät/Größe)
- Deep‑Analysis / Recovery Stundenpreis: 120–250 EUR / Stunde
- Erfolgs‑Fee (optional): 10–20% des wiederhergestellten Wertes (verhandelbar, rechtlich zu sichern)
- Fahrt / Sicherheitszuschläge: abhängig von Entfernung & Zeitfenster
- Notfall / Afterhours: +50–100% Aufschlag

SLA / Laufzeiten
----------------
- Responsezeit für Termin: innerhalb 48 Std
- Vor‑Ort‑Dauer (Standard): 2–6 Std (Imaging + Grundanalyse)
- Reporting: Owner‑Report innerhalb 24 Std nach Analyse; Court‑Report individuell

Vertrags‑ und Rechtsrahmen
--------------------------
- Consent Form & DPA zwingend vor Analyse (siehe templates).
- Separate schriftliche Einwilligung für Schlüssel‑Extraktion.
- Haftungsbegrenzung im DPA; Professional Indemnity empfohlen.
- Identity verification procedure (ID check) dokumentiert.

Betrieb & Organisation (Onsite流程)
-----------------------------------
- Pre‑Visit: Remote Intake (Client liefert Basisinfos), schedule, key checks.
- Onsite Step 1: ID & Consent, copy of signed form, photo of device, chain_of_custody init.
- Onsite Step 2: Imaging (use hardware write‑blocker if available), compute SHA256, record.
- Onsite Step 3: Run rustscanner + live GUI for client (masking enabled).
- Onsite Step 4: Discuss findings, decide on next steps (no extraction without extra consent).
- Onsite Step 5: Export Owner Report, GPG‑encrypt & sign artifacts, handover or encrypted transfer.
- Post‑Visit: Retention management, logs, package_for_legal produced.

Sicherheits‑ & Datenschutzmaßnahmen
----------------------------------
- No data leaves client premises unless encrypted and authorized.
- Store images in encrypted form (LUKS / GPG) with documented key custody.
- Operator keys stored in hardware token (YubiKey) or secure HSM.
- Audit logs + signed manifests for all actions.

Ausrüstung (Minimal)
--------------------
- Laptop (offline, dedicated for forensics)
- Hardware write‑blocker
- NVMe/SSD for images (encrypted storage)
- USB3 enclosure, spare drives
- Camera for photo documentation
- GPG key on hardware token
- Toolset: dd, losetup, rustscanner binary, python scripts, GUI monitor, shred

Risiko‑Management
-----------------
- Risiko: unbeabsichtigte Offenlegung von Seeds/Keys → Maßnahme: defaults maskieren, Consent‑Gate.
- Risiko: Reputation bei Fehlern → Maßnahme: klare DPA, Versicherung, QA und Checklisten.
- Risiko: rechtliche Anfragen (POI) → SOP für Behördenanfragen; nur auf rechtlicher Grundlage handeln.

Marketing & Vertrieb
--------------------
- Zielgruppenspezifische Leads: Anwälte, Nachlassverwalter, Krypto‑Foren.
- Vertrauensaufbau: Transparente Prozesse & Demo‑Slides, Referenzen (anonymisiert).
- Partnerships: Legal, Notare, Krypto‑Exchanges (Referral).
- Onsite demos: sichere, datenschutzkonforme Live‑Demo mit Dummy‑Case.

Metriken & KPIs
---------------
- Time to first appointment
- Cases per month
- Success rate (recoveries / cases)
- Average revenue per case
- Customer satisfaction (CSAT)
- Compliance score (DPA + audit pass)

Skalierungsplan
---------------
- Start lokal mit 1–2 Operatoren; standardisiere kit & runbooks
- Schrittweise: Franchise / regional partners with strict SOP & training
- Build central ops dashboard for case tracking (Postgres + UI) when >50 cases/month

Finanzielle Projektion (vereinfachtes Beispiel, Jahresbasis)
- 100 cases/year, avg revenue 800 EUR -> 80k EUR gross
- Costs: travel, equipment amortization, insurance, overhead -> ~40–50%
- Scale to 300 cases/year with regional teams -> break-even and profit growth

Nächste operative Schritte
--------------------------
1. Rechtliche Prüfung der Consent/DPA (Anwalt / DPO)
2. Lab‑Tests (2 dummy cases), finalize rustscanner PoC
3. Create standard offers & contracts, sign insurance
4. Pilot: 10 client cases in 3 months; collect feedback & KPI

Reputation & Ethik
------------------
- Transparenz: Kunde erhält sichtbare Live‑Logs & Owner‑Report.
- Diskretion: Keine Auslagerung ins Ausland; Geräte bleiben beim Kunden.
- Verantwortlichkeit: klare Haftungs- & Escrow‑Regeln bei erfolgreicher Recovery.
