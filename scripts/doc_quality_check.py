#!/usr/bin/env python3
"""
Doc quality checker for Markdown (.md) and text (.txt) files.

Checks performed (best-effort, offline, stdlib only):
- finds *.md and *.txt files (excluding .git, venv, node_modules)
- detects YAML frontmatter and parses simple keys (title, version, created_at, last_reviewed)
- checks for placeholder tokens (____, TODO, FIXME, {{...}}, YOUR_EMAIL, REPLACE_ME)
- verifies presence of required headings for key templates (client_acknowledgement_form, data_processing_agreement, expert_affidavit, probate_report)
- ensures major shell commands (dd, sha256sum, gpg) appear inside code fences (``` ... ```)
- heuristic scan for mnemonic-like sequences (12+ words lowercase) and long hex strings (>40 hex chars)
- reports results as JSON and prints a human summary

Usage:
  python3 scripts/doc_quality_check.py /path/to/repo
Outputs:
  - ./docs/doc_checks_report.json
  - human readable summary on stdout
"""
import sys
import os
import re
import json
from datetime import datetime

SKIP_DIRS = {'.git', '.venv', 'venv', 'node_modules', '__pycache__'}
MD_EXT = ('.md', '.markdown')
TXT_EXT = ('.txt',)

# Patterns
FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.S)
YAML_KV_RE = re.compile(r'^\s*([^:]+)\s*:\s*(.+?)\s*$', re.M)
PLACEHOLDER_PATTERNS = [
    re.compile(r'_{3,}'),                    # underscores like ____ 
    re.compile(r'\bTODO\b', re.I),
    re.compile(r'\bFIXME\b', re.I),
    re.compile(r'\{\{.+?\}\}'),              # {{placeholder}}
    re.compile(r'REPLACE(_|-)ME', re.I),
    re.compile(r'YOUR[_\sA-Z]*EMAIL', re.I),
]
CODE_FENCE_RE = re.compile(r'```.*?```', re.S)
SHELL_CMD_WORDS = ['dd ', 'sha256sum', 'gpg ', 'losetup', 'mount ', 'shred', 'bulk_extractor', 'yara ']

MNEMONIC_RE = re.compile(r'\b([a-z]{2,})(?:\s+[a-z]{2,}){11,24}\b', re.I)
LONG_HEX_RE = re.compile(r'\b[a-f0-9]{40,}\b', re.I)

# Required headings map: filename basename -> list of required headings (case-insensitive)
REQUIRED_HEADINGS = {
    'client_acknowledgement_form': [
        'Identitätsprüfung', 'Scope', 'Technische Kurzbeschreibung', 'Unterschriften', 'Aufbewahrung'
    ],
    'data_processing_agreement': [
        'Gegenstand', 'Kategorien personenbezogener Daten', 'Sicherheitsmaßnahmen', 'Anhang A', 'Löschung'
    ],
    'expert_affidavit': [
        'Qualifikation', 'Methodik', 'Feststellungen', 'Unterschrift'
    ],
    'probate_report': [
        'Auftrag', 'Imaging', 'Findings', 'Evidence package', 'Chain of Custody'
    ],
}

def is_text_file(path):
    return path.lower().endswith(MD_EXT + TXT_EXT)

def find_files(root):
    res = []
    for dirpath, dirnames, filenames in os.walk(root):
        # prune
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.startswith('.'):
                continue
            if fn.lower().endswith(MD_EXT + TXT_EXT):
                res.append(os.path.join(dirpath, fn))
    return sorted(res)

def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='latin-1') as f:
            return f.read()
    except Exception:
        return ''

def parse_frontmatter(text):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    body = m.group(1)
    data = {}
    for kv in YAML_KV_RE.finditer(body):
        k = kv.group(1).strip()
        v = kv.group(2).strip().strip('"').strip("'")
        data[k] = v
    return data

def headings_present(text, required_list):
    # find headings (#, ##, ###) text, normalize
    hs = re.findall(r'^\s{0,3}#{1,6}\s*(.+)$', text, re.M)
    hs_n = [h.strip().lower() for h in hs]
    missing = []
    for req in required_list:
        found = any(req.lower() in h for h in hs_n)
        if not found:
            missing.append(req)
    return missing

def commands_in_code_fence(text):
    # returns list of command words found outside code fences
    fences = [m.span() for m in CODE_FENCE_RE.finditer(text)]
    def in_fence(idx):
        for a,b in fences:
            if a <= idx < b:
                return True
        return False
    issues = []
    for word in SHELL_CMD_WORDS:
        for m in re.finditer(re.escape(word), text):
            if not in_fence(m.start()):
                issues.append(word.strip())
                break
    return sorted(set(issues))

def find_placeholders(text):
    hits = []
    for p in PLACEHOLDER_PATTERNS:
        for m in p.finditer(text):
            hits.append({'pattern': p.pattern, 'match': m.group(0), 'pos': m.start()})
    # detect literal 'TITEL HIER'
    for m in re.finditer(r'TITEL HIER', text, re.I):
        hits.append({'pattern': 'TITEL HIER', 'match': m.group(0), 'pos': m.start()})
    return hits

def find_sensitive_patterns(text):
    issues = []
    for m in MNEMONIC_RE.finditer(text):
        issues.append({'type': 'mnemonic', 'match': m.group(0)[:80], 'pos': m.start()})
    for m in LONG_HEX_RE.finditer(text):
        issues.append({'type': 'long_hex', 'match': m.group(0)[:80], 'pos': m.start()})
    return issues

def analyze_file(path, repo_root):
    rel = os.path.relpath(path, repo_root)
    text = read_file(path)
    fm = parse_frontmatter(text)
    placeholders = find_placeholders(text)
    sensitive = find_sensitive_patterns(text)
    cmd_issues = commands_in_code_fence(text)
    code_fences = bool(CODE_FENCE_RE.search(text))
    # required headings check by basename match
    base = os.path.basename(path).lower()
    required_missing = []
    for key, reqs in REQUIRED_HEADINGS.items():
        if key in base:
            missing = headings_present(text, reqs)
            required_missing = missing
            break
    return {
        'path': rel,
        'size_bytes': len(text.encode('utf-8')),
        'frontmatter': fm,
        'placeholders': placeholders,
        'sensitive_patterns': sensitive,
        'cmds_outside_code_fence': cmd_issues,
        'has_code_fences': code_fences,
        'required_headings_missing': required_missing,
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/doc_quality_check.py /path/to/repo")
        sys.exit(2)
    repo_root = os.path.abspath(sys.argv[1])
    out_json = os.path.join(repo_root, 'docs', 'doc_checks_report.json')
    os.makedirs(os.path.dirname(out_json), exist_ok=True)

    files = find_files(repo_root)
    results = []
    summary = {'files_checked': 0, 'files_with_issues': 0, 'placeholders_total': 0, 'sensitive_total': 0}
    for f in files:
        res = analyze_file(f, repo_root)
        results.append(res)
        summary['files_checked'] += 1
        if res['placeholders'] or res['sensitive_patterns'] or res['cmds_outside_code_fence'] or res['required_headings_missing']:
            summary['files_with_issues'] += 1
        summary['placeholders_total'] += len(res['placeholders'])
        summary['sensitive_total'] += len(res['sensitive_patterns'])

    report = {
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'repo_root': repo_root,
        'summary': summary,
        'results': results,
    }
    with open(out_json, 'w', encoding='utf-8') as jf:
        json.dump(report, jf, ensure_ascii=False, indent=2)

    # print human summary
    print("Dokumentprüfung abgeschlossen.")
    print(f"Repo: {repo_root}")
    print(f"Dateien geprüft: {summary['files_checked']}")
    print(f"Dateien mit Auffälligkeiten: {summary['files_with_issues']}")
    print(f"Gesamt Platzhalter‑Funde: {summary['placeholders_total']}")
    print(f"Gesamt Sensitive‑Pattern Funde (heuristisch): {summary['sensitive_total']}")
    print("")
    print("Wichtigste Hinweise (erste 20 Dateien mit Auffälligkeiten):")
    count = 0
    for r in results:
        issues = (len(r['placeholders']) + len(r['sensitive_patterns']) + len(r['cmds_outside_code_fence']) + len(r['required_headings_missing']))
        if issues:
            count += 1
            print(f"- {r['path']}: placeholders={len(r['placeholders'])}, sensitive={len(r['sensitive_patterns'])}, cmds_outside_codeblock={len(r['cmds_outside_code_fence'])}, missing_headings={len(r['required_headings_missing'])}")
            if count >= 20:
                break
    print("")
    print(f"Full JSON report written to: {out_json}")

if __name__ == '__main__':
    main()