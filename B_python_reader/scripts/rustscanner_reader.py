#!/usr/bin/env python3
"""
Consume rustscanner JSONL (file or stdin) and write:
- case_dir/reports/scan_results.jsonl (masked)
- case_dir/reports/scan_results.csv
- SQLite DB with hits table
Uses only Python standard library.
"""
import argparse
import json
import os
import sqlite3
import csv
import sys
import re
from datetime import datetime

def mask_snippet(s):
    # simple mask: hide long hex and mnemonic-like sequences
    s = re.sub(r'([a-f0-9]{20,})', lambda m: m.group(0)[:6] + '*'*(max(len(m.group(0))-10,4)) + m.group(0)[-4:], s, flags=re.IGNORECASE)
    s = re.sub(r'([a-z]+(?:\s+[a-z]+){11,24})', lambda m: m.group(0).split()[0] + ' ... ' + m.group(0).split()[-1], s, flags=re.IGNORECASE)
    if len(s) > 240:
        return s[:120] + ' ... ' + s[-120:]
    return s

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS hits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT,
        path TEXT,
        filesize INTEGER,
        pattern TEXT,
        snippet TEXT,
        sha256 TEXT,
        timestamp TEXT,
        scanner_version TEXT
    )''')
    conn.commit()
    return conn

def process_line(line, out_jsonl_fh, csv_writer, db_conn):
    try:
        obj = json.loads(line)
    except Exception:
        return
    obj['snippet'] = mask_snippet(obj.get('snippet',''))
    out_jsonl_fh.write(json.dumps(obj, ensure_ascii=False) + "\n")
    csv_writer.writerow([
        obj.get('case',''),
        obj.get('path',''),
        obj.get('filesize',''),
        obj.get('pattern',''),
        obj.get('snippet',''),
        obj.get('sha256',''),
        obj.get('timestamp',''),
        obj.get('scanner_version','')
    ])
    cur = db_conn.cursor()
    cur.execute('''INSERT INTO hits (case_id,path,filesize,pattern,snippet,sha256,timestamp,scanner_version)
                   VALUES (?,?,?,?,?,?,?,?)''', (
        obj.get('case',''),
        obj.get('path',''),
        obj.get('filesize',0),
        obj.get('pattern',''),
        obj.get('snippet',''),
        obj.get('sha256',''),
        obj.get('timestamp',''),
        obj.get('scanner_version','')
    ))
    db_conn.commit()

def main():
    p = argparse.ArgumentParser(description="Rustscanner JSONL reader -> case reports + sqlite")
    p.add_argument('--case-dir', required=True)
    p.add_argument('--jsonl', help='input JSONL file (omit to read stdin)')
    p.add_argument('--stream', action='store_true', help='read from stdin (use with pipe)')
    args = p.parse_args()

    case_dir = args.case_dir
    reports_dir = os.path.join(case_dir, 'reports')
    os.makedirs(reports_dir, exist_ok=True)

    out_jsonl = os.path.join(reports_dir, f'scan_results_{datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}.jsonl')
    out_csv = os.path.join(reports_dir, f'scan_results_{datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")}.csv')
    db_path = os.path.join(reports_dir, 'scan_results.db')

    conn = init_db(db_path)

    with open(out_jsonl, 'w', encoding='utf-8') as out_jf, open(out_csv, 'w', newline='', encoding='utf-8') as csvf:
        csvw = csv.writer(csvf)
        csvw.writerow(['case','path','filesize','pattern','snippet','sha256','timestamp','scanner_version'])
        if args.jsonl:
            with open(args.jsonl, 'r', encoding='utf-8') as inf:
                for line in inf:
                    process_line(line, out_jf, csvw, conn)
        else:
            # read stdin
            for line in sys.stdin:
                process_line(line, out_jf, csvw, conn)

    print("Processing complete. Reports in:", reports_dir)
    conn.close()

if __name__ == '__main__':
    main()