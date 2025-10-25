#!/usr/bin/env python3
"""
Simple offline Markdown -> HTML slide generator.
- Reads all training/*.md files and splits slides at top-level H1 (# ) headings and H2 (## ) optionally.
- Produces a single presentation HTML (presentation.html) and per-module HTML files.
- Uses only Python standard library.
Usage:
  python3 tools/slides/generate_slides.py /path/to/repo
"""
# Comments in English; UI/instructions in repository README.
import sys
import os
import re
from datetime import datetime
import html

if len(sys.argv) != 2:
    print("Usage: python3 tools/slides/generate_slides.py /path/to/repo")
    sys.exit(2)

REPO_ROOT = os.path.abspath(sys.argv[1])
TRAINING_DIR = os.path.join(REPO_ROOT, "training")
OUT_DIR = os.path.join(REPO_ROOT, "tools", "slides", "output")
os.makedirs(OUT_DIR, exist_ok=True)

CSS = """
/* Simple slide CSS */
body { margin: 0; font-family: Arial, Helvetica, sans-serif; background: #111; color: #eee; }
.slide { display: none; padding: 40px; height: 100vh; box-sizing: border-box; }
.slide.active { display: block; }
.container { max-width: 1100px; margin: 0 auto; }
h1 { font-size: 36px; margin-bottom: 8px; color: #fff; }
h2 { font-size: 28px; color: #ddd; }
p, li, pre { color: #ddd; font-size: 18px; line-height: 1.4; }
pre { background: rgba(255,255,255,0.03); padding: 12px; border-radius: 6px; overflow:auto; }
.footer { position: fixed; right: 20px; bottom: 12px; color: #888; font-size: 13px; }
.nav { position: fixed; left: 20px; bottom: 12px; color: #888; font-size: 13px; }
"""

JS = """
// Simple navigation: left/right arrows or space
let idx = 0;
const slides = document.querySelectorAll('.slide');
function show(i) {
  if (i < 0) i = 0;
  if (i >= slides.length) i = slides.length - 1;
  slides.forEach(s => s.classList.remove('active'));
  slides[i].classList.add('active');
  document.getElementById('counter').textContent = (i+1) + '/' + slides.length;
  idx = i;
}
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') show(idx+1);
  if (e.key === 'ArrowLeft'  || e.key === 'PageUp') show(idx-1);
});
document.getElementById('prev').addEventListener('click', () => show(idx-1));
document.getElementById('next').addEventListener('click', () => show(idx+1));
show(0);
"""

def md_to_html_fragment(md):
    # Very small markdown -> HTML converter for basic elements
    lines = md.splitlines()
    out = []
    in_pre = False
    for line in lines:
        if line.startswith("```"):
            in_pre = not in_pre
            if in_pre:
                out.append("<pre>")
            else:
                out.append("</pre>")
            continue
        if in_pre:
            out.append(html.escape(line))
            continue
        # headings
        if line.startswith("# "):
            out.append(f"<h1>{html.escape(line[2:].strip())}</h1>")
            continue
        if line.startswith("## "):
            out.append(f"<h2>{html.escape(line[3:].strip())}</h2>")
            continue
        if line.startswith("- "):
            # simple ul handling
            if not out or not out[-1].endswith("<ul>"):
                out.append("<ul>")
            out.append(f"<li>{html.escape(line[2:].strip())}</li>")
            # ensure close handled later
            continue
        # blank line handling and close ul
        if line.strip() == "":
            if out and out[-1] == "<ul>":
                out.append("</ul>")
            out.append("<p></p>")
            continue
        out.append(f"<p>{html.escape(line)}</p>")
    # close dangling lists
    html_text = "\n".join(out)
    html_text = html_text.replace("<ul>\n</ul>", "")
    return html_text

def split_into_slides(md):
    # Split on H1 headings; if no H1, put all in one slide
    parts = re.split(r'(^# .*$)', md, flags=re.MULTILINE)
    slides = []
    if len(parts) == 1:
        slides = [parts[0]]
    else:
        # parts structured as ['', '# Title', 'content', '# Next', 'content' ...]
        cur = ""
        for i in range(1, len(parts), 2):
            title = parts[i].strip()
            content = parts[i+1] if (i+1) < len(parts) else ""
            slides.append(title + "\n\n" + content)
    return slides

all_fragments = []
file_list = sorted([f for f in os.listdir(TRAINING_DIR) if f.endswith(".md")])
if not file_list:
    print("No training markdown files found in", TRAINING_DIR)
    sys.exit(1)

for fname in file_list:
    path = os.path.join(TRAINING_DIR, fname)
    with open(path, "r", encoding="utf-8") as fh:
        md = fh.read()
    slides = split_into_slides(md)
    for s in slides:
        # keep as fragment
        frag = md_to_html_fragment(s)
        all_fragments.append((fname, frag))

# Build HTML
html_lines = []
html_lines.append("<!doctype html><html><head><meta charset='utf-8'><title>Training Slides</title>")
html_lines.append(f"<style>{CSS}</style></head><body>")
for i, (src, frag) in enumerate(all_fragments):
    html_lines.append(f"<div class='slide' id='slide{i}'><div class='container'>")
    html_lines.append(f"<div style='color:#888;font-size:12px;margin-bottom:8px;'>Source: {html.escape(src)}</div>")
    html_lines.append(frag)
    html_lines.append("</div></div>")
# Footer/navigation
html_lines.append("<div class='nav'><button id='prev'>Prev</button> <button id='next'>Next</button></div>")
html_lines.append("<div class='footer' id='counter'></div>")
html_lines.append(f"<script>{JS}</script></body></html>")

OUT_FILE = os.path.join(OUT_DIR, "presentation.html")
with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(html_lines))

print("Slides generated:", OUT_FILE)
print("Open in browser (offline) to present. Use arrows or buttons to navigate.")