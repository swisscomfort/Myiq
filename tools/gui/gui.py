#!/usr/bin/env python3
"""
Enhanced Tkinter GUI with Affidavit integration and Scanner functionality.
- Scanner tab: Browse and select disk images or directories to scan
- Reports tab: Generate owner/court reports with GPG signing
- Monitor tab: Real-time case monitoring and log viewing
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import argparse
import os
import sys
import subprocess
import threading
import time
import json
import shutil

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from tools.gui import report_generator
    from tools.gui.affidavit_dialog import AffidavitDialog
except ImportError:
    # Fallback for direct execution
    import report_generator
    from affidavit_dialog import AffidavitDialog

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

        # Scanner tab (NEW)
        scanner_frame = ttk.Frame(self.nb)
        self.nb.add(scanner_frame, text="Scanner")
        self.create_scanner_tab(scanner_frame)

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

    def create_scanner_tab(self, parent):
        """New tab for selecting and scanning images or directories"""
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Instructions
        ttk.Label(main_frame, text="Scan Image or Directory", font=("", 12, "bold")).pack(anchor="w", pady=(0, 10))
        ttk.Label(main_frame, text="Select a disk image (.dd, .img, .raw) or a directory to scan for crypto artifacts.",
                  wraplength=600).pack(anchor="w", pady=(0, 20))

        # Image/Directory selection
        select_frame = ttk.LabelFrame(main_frame, text="Source Selection", padding=10)
        select_frame.pack(fill="x", pady=(0, 20))

        # Image file selection
        img_frame = ttk.Frame(select_frame)
        img_frame.pack(fill="x", pady=5)
        ttk.Label(img_frame, text="Image file:").pack(side="left", padx=(0, 10))
        self.image_path_var = tk.StringVar(value="")
        img_entry = ttk.Entry(img_frame, textvariable=self.image_path_var, width=50, state="readonly")
        img_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(img_frame, text="Browse Image...", command=self.browse_image).pack(side="left")
        ttk.Button(img_frame, text="Clear", command=lambda: self.image_path_var.set("")).pack(side="left", padx=(5, 0))

        # Directory selection
        dir_frame = ttk.Frame(select_frame)
        dir_frame.pack(fill="x", pady=5)
        ttk.Label(dir_frame, text="Directory:").pack(side="left", padx=(0, 10))
        self.dir_path_var = tk.StringVar(value="")
        dir_entry = ttk.Entry(dir_frame, textvariable=self.dir_path_var, width=50, state="readonly")
        dir_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(dir_frame, text="Browse Directory...", command=self.browse_directory).pack(side="left")
        ttk.Button(dir_frame, text="Clear", command=lambda: self.dir_path_var.set("")).pack(side="left", padx=(5, 0))

        # Note
        ttk.Label(select_frame, text="Note: Select either an image file OR a directory, not both.",
                  foreground="blue").pack(anchor="w", pady=(10, 0))

        # Scan options
        options_frame = ttk.LabelFrame(main_frame, text="Scan Options", padding=10)
        options_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(options_frame, text="Output directory (reports will be saved here):").pack(anchor="w")
        out_frame = ttk.Frame(options_frame)
        out_frame.pack(fill="x", pady=5)
        self.output_dir_var = tk.StringVar(value=os.path.join(self.case_dir, "reports"))
        ttk.Entry(out_frame, textvariable=self.output_dir_var, width=50, state="readonly").pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(out_frame, text="Change...", command=self.browse_output_dir).pack(side="left")

        # Scan button
        scan_btn_frame = ttk.Frame(main_frame)
        scan_btn_frame.pack(fill="x", pady=(10, 0))
        self.scan_btn = ttk.Button(scan_btn_frame, text="▶ Start Scan", command=self.start_scan)
        self.scan_btn.pack(side="left", padx=(0, 10))
        self.scan_status_var = tk.StringVar(value="Ready to scan")
        ttk.Label(scan_btn_frame, textvariable=self.scan_status_var, foreground="green").pack(side="left")

        # Output preview
        output_frame = ttk.LabelFrame(main_frame, text="Scan Output", padding=10)
        output_frame.pack(fill="both", expand=True)
        self.scan_output = tk.Text(output_frame, wrap="word", height=15, bg="#f7f7f7")
        self.scan_output.pack(fill="both", expand=True)
        scroll = ttk.Scrollbar(output_frame, command=self.scan_output.yview)
        self.scan_output.configure(yscrollcommand=scroll.set)

    def browse_image(self):
        """Open file dialog to select a disk image"""
        filepath = filedialog.askopenfilename(
            title="Select Disk Image",
            filetypes=[
                ("Disk Images", "*.dd *.img *.raw *.E01"),
                ("All files", "*.*")
            ],
            initialdir=os.path.expanduser("~")
        )
        if filepath:
            self.image_path_var.set(filepath)
            self.dir_path_var.set("")  # Clear directory if image selected
            self.scan_output.delete("1.0", "end")
            self.scan_output.insert("1.0", f"Image selected: {filepath}\n")

    def browse_directory(self):
        """Open directory dialog to select a folder to scan"""
        dirpath = filedialog.askdirectory(
            title="Select Directory to Scan",
            initialdir=os.path.expanduser("~")
        )
        if dirpath:
            self.dir_path_var.set(dirpath)
            self.image_path_var.set("")  # Clear image if directory selected
            self.scan_output.delete("1.0", "end")
            self.scan_output.insert("1.0", f"Directory selected: {dirpath}\n")

    def browse_output_dir(self):
        """Select output directory for scan results"""
        dirpath = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.case_dir
        )
        if dirpath:
            self.output_dir_var.set(dirpath)

    def start_scan(self):
        """Start the scanning process"""
        image_path = self.image_path_var.get().strip()
        dir_path = self.dir_path_var.get().strip()
        output_dir = self.output_dir_var.get().strip()

        # Validation
        if not image_path and not dir_path:
            messagebox.showerror("Error", "Please select either an image file or a directory to scan.")
            return

        if image_path and dir_path:
            messagebox.showerror("Error", "Please select either an image OR a directory, not both.")
            return

        if not output_dir:
            messagebox.showerror("Error", "Please specify an output directory.")
            return

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Disable scan button during scan
        self.scan_btn.config(state="disabled")
        self.scan_status_var.set("Scanning... (this may take a while)")
        self.scan_output.delete("1.0", "end")
        self.scan_output.insert("end", f"Starting scan...\n")
        self.scan_output.insert("end", f"Output directory: {output_dir}\n")
        self.scan_output.insert("end", "-" * 60 + "\n")

        def run_scan():
            try:
                if image_path:
                    # Scan image using analyze.sh
                    self.scan_output.insert("end", f"Scanning image: {image_path}\n")
                    self.scan_output.see("end")

                    analyze_script = os.path.join("scripts", "analyze.sh")
                    if not os.path.exists(analyze_script):
                        self.scan_output.insert("end", f"ERROR: Script not found: {analyze_script}\n")
                        return

                    cmd = ["bash", analyze_script, image_path, self.case_dir]
                    self.scan_output.insert("end", f"Running: {' '.join(cmd)}\n\n")
                    self.scan_output.see("end")

                    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                    for line in proc.stdout:
                        self.scan_output.insert("end", line)
                        self.scan_output.see("end")
                    proc.wait()

                    if proc.returncode == 0:
                        self.scan_output.insert("end", "\n✓ Image scan completed successfully!\n")
                        self.scan_status_var.set("Scan completed successfully")
                        log_event(self.case_dir, "info", f"Image scanned: {image_path}")
                    else:
                        self.scan_output.insert("end", f"\n✗ Scan failed with exit code {proc.returncode}\n")
                        self.scan_status_var.set("Scan failed")

                else:  # dir_path
                    # Scan directory using search.py directly
                    self.scan_output.insert("end", f"Scanning directory: {dir_path}\n")
                    self.scan_output.see("end")

                    search_script = os.path.join("tools", "modules", "search.py")
                    if not os.path.exists(search_script):
                        self.scan_output.insert("end", f"ERROR: Script not found: {search_script}\n")
                        return

                    cmd = ["python3", search_script, "--root", dir_path, "--outdir", output_dir]
                    self.scan_output.insert("end", f"Running: {' '.join(cmd)}\n\n")
                    self.scan_output.see("end")

                    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                    for line in proc.stdout:
                        self.scan_output.insert("end", line)
                        self.scan_output.see("end")
                    proc.wait()

                    if proc.returncode == 0:
                        self.scan_output.insert("end", "\n✓ Directory scan completed successfully!\n")
                        self.scan_status_var.set("Scan completed successfully")
                        log_event(self.case_dir, "info", f"Directory scanned: {dir_path}")
                    else:
                        self.scan_output.insert("end", f"\n✗ Scan failed with exit code {proc.returncode}\n")
                        self.scan_status_var.set("Scan failed")

                # Reload findings after scan
                self.load_findings()

            except Exception as e:
                self.scan_output.insert("end", f"\n✗ Error: {str(e)}\n")
                self.scan_status_var.set("Scan error")
            finally:
                self.scan_btn.config(state="normal")

        # Run scan in thread to avoid blocking GUI
        threading.Thread(target=run_scan, daemon=True).start()

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

    # Minimal implementations for missing callbacks so the GUI can start and be used for testing.
    def load_metadata(self):
        try:
            meta = report_generator.load_metadata(self.case_dir)
            self.client_var.set(meta.get('client','—'))
            self.created_var.set(meta.get('created_at','—'))
        except Exception:
            self.client_var.set('—')
            self.created_var.set('—')

    def load_findings(self):
        # Populate the treeview with masked findings
        try:
            findings = report_generator.load_masked_findings(self.case_dir, max_items=200)
            for i in self.find_tree.get_children():
                self.find_tree.delete(i)
            for f in findings:
                self.find_tree.insert('', 'end', values=(f.get('path',''), f.get('snippet',''), f.get('filesize','')))
        except Exception:
            pass

    def on_generate_owner(self):
        try:
            md = report_generator.generate_owner_report(self.case_dir, operator_name=self.op_entry.get(), client_notes=self.client_notes.get('1.0','end'))
            os.makedirs(os.path.join(self.case_dir, 'exports'), exist_ok=True)
            out = os.path.join(self.case_dir, 'exports', f'owner_report_{int(time.time())}.md')
            report_generator.export_markdown(md, out)
            self.last_report_path = out
            self.current_report_md = md
            self.preview.delete('1.0','end')
            self.preview.insert('1.0', md)
            messagebox.showinfo('Report generated', f'Owner report written to:\n{out}')
            log_event(self.case_dir, 'info', 'Owner report generated')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to generate owner report: {e}')

    def on_generate_court(self):
        try:
            md = report_generator.generate_court_report(self.case_dir, operator_name=self.op_entry.get(), detail_limit=200)
            os.makedirs(os.path.join(self.case_dir, 'exports'), exist_ok=True)
            out = os.path.join(self.case_dir, 'exports', f'court_report_{int(time.time())}.md')
            report_generator.export_markdown(md, out)
            self.last_report_path = out
            self.current_report_md = md
            self.preview.delete('1.0','end')
            self.preview.insert('1.0', md)
            messagebox.showinfo('Report generated', f'Court report written to:\n{out}')
            log_event(self.case_dir, 'info', 'Court report generated')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to generate court report: {e}')

    def on_sign_last(self):
        if not self.last_report_path or not os.path.exists(self.last_report_path):
            messagebox.showwarning('No report', 'No generated report found to sign.')
            return
        signer = self.gpg_entry.get().strip() or None
        try:
            sig_path = report_generator.sign_with_gpg(self.last_report_path, signer=signer)
            messagebox.showinfo('Signed', f'Signature created: {sig_path}')
            log_event(self.case_dir, 'info', f'Report signed: {os.path.basename(sig_path)}')
        except Exception as e:
            messagebox.showerror('GPG error', f'Failed to sign: {e}')

    def _run_script_with_output(self, cmd, title=None):
        win = ProcessOutputWindow(self, title=title or 'Command Output')
        def runner():
            try:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                for line in proc.stdout:
                    win.append(line.rstrip())
                proc.wait()
            except Exception as e:
                win.append(f'Error running command: {e}')
        threading.Thread(target=runner, daemon=True).start()

    def on_validate_case(self):
        if is_executable(VALIDATOR_SCRIPT):
            self._run_script_with_output([VALIDATOR_SCRIPT, self.case_dir], title='Validate Case')
        else:
            messagebox.showinfo('Validate', f'Validator script not executable: {VALIDATOR_SCRIPT}')

    def on_create_package(self):
        if is_executable(PACKAGE_SCRIPT):
            out = os.path.join(self.case_dir, 'legal_package.tar.gz')
            self._run_script_with_output([PACKAGE_SCRIPT, self.case_dir, out], title='Create Legal Package')
        else:
            messagebox.showinfo('Package', f'Package script not executable: {PACKAGE_SCRIPT}')

    def on_create_probate_package(self):
        if is_executable(PROBATE_SCRIPT):
            out = os.path.join(self.case_dir, 'probate_package.tar.gz')
            self._run_script_with_output([PROBATE_SCRIPT, self.case_dir, out], title='Create Probate Package')
        else:
            messagebox.showinfo('Probate', f'Probate script not executable: {PROBATE_SCRIPT}')

    def open_case(self):
        try:
            # Try to open in file manager if possible
            if shutil.which('xdg-open'):
                subprocess.Popen(['xdg-open', self.case_dir])
            else:
                messagebox.showinfo('Open case', f'Case directory: {self.case_dir}')
        except Exception:
            messagebox.showinfo('Open case', f'Case directory: {self.case_dir}')

    def tail_in_terminal(self):
        # Open a simple tail in a ProcessOutputWindow
        logf = os.path.join(self.case_dir, 'logs', 'process.log')
        win = ProcessOutputWindow(self, title='Tailing process.log')
        def tailer():
            try:
                if not os.path.exists(logf):
                    win.append('Log file not found: ' + logf)
                    return
                with open(logf, 'r', errors='ignore') as f:
                    # seek to end
                    f.seek(0, os.SEEK_END)
                    while True:
                        line = f.readline()
                        if not line:
                            time.sleep(0.5)
                            continue
                        win.append(line.rstrip())
            except Exception as e:
                win.append('Tail error: ' + str(e))
        threading.Thread(target=tailer, daemon=True).start()

    def poll(self):
        # Periodic update: reload metadata and findings
        try:
            self.load_metadata()
            self.load_findings()
        except Exception:
            pass
        self.after(2000, self.poll)

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