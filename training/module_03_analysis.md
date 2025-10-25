```markdown
---
title: "Modul 03 — Analyse: Suche nach Krypto‑Artefakten"
version: "2025-10-25"
---

# Modul 03 — Analyse & Masking

## Lernziel
Verstehen der Heuristiken und sicheren Umgang mit Funden.

## Tools / Heuristiken
- Filename patterns: wallet, keystore, seed, mnemonic  
- Content patterns: "crypto":, "address":, 64‑hex, mnemonic regex  
- Tools: rustscanner, bulk_extractor (optional), yara (optional), python scanner (masking)

## Masking Policy (Kurz)
- Hex strings >20 chars: keep first 6 and last 4 chars, mask middle.  
- Mnemonics (12–24 words): REDACTED oder show first + last word only.

## Ablauf
1. mount image read‑only  
2. run lightweight filename/head scan  
3. review masked results; flag sensitive findings  
4. only extract raw secrets with explicit extra consent
```