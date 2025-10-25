#!/usr/bin/env python3
"""
Recursive scanner for likely wallet artifacts (safe mode, stronger masking).
- Scans filenames for suspicious names
- Scans file contents for patterns such as JSON keystore markers
- Produces reports (CSV + JSON)
Notes:
- This script masks sensitive sequences strongly and marks 'sensitive' flags.
- Uses only standard library.
"""
import os
import sys
import argparse
import json
import csv
import hashlib
import re
from datetime import datetime

FILENAME_PATTERNS = [
    re.compile(r'wallet', re.IGNORECASE),
    re.compile(r'keystore', re.IGNORECASE),
    re.compile(r'mnemonic', re.IGNORECASE),
    re.compile(r'seed', re.IGNORECASE),
    re.compile(r'private.*key', re.IGNORECASE),
    re.compile(r'ethereum', re.IGNORECASE),
    re.compile(r'btc', re.IGNORECASE),
]

CONTENT_PATTERNS = [
    re.compile(r'"crypto"\s*:', re.IGNORECASE),
    re.compile(r'"address"\s*:', re.IGNORECASE),
    re.compile(r'(?:(?:[a-f0-9]{64})\b)', re.IGNORECASE),  # 64 hex
    re.compile(r'([a-z]+(\s+[a-z]+){11,24})', re.IGNORECASE),  # mnemonic-like
]

def mask_hex(s):
    # keep first 6 and last 4 chars, mask the rest
    def repl(m):
        t = m.group(0)
        if len(t) <= 14:
            return '*' * len(t)
        return t[:6] + '*'*(len(t)-10) + t[-4:]
    return re.sub(r'([a-f0-9]{20,})', repl, s, flags=re.IGNORECASE)

def mask_mnemonic(s):
    # keep only first and last word, replace middle with ***
    words = s.split()
    if len(words) <= 2:
        return '***'
    return words[0] + ' ' + '***' + ' ' + words[-1]

def mask_text(s):
    s = mask_hex(s)
    s = re.sub(r'([a-z]+(\s+[a-z]+){11,24})', lambda m: mask_mnemonic(m.group(0)), s, flags=re.IGNORECASE)
    # limit length
    if len(s) > 120:
        return s[:56] + ' ... ' + s[-56:]
    return s

def file_sha256(path):
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(65536), b''):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return ''

def scan(root, outdir):
    results = []
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            try:
                stat = os.lstat(full)
            except Exception:
                continue

            fname_match = None
            for p in FILENAME_PATTERNS:
                if p.search(fn):
                    fname_match = p.pattern
                    break

            content_match = None
            snippet = ''
            sensitive = False
            try:
                size = os.path.getsize(full)
                if size <= 2000000:  # smaller limit to avoid reading huge files
                    with open(full, 'r', errors='ignore') as f:
                        data = f.read()
                else:
                    with open(full, 'r', errors='ignore') as f:
                        data = f.read(100000)
                for p in CONTENT_PATTERNS:
                    m = p.search(data)
                    if m:
                        content_match = p.pattern
                        start = max(m.start()-40, 0)
                        end = min(m.end()+40, len(data))
                        raw = data[start:end]
                        # If pattern is a mnemonic or long hex, mark sensitive
                        if p.pattern.find('{64}') != -1 or p.pattern.find('mnemonic') != -1 or p.pattern.find('{11,24}') != -1 or 'mnemonic' in p.pattern.lower():
                            sensitive = True
                        snippet = mask_text(raw)
                        break
            except Exception:
                data = ''

            if fname_match or content_match:
                res = {
                    'path': rel,
                    'filename': fn,
                    'filesize': os.path.getsize(full),
                    'filename_pattern': fname_match or '',
                    'content_pattern': content_match or '',
                    'sensitive': sensitive,
                    'snippet': snippet if not sensitive else 'REDACTED: sensitive content (masked)',
                    'sha256': file_sha256(full),
                }
                results.append(res)

    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    json_path = os.path.join(outdir, f'scan_results_{timestamp}.json')
    csv_path = os.path.join(outdir, f'scan_results_{timestamp}.csv')
    with open(json_path, 'w') as jf:
        json.dump(results, jf, indent=2)
    with open(csv_path, 'w', newline='') as cf:
        writer = csv.writer(cf)
        writer.writerow(['path','filename','filesize','filename_pattern','content_pattern','sensitive','snippet','sha256'])
        for r in results:
            writer.writerow([r['path'], r['filename'], r['filesize'], r['filename_pattern'], r['content_pattern'], str(r['sensitive']), r['snippet'], r['sha256']])
    print(f"Scan complete. JSON: {json_path} CSV: {csv_path}")

def main():
    p = argparse.ArgumentParser(description='Search filesystem for wallet artifacts (safe mode)')
    p.add_argument('--root', required=True, help='Root directory to scan (mounted image)')
    p.add_argument('--outdir', required=True, help='Directory for reports')
    args = p.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    scan(args.root, args.outdir)

if __name__ == '__main__':
    main()