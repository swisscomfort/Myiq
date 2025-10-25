```markdown
---
title: "Modul 02 — Forensisches Imaging"
version: "2025-10-25"
---

# Modul 02 — Forensisches Imaging (Praxis)

## Lernziel
Sichere Erstellung von forensischen Images und Integritätsnachweis.

## Wichtige Befehle (Beispiele)
- Create image:
  - dd if=/dev/sdX of=/path/to/case/image.dd bs=4M conv=sync,noerror status=progress
- Compute SHA256:
  - sha256sum /path/to/case/image.dd > /path/to/case/image.dd.sha256
- Mount read‑only (loop):
  - LOOP=$(losetup --show -fP /path/to/case/image.dd)
  - mount -o ro ${LOOP}p1 /mnt/case_mount
  - umount /mnt/case_mount; losetup -d $LOOP

## Operational Checklist
- Consent und ID‑Check vor Imaging.  
- Foto‑Dokumentation des Geräts.  
- Use write‑blocker when available.  
- Store image encrypted at rest.
```