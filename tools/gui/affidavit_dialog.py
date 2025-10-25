#!/usr/bin/env python3
"""
Affidavit dialog: fill, save and sign expert affidavit within the GUI.
- Loads templates/expert_affidavit.md, fills metadata placeholders, allows editing.
- Saves to case_dir/archives/expert_affidavit_filled_<timestamp>.md
- Optional: clearsign via gpg, optional encrypt for recipient in env GPG_RECIPIENT or provided key.
- Uses only Python standard library.
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import subprocess
import shlex

TEMPLATE_PATH = os.path.join("templates", "expert_affidavit.md")

def read_template():
    if os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return ("# Expert Affidavit\n\n"
            "Please edit this affidavit.\n")

def safe_mkdir(path):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        pass

class AffidavitDialog(tk.Toplevel):
    def __init__(self, master, case_dir, log_event_fn=None):
        super().__init__(master)
        self.case_dir = os.path.abspath(case_dir)
        self.log_event_fn = log_event_fn
        self.title("Affidavit Editor")
        self.geometry("900x700")
        self.create_widgets()
        self.prefill_template()

    def create_widgets(self):
        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True, padx=8, pady=8)

        topbar = ttk.Frame(frm)
        topbar.pack(fill="x", pady=(0,6))
        ttk.Label(topbar, text="Affidavit (Expert) — bearbeiten und signieren").pack(side="left")
        btn_frame = ttk.Frame(topbar)
        btn_frame.pack(side="right")
        ttk.Button(btn_frame, text="Save", command=self.on_save).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Clearsign (GPG)", command=self.on_clearsign).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Encrypt & Save (optional)", command=self.on_encrypt_save).pack(side="left", padx=4)
        ttk.Button(btn_frame, text="Close", command=self.destroy).pack(side="left", padx=4)

        # metadata preview
        meta_frame = ttk.LabelFrame(frm, text="Case metadata (preview)")
        meta_frame.pack(fill="x", pady=(0,6))
        self.meta_text = tk.Text(meta_frame, height=6, wrap="word", bg="#f3f3f3")
        self.meta_text.pack(fill="both", expand=True, padx=4, pady=4)
        self.meta_text.configure(state="disabled")

        # editor
        ed_frame = ttk.LabelFrame(frm, text="Affidavit (Markdown)")
        ed_frame.pack(fill="both", expand=True)
        self.editor = tk.Text(ed_frame, wrap="word")
        self.editor.pack(fill="both", expand=True, padx=4, pady=4)

    def prefill_template(self):
        # load template and replace placeholders with metadata from case_dir
        tpl = read_template()
        meta = self._read_metadata()
        # basic placeholders replacement
        replacements = {
            "{{case_id}}": os.path.basename(self.case_dir),
            "{{client}}": meta.get("client",""),
            "{{operator}}": meta.get("operator",""),
            "{{created_at}}": meta.get("created_at", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")),
        }
        for k,v in replacements.items():
            tpl = tpl.replace(k, v)
        self.editor.delete("1.0", "end")
        self.editor.insert("1.0", tpl)
        # fill meta preview
        meta_text = []
        meta_text.append(f"Case: {replacements['{{case_id}}']}")
        meta_text.append(f"Client: {replacements['{{client}}']}")
        meta_text.append(f"Operator: {replacements['{{operator}}']}")
        meta_text.append(f"Created at: {replacements['{{created_at}}']}")
        self.meta_text.configure(state="normal")
        self.meta_text.delete("1.0","end")
        self.meta_text.insert("1.0", "\n".join(meta_text))
        self.meta_text.configure(state="disabled")

    def _read_metadata(self):
        meta = {}
        mfile = os.path.join(self.case_dir, "metadata.txt")
        if os.path.exists(mfile):
            try:
                with open(mfile,"r",encoding="utf-8") as f:
                    for line in f:
                        if ":" in line:
                            k,v = line.split(":",1)
                            meta[k.strip()] = v.strip()
            except Exception:
                pass
        return meta

    def _archivedir(self):
        ad = os.path.join(self.case_dir, "archives")
        safe_mkdir(ad)
        return ad

    def _timestamp(self):
        return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    def _write_file(self, content, filename):
        path = os.path.join(self._archivedir(), filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        try:
            os.chmod(path, 0o600)
        except Exception:
            pass
        return path

    def on_save(self):
        content = self.editor.get("1.0", "end").rstrip() + "\n"
        fname = f"expert_affidavit_filled_{self._timestamp()}.md"
        out = self._write_file(content, fname)
        messagebox.showinfo("Saved", f"Affidavit saved to:\n{out}")
        if self.log_event_fn:
            try:
                self.log_event_fn(self.case_dir, "info", f"Affidavit saved: {os.path.basename(out)}", 0)
            except Exception:
                pass

    def on_clearsign(self):
        # First save current content
        content = self.editor.get("1.0", "end").rstrip() + "\n"
        base_fname = f"expert_affidavit_filled_{self._timestamp()}.md"
        out_path = self._write_file(content, base_fname)
        signed_path = out_path + ".asc"
        # Run gpg clearsign
        if not shutil.which("gpg"):
            messagebox.showerror("GPG fehlt", "gpg ist nicht installiert oder nicht im PATH.")
            return
        try:
            # clearsign into signed_path
            cmd = ["gpg", "--yes", "--batch", "--armor", "--clearsign", "--output", signed_path, out_path]
            subprocess.check_call(cmd)
            messagebox.showinfo("Signed", f"Clearsigned affidavit: {signed_path}")
            if self.log_event_fn:
                try:
                    self.log_event_fn(self.case_dir, "info", f"Affidavit clearsigned: {os.path.basename(signed_path)}", 0)
                except Exception:
                    pass
        except subprocess.CalledProcessError as e:
            messagebox.showerror("GPG Fehler", f"gpg failed with code {e.returncode}")

    def on_encrypt_save(self):
        # Save then encrypt for recipient
        content = self.editor.get("1.0", "end").rstrip() + "\n"
        base_fname = f"expert_affidavit_filled_{self._timestamp()}.md"
        out_path = self._write_file(content, base_fname)
        # ask for recipient or use env
        recipient = os.environ.get("GPG_RECIPIENT","").strip()
        if not recipient:
            recipient = tk.simpledialog.askstring("GPG Recipient", "Enter GPG recipient key id or email (leave empty to cancel):")
        if not recipient:
            messagebox.showinfo("Abgebrochen", "Keine Verschlüsselung durchgeführt.")
            return
        enc_path = out_path + ".gpg"
        if not shutil.which("gpg"):
            messagebox.showerror("GPG fehlt", "gpg ist nicht installiert oder nicht im PATH.")
            return
        try:
            cmd = ["gpg", "--yes", "--batch", "--recipient", recipient, "--encrypt", "--output", enc_path, out_path]
            subprocess.check_call(cmd)
            messagebox.showinfo("Encrypted", f"Encrypted affidavit: {enc_path}")
            if self.log_event_fn:
                try:
                    self.log_event_fn(self.case_dir, "info", f"Affidavit encrypted for {recipient}: {os.path.basename(enc_path)}", 0)
                except Exception:
                    pass
        except subprocess.CalledProcessError as e:
            messagebox.showerror("GPG Fehler", f"gpg failed with code {e.returncode}")