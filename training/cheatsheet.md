```markdown
---
title: "Cheatsheet & Schnellreferenz"
version: "2025-10-25"
---

# Cheatsheet

Wichtige Pfade:
- cases/: case_YYYY...  
- reports/: case_dir/reports  
- logs/: case_dir/logs  
- archives/: case_dir/archives

Kommandoauszug:
- Imaging: dd if=/dev/sdX of=case_dir/image.dd bs=4M conv=sync,noerror status=progress  
- SHA256: sha256sum image.dd > image.dd.sha256  
- Verify: ./scripts/verify_integrity.sh image.dd image.dd.sha256  
- Package: ./scripts/package_for_legal_strict.sh case_dir /tmp/pkg.tar.gz
```