<!-- Copilot instructions for contributors and AI coding agents. Keep concise and actionable. -->
# Repo orientation for AI coding agents

This repository is an offline forensic toolkit for crypto-recovery workflows. The codebase is split into small utilities, shell orchestrators, a Python scanner and a Tk-based reporting GUI. The notes below highlight repository-specific patterns and commands for AI agents.

Key places to read first
- `start.sh` — top-level orchestrator (example: `./start.sh /dev/sdX ./cases "Client Name"`). Calls `scripts/image_disk.sh` and `scripts/analyze.sh`.
- `scripts/analyze.sh` — mounts images (uses `losetup --show -fP`), conditionally runs `bulk_extractor`/`yara`, then runs `python3 tools/modules/search.py`.
- `tools/modules/search.py` — portable Python scanner used by `analyze.sh` (look for masking/snippet logic).
- `tools/gui/report_generator.py` — report templates + gpg signing (`gpg --armor --detach-sign`).

- Architecture & patterns (why it's structured this way)
- Shell-first orchestration: `start.sh` and `scripts/*` implement the end-to-end flow (imaging → mount → scan → report). Prefer small shell edits for workflow changes.
- Python scanner: portable scanning with masking logic. Components communicate via files/JSON in the case directory.
- Minimal external deps: scripts assume Debian coreutils + Python stdlib; optional tools (`bulk_extractor`, `yara`) are used only if present.
- Create a case (example):
  - ./start.sh /dev/sdX ./case_output "Client Name"
  - This will call `scripts/image_disk.sh` and `scripts/analyze.sh`.
- Analyze an existing image manually:
  - ./scripts/analyze.sh /path/to/image.dd /path/to/case_dir
  - The script sets up a loop device, mounts read-only, runs optional tools, then `python3 tools/modules/search.py --root "$MOUNT_DIR" --outdir "$REPORT_DIR"`.


Important conventions (project-specific)
- Masking: findings are masked before being written into reports. When editing `tools/modules/search.py` or `tools/gui/report_generator.py`, preserve `snippet` masking and `sensitive` flags.
- Case layout: each case folder contains `image.dd`, `reports/`, `metadata.txt`, `config.ini` (copied from `config/case_policy.ini`) and `templates/`. Use these paths when wiring features.
- Loop device handling: `scripts/analyze.sh` uses `losetup --show -fP` and may mount `${LOOP}p1`. Cleanup uses `trap 'losetup -d "${LOOP}" || true' EXIT` — be conservative changing mount/cleanup logic.


Developer workflows (commands you'll use)
- Create a case (example):
  ./start.sh /dev/sdX ./case_output "Client Name"
- Analyze an existing image manually:
  ./scripts/analyze.sh /path/to/image.dd /path/to/case_dir
  (it will mount the image, run optional tools, then `python3 tools/modules/search.py --root "${MOUNT_DIR}" --outdir "${REPORT_DIR}"`)

Files that commonly change together
- `scripts/analyze.sh` ↔ `tools/modules/search.py` (mount/scan integration)
- `tools/gui/report_generator.py` ↔ templates in `D_reports/templates/` (report formatting + signing)

When merging existing instructions
- No existing `.github/copilot-instructions.md` or AGENT files were found; preserve this file as the canonical concise guidance for AI agents. If you want to add more detail, prefer small, example-driven snippets rather than generic rules.

If anything is unclear or you want deeper examples (unit tests, exact JSON schemas, or more run permutations), tell me which area to expand and I will iterate.

---
Last updated: 2025-10-25
