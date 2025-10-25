```markdown
---
title: "Technischer Evidence‑Guide für rechtliche Prüfung"
version: "2025-10-25"
notes: "Kurz, präzise Nachweisliste und Prüfbefehle für Legal."
---

# Technischer Evidence‑Guide für rechtliche Prüfung (Kurz)

Dieses Dokument listet die exakt zu erzeugenden Artefakte und die Prüfbefehle, die die Rechtsabteilung / Notariat erwarten kann.

## Pflichtartefakte pro Case
- metadata.txt — Client, device, operator, created_at  
- chain_of_custody.txt — vollständige Übertragungs‑ und Aktionseinträge  
- image.dd.sha256 — SHA‑256 der Image‑Datei  
- reports/*.jsonl / *.csv — maskierte Scan‑Results  
- exports/owner_report_*.md, exports/court_report_*.md — signiert falls erstellt  
- archives/consent_filled_*.md.asc — clearsigned Consent  
- archives/manifest.txt + manifest.txt.sig — manifest + detached GPG‑Signatur  
- logs/process.log (JSONL) + logs/process.txt — strukturierte + human‑readable Logs

## Wichtige Shell‑Prüfungen (Beispiele)
- SHA256 prüfen:
  - sha256sum -c image.dd.sha256
- GPG Signatur prüfen:
  - gpg --verify manifest.txt.sig manifest.txt
- Masking‑Quickcheck (heuristisch):
  - grep -E -i "mnemonic|seed|private|[a-f0-9]{32,}" reports/*.jsonl || echo "No obvious unmasked secrets found"  
  Hinweis: grep ist heuristisch; Rechtsprüfung verlangt händische Kontrolle sensibler Treffer.

## Manifest‑Format
- Jede Zeile: "<sha256hex>  <relative/path>"
- Beispiel: 3a7f...  reports/scan_results_20251025.jsonl

## Empfohlener Workflow (Kurz)
1. Imaging:
   - dd if=/dev/sdX of=/case/case_*/image.dd bs=4M conv=sync,noerror status=progress
   - sha256sum image.dd > image.dd.sha256
2. Analyse & Reports:
   - rustscanner | python3 scripts/rustscanner_reader.py --case-dir ./case_dir --stream
3. Packaging:
   - ./scripts/validate_case_before_packaging.sh ./case_dir
   - ./scripts/package_for_legal_strict.sh ./case_dir /tmp/legal_package.tar.gz
4. Probate:
   - ./scripts/create_probate_package.sh ./case_dir /tmp/probate_package.tar.gz

## Hinweise für Legal Review
- Ohne clearsigned Consent oder gültige DPA keine Analyse durchführen.
- Fordere die operator key fingerprints (gpg --list-keys) und Nachweis der Signatur (manifest.txt.sig).
- Bei Nachlassfällen: Affidavit und Witness Log verlangen.

```