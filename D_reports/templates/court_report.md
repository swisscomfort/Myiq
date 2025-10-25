```markdown
# Court / Technical Report — {{case_id}}

Client: {{client}}
Case created: {{created_at}}
Operator: {{operator}}
Generated: {{generated}}

## Scope & Methodology
- Imaging: dd (or equivalent). SHA256: {{image_sha256}}
- Scanning tool: rustscanner v{{scanner_version}}
- Scan modes: filename/head/deep

## Findings (masked)
{% for h in findings %}
### Finding {{ loop.index }}
- path: `{{ h.path }}`
- filesize: {{ h.filesize }}
- sha256: `{{ h.sha256 }}`
- snippet (masked): `{{ h.snippet }}`
{% endfor %}

## Evidence & Chain of Custody
- chain_of_custody: see attached chain_of_custody.txt
- manifest & signatures included
```