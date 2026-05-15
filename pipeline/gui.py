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
        tk.Label(hdr, text="Wurm Market Observatory — ferramenta de pipeline local",
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
        self._tab_merge    = ttk.Frame(nb)
        self._tab_calibrate= ttk.Frame(nb)
        self._tab_settings = ttk.Frame(nb)
        self._tab_run      = ttk.Frame(nb)

        nb.add(self._tab_corpus,    text="  Corpus  ")
        nb.add(self._tab_merge,     text="  Mesclar  ")
        nb.add(self._tab_calibrate, text="  Calibrar  ")
        nb.add(self._tab_settings,  text="  Configurações  ")
        nb.add(self._tab_run,       text="  Executar  ")

        self._build_corpus_tab(self._tab_corpus)
        self._build_merge_tab(self._tab_merge)
        self._build_calibrate_tab(self._tab_calibrate)
        self._build_settings_tab(self._tab_settings)
        self._build_run_tab(self._tab_run)

    # ── Tab 1: Corpus ────────────────────────────────────────────────────────

    def _build_corpus_tab(self, parent):
        pad = {"padx": 20}

        # File picker
        row = tk.Frame(parent, bg=C["bg"])
        row.pack(fill="x", padx=20, pady=(18, 4))
        tk.Label(row, text="Corpus restaurado (.txt)", bg=C["bg"],
                 fg=C["fg_dim"], font=FONT_SM).pack(anchor="w")

        pick_row = tk.Frame(row, bg=C["bg"])
        pick_row.pack(fill="x", pady=(4, 0))
        tk.Entry(pick_row, textvariable=self.txt_path, bg=C["bg_input"], fg=C["fg"],
                 font=FONT_MONO, insertbackground=C["fg"], relief="flat",
                 highlightthickness=1, highlightcolor=C["amber"],
                 highlightbackground=C["border"]).pack(side="left", fill="x", expand=True)
        tk.Button(pick_row, text="Procurar…", command=self._pick_file,
                  bg=C["bg_card"], fg=C["amber"], font=FONT_SM,
                  relief="flat", padx=10, cursor="hand2",
                  activebackground=C["border"], activeforeground=C["amber"]
                  ).pack(side="left", padx=(8, 0))

        # Scan button
        tk.Button(parent, text="↳  Analisar Corpus", command=self._scan_corpus,
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
            ("period",    "Período"),
            ("lines",     "Linhas de log lidas"),
            ("days",      "Dias encontrados"),
            ("coverage",  "Cobertura"),
            ("gaps",      "Gaps (falhas) detectados"),
            ("servers",   "Servidores observados"),
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
        tk.Label(parent, text="Gaps detectados:", bg=C["bg"],
                 fg=C["fg_dim"], font=FONT_SM).pack(anchor="w", padx=20)
        self._gap_text = tk.Text(parent, height=4, bg=C["bg_card"], fg=C["warn"],
                                 font=FONT_SM, relief="flat", state="disabled",
                                 highlightthickness=1, highlightbackground=C["border"])
        self._gap_text.pack(fill="x", padx=20, pady=(2, 10))

    def _pick_file(self):
        path = filedialog.askopenfilename(
            title="Selecione o corpus restaurado do Wurm",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if path:
            self.txt_path.set(path)

    # ── Tab 2: Merge ─────────────────────────────────────────────────────────

    def _build_merge_tab(self, parent):
        tk.Label(parent, text="Selecione vários arquivos .txt para mesclar em um único corpus antes da análise.",
                 bg=C["bg"], fg=C["fg_dim"], font=FONT_SM).pack(anchor="w", padx=20, pady=(16, 4))
        tk.Label(parent, text="Duplicatas por dia são removidas. Os arquivos são mesclados em ordem cronológica.",
                 bg=C["bg"], fg=C["fg_faint"], font=FONT_SM).pack(anchor="w", padx=20, pady=(0, 10))

        btn_row = tk.Frame(parent, bg=C["bg"])
        btn_row.pack(fill="x", padx=20, pady=(0, 8))
        tk.Button(btn_row, text="Adicionar Arquivos…", command=self._merge_add_files,
                  bg=C["bg_card"], fg=C["amber"], font=FONT_SM, relief="flat",
                  padx=10, cursor="hand2",
                  activebackground=C["border"]).pack(side="left")
        tk.Button(btn_row, text="Limpar Lista", command=self._merge_clear,
                  bg=C["bg_card"], fg=C["fg_dim"], font=FONT_SM, relief="flat",
                  padx=10, cursor="hand2",
                  activebackground=C["border"]).pack(side="left", padx=(6, 0))

        list_frame = tk.Frame(parent, bg=C["bg_card"],
                              highlightthickness=1, highlightbackground=C["border"])
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 8))
        self._merge_listbox = tk.Listbox(list_frame, bg=C["bg_card"], fg=C["fg"],
                                         font=FONT_SM, relief="flat", selectbackground=C["border"],
                                         activestyle="none", height=8)
        self._merge_listbox.pack(side="left", fill="both", expand=True, padx=6, pady=6)
        sb = ttk.Scrollbar(list_frame, command=self._merge_listbox.yview)
        sb.pack(side="right", fill="y")
        self._merge_listbox.configure(yscrollcommand=sb.set)

        self._merge_files = []  # list of Path

        merge_out_row = tk.Frame(parent, bg=C["bg"])
        merge_out_row.pack(fill="x", padx=20, pady=(0, 6))
        tk.Label(merge_out_row, text="Salvar arquivo mesclado como:", bg=C["bg"],
                 fg=C["fg_dim"], font=FONT_SM).pack(side="left")
        self._merge_out_var = tk.StringVar(value="")
        tk.Entry(merge_out_row, textvariable=self._merge_out_var, bg=C["bg_input"],
                 fg=C["fg"], font=FONT_MONO, insertbackground=C["fg"],
                 relief="flat", highlightthickness=1, highlightcolor=C["amber"],
                 highlightbackground=C["border"], width=36).pack(side="left", padx=(8, 6))
        tk.Button(merge_out_row, text="Procurar…", command=self._merge_pick_out,
                  bg=C["bg_card"], fg=C["amber"], font=FONT_SM,
                  relief="flat", padx=8, cursor="hand2").pack(side="left")

        tk.Button(parent, text="⊕  Mesclar e Carregar na aba Corpus",
                  command=self._merge_run,
                  bg=C["amber_dim"], fg=C["bg"],
                  font=("JetBrains Mono", 9, "bold"),
                  relief="flat", padx=14, pady=6, cursor="hand2",
                  activebackground=C["amber"]
                  ).pack(anchor="w", padx=20, pady=(0, 10))

        self._merge_status = tk.StringVar(value="")
        tk.Label(parent, textvariable=self._merge_status, bg=C["bg"],
                 fg=C["success"], font=FONT_SM).pack(anchor="w", padx=20)

    def _merge_add_files(self):
        paths = filedialog.askopenfilenames(
            title="Selecione os arquivos .txt do corpus do Wurm",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        for p in paths:
            if p not in [str(f) for f in self._merge_files]:
                self._merge_files.append(Path(p))
                self._merge_listbox.insert("end", f"  {Path(p).name}")
        if paths and not self._merge_out_var.get():
            default_out = str(Path(paths[0]).parent / "corpus_merged.txt")
            self._merge_out_var.set(default_out)

    def _merge_clear(self):
        self._merge_files.clear()
        self._merge_listbox.delete(0, "end")
        self._merge_status.set("")

    def _merge_pick_out(self):
        path = filedialog.asksaveasfilename(
            title="Salvar corpus mesclado como…",
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt")]
        )
        if path:
            self._merge_out_var.set(path)

    def _merge_run(self):
        if not self._merge_files:
            messagebox.showwarning("Nenhum arquivo", "Adicione pelo menos um arquivo .txt para mesclar.")
            return
        out_path = self._merge_out_var.get().strip()
        if not out_path:
            messagebox.showwarning("Nenhuma saída", "Escolha onde salvar o arquivo mesclado.")
            return

        self._merge_status.set("Mesclando…")
        self.status.set("Mesclando arquivos…")

        def run():
            try:
                import re
                DAY_RE = re.compile(r'^Logging started (\d{4}-\d{2}-\d{2})')
                day_lines = {}   # {date_str: set(lines)}
                day_order = []   # preserve chronological order

                for fpath in self._merge_files:
                    current_day = None
                    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                        for line in f:
                            line = line.rstrip('\n')
                            dm = DAY_RE.match(line)
                            if dm:
                                current_day = dm.group(1)
                                if current_day not in day_lines:
                                    day_lines[current_day] = set()
                                    day_order.append(current_day)
                            elif current_day and line.strip():
                                day_lines[current_day].add(line.strip())

                day_order.sort()
                output_lines = []
                for day in day_order:
                    output_lines.append(f"Logging started {day}")
                    output_lines.extend(sorted(day_lines[day]))
                    output_lines.append("")

                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(output_lines))

                n_days = len(day_order)
                n_files = len(self._merge_files)
                merged_path = out_path

                def finish():
                    self._merge_status.set(
                        f"✓ Mesclou {n_files} arquivos · {n_days} dias · salvo em {Path(merged_path).name}"
                    )
                    self.txt_path.set(merged_path)
                    self.status.set("Mesclagem concluída. Vá para a aba Corpus e clique em Analisar Corpus.")
                    messagebox.showinfo("Mesclagem concluída",
                        f"{n_files} arquivos mesclados em {n_days} dias únicos.\n"
                        f"Arquivo carregado na aba Corpus — clique em 'Analisar Corpus' para verificar.")

                self.root.after(0, finish)

            except Exception as e:
                import traceback
                err = traceback.format_exc()
                self.root.after(0, lambda: [
                    self._merge_status.set(f"Erro: {e}"),
                    messagebox.showerror("Erro na Mesclagem", err)
                ])

        threading.Thread(target=run, daemon=True).start()

    # ── Tab 3: Calibrate ─────────────────────────────────────────────────────

    def _build_calibrate_tab(self, parent):
        tk.Label(parent,
                 text="Cole algumas linhas do seu .txt real aqui para verificar se o sistema lê corretamente.",
                 bg=C["bg"], fg=C["fg_dim"], font=FONT_SM).pack(anchor="w", padx=20, pady=(16, 4))
        tk.Label(parent,
                 text="O sistema espera o formato: [HH:MM:SS] <NomeDoJogador> (NomeDoServidor) texto da mensagem",
                 bg=C["bg"], fg=C["fg_faint"], font=FONT_SM).pack(anchor="w", padx=20, pady=(0, 8))

        input_frame = tk.Frame(parent, bg=C["bg_card"],
                               highlightthickness=1, highlightbackground=C["border"])
        input_frame.pack(fill="x", padx=20, pady=(0, 8))
        self._calib_input = tk.Text(input_frame, bg=C["bg_card"], fg=C["fg"],
                                    font=("JetBrains Mono", 8), height=7,
                                    relief="flat", padx=8, pady=6,
                                    insertbackground=C["fg"])
        self._calib_input.pack(fill="x")
        self._calib_input.insert("end",
            "Logging started 2024-11-01\n"
            "[12:34:56] <Valdris> (Xanadu) WTS longsword 90ql 3s\n"
            "[12:35:10] <IronMere> (Xanadu) WTS plate set 80ql 15s\n"
        )

        tk.Button(parent, text="↳  Analisar e Inspecionar", command=self._calib_run,
                  bg=C["amber_dim"], fg=C["bg"],
                  font=("JetBrains Mono", 9, "bold"),
                  relief="flat", padx=14, pady=6, cursor="hand2",
                  activebackground=C["amber"]).pack(anchor="w", padx=20, pady=(0, 8))

        out_frame = tk.Frame(parent, bg=C["bg_card"],
                             highlightthickness=1, highlightbackground=C["border"])
        out_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self._calib_out = tk.Text(out_frame, bg=C["bg_card"], fg=C["fg"],
                                  font=("JetBrains Mono", 8), height=10,
                                  relief="flat", padx=8, pady=6,
                                  state="disabled", cursor="arrow")
        self._calib_out.pack(fill="both", expand=True)
        self._calib_out.tag_configure("ok",    foreground=C["success"])
        self._calib_out.tag_configure("warn",  foreground=C["warn"])
        self._calib_out.tag_configure("amber", foreground=C["amber"])
        self._calib_out.tag_configure("dim",   foreground=C["fg_dim"])

    def _calib_write(self, msg, tag=""):
        self._calib_out.config(state="normal")
        self._calib_out.insert("end", msg + "\n", tag)
        self._calib_out.config(state="disabled")

    def _calib_run(self):
        import re, tempfile, os
        text = self._calib_input.get("1.0", "end").strip()
        if not text:
            return

        self._calib_out.config(state="normal")
        self._calib_out.delete("1.0", "end")
        self._calib_out.config(state="disabled")

        # Write to temp file and parse
        tmp = Path(tempfile.mktemp(suffix=".txt"))
        tmp.write_text(text, encoding="utf-8")

        try:
            result = core.parse_file(str(tmp), self.config)
            tmp.unlink()

            self._calib_write("─── Resultado da Análise ───", "amber")
            self._calib_write(f"  Linhas brutas lidas: {result.total_raw_lines}", "dim")
            self._calib_write(f"  Linhas lidas OK:     {len(result.lines)}", "ok" if result.lines else "warn")
            self._calib_write(f"  Linhas ignoradas:    {result.skipped_lines}", "dim")
            self._calib_write(f"  Dias encontrados:    {len(result.days_found)}", "dim")
            self._calib_write(f"  Servidores:          {', '.join(sorted(result.servers_found)) or 'none'}", "dim")
            self._calib_write("")

            if result.lines:
                self._calib_write("─── Primeiras 5 linhas interpretadas ───", "amber")
                for line in result.lines[:5]:
                    wts_kw = [k.lower() for k in self.config.get("cleaning", {}).get("wts_keywords", ["wts"])]
                    is_wts = any(k in line.message.lower() for k in wts_kw)
                    tag = "ok" if is_wts else "dim"
                    marker = "[WTS]" if is_wts else "     "
                    self._calib_write(
                        f"  {marker} {line.day} {line.timestamp}  <{line.player}> ({line.server})", tag
                    )
                    self._calib_write(f"          {line.message[:80]}", "dim")

                if len(result.lines) > 5:
                    self._calib_write(f"  … e mais {len(result.lines)-5} linhas.", "dim")
            else:
                self._calib_write("  ⚠ Nenhuma linha interpretada. Verifique se o formato bate:", "warn")
                self._calib_write("    [HH:MM:SS] <Player> (Server) message", "warn")
                self._calib_write("", "")
                self._calib_write("  Se seus logs usam um formato diferente, cole de 5 a 10 linhas reais", "dim")
                self._calib_write("  e compartilhe para que o leitor possa ser ajustado.", "dim")

        except Exception as e:
            tmp.unlink(missing_ok=True)
            self._calib_write(f"Erro: {e}", "warn")

    def _scan_corpus(self):
        path = self.txt_path.get().strip()
        if not path or not Path(path).exists():
            messagebox.showerror("Erro", "Por favor, selecione um arquivo .txt válido primeiro.")
            return
        self.status.set("Analisando corpus…")

        def run():
            try:
                result   = core.parse_file(path, self.config)
                coverage = core.compute_coverage(result)
                self._parse_result = result
                self._coverage     = coverage
                self.root.after(0, lambda: self._update_corpus_info(result, coverage))
            except Exception as e:
                import traceback
                err = traceback.format_exc()
                self.root.after(0, lambda: [
                    self.status.set(f"Erro: {e}"),
                    messagebox.showerror("Erro na Análise", f"Erro inesperado:\n\n{err}")
                ])

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
            self._gap_text.insert("end", "  Nenhum gap detectado — cobertura total.\n")
        self._gap_text.config(state="disabled")
        self.status.set("Corpus analisado. Pronto para executar.")

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
        section("Saída")
        self._out_path_var = tk.StringVar(value=self.config.get("output_dir", "../src/data"))
        kv_row(inner, "Caminho de dados do Observatory", self._out_path_var)
        self._server_var = tk.StringVar(value=self.config.get("observatory", {}).get("server", "SFI"))
        kv_row(inner, "Servidor (SFI / NFI)", self._server_var)

        # Cleaning
        section("Regras de Limpeza")
        cl = self.config.get("cleaning", {})
        self._wts_var = tk.StringVar(value=", ".join(cl.get("wts_keywords", [])))
        self._wtb_var = tk.StringVar(value=", ".join(cl.get("wtb_keywords", [])))
        self._min_len_var = tk.StringVar(value=str(cl.get("min_message_length", 5)))
        kv_row(inner, "Palavras-chave WTS (separadas por vírgula)", self._wts_var)
        kv_row(inner, "Palavras-chave WTB (separadas por vírgula)", self._wtb_var)
        kv_row(inner, "Tamanho mínimo da mensagem", self._min_len_var)

        # Lenses toggles
        section("Lentes (Filtros) para Gerar")
        lens_cfg = self.config.get("lenses", {})
        self._seller_enabled = tk.BooleanVar(value=lens_cfg.get("seller_activity", {}).get("enabled", True))
        self._buyer_enabled  = tk.BooleanVar(value=lens_cfg.get("buyer_activity",  {}).get("enabled", False))
        self._top_n_var      = tk.StringVar(value=str(lens_cfg.get("seller_activity", {}).get("top_sellers_count", 10)))
        self._min_m_var      = tk.StringVar(value=str(lens_cfg.get("seller_activity", {}).get("min_mentions", 3)))

        for var, label in [(self._seller_enabled, "Atividade de Vendedores"), (self._buyer_enabled, "Atividade de Compradores")]:
            r = tk.Frame(inner, bg=C["bg"])
            r.pack(anchor="w", padx=24, pady=2)
            tk.Checkbutton(r, text=label, variable=var, bg=C["bg"], fg=C["fg"],
                           selectcolor=C["bg_input"], activebackground=C["bg"],
                           activeforeground=C["amber"], font=FONT_MONO).pack(side="left")

        kv_row(inner, "Top vendedores para mostrar", self._top_n_var)
        kv_row(inner, "Mínimo de menções", self._min_m_var)

        # Categories
        section("Categorias de Itens  (edite o config.json para controle total)")
        cats_text = "\n".join(f'  "{cat}": {kws}' for cat, kws in self.config.get("categories", {}).items())
        tk.Label(inner, text=cats_text, bg=C["bg_card"], fg=C["fg_dim"],
                 font=("JetBrains Mono", 8), justify="left", anchor="w",
                 padx=14, pady=10).pack(fill="x", padx=20, pady=(0, 8))

        # Save button
        tk.Button(inner, text="Salvar Configurações", command=self._save_settings,
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
        self.status.set("Configurações salvas.")
        messagebox.showinfo("Salvo", "Configurações salvas no config.json")

    # ── Tab 5: Run ───────────────────────────────────────────────────────────

    def _build_run_tab(self, parent):
        top = tk.Frame(parent, bg=C["bg"])
        top.pack(fill="x", padx=20, pady=(16, 8))

        tk.Label(top, text="Gerar arquivos JSON a partir do corpus analisado.",
                 bg=C["bg"], fg=C["fg_dim"], font=FONT_SM).pack(anchor="w")

        tk.Button(top, text="▶  Executar Pipeline", command=self._run_pipeline,
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
            messagebox.showwarning("Nenhum corpus", "Vá para a aba Corpus e analise um arquivo primeiro.")
            return

        self._log.config(state="normal")
        self._log.delete("1.0", "end")
        self._log.config(state="disabled")

        self.status.set("Executando pipeline…")

        def run():
            self._log_write("─── Pipeline Corpus Workbench ───", "amber")
            self._log_write(f"  Corpus:   {Path(self._parse_result.file_path).name}", "dim")
            self._log_write(f"  Linhas:   {len(self._parse_result.lines):,}", "dim")
            self._log_write(f"  Cobertura:{round(self._coverage.coverage_pct * 100, 1)}%", "dim")
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
            self._log_write("Gerando corpus-meta.json…", "amber")
            meta = core.build_corpus_meta(self._parse_result, self._coverage, self.config)
            meta_path = out_dir / "corpus-meta.json"
            with open(meta_path, "w", encoding="utf-8") as f:
                _json.dump(meta, f, indent=2, ensure_ascii=False)
            self._log_write(f"  ✓ corpus-meta.json gravado", "ok")
            self._log_write(f"    Período:   {meta['active']['period']}", "dim")
            self._log_write(f"    Cobertura: {round(meta['active']['coverage'] * 100, 1)}%", "dim")
            self._log_write(f"    Meses:     {len(meta['all_corpora'])}", "dim")
            self._log_write("")

            # 2. seller-activity.json
            lens_cfg = self.config.get("lenses", {})
            if lens_cfg.get("seller_activity", {}).get("enabled", True):
                self._log_write("Gerando seller-activity.json…", "amber")
                seller_data = lens_mod.process_seller_lens(
                    self._parse_result, self._coverage, self.config
                )
                seller_path = out_dir / "seller-activity.json"
                with open(seller_path, "w", encoding="utf-8") as f:
                    _json.dump(seller_data, f, indent=2, ensure_ascii=False)
                n_sellers = seller_data["summary"]["unique_sellers"]
                n_list    = seller_data["summary"]["total_listings"]
                top_cat   = seller_data["summary"]["top_category"]
                self._log_write(f"  ✓ seller-activity.json gravado", "ok")
                self._log_write(f"    Vendedores únicos:  {n_sellers}", "dim")
                self._log_write(f"    Total de menções:   {n_list:,}", "dim")
                self._log_write(f"    Top categoria:      {top_cat}", "dim")
                if seller_data["top_sellers"]:
                    self._log_write(f"    Top vendedor:       {seller_data['top_sellers'][0]['name']} "
                                    f"({seller_data['top_sellers'][0]['count']} menções)", "dim")
                self._log_write("")

            # 3. buyer-activity.json
            if lens_cfg.get("buyer_activity", {}).get("enabled", False):
                self._log_write("Gerando buyer-activity.json…", "amber")
                buyer_data = lens_mod.process_buyer_lens(
                    self._parse_result, self._coverage, self.config
                )
                buyer_path = out_dir / "buyer-activity.json"
                with open(buyer_path, "w", encoding="utf-8") as f:
                    _json.dump(buyer_data, f, indent=2, ensure_ascii=False)
                self._log_write(f"  ✓ buyer-activity.json gravado", "ok")
                self._log_write(f"    Compradores únicos:   {buyer_data['summary']['unique_buyers']}", "dim")
                self._log_write("")

            self._log_write("─── Pipeline concluído ───────────────", "amber")
            self._log_write(f"  Arquivos salvos em: {out_dir}", "ok")
            self._log_write("")
            self._log_write("  Recarregue o dev server do Observatory para ver os dados reais.", "amber")
            self.root.after(0, lambda: self.status.set("Concluído. Arquivos JSON prontos."))

        threading.Thread(target=run, daemon=True).start()

    # ── Status bar ────────────────────────────────────────────────────────────

    def _build_statusbar(self):
        bar = tk.Frame(self.root, bg=C["bg_card"],
                       highlightthickness=1, highlightbackground=C["border"])
        bar.pack(fill="x", side="bottom")
        tk.Label(bar, textvariable=self.status, bg=C["bg_card"], fg=C["fg_dim"],
                 font=FONT_SM, anchor="w", padx=12, pady=4).pack(side="left")
        tk.Label(bar, text="Sem internet · Sem banco de dados · Apenas local",
                 bg=C["bg_card"], fg=C["fg_faint"], font=FONT_SM, anchor="e", padx=12
                 ).pack(side="right")


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app  = WorkbenchApp(root)
    root.mainloop()
