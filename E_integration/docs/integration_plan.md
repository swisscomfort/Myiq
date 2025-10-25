```markdown
# Integration & Operations Plan — rustscanner + Orchestrator + Reports

Kurz: Dieses Dokument beschreibt Deployment, Ops, Security, Testing, Acceptance Criteria und Checklisten für produktiven Einsatz.

1) Deployment (single-host PoC)
- Install rustscanner binary on operator machine (build from A_rustscanner).
- Place Python orchestrator and reader scripts in scripts/.
- Ensure GPG, python3, losetup tools installed.
- Case directories follow existing layout: case_<TIMESTAMP> with metadata, logs, reports.

2) Ops / Runbook
- Start a case: scripts/auto_case_setup.sh
- Run orchestrator: python3 C_api_spec/scripts/orchestrator_shim.py --case-dir ./cases/case_...
- Monitor logs via GUI or tail case_dir/logs/process.txt
- After scan, run scripts/rustscanner_reader.py to ingest results into sqlite
- Generate reports: D_reports/scripts/generate_reports_from_jsonl.py

3) Security & Consent gating
- Orchestrator must check presence of signed consent before enabling "deep" mode or carving.
- Default: output masked snippets only.

4) Scaling
- For many parallel cases: use job queue (Redis) and spawn multiple orchestrator workers
- Store results centrally in Postgres for aggregation (optional)

5) Testing & QA
- Unit tests for Rust scanner (matchers)
- Regression corpus with labelled test images
- Performance benchmarks (I/O throughput)

6) Acceptance Criteria
- JSONL schema compliant, sample ingestion successful
- Owner & Court reports generated and signable
- Retention manager and secure_delete integrated

7) Next Steps (first 4 weeks)
- Build and run Rust PoC on lab images
- Validate masking & consent gating
- Integrate with existing GUI report tab and training materials
```