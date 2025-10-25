```markdown
# Rustscanner JSONL reader (Python) — PoC
This script reads rustscanner JSONL output (from stdout or file) and stores masked hits into case_dir/reports and into a SQLite DB.
It uses only Python standard library.
Usage (example):
  python3 scripts/rustscanner_reader.py --case-dir ./cases/case_20251025... --jsonl ./scan_results.jsonl
Or stream:
  rustscanner ... | python3 scripts/rustscanner_reader.py --case-dir ./cases/case_... --stream
```