```markdown
---
title: "Praktische Übungen — Dummy‑Fälle"
version: "2025-10-25"
---

# Übungen (Praktisch)

## Übung A — End‑to‑End (90–120 min)
1. create dummy image (README_INSTALL_LEGAL.md).  
2. ./scripts/auto_case_setup.sh ./cases "Training" "Dev123"  
3. ./start.sh /tmp/test.img ./cases "Training"  (oder Imaging manuell)  
4. run analysis (rustscanner + reader)  
5. generate owner report and sign; create legal package

## Übung B — Legal Packaging
- Erzeuge clearsigned consent (gpg --clearsign consent_filled.md)  
- ./scripts/validate_case_before_packaging.sh ./cases/case_...  
- ./scripts/package_for_legal_strict.sh ./cases/case_... /tmp/legal_package.tar.gz

## Übung C — Retention & Deletion
- set retention_days=0 in case config.ini  
- run ./scripts/retention_manager.sh ./cases
```