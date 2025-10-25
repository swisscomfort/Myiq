```markdown
# rustscanner ↔ Orchestrator API / CLI Spec (PoC)

Dieses Dokument beschreibt:
- CLI arguments for rustscanner
- JSONL event schema (hits + progress)
- Orchestrator behaviour and example shim

## CLI (rustscanner)
- --root PATH       : path to case root or mounted image
- --head-size N     : bytes to read from file head for content heuristics
- --threads N       : optional number of threads

## JSONL Output Schemas

### Hit (per line)
{
  "case": "string",             // case identifier (path)
  "path": "string",             // file path relative or absolute
  "filesize": 12345,            // integer
  "pattern": "string",          // matched heuristic
  "snippet": "string",          // masked snippet (short)
  "sha256": "hex",              // sha256 of file
  "timestamp": "RFC3339",
  "scanner_version": "x.y.z"
}

### Progress event (emit periodically to stdout)
{
  "event": "progress",
  "case": "string",
  "progress": 45,               // percent 0-100
  "files_scanned": 1234,
  "hits_found": 12,
  "timestamp": "RFC3339"
}

## Orchestrator responsibilities
- Create case_dir and metadata (case_id, operator)
- Start rustscanner as subprocess and capture stdout
- Pipe JSONL into rustscanner_reader or write to file
- Convert progress events into case logs: case_dir/logs/process.log and status.json
- Enforce consent gating: do not allow extraction mode unless consent flag present

## Example invocation pattern (Python shim)
- subprocess.Popen(['rustscanner','--root',case_dir,'--head-size','200000'], stdout=PIPE)
- read lines, if line contains event: parse and write to logs; if hit: forward to ingest

```
```

```python name=C_api_spec/scripts/orchestrator_shim.py
#!/usr/bin/env python3
"""
Simple orchestrator shim (PoC):
- Launches rustscanner (binary must be in PATH)
- Reads stdout line by line, distinguishes progress events vs hits
- Writes structured logs to case_dir/logs and writes hits to a jsonl file
Use only Python standard library.
"""
import subprocess
import argparse
import json
import os
from datetime import datetime

def log_event(case_dir, level, message, progress=None):
    logdir = os.path.join(case_dir, 'logs')
    os.makedirs(logdir, exist_ok=True)
    ts = datetime.utcnow().isoformat() + 'Z'
    entry = {"timestamp": ts, "level": level, "message": message}
    if progress is not None:
        entry["progress"] = progress
    with open(os.path.join(logdir, 'process.log'), 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    with open(os.path.join(logdir, 'process.txt'), 'a', encoding='utf-8') as f:
        f.write(f"[{ts}] {level.upper()}: {message}\n")

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--case-dir', required=True)
    p.add_argument('--head-size', default='200000')
    args = p.parse_args()
    case_dir = args.case_dir
    os.makedirs(case_dir, exist_ok=True)
    reports_dir = os.path.join(case_dir, 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    jsonl_out = os.path.join(reports_dir, f'scan_results_{datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}.jsonl')
    cmd = ['rustscanner', '--root', case_dir, '--head-size', args.head_size]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    log_event(case_dir, 'info', 'rustscanner started', 0)
    with open(jsonl_out, 'w', encoding='utf-8') as outjf:
        for line in proc.stdout:
            try:
                obj = json.loads(line)
                # detect progress event
                if obj.get('event') == 'progress':
                    log_event(case_dir, 'info', f"Progress: {obj.get('progress')}%", obj.get('progress'))
                else:
                    # a hit
                    outjf.write(json.dumps(obj, ensure_ascii=False) + "\n")
            except json.JSONDecodeError:
                # unknown line, write to stderr log
                log_event(case_dir, 'warn', f"Non-JSON output: {line.strip()}")
    proc.wait()
    log_event(case_dir, 'info', f"rustscanner exited with {proc.returncode}", 100)

if __name__ == '__main__':
    main()
```

````markdown name=D_reports/templates/owner_report.md
```markdown
# Owner Report — {{case_id}}

Client: {{client}}
Case created: {{created_at}}
Operator: {{operator}}
Generated: {{generated}}

## Zusammenfassung (für Laien)
Kurze, verständliche Erklärung, welche Schritte durchgeführt wurden und welche Hinweise gefunden wurden.

## Gefundene Hinweise (maskiert)
{% for h in findings %}
- Pfad: `{{ h.path }}`
  - Snippet (maskiert): `{{ h.snippet }}`
  - Empfehlung: {{ h.recommendation }}
{% endfor %}

## Nächste Schritte (Empfehlung)
- Besprechung mit Operator: Optionen zur sicheren Übergabe.
- Keine Weitergabe sensibler Daten ohne gesonderte, schriftliche Einwilligung.
```