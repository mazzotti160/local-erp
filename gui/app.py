import tkinter as tk
from tkinter import ttk, messagebox

from models import ingredient as ing_model
from models import product as prod_model
from models import composition as comp_model

FONT_TITLE  = ("Segoe UI", 11, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_LABEL  = ("Segoe UI", 9)
BG          = "#f5f5f5"
GREEN       = "#2e7d32"
RED         = "#c62828"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Local ERP — Controle de Custos")
        self.geometry("960x620")
        self.minsize(800, 500)
        self.configure(bg=BG)
        self._apply_style()
        self._build_header()
        self._build_notebook()

    # ─── STYLE ───────────────────────────────────────────────────────────────
    def _apply_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook",            background=BG,  borderwidth=0)
        style.configure("TNotebook.Tab",        font=FONT_NORMAL, padding=(14, 6))
        style.map("TNotebook.Tab",              background=[("selected", "#ffffff"), ("!selected", "#dde4ea")])
        style.configure("TFrame",               background=BG)
        style.configure("TLabel",               background=BG,  font=FONT_NORMAL)
        style.configure("TLabelframe",          background=BG,  font=FONT_LABEL)
        style.configure("TLabelframe.Label",    background=BG,  font=("Segoe UI", 9, "bold"), foreground="#555")
        style.configure("TButton",              font=FONT_NORMAL, padding=(10, 4))
        style.configure("TEntry",               font=FONT_NORMAL)
        style.configure("Treeview",             font=FONT_NORMAL, rowheight=26)
        style.configure("Treeview.Heading",     font=("Segoe UI", 9, "bold"))
        style.map("Treeview",                   background=[("selected", "#bbdefb")])

    # ─── HEADER ──────────────────────────────────────────────────────────────
    def _build_header(self):
        bar = tk.Frame(self, bg="#1565c0", height=48)
        bar.pack(fill="x")
        tk.Label(
            bar,
            text="  📦  Local ERP — Controle de Custos e Produtos",
            bg="#1565c0", fg="white",
            font=("Segoe UI", 12, "bold"),
            anchor="w",
        ).pack(side="left", fill="y", padx=8)

    # ─── NOTEBOOK ────────────────────────────────────────────────────────────
    def _build_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(6, 10))

        self.tab_ing  = ttk.Frame(self.notebook)
        self.tab_prod = ttk.Frame(self.notebook)
        self.tab_comp = ttk.Frame(self.notebook)
        self.tab_res  = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_ing,  text="  Insumos  ")
        self.notebook.add(self.tab_prod, text="  Produtos  ")
        self.notebook.add(self.tab_comp, text="  Composição  ")
        self.notebook.add(self.tab_res,  text="  Resultados  ")

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

        self._build_ingredients_tab()
        self._build_products_tab()
        self._build_composition_tab()
        self._build_results_tab()

    def _on_tab_change(self, event):
        idx = event.widget.index("current")
        if idx == 2:
            self._refresh_comp_combos()
        elif idx == 3:
            self._refresh_results()

    # ─── TOAST ───────────────────────────────────────────────────────────────
    def _toast(self, msg: str, error: bool = False):
        color = RED if error else GREEN
        lbl = tk.Label(self, text=f"  {'✖' if error else '✔'}  {msg}  ",
                       bg=color, fg="white", font=("Segoe UI", 9, "bold"),
                       relief="flat", bd=0)
        lbl.place(relx=0.5, rely=0.97, anchor="center")
        self.after(2800, lbl.destroy)

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 1 — INSUMOS
    # ═══════════════════════════════════════════════════════════════════════
    def _build_ingredients_tab(self):
        tab = self.tab_ing

        # form
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

        # list
        lf = ttk.LabelFrame(tab, text="Insumos Cadastrados", padding=(10, 6))
        lf.pack(fill="both", expand=True, padx=14, pady=4)

        cols = ("ID", "Nome", "Custo / Unidade", "Unidade")
        self.ing_tree = ttk.Treeview(lf, columns=cols, show="headings", selectmode="browse")
        self.ing_tree.heading("ID",             text="ID")
        self.ing_tree.heading("Nome",           text="Nome")
        self.ing_tree.heading("Custo / Unidade",text="Custo / Unidade")
        self.ing_tree.heading("Unidade",        text="Unidade")
        self.ing_tree.column("ID",              width=55,  anchor="center", stretch=False)
        self.ing_tree.column("Nome",            width=280)
        self.ing_tree.column("Custo / Unidade", width=160, anchor="center")
        self.ing_tree.column("Unidade",         width=110, anchor="center")

        vsb = ttk.Scrollbar(lf, orient="vertical", command=self.ing_tree.yview)
        self.ing_tree.configure(yscrollcommand=vsb.set)
        self.ing_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        ttk.Button(tab, text="Remover Selecionado", command=self._delete_ingredient).pack(pady=(4, 8))
        self._refresh_ingredients()

    def _add_ingredient(self):
        name = self.ing_name.get().strip()
        cost_str = self.ing_cost.get().strip().replace(",", ".")
        unit = self.ing_unit.get().strip()

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
    # TAB 2 — PRODUTOS
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
        self.prod_tree.heading("ID",            text="ID")
        self.prod_tree.heading("Nome",          text="Nome")
        self.prod_tree.heading("Preço de Venda",text="Preço de Venda")
        self.prod_tree.column("ID",             width=55,  anchor="center", stretch=False)
        self.prod_tree.column("Nome",           width=350)
        self.prod_tree.column("Preço de Venda", width=160, anchor="center")

        vsb = ttk.Scrollbar(lf, orient="vertical", command=self.prod_tree.yview)
        self.prod_tree.configure(yscrollcommand=vsb.set)
        self.prod_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        ttk.Button(tab, text="Remover Selecionado", command=self._delete_product).pack(pady=(4, 8))
        self._refresh_products()

    def _add_product(self):
        name = self.prod_name.get().strip()
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
    # TAB 3 — COMPOSIÇÃO
    # ═══════════════════════════════════════════════════════════════════════
    def _build_composition_tab(self):
        tab = self.tab_comp

        # product selector
        sel_frame = ttk.Frame(tab)
        sel_frame.pack(fill="x", padx=14, pady=(10, 4))
        ttk.Label(sel_frame, text="Produto:", font=FONT_TITLE).pack(side="left", padx=(0, 8))
        self._comp_prod_var = tk.StringVar()
        self.comp_prod_combo = ttk.Combobox(sel_frame, textvariable=self._comp_prod_var, width=36, state="readonly")
        self.comp_prod_combo.pack(side="left")
        self.comp_prod_combo.bind("<<ComboboxSelected>>", lambda _: self._refresh_comp_list())

        # add ingredient form
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

        # list
        lf = ttk.LabelFrame(tab, text="Insumos do Produto", padding=(10, 6))
        lf.pack(fill="both", expand=True, padx=14, pady=4)

        cols = ("ID", "Insumo", "Unidade", "Quantidade", "Custo Unit.", "Custo Total")
        self.comp_tree = ttk.Treeview(lf, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self.comp_tree.heading(c, text=c)
        self.comp_tree.column("ID",         width=55,  anchor="center", stretch=False)
        self.comp_tree.column("Insumo",     width=210)
        self.comp_tree.column("Unidade",    width=90,  anchor="center")
        self.comp_tree.column("Quantidade", width=100, anchor="center")
        self.comp_tree.column("Custo Unit.",width=120, anchor="center")
        self.comp_tree.column("Custo Total",width=120, anchor="center")

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
                row["id"],
                row["name"],
                row["unit"],
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
        if not qty_str:
            self._toast("Informe a quantidade.", error=True)
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
    # TAB 4 — RESULTADOS
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

        self.res_tree.tag_configure("lucro",   background="#e8f5e9", foreground="#1b5e20")
        self.res_tree.tag_configure("prejuizo",background="#ffebee", foreground="#b71c1c")
        self.res_tree.tag_configure("zero",    background="#fff9c4", foreground="#f57f17")

    def _refresh_results(self):
        self.res_tree.delete(*self.res_tree.get_children())
        for r in comp_model.get_all_results():
            if r["profit"] > 0:
                tag = "lucro"
            elif r["profit"] < 0:
                tag = "prejuizo"
            else:
                tag = "zero"
            self.res_tree.insert("", "end", values=(
                r["name"],
                f"R$ {r['cost']:.2f}",
                f"R$ {r['price']:.2f}",
                f"R$ {r['profit']:.2f}",
                f"{r['margin']:.1f}%",
            ), tags=(tag,))
