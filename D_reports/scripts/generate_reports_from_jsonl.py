#!/usr/bin/env python3
"""
Generate Owner and Court Markdown reports from a scan_results JSONL file.
- Minimal templating using Python str.replace / simple loops
- Uses only Python standard library
Usage:
  python3 scripts/generate_reports_from_jsonl.py /path/to/case_dir /path/to/jsonl
"""
import sys
import os
import json
from datetime import datetime

def load_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                yield json.loads(line)
            except Exception:
                continue

def generate_owner(case_dir, metadata, findings):
    tpl = open(os.path.join('D_reports','templates','owner_report.md')).read()
    report = tpl.replace('{{case_id}}', os.path.basename(case_dir))
    report = report.replace('{{client}}', metadata.get('client','-'))
    report = report.replace('{{created_at}}', metadata.get('created_at', ''))
    report = report.replace('{{operator}}', metadata.get('operator',''))
    report = report.replace('{{generated}}', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ'))
    # simple findings insertion
    findings_md = ''
    for h in findings[:20]:
        findings_md += f"- Pfad: `{h.get('path','')}`\n  - Snippet (maskiert): `{h.get('snippet','')}`\n  - Empfehlung: Besprechung mit Operator\n\n"
    report = report.replace('{% for h in findings %}\n- Pfad: `{{ h.path }}`\n  - Snippet (maskiert): `{{ h.snippet }}`\n  - Empfehlung: {{ h.recommendation }}\n{% endfor %}', findings_md)
    out = os.path.join(case_dir, 'exports', f'owner_report_{datetime.utcnow().strftime(\"%Y%m%dT%H%M%SZ\")}.md')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(report)
    print("Owner report written to", out)
    return out

def generate_court(case_dir, metadata, findings):
    tpl = open(os.path.join('D_reports','templates','court_report.md')).read()
    report = tpl.replace('{{case_id}}', os.path.basename(case_dir))
    report = report.replace('{{client}}', metadata.get('client','-'))
    report = report.replace('{{created_at}}', metadata.get('created_at',''))
    report = report.replace('{{operator}}', metadata.get('operator',''))
    report = report.replace('{{generated}}', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%SZ'))
    report = report.replace('{{image_sha256}}', metadata.get('image_sha256','-'))
    report = report.replace('{{scanner_version}}', metadata.get('scanner_version','-'))
    findings_md = ''
    for h in findings:
        findings_md += f"### Finding\n- path: `{h.get('path','')}`\n- filesize: {h.get('filesize','')}\n- sha256: `{h.get('sha256','')}`\n- snippet (masked): `{h.get('snippet','')}`\n\n"
    report = report.replace('{% for h in findings %}\n### Finding {{ loop.index }}\n- path: `{{ h.path }}`\n- filesize: {{ h.filesize }}\n- sha256: `{{ h.sha256 }}`\n- snippet (masked): `{{ h.snippet }}`\n{% endfor %}', findings_md)
    out = os.path.join(case_dir, 'exports', f'court_report_{datetime.utcnow().strftime(\"%Y%m%dT%H%M%SZ\")}.md')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(report)
    print("Court report written to", out)
    return out

def read_metadata(case_dir):
    meta = {}
    mfile = os.path.join(case_dir, 'metadata.txt')
    if os.path.exists(mfile):
        with open(mfile, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    k,v = line.split(':',1)
                    meta[k.strip()] = v.strip()
    return meta

def main():
    if len(sys.argv) != 3:
        print("Usage: generate_reports_from_jsonl.py /path/to/case_dir /path/to/jsonl")
        sys.exit(2)
    case_dir = sys.argv[1]
    jsonl = sys.argv[2]
    findings = list(load_jsonl(jsonl))
    metadata = read_metadata(case_dir)
    metadata['scanner_version'] = findings[0].get('scanner_version','-') if findings else '-'
    os.makedirs(os.path.join(case_dir,'exports'), exist_ok=True)
    generate_owner(case_dir, metadata, findings)
    generate_court(case_dir, metadata, findings)

if __name__ == '__main__':
    main()