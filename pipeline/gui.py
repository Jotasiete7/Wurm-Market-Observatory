"""
gui.py — Corpus Workbench GUI
A local desktop tool to process Wurm .txt logs into Observatory JSON datasets.

Run with: py -m pipeline  (from the observatory root)
      or: py pipeline/gui.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import threading
import sys
import os
from pathlib import Path

# ─── Resolve pipeline directory path ─────────────────────────────────────────
PIPELINE_DIR = Path(__file__).parent
CONFIG_PATH  = PIPELINE_DIR / "config.json"
sys.path.insert(0, str(PIPELINE_DIR))

import core
import lenses as lens_mod

# ─── Colour Palette (Dark Archive) ───────────────────────────────────────────
C = {
    "bg":        "#1a1814",
    "bg_card":   "#1f1d1a",
    "bg_input":  "#252320",
    "fg":        "#dcd3c1",
    "fg_dim":    "#8a8477",
    "fg_faint":  "#5c584f",
    "amber":     "#d4a259",
    "amber_dim": "#a87228",
    "border":    "#333029",
    "success":   "#7aad6e",
    "warn":      "#c47a3a",
    "error":     "#c46a6a",
}
FONT_MONO  = ("JetBrains Mono", 9)
FONT_TITLE = ("Georgia", 13)
FONT_SM    = ("JetBrains Mono", 8)


def load_config() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(cfg: dict):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


# ─── Main Application ─────────────────────────────────────────────────────────

class WorkbenchApp:
    def __init__(self, root: tk.Tk):
        self.root   = root
        self.config = load_config()
        self.txt_path = tk.StringVar()
        self.status   = tk.StringVar(value="Ready.")
        self._parse_result  = None
        self._coverage      = None

        root.title("Corpus Workbench — Wurm Market Observatory")
        root.configure(bg=C["bg"])
        root.minsize(760, 560)
        root.geometry("820x640")

        self._build_header()
        self._build_notebook()
        self._build_statusbar()

    # ── Header ──────────────────────────────────────────────────────────────

    def _build_header(self):
        hdr = tk.Frame(self.root, bg=C["bg"], pady=10)
        hdr.pack(fill="x", padx=20)
        tk.Label(hdr, text="◆  CORPUS WORKBENCH", bg=C["bg"], fg=C["amber"],
                 font=("JetBrains Mono", 10), anchor="w").pack(side="left")
        tk.Label(hdr, text="Wurm Market Observatory — local pipeline tool",
                 bg=C["bg"], fg=C["fg_dim"], font=FONT_SM, anchor="e").pack(side="right")
        ttk.Separator(self.root, orient="horizontal").pack(fill="x", padx=0)

    # ── Notebook (Tabs) ──────────────────────────────────────────────────────

    def _build_notebook(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook",        background=C["bg"],      borderwidth=0)
        style.configure("TNotebook.Tab",    background=C["bg_card"], foreground=C["fg_dim"],
                        font=FONT_SM, padding=[12, 5])
        style.map("TNotebook.Tab",
                  background=[("selected", C["bg"])],
                  foreground=[("selected", C["amber"])])
        style.configure("TFrame",           background=C["bg"])
        style.configure("TSeparator",       background=C["border"])
        style.configure("TEntry",           fieldbackground=C["bg_input"], foreground=C["fg"],
                        insertcolor=C["fg"], bordercolor=C["border"])
        style.configure("TCombobox",        fieldbackground=C["bg_input"], foreground=C["fg"])

        nb = ttk.Notebook(self.root)
        nb.pack(fill="both", expand=True, padx=0, pady=0)

        self._tab_corpus   = ttk.Frame(nb)
        self._tab_settings = ttk.Frame(nb)
        self._tab_run      = ttk.Frame(nb)

        nb.add(self._tab_corpus,   text="  Corpus  ")
        nb.add(self._tab_settings, text="  Settings  ")
        nb.add(self._tab_run,      text="  Run  ")

        self._build_corpus_tab(self._tab_corpus)
        self._build_settings_tab(self._tab_settings)
        self._build_run_tab(self._tab_run)

    # ── Tab 1: Corpus ────────────────────────────────────────────────────────

    def _build_corpus_tab(self, parent):
        pad = {"padx": 20}

        # File picker
        row = tk.Frame(parent, bg=C["bg"])
        row.pack(fill="x", padx=20, pady=(18, 4))
        tk.Label(row, text="Restored corpus (.txt)", bg=C["bg"],
                 fg=C["fg_dim"], font=FONT_SM).pack(anchor="w")

        pick_row = tk.Frame(row, bg=C["bg"])
        pick_row.pack(fill="x", pady=(4, 0))
        tk.Entry(pick_row, textvariable=self.txt_path, bg=C["bg_input"], fg=C["fg"],
                 font=FONT_MONO, insertbackground=C["fg"], relief="flat",
                 highlightthickness=1, highlightcolor=C["amber"],
                 highlightbackground=C["border"]).pack(side="left", fill="x", expand=True)
        tk.Button(pick_row, text="Browse…", command=self._pick_file,
                  bg=C["bg_card"], fg=C["amber"], font=FONT_SM,
                  relief="flat", padx=10, cursor="hand2",
                  activebackground=C["border"], activeforeground=C["amber"]
                  ).pack(side="left", padx=(8, 0))

        # Scan button
        tk.Button(parent, text="↳  Scan Corpus", command=self._scan_corpus,
                  bg=C["amber_dim"], fg=C["bg"], font=("JetBrains Mono", 9, "bold"),
                  relief="flat", padx=14, pady=6, cursor="hand2",
                  activebackground=C["amber"], activeforeground=C["bg"]
                  ).pack(anchor="w", **pad, pady=(2, 12))

        # Info panel (shows after scan)
        self._info_frame = tk.Frame(parent, bg=C["bg_card"],
                                    highlightthickness=1, highlightbackground=C["border"])
        self._info_frame.pack(fill="x", **pad, pady=(0, 10))
        self._info_vars = {}
        fields = [
            ("period",    "Period"),
            ("lines",     "Log lines parsed"),
            ("days",      "Days found"),
            ("coverage",  "Coverage"),
            ("gaps",      "Gaps detected"),
            ("servers",   "Servers observed"),
        ]
        for i, (key, label) in enumerate(fields):
            r = tk.Frame(self._info_frame, bg=C["bg_card"])
            r.pack(fill="x", padx=14, pady=3)
            tk.Label(r, text=label, bg=C["bg_card"], fg=C["fg_dim"],
                     font=FONT_SM, width=22, anchor="w").pack(side="left")
            var = tk.StringVar(value="—")
            self._info_vars[key] = var
            tk.Label(r, textvariable=var, bg=C["bg_card"], fg=C["fg"],
                     font=FONT_MONO, anchor="w").pack(side="left")

        # Gap list
        tk.Label(parent, text="Detected gaps:", bg=C["bg"],
                 fg=C["fg_dim"], font=FONT_SM).pack(anchor="w", padx=20)
        self._gap_text = tk.Text(parent, height=4, bg=C["bg_card"], fg=C["warn"],
                                 font=FONT_SM, relief="flat", state="disabled",
                                 highlightthickness=1, highlightbackground=C["border"])
        self._gap_text.pack(fill="x", padx=20, pady=(2, 10))

    def _pick_file(self):
        path = filedialog.askopenfilename(
            title="Select restored Wurm corpus",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if path:
            self.txt_path.set(path)

    def _scan_corpus(self):
        path = self.txt_path.get().strip()
        if not path or not Path(path).exists():
            messagebox.showerror("Error", "Please select a valid .txt file first.")
            return
        self.status.set("Scanning corpus…")

        def run():
            result   = core.parse_file(path, self.config)
            coverage = core.compute_coverage(result)
            self._parse_result = result
            self._coverage     = coverage
            self.root.after(0, lambda: self._update_corpus_info(result, coverage))

        threading.Thread(target=run, daemon=True).start()

    def _update_corpus_info(self, result, cov):
        def pct(v): return f"{round(v * 100, 1)}%"
        self._info_vars["period"].set(
            core._period_label(result.period_start, result.period_end)
        )
        self._info_vars["lines"].set(f"{len(result.lines):,}  (skipped: {result.skipped_lines:,})")
        self._info_vars["days"].set(f"{len(cov.days_found)} of {len(cov.days_expected)}")
        self._info_vars["coverage"].set(pct(cov.coverage_pct))
        self._info_vars["gaps"].set(str(len(cov.gaps)))
        self._info_vars["servers"].set(", ".join(sorted(result.servers_found)) or "—")

        self._gap_text.config(state="normal")
        self._gap_text.delete("1.0", "end")
        if cov.gaps:
            for g in cov.gaps:
                self._gap_text.insert("end", f"  ▲ {g['label']}  ({g['start']} → {g['end']})\n")
        else:
            self._gap_text.insert("end", "  No gaps detected — full coverage.\n")
        self._gap_text.config(state="disabled")
        self.status.set("Corpus scanned. Ready to run.")

    # ── Tab 2: Settings ──────────────────────────────────────────────────────

    def _build_settings_tab(self, parent):
        canvas = tk.Canvas(parent, bg=C["bg"], highlightthickness=0)
        scroll = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=C["bg"])
        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        def section(title):
            tk.Label(inner, text=title, bg=C["bg"], fg=C["amber"],
                     font=("JetBrains Mono", 9, "bold")).pack(anchor="w", padx=20, pady=(16, 4))
            ttk.Separator(inner, orient="horizontal").pack(fill="x", padx=20, pady=(0, 8))

        def kv_row(parent_frame, label, var):
            r = tk.Frame(parent_frame, bg=C["bg"])
            r.pack(fill="x", padx=24, pady=2)
            tk.Label(r, text=label, bg=C["bg"], fg=C["fg_dim"],
                     font=FONT_SM, width=26, anchor="w").pack(side="left")
            tk.Entry(r, textvariable=var, bg=C["bg_input"], fg=C["fg"],
                     font=FONT_MONO, insertbackground=C["fg"], relief="flat",
                     highlightthickness=1, highlightcolor=C["amber"],
                     highlightbackground=C["border"], width=46).pack(side="left")

        # Output path
        section("Output")
        self._out_path_var = tk.StringVar(value=self.config.get("output_dir", "../src/data"))
        kv_row(inner, "Observatory data path", self._out_path_var)
        self._server_var = tk.StringVar(value=self.config.get("observatory", {}).get("server", "SFI"))
        kv_row(inner, "Server (SFI / NFI)", self._server_var)

        # Cleaning
        section("Cleaning Rules")
        cl = self.config.get("cleaning", {})
        self._wts_var = tk.StringVar(value=", ".join(cl.get("wts_keywords", [])))
        self._wtb_var = tk.StringVar(value=", ".join(cl.get("wtb_keywords", [])))
        self._min_len_var = tk.StringVar(value=str(cl.get("min_message_length", 5)))
        kv_row(inner, "WTS keywords (comma-separated)", self._wts_var)
        kv_row(inner, "WTB keywords (comma-separated)", self._wtb_var)
        kv_row(inner, "Min message length", self._min_len_var)

        # Lenses toggles
        section("Lenses to Generate")
        lens_cfg = self.config.get("lenses", {})
        self._seller_enabled = tk.BooleanVar(value=lens_cfg.get("seller_activity", {}).get("enabled", True))
        self._buyer_enabled  = tk.BooleanVar(value=lens_cfg.get("buyer_activity",  {}).get("enabled", False))
        self._top_n_var      = tk.StringVar(value=str(lens_cfg.get("seller_activity", {}).get("top_sellers_count", 10)))
        self._min_m_var      = tk.StringVar(value=str(lens_cfg.get("seller_activity", {}).get("min_mentions", 3)))

        for var, label in [(self._seller_enabled, "Seller Activity"), (self._buyer_enabled, "Buyer Activity")]:
            r = tk.Frame(inner, bg=C["bg"])
            r.pack(anchor="w", padx=24, pady=2)
            tk.Checkbutton(r, text=label, variable=var, bg=C["bg"], fg=C["fg"],
                           selectcolor=C["bg_input"], activebackground=C["bg"],
                           activeforeground=C["amber"], font=FONT_MONO).pack(side="left")

        kv_row(inner, "Top sellers to show", self._top_n_var)
        kv_row(inner, "Minimum mentions", self._min_m_var)

        # Categories
        section("Item Categories  (edit config.json for full control)")
        cats_text = "\n".join(f'  "{cat}": {kws}' for cat, kws in self.config.get("categories", {}).items())
        tk.Label(inner, text=cats_text, bg=C["bg_card"], fg=C["fg_dim"],
                 font=("JetBrains Mono", 8), justify="left", anchor="w",
                 padx=14, pady=10).pack(fill="x", padx=20, pady=(0, 8))

        # Save button
        tk.Button(inner, text="Save Settings", command=self._save_settings,
                  bg=C["amber_dim"], fg=C["bg"], font=("JetBrains Mono", 9, "bold"),
                  relief="flat", padx=12, pady=5, cursor="hand2",
                  activebackground=C["amber"]).pack(anchor="w", padx=20, pady=12)

    def _save_settings(self):
        cfg = self.config
        cfg["output_dir"] = self._out_path_var.get().strip()
        cfg.setdefault("observatory", {})["server"] = self._server_var.get().strip()
        cfg.setdefault("cleaning", {})["wts_keywords"] = [k.strip() for k in self._wts_var.get().split(",") if k.strip()]
        cfg.setdefault("cleaning", {})["wtb_keywords"] = [k.strip() for k in self._wtb_var.get().split(",") if k.strip()]
        try:
            cfg["cleaning"]["min_message_length"] = int(self._min_len_var.get())
        except ValueError:
            pass
        cfg.setdefault("lenses", {}).setdefault("seller_activity", {})["enabled"]           = self._seller_enabled.get()
        cfg["lenses"].setdefault("buyer_activity",  {})["enabled"]                           = self._buyer_enabled.get()
        try:
            cfg["lenses"]["seller_activity"]["top_sellers_count"] = int(self._top_n_var.get())
            cfg["lenses"]["seller_activity"]["min_mentions"]       = int(self._min_m_var.get())
        except ValueError:
            pass
        save_config(cfg)
        self.status.set("Settings saved.")
        messagebox.showinfo("Saved", "Settings saved to config.json")

    # ── Tab 3: Run ───────────────────────────────────────────────────────────

    def _build_run_tab(self, parent):
        top = tk.Frame(parent, bg=C["bg"])
        top.pack(fill="x", padx=20, pady=(16, 8))

        tk.Label(top, text="Generate JSON datasets from scanned corpus.",
                 bg=C["bg"], fg=C["fg_dim"], font=FONT_SM).pack(anchor="w")

        tk.Button(top, text="▶  Run Pipeline", command=self._run_pipeline,
                  bg=C["amber_dim"], fg=C["bg"],
                  font=("JetBrains Mono", 11, "bold"),
                  relief="flat", padx=20, pady=10, cursor="hand2",
                  activebackground=C["amber"], activeforeground=C["bg"]
                  ).pack(anchor="w", pady=(10, 0))

        tk.Label(parent, text="Log:", bg=C["bg"], fg=C["fg_dim"],
                 font=FONT_SM).pack(anchor="w", padx=20, pady=(8, 2))

        log_frame = tk.Frame(parent, bg=C["bg_card"],
                             highlightthickness=1, highlightbackground=C["border"])
        log_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self._log = tk.Text(log_frame, bg=C["bg_card"], fg=C["fg"],
                            font=("JetBrains Mono", 8),
                            state="disabled", relief="flat", padx=10, pady=8,
                            wrap="word", cursor="arrow")
        self._log.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(log_frame, command=self._log.yview)
        sb.pack(side="right", fill="y")
        self._log.configure(yscrollcommand=sb.set)

        # Color tags
        self._log.tag_configure("ok",    foreground=C["success"])
        self._log.tag_configure("warn",  foreground=C["warn"])
        self._log.tag_configure("error", foreground=C["error"])
        self._log.tag_configure("dim",   foreground=C["fg_dim"])
        self._log.tag_configure("amber", foreground=C["amber"])

    def _log_write(self, msg: str, tag: str = ""):
        self._log.config(state="normal")
        self._log.insert("end", msg + "\n", tag)
        self._log.see("end")
        self._log.config(state="disabled")

    def _run_pipeline(self):
        if not self._parse_result:
            messagebox.showwarning("No corpus", "Go to the Corpus tab and scan a file first.")
            return

        self._log.config(state="normal")
        self._log.delete("1.0", "end")
        self._log.config(state="disabled")

        self.status.set("Running pipeline…")

        def run():
            self._log_write("─── Corpus Workbench Pipeline ───", "amber")
            self._log_write(f"  Corpus:   {Path(self._parse_result.file_path).name}", "dim")
            self._log_write(f"  Lines:    {len(self._parse_result.lines):,}", "dim")
            self._log_write(f"  Coverage: {round(self._coverage.coverage_pct * 100, 1)}%", "dim")
            self._log_write(f"  Gaps:     {len(self._coverage.gaps)}", "dim")
            self._log_write("")

            # Resolve output directory
            out_dir_raw = self.config.get("output_dir", "../src/data")
            out_dir = Path(PIPELINE_DIR) / out_dir_raw
            out_dir = out_dir.resolve()
            out_dir.mkdir(parents=True, exist_ok=True)

            self._log_write(f"Output → {out_dir}", "dim")
            self._log_write("")

            import json as _json
            from datetime import datetime

            # 1. corpus-meta.json
            self._log_write("Generating corpus-meta.json…", "amber")
            meta = core.build_corpus_meta(self._parse_result, self._coverage, self.config)
            meta_path = out_dir / "corpus-meta.json"
            with open(meta_path, "w", encoding="utf-8") as f:
                _json.dump(meta, f, indent=2, ensure_ascii=False)
            self._log_write(f"  ✓ corpus-meta.json written", "ok")
            self._log_write(f"    Period:   {meta['active']['period']}", "dim")
            self._log_write(f"    Coverage: {round(meta['active']['coverage'] * 100, 1)}%", "dim")
            self._log_write(f"    Months:   {len(meta['all_corpora'])}", "dim")
            self._log_write("")

            # 2. seller-activity.json
            lens_cfg = self.config.get("lenses", {})
            if lens_cfg.get("seller_activity", {}).get("enabled", True):
                self._log_write("Generating seller-activity.json…", "amber")
                seller_data = lens_mod.process_seller_lens(
                    self._parse_result, self._coverage, self.config
                )
                seller_path = out_dir / "seller-activity.json"
                with open(seller_path, "w", encoding="utf-8") as f:
                    _json.dump(seller_data, f, indent=2, ensure_ascii=False)
                n_sellers = seller_data["summary"]["unique_sellers"]
                n_list    = seller_data["summary"]["total_listings"]
                top_cat   = seller_data["summary"]["top_category"]
                self._log_write(f"  ✓ seller-activity.json written", "ok")
                self._log_write(f"    Unique sellers:  {n_sellers}", "dim")
                self._log_write(f"    Total mentions:  {n_list:,}", "dim")
                self._log_write(f"    Top category:    {top_cat}", "dim")
                if seller_data["top_sellers"]:
                    self._log_write(f"    Top seller:      {seller_data['top_sellers'][0]['name']} "
                                    f"({seller_data['top_sellers'][0]['count']} mentions)", "dim")
                self._log_write("")

            # 3. buyer-activity.json
            if lens_cfg.get("buyer_activity", {}).get("enabled", False):
                self._log_write("Generating buyer-activity.json…", "amber")
                buyer_data = lens_mod.process_buyer_lens(
                    self._parse_result, self._coverage, self.config
                )
                buyer_path = out_dir / "buyer-activity.json"
                with open(buyer_path, "w", encoding="utf-8") as f:
                    _json.dump(buyer_data, f, indent=2, ensure_ascii=False)
                self._log_write(f"  ✓ buyer-activity.json written", "ok")
                self._log_write(f"    Unique buyers:   {buyer_data['summary']['unique_buyers']}", "dim")
                self._log_write("")

            self._log_write("─── Pipeline complete ───────────────", "amber")
            self._log_write(f"  Files written to: {out_dir}", "ok")
            self._log_write("")
            self._log_write("  Reload your Observatory dev server to see real data.", "amber")
            self.root.after(0, lambda: self.status.set("Done. JSON datasets ready."))

        threading.Thread(target=run, daemon=True).start()

    # ── Status bar ────────────────────────────────────────────────────────────

    def _build_statusbar(self):
        bar = tk.Frame(self.root, bg=C["bg_card"],
                       highlightthickness=1, highlightbackground=C["border"])
        bar.pack(fill="x", side="bottom")
        tk.Label(bar, textvariable=self.status, bg=C["bg_card"], fg=C["fg_dim"],
                 font=FONT_SM, anchor="w", padx=12, pady=4).pack(side="left")
        tk.Label(bar, text="No network · No database · Local only",
                 bg=C["bg_card"], fg=C["fg_faint"], font=FONT_SM, anchor="e", padx=12
                 ).pack(side="right")


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app  = WorkbenchApp(root)
    root.mainloop()
