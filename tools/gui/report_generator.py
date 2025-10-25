#!/usr/bin/env python3
"""
Report generator for owner and court reports.
- Reads case metadata, chain_of_custody and masked scan reports (JSON/CSV).
- Produces Markdown reports and simple HTML exports.
- Can sign reports using gpg (armor detached signature or inline sign).
Uses only Python standard library and subprocess for gpg.
"""
from datetime import datetime
import os
import json
import csv
import subprocess
import html
import tempfile

# Load basic metadata from case directory
def load_metadata(case_dir):
    meta = {}
    mfile = os.path.join(case_dir, "metadata.txt")
    if os.path.exists(mfile):
        try:
            with open(mfile, "r") as f:
                for line in f:
                    if ":" in line:
                        k, v = line.split(":", 1)
                        meta[k.strip()] = v.strip()
        except Exception:
            pass
    return meta

# Load chain_of_custody if present (text)
def load_chain_of_custody(case_dir):
    path = os.path.join(case_dir, "chain_of_custody.txt")
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return f.read()
        except Exception:
            return ""
    return ""

# Collect masked findings from JSON/CSV scan results
def load_masked_findings(case_dir, max_items=200):
    findings = []
    reports_dir = os.path.join(case_dir, "reports")
    if not os.path.isdir(reports_dir):
        return findings
    # JSON files
    for name in sorted(os.listdir(reports_dir)):
        path = os.path.join(reports_dir, name)
        try:
            if name.endswith(".json"):
                with open(path, "r", errors="ignore") as f:
                    data = json.load(f)
                for item in data:
                    # Use snippet if present, otherwise redact
                    snippet = item.get("snippet", "")
                    sensitive = item.get("sensitive", False)
                    if sensitive:
                        snippet = "REDACTED: sensitive"
                    findings.append({
                        "path": item.get("path",""),
                        "snippet": snippet,
                        "filesize": item.get("filesize",""),
                        "sha256": item.get("sha256","")
                    })
            elif name.endswith(".csv"):
                with open(path, "r", errors="ignore") as f:
                    rdr = csv.reader(f)
                    headers = next(rdr, [])
                    try:
                        idx_path = headers.index("path")
                    except ValueError:
                        idx_path = 0
                    try:
                        idx_snip = headers.index("snippet")
                    except ValueError:
                        idx_snip = None
                    for row in rdr:
                        snippet = row[idx_snip] if idx_snip is not None and idx_snip < len(row) else ""
                        findings.append({
                            "path": row[idx_path] if idx_path is not None and idx_path < len(row) else "",
                            "snippet": snippet,
                            "filesize": row[2] if len(row)>2 else "",
                            "sha256": row[-1] if len(row)>0 else ""
                        })
        except Exception:
            continue
        if len(findings) >= max_items:
            break
    return findings[:max_items]

# Helper to escape markdown
def md_escape(s):
    return s.replace("`", "\\`")

# Generate a simple owner (layman) report in Markdown
def generate_owner_report(case_dir, operator_name="", client_notes=""):
    meta = load_metadata(case_dir)
    findings = load_masked_findings(case_dir, max_items=100)
    coc = load_chain_of_custody(case_dir)
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
    lines = []
    lines.append("# Recovery Report (Owner)")
    lines.append(f"- Case: {os.path.basename(case_dir)}")
    lines.append(f"- Client: {meta.get('client','-')}")
    lines.append(f"- Created: {meta.get('created_at', now)}")
    lines.append(f"- Operator: {operator_name or meta.get('operator','-')}")
    lines.append(f"- Generated: {now}")
    lines.append("")
    lines.append("## Kurzbeschreibung (für den Auftraggeber)")
    lines.append("Diese Zusammenfassung richtet sich an eine nicht‑technische Leserschaft.")
    lines.append("")
    if client_notes:
        lines.append("### Kundenhinweis")
        lines.append(md_escape(client_notes))
        lines.append("")
    lines.append("## Was wurde gemacht")
    lines.append("- Forensisches Image erstellt und verifiziert (SHA256 vorhanden).")
    lines.append("- Automatischer Scan nach möglichen wallet‑Artefakten (maskiert).")
    lines.append("- Nur maskierte Snippets werden in diesem Bericht gezeigt; private Schlüssel wurden nicht automatisch extrahiert.")
    lines.append("")
    lines.append("## Gefundene Hinweise (maskiert)")
    if not findings:
        lines.append("Keine relevanten Artefakte in den maskierten Berichten gefunden.")
    else:
        for i, f in enumerate(findings[:10], start=1):
            lines.append(f"### Hinweis {i}")
            lines.append(f"- Pfad: `{md_escape(f.get('path',''))}`")
            snippet = f.get("snippet","")
            lines.append(f"- Snippet: `{md_escape(snippet)}`")
            lines.append("")
    lines.append("## Nächste Schritte (Empfehlung)")
    lines.append("- Wenn ein Hinweis bestätigt wird, besprechen Sie mit dem Operator die sichere Übergabe oder weitere autorisierte Schritte.")
    lines.append("- Keine Passwörter oder seed phrases per E‑Mail senden.")
    lines.append("")
    lines.append("## Chain of Custody (Auszug)")
    lines.append("```")
    lines.append(coc if coc else "Chain of custody not available.")
    lines.append("```")
    return "\n".join(lines)

# Generate court (technical) report in Markdown
def generate_court_report(case_dir, operator_name="", detail_limit=200):
    meta = load_metadata(case_dir)
    findings = load_masked_findings(case_dir, max_items=detail_limit)
    coc = load_chain_of_custody(case_dir)
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
    lines = []
    lines.append("# Forensic Report (Court / Technical)")
    lines.append(f"- Case: {os.path.basename(case_dir)}")
    lines.append(f"- Client: {meta.get('client','-')}")
    lines.append(f"- Created: {meta.get('created_at', now)}")
    lines.append(f"- Operator: {operator_name or meta.get('operator','-')}")
    lines.append(f"- Generated: {now}")
    lines.append("")
    lines.append("## Scope and Methodology")
    lines.append("- Imaging tool: dd (or equivalent). Image SHA256 stored alongside the image.")
    lines.append("- Scanning: automated filename/content heuristics, yara rules (if available), bulk_extractor (if available).")
    lines.append("- All analysis performed on READ‑ONLY copy of the image.")
    lines.append("")
    lines.append("## Findings (masked / identifiers)")
    if not findings:
        lines.append("No masked findings present.")
    else:
        for i, f in enumerate(findings, start=1):
            lines.append(f"### Finding {i}")
            lines.append(f"- path: `{md_escape(f.get('path',''))}`")
            lines.append(f"- filesize: {f.get('filesize','')}")
            lines.append(f"- sha256: `{f.get('sha256','')}`")
            snippet = f.get("snippet","")
            lines.append(f"- snippet (masked): `{md_escape(snippet)}`")
            lines.append("")
    lines.append("## Evidence and Integrity")
    lines.append("- Image SHA256 files are preserved in the case directory (see image.dd.sha256).")
    lines.append("- Manifest and signed manifest included if produced.")
    lines.append("")
    lines.append("## Chain of Custody (full)")
    lines.append("```")
    lines.append(coc if coc else "Chain of custody not available.")
    lines.append("```")
    lines.append("")
    lines.append("## Notes for the Court")
    lines.append("- All sensitive values in this report are masked. Raw secrets are held securely and only released under explicit, signed client consent.")
    return "\n".join(lines)

# Export markdown to file
def export_markdown(markdown_text, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    return out_path

# Simple HTML export (very small template)
def export_html(markdown_text, out_path):
    # minimal conversion: escape and wrap paragraphs by double newlines
    esc = html.escape(markdown_text)
    # naive paragraphing
    paragraphs = esc.split("\n\n")
    body = "\n".join(f"<p>{p.replace(chr(10), '<br/>')}</p>" for p in paragraphs)
    html_doc = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<title>Report</title>
<style>
body{{font-family: sans-serif; margin: 24px;}}
pre{{background:#f7f7f7; padding:8px; border-radius:4px;}}
</style>
</head><body>
{body}
</body></html>"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_doc)
    return out_path

# Sign a file with GPG (creates detached armored signature)
def sign_with_gpg(file_path, signer=None, output_sig=None):
    # signer: optional key id or email
    if output_sig is None:
        output_sig = file_path + ".asc"
    cmd = ["gpg", "--armor", "--detach-sign", "--output", output_sig, file_path]
    if signer:
        cmd[2:2] = ["--local-user", signer]
    # call gpg; will use system gpg agent / prompt if needed
    try:
        subprocess.check_call(cmd)
        return output_sig
    except subprocess.CalledProcessError:
        return None