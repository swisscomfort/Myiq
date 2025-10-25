<!-- Copilot instructions for contributors and AI coding agents. Keep concise and actionable. -->
# Repo orientation for AI coding agents

This repository is an offline forensic toolkit for crypto-recovery workflows. The codebase is split into small utilities, scripts and a Rust scanner PoC. Below are project-specific patterns, commands, and examples that help an AI agent be productive immediately.

Key directories & files
- `start.sh` — top-level orchestrator used to create case directories and run imaging + analysis (example usage: `./start.sh /dev/sdX ./cases "Client Name"`). See `scripts/image_disk.sh` and `scripts/analyze.sh` for detailed steps.
- `scripts/analyze.sh` — mounts an image read-only, runs optional tools (bulk_extractor, yara) and the Python scanner (`tools/modules/search.py`). Important: it uses `losetup -P` and may mount `${LOOP}p1` if present.
- `A_rustscanner/` — Rust PoC scanner that emits JSONL hits to stdout. Entry: `A_rustscanner/src/main.rs`. Build with `cargo build` in that directory.
- `B_python_reader/` — Python reader utilities and a README describing how to ingest rustscanner JSONL output.
- `tools/modules/search.py` — primary Python scanner used by `analyze.sh` to walk a mounted filesystem and produce masked findings in `case/reports/`.
- `tools/gui/` — Tkinter GUI and helpers (monitor, report generator). Useful when adding features that integrate with packaging scripts.
- `scripts/*.sh` — many orchestrator and helper scripts (packaging, encryption, verification). Prefer modifying shell scripts for operational changes.

Big-picture architecture
- Orchestration (shell): `start.sh` creates a `case_YYYY...` directory, calls `scripts/image_disk.sh` to produce an image and `scripts/analyze.sh` to analyze it. Follow the shell flow when adding or modifying workflows.
- Scanners:
  - Rust scanner (`A_rustscanner`) — high-performance file walker that writes JSONL to stdout. Good for CPU-bound, parallel scanning.
  - Python scanner (`tools/modules/search.py`) — used in `analyze.sh`; walks mounted FS and writes masked outputs to `reports/`. Prefer this for portability and for changes that must run with standard Python only.
- Reporting: `tools/gui/report_generator.py` and `tools/gui/gui.py` produce Markdown/HTML reports and handle signing with `gpg`.

Developer workflows & commands
- Create a case (example):
  - ./start.sh /dev/sdX ./case_output "Client Name"
  - This will call `scripts/image_disk.sh` and `scripts/analyze.sh`.
- Analyze an existing image manually:
  - ./scripts/analyze.sh /path/to/image.dd /path/to/case_dir
  - The script sets up a loop device, mounts read-only, runs optional tools, then `python3 tools/modules/search.py --root "$MOUNT_DIR" --outdir "$REPORT_DIR"`.
- Build the Rust scanner:
  - cd A_rustscanner && cargo build --release
  - The scanner CLI accepts `--root`, `--head-size`, and optional `--threads` flags and emits JSONL.
- Run the Python reader against rustscanner output:
  - python3 B_python_reader/scripts/rustscanner_reader.py --case-dir ./cases/... --jsonl ./scan_results.jsonl

Project-specific conventions and patterns
- Minimal external deps: many scripts assume only standard Debian utilities and Python standard library. Optional tools like `bulk_extractor` and `yara` are used only if present.
- Masking sensitive data: Scan outputs are intentionally masked before being included in reports. When editing `tools/modules/search.py` or report code in `tools/gui/report_generator.py`, preserve the masking behavior—look for `snippet` handling and `sensitive` flags.
- Case directory layout: `case_dir/` contains `image.dd`, `reports/`, `metadata.txt`, `config.ini` (copied from `config/case_policy.ini`), and `templates/`. Use these paths when creating integrations.
- Shell-first orchestration: High-level workflow is implemented in shell scripts; prefer updating scripts for orchestration changes instead of embedding complex shell logic in Python or Rust.

Integration points & cross-component communication
- Filesystem & JSONL: The Rust scanner writes JSONL (one object per line) to stdout; the Python reader or other processors read that JSONL. `analyze.sh` and `start.sh` coordinate by file paths in the case directory.
- Loop devices and mounts: `scripts/analyze.sh` uses `losetup --show -fP` and looks for `${LOOP}p1`. Be careful when changing mount or loop cleanup logic—trap cleanup is used (`trap 'losetup -d "$LOOP" || true' EXIT`).
- Optional tools: `bulk_extractor` and `yara` are conditionally invoked. Check for `command -v bulk_extractor` / `command -v yara` before assuming availability.
- GPG signing: `tools/gui/report_generator.py` calls `gpg --armor --detach-sign`. When adding signing features, follow the existing subprocess-based approach.

Files to read first for modifications
- `start.sh`, `scripts/analyze.sh`, `scripts/image_disk.sh` — orchestration and imaging.
- `tools/modules/search.py`, `B_python_reader/scripts/rustscanner_reader.py` — scanning and ingestion.
- `A_rustscanner/src/main.rs`, `A_rustscanner/Cargo.toml` — parallel scanner behavior and JSONL schema (`Hit` struct).
- `tools/gui/report_generator.py`, `tools/gui/gui.py` — report generation and packaging hooks.

Quick examples to reference in edits
- JSONL hit structure (Rust) — each line is one JSON object with these fields:
  ```json
  {
    "case": "string (root path or case id)",
    "path": "string (absolute file path)",
    "filesize": 12345,
    "pattern": "string (e.g. 'filename:(?i)wallet' or 'content:...')",
    "snippet": "string (masked/truncated content or '[FILENAME MATCH]')",
    "sha256": "hex string (file hash)",
    "timestamp": "RFC3339 timestamp",
    "scanner_version": "0.1.0"
  }
  ```
  See `A_rustscanner/src/main.rs` for the `Hit` struct definition.
- Mount+analyze flow (from `scripts/analyze.sh`): losetup -> mount -> optional bulk_extractor/yara -> python scanner -> umount -> optional integrity check -> optional `encrypt_reports.sh` if `config.ini` has `auto_encrypt = yes`.
- Example rustscanner invocation:
  ```bash
  cd A_rustscanner
  cargo build --release
  ./target/release/rustscanner --root /mnt/case_mount --head-size 200000 --threads 4 > hits.jsonl
  ```

When merging existing instructions
- No existing `.github/copilot-instructions.md` or AGENT files were found; preserve this file as the canonical concise guidance for AI agents. If you want to add more detail, prefer small, example-driven snippets rather than generic rules.

If anything is unclear or you want deeper examples (unit tests, exact JSON schemas, or more run permutations), tell me which area to expand and I will iterate.

---
Last updated: 2025-10-25
