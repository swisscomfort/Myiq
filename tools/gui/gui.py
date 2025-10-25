#!/usr/bin/env python3
"""
Enhanced Tkinter GUI with Affidavit integration.
- Adds "Fill Affidavit" button to Reports tab which opens affidavit_editor (tools/gui/affidavit_dialog.py)
- All other features (validate/package/probate) unchanged.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import argparse
import os
import subprocess
import threading
import time
import json
import shutil

# import affidavit dialog
from tools.gui.affidavit_dialog import AffidavitDialog

LOG_HELPER = os.path.join("scripts", "log_event.sh")
VALIDATOR_SCRIPT = os.path.join("scripts", "validate_case_before_packaging.sh")
PACKAGE_SCRIPT = os.path.join("scripts", "package_for_legal_strict.sh")
PROBATE_SCRIPT = os.path.join("scripts", "create_probate_package.sh")

def is_executable(path):
    return os.path.exists(path) and os.access(path, os.X_OK)

def log_event(case_dir, level, message, progress=None):
    if os.path.exists(LOG_HELPER) and os.access(LOG_HELPER, os.X_OK):
        args = [LOG_HELPER, case_dir, level, message]
        if progress is not None:
            args.append(str(progress))
        try:
            subprocess.Popen(args)
        except Exception:
            pass

class ProcessOutputWindow(tk.Toplevel):
    def __init__(self, master, title="Command Output"):
        super().__init__(master)
        self.title(title)
        self.geometry("900x500")
        self.text = tk.Text(self, wrap="none", state="normal", bg="#111", fg="#eee")
        self.text.pack(fill="both", expand=True)
        btn = ttk.Button(self, text="Schließen", command=self.destroy)
        btn.pack(side="bottom", pady=6)

    def append(self, line):
        self.text.insert("end", line + "\n")
        self.text.see("end")
        self.update_idletasks()

class MonitorApp(tk.Tk):
    def __init__(self, case_dir):
        super().__init__()
        self.case_dir = os.path.abspath(case_dir)
        self.title(f"Crypto Recovery — Monitor: {os.path.basename(self.case_dir)}")
        self.geometry("1100x760")
        self.create_widgets()
        self._log_pos = 0
        self.after(1000, self.poll)

    def create_widgets(self):
        # Top frame: metadata + progress
        top = ttk.Frame(self)
        top.pack(fill="x", padx=8, pady=6)

        meta_frame = ttk.LabelFrame(top, text="Case metadata")
        meta_frame.pack(side="left", fill="x", expand=True, padx=4)

        self.client_var = tk.StringVar(value="—")
        self.created_var = tk.StringVar(value="—")
        ttk.Label(meta_frame, text="Client:").grid(row=0, column=0, sticky="w")
        ttk.Label(meta_frame, textvariable=self.client_var).grid(row=0, column=1, sticky="w")
        ttk.Label(meta_frame, text="Created:").grid(row=1, column=0, sticky="w")
        ttk.Label(meta_frame, textvariable=self.created_var).grid(row=1, column=1, sticky="w")

        progress_frame = ttk.LabelFrame(top, text="Progress")
        progress_frame.pack(side="right", fill="x", padx=4)
        self.progress_var = tk.IntVar(value=0)
        self.progressbar = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="determinate", variable=self.progress_var, maximum=100)
        self.progressbar.pack(padx=8, pady=8)
        self.last_event_var = tk.StringVar(value="—")
        ttk.Label(progress_frame, textvariable=self.last_event_var, wraplength=300).pack(padx=8)

        # Notebook for tabs
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=8, pady=6)

        # Log tab
        log_frame = ttk.Frame(self.nb)
        self.nb.add(log_frame, text="Monitor / Log")
        self.log_text = tk.Text(log_frame, wrap="none", state="disabled", bg="#f7f7f7")
        self.log_text.pack(fill="both", expand=True, side="left")
        scroll_y = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="left", fill="y", padx=(0,4))

        # Findings tab
        findings_frame = ttk.Frame(self.nb)
        self.nb.add(findings_frame, text="Masked Findings")
        self.find_tree = ttk.Treeview(findings_frame, columns=("file", "snippet", "size"), show="headings")
        self.find_tree.heading("file", text="File")
        self.find_tree.heading("snippet", text="Snippet (masked)")
        self.find_tree.heading("size", text="Size")
        self.find_tree.column("file", width=380)
        self.find_tree.column("snippet", width=560)
        self.find_tree.column("size", width=80, anchor="e")
        self.find_tree.pack(fill="both", expand=True)

        # Reports tab
        report_frame = ttk.Frame(self.nb)
        self.nb.add(report_frame, text="Reports / Export")
        self.create_report_tab(report_frame)

        # Bottom buttons
        bottom = ttk.Frame(self)
        bottom.pack(fill="x", padx=8, pady=6)
        ttk.Button(bottom, text="Open case folder", command=self.open_case).pack(side="left")
        ttk.Button(bottom, text="Refresh findings", command=self.load_findings).pack(side="left", padx=6)
        ttk.Button(bottom, text="Tail log file in terminal", command=self.tail_in_terminal).pack(side="left", padx=6)
        ttk.Button(bottom, text="Quit", command=self.quit).pack(side="right")

        # Initialize metadata and findings
        self.load_metadata()
        self.load_findings()

    def create_report_tab(self, parent):
        # Left: form + Packaging controls
        left = ttk.Frame(parent)
        left.pack(side="left", fill="y", padx=6, pady=6)
        ttk.Label(left, text="Operator name:").pack(anchor="w")
        self.op_entry = ttk.Entry(left, width=40)
        self.op_entry.pack(anchor="w", pady=2)
        ttk.Label(left, text="Client notes (owner):").pack(anchor="w", pady=(8,0))
        self.client_notes = tk.Text(left, width=40, height=6)
        self.client_notes.pack(anchor="w")
        self.consent_var = tk.IntVar(value=0)
        ttk.Checkbutton(left, text="Consent signed (required for court report)", variable=self.consent_var).pack(anchor="w", pady=8)
        ttk.Label(left, text="Export options:").pack(anchor="w", pady=(8,0))
        self.export_md_var = tk.IntVar(value=1)
        self.export_html_var = tk.IntVar(value=1)
        ttk.Checkbutton(left, text="Export Markdown (.md)", variable=self.export_md_var).pack(anchor="w")
        ttk.Checkbutton(left, text="Export HTML (.html)", variable=self.export_html_var).pack(anchor="w")
        ttk.Label(left, text="GPG signer (optional key id/email):").pack(anchor="w", pady=(8,0))
        self.gpg_entry = ttk.Entry(left, width=40)
        self.gpg_entry.pack(anchor="w", pady=2)

        # Report actions
        ttk.Button(left, text="Generate Owner Report", command=self.on_generate_owner).pack(fill="x", pady=(12,4))
        ttk.Button(left, text="Generate Court Report", command=self.on_generate_court).pack(fill="x", pady=(0,4))
        ttk.Button(left, text="Sign last generated report", command=self.on_sign_last).pack(fill="x", pady=(8,4))

        # Packaging actions
        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=8)
        ttk.Label(left, text="Packaging & Legal").pack(anchor="w", pady=(4,2))
        self.validate_btn = ttk.Button(left, text="Validate Case (pre-packaging)", command=self.on_validate_case)
        self.validate_btn.pack(fill="x", pady=(4,2))
        self.package_btn = ttk.Button(left, text="Create Legal Package", command=self.on_create_package)
        self.package_btn.pack(fill="x", pady=(4,2))
        self.probate_btn = ttk.Button(left, text="Create Probate Package", command=self.on_create_probate_package)
        self.probate_btn.pack(fill="x", pady=(4,2))

        # Affidavit button
        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=8)
        ttk.Label(left, text="Affidavit / Expert Statement").pack(anchor="w", pady=(4,2))
        self.affidavit_btn = ttk.Button(left, text="Fill Affidavit (Editor)", command=self.on_fill_affidavit)
        self.affidavit_btn.pack(fill="x", pady=(4,2))

        # Right: preview
        right = ttk.Frame(parent)
        right.pack(side="right", fill="both", expand=True, padx=6, pady=6)
        ttk.Label(right, text="Report preview").pack(anchor="w")
        self.preview = tk.Text(right, wrap="word")
        self.preview.pack(fill="both", expand=True)
        # status
        self.last_report_path = None
        self.current_report_md = ""

    # ... existing methods unchanged (load_metadata, poll, update_log, etc.) ...
    # For brevity we reuse earlier definitions; ensure they are present when integrating.

    # Affidavit handler
    def on_fill_affidavit(self):
        # open the affidavit dialog
        dlg = AffidavitDialog(self, self.case_dir, log_event_fn=log_event)
        dlg.grab_set()

    # The rest of methods (on_generate_owner, on_generate_court, on_validate_case, on_create_package,
    # on_create_probate_package, on_sign_last, load_findings, update_log, update_status, etc.)
    # are unchanged from the previous GUI implementation and must be present here.
    # For integration: copy the implementations from your existing GUI file into this class.
    #
    # NOTE: If you replaced an existing tools/gui/gui.py, ensure you include the full class methods
    # from the earlier version. This file shows the Affidavit integration points.

def main():
    p = argparse.ArgumentParser(description="GUI monitor + report generator + packaging for crypto recovery case")
    p.add_argument("--case-dir", required=True, help="Path to case directory (case_YYYY...)")
    args = p.parse_args()
    if not os.path.isdir(args.case_dir):
        print("Case directory not found:", args.case_dir)
        return
    app = MonitorApp(args.case_dir)
    app.mainloop()

if __name__ == "__main__":
    main()