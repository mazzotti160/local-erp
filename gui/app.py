import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta

from models import ingredient as ing_model
from models import product as prod_model
from models import composition as comp_model
from models import sale as sale_model
from models import cash_flow as cf_model

FONT_TITLE  = ("Segoe UI", 11, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_LABEL  = ("Segoe UI", 9)
FONT_BIG    = ("Segoe UI", 13, "bold")
BG          = "#f5f5f5"
GREEN       = "#2e7d32"
RED         = "#c62828"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Local ERP — Gestão de Negócios")
        self.geometry("1020x660")
        self.minsize(860, 540)
        self.configure(bg=BG)
        self._apply_style()
        self._build_header()
        self._build_notebook()

    # ─── STYLE ───────────────────────────────────────────────────────────────
    def _apply_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook",          background=BG, borderwidth=0)
        style.configure("TNotebook.Tab",      font=FONT_NORMAL, padding=(14, 6))
        style.map("TNotebook.Tab",            background=[("selected", "#ffffff"), ("!selected", "#dde4ea")])
        style.configure("TFrame",             background=BG)
        style.configure("TLabel",             background=BG, font=FONT_NORMAL)
        style.configure("TLabelframe",        background=BG)
        style.configure("TLabelframe.Label",  background=BG, font=("Segoe UI", 9, "bold"), foreground="#555")
        style.configure("TButton",            font=FONT_NORMAL, padding=(10, 4))
        style.configure("TEntry",             font=FONT_NORMAL)
        style.configure("Treeview",           font=FONT_NORMAL, rowheight=26)
        style.configure("Treeview.Heading",   font=("Segoe UI", 9, "bold"))
        style.map("Treeview",                 background=[("selected", "#bbdefb")])
        style.configure("Card.TFrame",        background="#ffffff", relief="solid", borderwidth=1)
        style.configure("Card.TLabel",        background="#ffffff", font=FONT_NORMAL)
        style.configure("CardTitle.TLabel",   background="#ffffff", font=("Segoe UI", 9), foreground="#666")
        style.configure("CardValue.TLabel",   background="#ffffff", font=FONT_BIG)

    # ─── HEADER ──────────────────────────────────────────────────────────────
    def _build_header(self):
        bar = tk.Frame(self, bg="#1565c0", height=48)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        tk.Label(
            bar,
            text="  \U0001f4e6  Local ERP — Gestão de Negócios",
            bg="#1565c0", fg="white",
            font=("Segoe UI", 12, "bold"),
            anchor="w",
        ).pack(side="left", fill="y", padx=8)
        today_str = date.today().strftime("%d/%m/%Y")
        tk.Label(bar, text=today_str, bg="#1565c0", fg="#90caf9",
                 font=("Segoe UI", 10)).pack(side="right", padx=16)

    # ─── NOTEBOOK ────────────────────────────────────────────────────────────
    def _build_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(6, 10))

        self.tab_sales  = ttk.Frame(self.notebook)
        self.tab_cash   = ttk.Frame(self.notebook)
        self.tab_ing    = ttk.Frame(self.notebook)
        self.tab_prod   = ttk.Frame(self.notebook)
        self.tab_comp   = ttk.Frame(self.notebook)
        self.tab_res    = ttk.Frame(self.notebook)
        self.tab_report = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_sales,  text="  Vendas  ")
        self.notebook.add(self.tab_cash,   text="  Caixa  ")
        self.notebook.add(self.tab_ing,    text="  Insumos  ")
        self.notebook.add(self.tab_prod,   text="  Produtos  ")
        self.notebook.add(self.tab_comp,   text="  Composição  ")
        self.notebook.add(self.tab_res,    text="  Custos  ")
        self.notebook.add(self.tab_report, text="  Relatórios  ")

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

        self._build_sales_tab()
        self._build_cash_tab()
        self._build_ingredients_tab()
        self._build_products_tab()
        self._build_composition_tab()
        self._build_results_tab()
        self._build_reports_tab()

    def _on_tab_change(self, event):
        idx = event.widget.index("current")
        if idx == 0:
            self._refresh_sales_combo()
            self._refresh_sales_list()
        elif idx == 1:
            self._refresh_cash_list()
        elif idx == 4:
            self._refresh_comp_combos()
        elif idx == 5:
            self._refresh_results()

    # ─── TOAST ───────────────────────────────────────────────────────────────
    def _toast(self, msg: str, error: bool = False):
        color = RED if error else GREEN
        lbl = tk.Label(self, text=f"  {'✖' if error else '✔'}  {msg}  ",
                       bg=color, fg="white", font=("Segoe UI", 9, "bold"),
                       relief="flat", bd=0)
        lbl.place(relx=0.5, rely=0.97, anchor="center")
        self.after(2800, lbl.destroy)

    # ─── CARD HELPER ─────────────────────────────────────────────────────────
    def _card(self, parent, title: str, value: str, fg: str = "#1565c0"):
        f = ttk.Frame(parent, style="Card.TFrame", padding=(14, 8))
        ttk.Label(f, text=title, style="CardTitle.TLabel").pack(anchor="w")
        lbl = ttk.Label(f, text=value, style="CardValue.TLabel", foreground=fg)
        lbl.pack(anchor="w")
        return f, lbl

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 0 — VENDAS
    # ═══════════════════════════════════════════════════════════════════════
    def _build_sales_tab(self):
        tab = self.tab_sales

        form = ttk.LabelFrame(tab, text="Registrar Venda", padding=(12, 8))
        form.pack(fill="x", padx=14, pady=(10, 4))

        ttk.Label(form, text="Produto:").grid(row=0, column=0, sticky="w", padx=(0, 4))
        self._sale_prod_var = tk.StringVar()
        self.sale_prod_combo = ttk.Combobox(form, textvariable=self._sale_prod_var, width=30, state="readonly")
        self.sale_prod_combo.grid(row=0, column=1, padx=4)
        self.sale_prod_combo.bind("<<ComboboxSelected>>", lambda _: self._update_sale_preview())

        ttk.Label(form, text="Quantidade:").grid(row=0, column=2, sticky="w", padx=(14, 4))
        self.sale_qty = ttk.Entry(form, width=10)
        self.sale_qty.grid(row=0, column=3, padx=4)
        self.sale_qty.bind("<KeyRelease>", lambda _: self._update_sale_preview())

        self._sale_preview_lbl = ttk.Label(form, text="Total: R$ 0,00", font=FONT_TITLE, foreground="#1565c0")
        self._sale_preview_lbl.grid(row=0, column=4, padx=(18, 4))

        ttk.Button(form, text="Registrar Venda", command=self._add_sale).grid(row=0, column=5, padx=(14, 0))

        # cards
        cards_frame = ttk.Frame(tab)
        cards_frame.pack(fill="x", padx=14, pady=(6, 4))
        _, self._sales_total_lbl = self._card(cards_frame, "Total Vendido Hoje", "R$ 0,00", "#2e7d32")
        self._sales_total_lbl.master.pack(side="left", padx=(0, 10))
        _, self._sales_count_lbl = self._card(cards_frame, "Vendas Hoje", "0", "#1565c0")
        self._sales_count_lbl.master.pack(side="left")

        # list
        lf = ttk.LabelFrame(tab, text="Vendas de Hoje", padding=(10, 6))
        lf.pack(fill="both", expand=True, padx=14, pady=4)

        cols = ("ID", "Produto", "Qtd", "Total (R$)")
        self.sales_tree = ttk.Treeview(lf, columns=cols, show="headings", selectmode="browse")
        self.sales_tree.heading("ID",         text="ID")
        self.sales_tree.heading("Produto",    text="Produto")
        self.sales_tree.heading("Qtd",        text="Qtd")
        self.sales_tree.heading("Total (R$)", text="Total (R$)")
        self.sales_tree.column("ID",          width=55,  anchor="center", stretch=False)
        self.sales_tree.column("Produto",     width=300)
        self.sales_tree.column("Qtd",         width=90,  anchor="center")
        self.sales_tree.column("Total (R$)",  width=140, anchor="center")

        vsb = ttk.Scrollbar(lf, orient="vertical", command=self.sales_tree.yview)
        self.sales_tree.configure(yscrollcommand=vsb.set)
        self.sales_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        ttk.Button(tab, text="Remover Selecionado", command=self._delete_sale).pack(pady=(4, 8))

        self._sale_prod_map: dict = {}
        self._refresh_sales_combo()
        self._refresh_sales_list()

    def _refresh_sales_combo(self):
        products = prod_model.get_all()
        self._sale_prod_map = {f"{p['name']}  —  R$ {p['sale_price']:.2f}": p for p in products}
        self.sale_prod_combo["values"] = list(self._sale_prod_map.keys())
        if self._sale_prod_var.get() not in self._sale_prod_map:
            self._sale_prod_var.set("")

    def _update_sale_preview(self):
        key = self._sale_prod_var.get()
        qty_str = self.sale_qty.get().strip().replace(",", ".")
        try:
            qty = float(qty_str) if qty_str else 0.0
            price = self._sale_prod_map[key]["sale_price"] if key else 0.0
            total = qty * price
            self._sale_preview_lbl.config(text=f"Total: R$ {total:.2f}")
        except (ValueError, KeyError):
            self._sale_preview_lbl.config(text="Total: R$ 0,00")

    def _add_sale(self):
        key = self._sale_prod_var.get()
        qty_str = self.sale_qty.get().strip().replace(",", ".")
        if not key:
            self._toast("Selecione um produto.", error=True)
            return
        try:
            qty = float(qty_str)
            if qty <= 0:
                raise ValueError
        except ValueError:
            self._toast("Quantidade inválida.", error=True)
            return
        prod = self._sale_prod_map[key]
        total = qty * prod["sale_price"]
        sale_model.add(prod["id"], qty, total)
        self.sale_qty.delete(0, "end")
        self._sale_preview_lbl.config(text="Total: R$ 0,00")
        self._refresh_sales_list()
        self._toast(f"Venda registrada — R$ {total:.2f}")

    def _delete_sale(self):
        sel = self.sales_tree.selection()
        if not sel:
            self._toast("Selecione uma venda para remover.", error=True)
            return
        iid = self.sales_tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirmar", "Remover esta venda?"):
            sale_model.delete(iid)
            self._refresh_sales_list()

    def _refresh_sales_list(self):
        self.sales_tree.delete(*self.sales_tree.get_children())
        rows = sale_model.get_today()
        for row in rows:
            self.sales_tree.insert("", "end", values=(
                row["id"], row["name"],
                f"{row['quantity']:.2f}".rstrip("0").rstrip("."),
                f"R$ {row['total_price']:.2f}",
            ))
        total = sale_model.get_total_today()
        self._sales_total_lbl.config(text=f"R$ {total:.2f}")
        self._sales_count_lbl.config(text=str(len(rows)))

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 1 — CAIXA
    # ═══════════════════════════════════════════════════════════════════════
    def _build_cash_tab(self):
        tab = self.tab_cash

        form = ttk.LabelFrame(tab, text="Lançamento no Caixa", padding=(12, 8))
        form.pack(fill="x", padx=14, pady=(10, 4))

        ttk.Label(form, text="Tipo:").grid(row=0, column=0, sticky="w", padx=(0, 4))
        self._cf_type_var = tk.StringVar(value="entrada")
        ttk.Radiobutton(form, text="Entrada", variable=self._cf_type_var, value="entrada").grid(row=0, column=1, padx=4)
        ttk.Radiobutton(form, text="Saída",   variable=self._cf_type_var, value="saida").grid(row=0, column=2, padx=4)

        ttk.Label(form, text="Descrição:").grid(row=0, column=3, sticky="w", padx=(14, 4))
        self.cf_desc = ttk.Entry(form, width=28)
        self.cf_desc.grid(row=0, column=4, padx=4)

        ttk.Label(form, text="Valor (R$):").grid(row=0, column=5, sticky="w", padx=(14, 4))
        self.cf_value = ttk.Entry(form, width=12)
        self.cf_value.grid(row=0, column=6, padx=4)

        ttk.Button(form, text="Lançar", command=self._add_cash_entry).grid(row=0, column=7, padx=(14, 0))

        # cards
        cards_frame = ttk.Frame(tab)
        cards_frame.pack(fill="x", padx=14, pady=(6, 4))
        _, self._cf_entrada_lbl = self._card(cards_frame, "Entradas Hoje", "R$ 0,00", "#2e7d32")
        self._cf_entrada_lbl.master.pack(side="left", padx=(0, 10))
        _, self._cf_saida_lbl = self._card(cards_frame, "Saídas Hoje", "R$ 0,00", "#c62828")
        self._cf_saida_lbl.master.pack(side="left", padx=(0, 10))
        _, self._cf_saldo_lbl = self._card(cards_frame, "Saldo Hoje", "R$ 0,00", "#1565c0")
        self._cf_saldo_lbl.master.pack(side="left")

        # list
        lf = ttk.LabelFrame(tab, text="Lançamentos de Hoje", padding=(10, 6))
        lf.pack(fill="both", expand=True, padx=14, pady=4)

        cols = ("ID", "Tipo", "Descrição", "Valor (R$)")
        self.cf_tree = ttk.Treeview(lf, columns=cols, show="headings", selectmode="browse")
        self.cf_tree.heading("ID",          text="ID")
        self.cf_tree.heading("Tipo",        text="Tipo")
        self.cf_tree.heading("Descrição",   text="Descrição")
        self.cf_tree.heading("Valor (R$)",  text="Valor (R$)")
        self.cf_tree.column("ID",           width=55,  anchor="center", stretch=False)
        self.cf_tree.column("Tipo",         width=100, anchor="center")
        self.cf_tree.column("Descrição",    width=360)
        self.cf_tree.column("Valor (R$)",   width=140, anchor="center")

        self.cf_tree.tag_configure("entrada", foreground="#1b5e20")
        self.cf_tree.tag_configure("saida",   foreground="#b71c1c")

        vsb = ttk.Scrollbar(lf, orient="vertical", command=self.cf_tree.yview)
        self.cf_tree.configure(yscrollcommand=vsb.set)
        self.cf_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        ttk.Button(tab, text="Remover Selecionado", command=self._delete_cash_entry).pack(pady=(4, 8))
        self._refresh_cash_list()

    def _add_cash_entry(self):
        type_  = self._cf_type_var.get()
        desc   = self.cf_desc.get().strip()
        val_str = self.cf_value.get().strip().replace(",", ".")
        if not desc:
            self._toast("Informe uma descrição.", error=True)
            return
        try:
            value = float(val_str)
            if value <= 0:
                raise ValueError
        except ValueError:
            self._toast("Valor inválido.", error=True)
            return
        cf_model.add(type_, desc, value)
        self.cf_desc.delete(0, "end")
        self.cf_value.delete(0, "end")
        self._refresh_cash_list()
        label = "Entrada" if type_ == "entrada" else "Saída"
        self._toast(f"{label} de R$ {value:.2f} registrada!")

    def _delete_cash_entry(self):
        sel = self.cf_tree.selection()
        if not sel:
            self._toast("Selecione um lançamento para remover.", error=True)
            return
        iid = self.cf_tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirmar", "Remover este lançamento?"):
            cf_model.delete(iid)
            self._refresh_cash_list()

    def _refresh_cash_list(self):
        self.cf_tree.delete(*self.cf_tree.get_children())
        for row in cf_model.get_today():
            label = "Entrada" if row["type"] == "entrada" else "Saída"
            self.cf_tree.insert("", "end", values=(
                row["id"], label, row["description"], f"R$ {row['value']:.2f}",
            ), tags=(row["type"],))
        s = cf_model.get_summary_today()
        saldo = s["entradas"] - s["saidas"]
        self._cf_entrada_lbl.config(text=f"R$ {s['entradas']:.2f}")
        self._cf_saida_lbl.config(text=f"R$ {s['saidas']:.2f}")
        self._cf_saldo_lbl.config(
            text=f"R$ {saldo:.2f}",
            foreground=("#2e7d32" if saldo >= 0 else "#c62828"),
        )

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 2 — INSUMOS
    # ═══════════════════════════════════════════════════════════════════════
    def _build_ingredients_tab(self):
        tab = self.tab_ing

        form = ttk.LabelFrame(tab, text="Novo Insumo", padding=(12, 8))
        form.pack(fill="x", padx=14, pady=(10, 4))

        ttk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w", padx=(0, 4))
        self.ing_name = ttk.Entry(form, width=26)
        self.ing_name.grid(row=0, column=1, padx=4)

        ttk.Label(form, text="Custo por Unidade (R$):").grid(row=0, column=2, sticky="w", padx=(12, 4))
        self.ing_cost = ttk.Entry(form, width=12)
        self.ing_cost.grid(row=0, column=3, padx=4)

        ttk.Label(form, text="Unidade:").grid(row=0, column=4, sticky="w", padx=(12, 4))
        self.ing_unit = ttk.Combobox(
            form,
            values=["unidade", "kg", "g", "litro", "ml", "caixa", "pacote", "metro", "cm"],
            width=10,
        )
        self.ing_unit.set("unidade")
        self.ing_unit.grid(row=0, column=5, padx=4)

        ttk.Button(form, text="Adicionar", command=self._add_ingredient).grid(row=0, column=6, padx=(14, 0))

        lf = ttk.LabelFrame(tab, text="Insumos Cadastrados", padding=(10, 6))
        lf.pack(fill="both", expand=True, padx=14, pady=4)

        cols = ("ID", "Nome", "Custo / Unidade", "Unidade")
        self.ing_tree = ttk.Treeview(lf, columns=cols, show="headings", selectmode="browse")
        self.ing_tree.heading("ID",              text="ID")
        self.ing_tree.heading("Nome",            text="Nome")
        self.ing_tree.heading("Custo / Unidade", text="Custo / Unidade")
        self.ing_tree.heading("Unidade",         text="Unidade")
        self.ing_tree.column("ID",               width=55,  anchor="center", stretch=False)
        self.ing_tree.column("Nome",             width=280)
        self.ing_tree.column("Custo / Unidade",  width=160, anchor="center")
        self.ing_tree.column("Unidade",          width=110, anchor="center")

        vsb = ttk.Scrollbar(lf, orient="vertical", command=self.ing_tree.yview)
        self.ing_tree.configure(yscrollcommand=vsb.set)
        self.ing_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        ttk.Button(tab, text="Remover Selecionado", command=self._delete_ingredient).pack(pady=(4, 8))
        self._refresh_ingredients()

    def _add_ingredient(self):
        name     = self.ing_name.get().strip()
        cost_str = self.ing_cost.get().strip().replace(",", ".")
        unit     = self.ing_unit.get().strip()
        if not name or not cost_str or not unit:
            self._toast("Preencha todos os campos.", error=True)
            return
        try:
            cost = float(cost_str)
            if cost < 0:
                raise ValueError
        except ValueError:
            self._toast("Custo inválido.", error=True)
            return
        ing_model.add(name, cost, unit)
        self.ing_name.delete(0, "end")
        self.ing_cost.delete(0, "end")
        self._refresh_ingredients()
        self._toast("Insumo salvo com sucesso!")

    def _delete_ingredient(self):
        sel = self.ing_tree.selection()
        if not sel:
            self._toast("Selecione um insumo para remover.", error=True)
            return
        iid = self.ing_tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirmar", "Remover este insumo?\nEle será removido de todas as composições."):
            ing_model.delete(iid)
            self._refresh_ingredients()

    def _refresh_ingredients(self):
        self.ing_tree.delete(*self.ing_tree.get_children())
        for row in ing_model.get_all():
            self.ing_tree.insert("", "end", values=(
                row["id"], row["name"], f"R$ {row['cost_per_unit']:.2f}", row["unit"],
            ))

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 3 — PRODUTOS
    # ═══════════════════════════════════════════════════════════════════════
    def _build_products_tab(self):
        tab = self.tab_prod

        form = ttk.LabelFrame(tab, text="Novo Produto", padding=(12, 8))
        form.pack(fill="x", padx=14, pady=(10, 4))

        ttk.Label(form, text="Nome:").grid(row=0, column=0, sticky="w", padx=(0, 4))
        self.prod_name = ttk.Entry(form, width=32)
        self.prod_name.grid(row=0, column=1, padx=4)

        ttk.Label(form, text="Preço de Venda (R$):").grid(row=0, column=2, sticky="w", padx=(12, 4))
        self.prod_price = ttk.Entry(form, width=14)
        self.prod_price.grid(row=0, column=3, padx=4)

        ttk.Button(form, text="Adicionar", command=self._add_product).grid(row=0, column=4, padx=(14, 0))

        lf = ttk.LabelFrame(tab, text="Produtos Cadastrados", padding=(10, 6))
        lf.pack(fill="both", expand=True, padx=14, pady=4)

        cols = ("ID", "Nome", "Preço de Venda")
        self.prod_tree = ttk.Treeview(lf, columns=cols, show="headings", selectmode="browse")
        self.prod_tree.heading("ID",             text="ID")
        self.prod_tree.heading("Nome",           text="Nome")
        self.prod_tree.heading("Preço de Venda", text="Preço de Venda")
        self.prod_tree.column("ID",              width=55,  anchor="center", stretch=False)
        self.prod_tree.column("Nome",            width=350)
        self.prod_tree.column("Preço de Venda",  width=160, anchor="center")

        vsb = ttk.Scrollbar(lf, orient="vertical", command=self.prod_tree.yview)
        self.prod_tree.configure(yscrollcommand=vsb.set)
        self.prod_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        ttk.Button(tab, text="Remover Selecionado", command=self._delete_product).pack(pady=(4, 8))
        self._refresh_products()

    def _add_product(self):
        name      = self.prod_name.get().strip()
        price_str = self.prod_price.get().strip().replace(",", ".")
        if not name or not price_str:
            self._toast("Preencha todos os campos.", error=True)
            return
        try:
            price = float(price_str)
            if price < 0:
                raise ValueError
        except ValueError:
            self._toast("Preço inválido.", error=True)
            return
        prod_model.add(name, price)
        self.prod_name.delete(0, "end")
        self.prod_price.delete(0, "end")
        self._refresh_products()
        self._toast("Produto salvo com sucesso!")

    def _delete_product(self):
        sel = self.prod_tree.selection()
        if not sel:
            self._toast("Selecione um produto para remover.", error=True)
            return
        iid = self.prod_tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirmar", "Remover este produto e toda a sua composição?"):
            prod_model.delete(iid)
            self._refresh_products()

    def _refresh_products(self):
        self.prod_tree.delete(*self.prod_tree.get_children())
        for row in prod_model.get_all():
            self.prod_tree.insert("", "end", values=(
                row["id"], row["name"], f"R$ {row['sale_price']:.2f}",
            ))

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 4 — COMPOSIÇÃO
    # ═══════════════════════════════════════════════════════════════════════
    def _build_composition_tab(self):
        tab = self.tab_comp

        sel_frame = ttk.Frame(tab)
        sel_frame.pack(fill="x", padx=14, pady=(10, 4))
        ttk.Label(sel_frame, text="Produto:", font=FONT_TITLE).pack(side="left", padx=(0, 8))
        self._comp_prod_var = tk.StringVar()
        self.comp_prod_combo = ttk.Combobox(sel_frame, textvariable=self._comp_prod_var, width=36, state="readonly")
        self.comp_prod_combo.pack(side="left")
        self.comp_prod_combo.bind("<<ComboboxSelected>>", lambda _: self._refresh_comp_list())

        form = ttk.LabelFrame(tab, text="Adicionar Insumo à Composição", padding=(12, 8))
        form.pack(fill="x", padx=14, pady=4)

        ttk.Label(form, text="Insumo:").grid(row=0, column=0, sticky="w", padx=(0, 4))
        self._comp_ing_var = tk.StringVar()
        self.comp_ing_combo = ttk.Combobox(form, textvariable=self._comp_ing_var, width=28, state="readonly")
        self.comp_ing_combo.grid(row=0, column=1, padx=4)

        ttk.Label(form, text="Quantidade:").grid(row=0, column=2, sticky="w", padx=(12, 4))
        self.comp_qty = ttk.Entry(form, width=10)
        self.comp_qty.grid(row=0, column=3, padx=4)

        ttk.Button(form, text="Adicionar", command=self._add_composition).grid(row=0, column=4, padx=(14, 0))

        lf = ttk.LabelFrame(tab, text="Insumos do Produto", padding=(10, 6))
        lf.pack(fill="both", expand=True, padx=14, pady=4)

        cols = ("ID", "Insumo", "Unidade", "Quantidade", "Custo Unit.", "Custo Total")
        self.comp_tree = ttk.Treeview(lf, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self.comp_tree.heading(c, text=c)
        self.comp_tree.column("ID",          width=55,  anchor="center", stretch=False)
        self.comp_tree.column("Insumo",      width=210)
        self.comp_tree.column("Unidade",     width=90,  anchor="center")
        self.comp_tree.column("Quantidade",  width=100, anchor="center")
        self.comp_tree.column("Custo Unit.", width=120, anchor="center")
        self.comp_tree.column("Custo Total", width=120, anchor="center")

        vsb = ttk.Scrollbar(lf, orient="vertical", command=self.comp_tree.yview)
        self.comp_tree.configure(yscrollcommand=vsb.set)
        self.comp_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        bottom = ttk.Frame(tab)
        bottom.pack(fill="x", padx=14, pady=(4, 8))
        ttk.Button(bottom, text="Remover Selecionado", command=self._delete_composition).pack(side="left")
        self._comp_total_lbl = ttk.Label(bottom, text="Custo Total: R$ 0,00", font=FONT_TITLE)
        self._comp_total_lbl.pack(side="right", padx=6)

    def _refresh_comp_combos(self):
        products = prod_model.get_all()
        self._prod_map = {f"{p['name']}  (ID {p['id']})": p["id"] for p in products}
        self.comp_prod_combo["values"] = list(self._prod_map.keys())

        ingredients = ing_model.get_all()
        self._ing_map = {f"{i['name']}  ({i['unit']})": i["id"] for i in ingredients}
        self.comp_ing_combo["values"] = list(self._ing_map.keys())

        if self._comp_prod_var.get() not in self._prod_map:
            self._comp_prod_var.set("")
        self._refresh_comp_list()

    def _refresh_comp_list(self):
        self.comp_tree.delete(*self.comp_tree.get_children())
        key = self._comp_prod_var.get()
        if not key:
            self._comp_total_lbl.config(text="Custo Total: R$ 0,00")
            return
        prod_id = self._prod_map.get(key)
        total = 0.0
        for row in comp_model.get_by_product(prod_id):
            self.comp_tree.insert("", "end", values=(
                row["id"], row["name"], row["unit"],
                f"{row['quantity']:.4f}".rstrip("0").rstrip("."),
                f"R$ {row['cost_per_unit']:.2f}",
                f"R$ {row['total_cost']:.2f}",
            ))
            total += row["total_cost"]
        self._comp_total_lbl.config(text=f"Custo Total: R$ {total:.2f}")

    def _add_composition(self):
        prod_key = self._comp_prod_var.get()
        ing_key  = self._comp_ing_var.get()
        qty_str  = self.comp_qty.get().strip().replace(",", ".")
        if not prod_key:
            self._toast("Selecione um produto.", error=True)
            return
        if not ing_key:
            self._toast("Selecione um insumo.", error=True)
            return
        try:
            qty = float(qty_str)
            if qty <= 0:
                raise ValueError
        except ValueError:
            self._toast("Quantidade inválida.", error=True)
            return
        comp_model.add(self._prod_map[prod_key], self._ing_map[ing_key], qty)
        self.comp_qty.delete(0, "end")
        self._refresh_comp_list()
        self._toast("Insumo adicionado à composição!")

    def _delete_composition(self):
        sel = self.comp_tree.selection()
        if not sel:
            self._toast("Selecione um item para remover.", error=True)
            return
        iid = self.comp_tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirmar", "Remover este insumo da composição?"):
            comp_model.delete(iid)
            self._refresh_comp_list()

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 5 — CUSTOS / RESULTADOS
    # ═══════════════════════════════════════════════════════════════════════
    def _build_results_tab(self):
        tab = self.tab_res

        header = ttk.Frame(tab)
        header.pack(fill="x", padx=14, pady=(10, 4))
        ttk.Label(header, text="Análise de Custos e Rentabilidade", font=FONT_TITLE).pack(side="left")
        ttk.Button(header, text="↻  Atualizar", command=self._refresh_results).pack(side="right")

        lf = ttk.LabelFrame(tab, text="Produtos", padding=(10, 6))
        lf.pack(fill="both", expand=True, padx=14, pady=4)

        cols = ("Produto", "Custo (R$)", "Preço Venda (R$)", "Lucro (R$)", "Margem (%)")
        self.res_tree = ttk.Treeview(lf, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self.res_tree.heading(c, text=c)
        self.res_tree.column("Produto",          width=250)
        self.res_tree.column("Custo (R$)",        width=140, anchor="center")
        self.res_tree.column("Preço Venda (R$)",  width=160, anchor="center")
        self.res_tree.column("Lucro (R$)",        width=140, anchor="center")
        self.res_tree.column("Margem (%)",        width=120, anchor="center")

        vsb = ttk.Scrollbar(lf, orient="vertical", command=self.res_tree.yview)
        self.res_tree.configure(yscrollcommand=vsb.set)
        self.res_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        self.res_tree.tag_configure("lucro",    background="#e8f5e9", foreground="#1b5e20")
        self.res_tree.tag_configure("prejuizo", background="#ffebee", foreground="#b71c1c")
        self.res_tree.tag_configure("zero",     background="#fff9c4", foreground="#f57f17")

    def _refresh_results(self):
        self.res_tree.delete(*self.res_tree.get_children())
        for r in comp_model.get_all_results():
            tag = "lucro" if r["profit"] > 0 else ("prejuizo" if r["profit"] < 0 else "zero")
            self.res_tree.insert("", "end", values=(
                r["name"],
                f"R$ {r['cost']:.2f}",
                f"R$ {r['price']:.2f}",
                f"R$ {r['profit']:.2f}",
                f"{r['margin']:.1f}%",
            ), tags=(tag,))

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 6 — RELATÓRIOS
    # ═══════════════════════════════════════════════════════════════════════
    def _build_reports_tab(self):
        tab = self.tab_report

        # date range
        filter_frame = ttk.LabelFrame(tab, text="Período", padding=(12, 8))
        filter_frame.pack(fill="x", padx=14, pady=(10, 4))

        ttk.Label(filter_frame, text="De:").grid(row=0, column=0, sticky="w", padx=(0, 4))
        self.rep_from = ttk.Entry(filter_frame, width=13)
        self.rep_from.grid(row=0, column=1, padx=4)
        self.rep_from.insert(0, date.today().strftime("%Y-%m-%d"))

        ttk.Label(filter_frame, text="Até:").grid(row=0, column=2, sticky="w", padx=(12, 4))
        self.rep_to = ttk.Entry(filter_frame, width=13)
        self.rep_to.grid(row=0, column=3, padx=4)
        self.rep_to.insert(0, date.today().strftime("%Y-%m-%d"))

        ttk.Label(filter_frame, text="(formato AAAA-MM-DD)",
                  foreground="#888").grid(row=0, column=4, padx=(8, 4))

        ttk.Button(filter_frame, text="Gerar Relatório",
                   command=self._generate_report).grid(row=0, column=5, padx=(16, 0))

        # summary cards
        self._rep_cards_frame = ttk.Frame(tab)
        self._rep_cards_frame.pack(fill="x", padx=14, pady=(6, 4))

        _, self._rep_vendas_lbl   = self._card(self._rep_cards_frame, "Total em Vendas",   "R$ 0,00", "#2e7d32")
        _, self._rep_entradas_lbl = self._card(self._rep_cards_frame, "Entradas no Caixa", "R$ 0,00", "#1565c0")
        _, self._rep_saidas_lbl   = self._card(self._rep_cards_frame, "Saídas no Caixa",   "R$ 0,00", "#c62828")
        _, self._rep_saldo_lbl    = self._card(self._rep_cards_frame, "Saldo do Período",  "R$ 0,00", "#1565c0")

        for lbl in (self._rep_vendas_lbl, self._rep_entradas_lbl,
                    self._rep_saidas_lbl, self._rep_saldo_lbl):
            lbl.master.pack(side="left", padx=(0, 10))

        # two side-by-side tables
        tables_frame = ttk.Frame(tab)
        tables_frame.pack(fill="both", expand=True, padx=14, pady=4)

        # sales table
        lf_sales = ttk.LabelFrame(tables_frame, text="Vendas por Produto", padding=(8, 6))
        lf_sales.pack(side="left", fill="both", expand=True, padx=(0, 6))

        cols_s = ("Data", "Produto", "Qtd", "Total (R$)")
        self.rep_sales_tree = ttk.Treeview(lf_sales, columns=cols_s, show="headings", height=10)
        for c in cols_s:
            self.rep_sales_tree.heading(c, text=c)
        self.rep_sales_tree.column("Data",       width=100, anchor="center")
        self.rep_sales_tree.column("Produto",    width=180)
        self.rep_sales_tree.column("Qtd",        width=70,  anchor="center")
        self.rep_sales_tree.column("Total (R$)", width=110, anchor="center")
        vsb1 = ttk.Scrollbar(lf_sales, orient="vertical", command=self.rep_sales_tree.yview)
        self.rep_sales_tree.configure(yscrollcommand=vsb1.set)
        self.rep_sales_tree.pack(side="left", fill="both", expand=True)
        vsb1.pack(side="right", fill="y")

        # cash flow table
        lf_cf = ttk.LabelFrame(tables_frame, text="Movimentações do Caixa", padding=(8, 6))
        lf_cf.pack(side="left", fill="both", expand=True)

        cols_c = ("Data", "Tipo", "Descrição", "Valor (R$)")
        self.rep_cf_tree = ttk.Treeview(lf_cf, columns=cols_c, show="headings", height=10)
        for c in cols_c:
            self.rep_cf_tree.heading(c, text=c)
        self.rep_cf_tree.column("Data",        width=100, anchor="center")
        self.rep_cf_tree.column("Tipo",        width=80,  anchor="center")
        self.rep_cf_tree.column("Descrição",   width=200)
        self.rep_cf_tree.column("Valor (R$)",  width=100, anchor="center")
        self.rep_cf_tree.tag_configure("entrada", foreground="#1b5e20")
        self.rep_cf_tree.tag_configure("saida",   foreground="#b71c1c")
        vsb2 = ttk.Scrollbar(lf_cf, orient="vertical", command=self.rep_cf_tree.yview)
        self.rep_cf_tree.configure(yscrollcommand=vsb2.set)
        self.rep_cf_tree.pack(side="left", fill="both", expand=True)
        vsb2.pack(side="right", fill="y")

    def _generate_report(self):
        start = self.rep_from.get().strip()
        end   = self.rep_to.get().strip()
        try:
            from datetime import datetime
            datetime.strptime(start, "%Y-%m-%d")
            datetime.strptime(end,   "%Y-%m-%d")
        except ValueError:
            self._toast("Datas inválidas. Use AAAA-MM-DD.", error=True)
            return

        # summary
        total_vendas = sale_model.get_total_by_date_range(start, end)
        cf_summary   = cf_model.get_summary_by_date_range(start, end)
        saldo = cf_summary["entradas"] - cf_summary["saidas"]

        self._rep_vendas_lbl.config(text=f"R$ {total_vendas:.2f}")
        self._rep_entradas_lbl.config(text=f"R$ {cf_summary['entradas']:.2f}")
        self._rep_saidas_lbl.config(text=f"R$ {cf_summary['saidas']:.2f}")
        self._rep_saldo_lbl.config(
            text=f"R$ {saldo:.2f}",
            foreground=("#2e7d32" if saldo >= 0 else "#c62828"),
        )

        # sales table
        self.rep_sales_tree.delete(*self.rep_sales_tree.get_children())
        for row in sale_model.get_by_date_range(start, end):
            self.rep_sales_tree.insert("", "end", values=(
                row["date"], row["name"],
                f"{row['qty']:.2f}".rstrip("0").rstrip("."),
                f"R$ {row['total']:.2f}",
            ))

        # cash flow table
        self.rep_cf_tree.delete(*self.rep_cf_tree.get_children())
        for row in cf_model.get_by_date_range(start, end):
            label = "Entrada" if row["type"] == "entrada" else "Saída"
            self.rep_cf_tree.insert("", "end", values=(
                row["date"], label, row["description"], f"R$ {row['value']:.2f}",
            ), tags=(row["type"],))

        self._toast("Relatório gerado!")
