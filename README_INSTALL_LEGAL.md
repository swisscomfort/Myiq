```markdown
---
title: "Installations‑ und Prüfungsanleitung — Crypto Recovery Toolkit"
version: "2025-10-25"
notes: "Detaillierte Anleitung zur Installation, Test und juristischen Prüfung."
---

# Installations‑ & Prüfungsanleitung (Kurz)

## Voraussetzungen
- Debian/Ubuntu, sudo access  
- Tools: bash, dd, losetup, sha256sum, gpg, python3, python3‑tk (für GUI)

## Schnellstart (Beispiel)
1. Pakete:
   - sudo apt update
   - sudo apt install -y gnupg python3 python3‑tk coreutils util-linux e2fsprogs

2. Repo nach /opt/crypto-toolkit kopieren und Rechte setzen:
   - sudo mkdir -p /opt/crypto-toolkit
   - sudo chown $(whoami):$(whoami) /opt/crypto-toolkit
   - chmod +x scripts/*.sh tools/gui/*.py start.sh

3. GPG Key:
   - gpg --full-generate-key
   - gpg --armor --export YOURKEY > keys/operator_pubkey.asc

4. Testlauf mit Dummy‑Image (siehe training/exercises.md)

## Juristische Prüfungsartefakte (Kurz)
- clearsigned consent (archives/consent_*.asc)  
- manifest + manifest.txt.sig  
- image.dd.sha256  
- signed affidavit (if probate)
```