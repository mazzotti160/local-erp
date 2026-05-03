import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from database.config import get_db_path, set_db_path

BG     = "#f5f5f5"
BLUE   = "#1565c0"
GREEN  = "#2e7d32"


def run_setup_if_needed():
    if get_db_path():
        return
    _show_setup_dialog()


def _show_setup_dialog():
    default_folder = os.path.join(os.path.expanduser("~"), "Documents", "lk-local-erp")

    root = tk.Tk()
    root.title("LK ERP — Configuração Inicial")
    root.geometry("580x300")
    root.resizable(False, False)
    root.configure(bg=BG)
    root.eval("tk::PlaceWindow . center")

    # Header
    header = tk.Frame(root, bg=BLUE, height=52)
    header.pack(fill="x")
    header.pack_propagate(False)
    tk.Label(
        header,
        text="  \U0001f4e6  LK ERP — Primeira Configuração",
        bg=BLUE, fg="white",
        font=("Segoe UI", 12, "bold"),
        anchor="w",
    ).pack(side="left", fill="y", padx=10)

    # Body
    body = tk.Frame(root, bg=BG, padx=28, pady=20)
    body.pack(fill="both", expand=True)

    tk.Label(
        body,
        text="Bem-vindo ao LK ERP!\nEscolha onde o banco de dados será armazenado:",
        bg=BG,
        font=("Segoe UI", 10),
        justify="left",
        anchor="w",
    ).pack(fill="x", pady=(0, 14))

    path_frame = tk.Frame(body, bg=BG)
    path_frame.pack(fill="x")

    tk.Label(path_frame, text="Pasta:", bg=BG, font=("Segoe UI", 10)).pack(side="left", padx=(0, 8))

    folder_var = tk.StringVar(value=default_folder)
    entry = ttk.Entry(path_frame, textvariable=folder_var, width=46, font=("Segoe UI", 10))
    entry.pack(side="left", padx=(0, 6))

    def browse():
        folder = filedialog.askdirectory(
            title="Selecione a pasta para o banco de dados",
            initialdir=os.path.expanduser("~"),
        )
        if folder:
            folder_var.set(folder)

    ttk.Button(path_frame, text="Procurar...", command=browse).pack(side="left")

    tk.Label(
        body,
        text="O arquivo database.db será criado dentro dessa pasta.",
        bg=BG,
        font=("Segoe UI", 8),
        foreground="#888",
    ).pack(anchor="w", pady=(6, 0))

    confirmed = [False]

    def confirm():
        folder = folder_var.get().strip()
        if not folder:
            messagebox.showerror("Erro", "Informe a pasta de destino.", parent=root)
            return
        try:
            os.makedirs(folder, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível criar a pasta:\n{e}", parent=root)
            return
        db_path = os.path.join(folder, "database.db")
        set_db_path(db_path)
        confirmed[0] = True
        root.destroy()

    def on_close():
        if not confirmed[0]:
            root.destroy()
            import sys
            sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_close)

    btn_frame = tk.Frame(body, bg=BG)
    btn_frame.pack(fill="x", pady=(18, 0))

    confirm_btn = tk.Button(
        btn_frame,
        text="  Confirmar e Abrir ERP  ",
        command=confirm,
        bg=BLUE, fg="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        padx=6, pady=4,
    )
    confirm_btn.pack(side="right")

    root.mainloop()
