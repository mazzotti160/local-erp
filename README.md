# 📦 Local ERP — Controle de Custos e Produtos

> Sistema desktop simples para pequenos empreendedores entenderem o custo real dos seus produtos, calcularem lucro e tomarem decisões corretas de precificação.

---

## 🧩 O Problema

Pequenos negócios frequentemente precificam no "achismo": cobram R$ 15 no produto sem saber que o custo dos insumos é R$ 13. Resultado: trabalham para pagar despesas e nunca lucram.

**Local ERP** resolve isso com uma ferramenta objetiva, offline e sem burocracia.

---

## ✅ Solução

- Cadastre seus **insumos** com custo e unidade
- Cadastre seus **produtos** com preço de venda
- Monte a **composição** de cada produto (quais insumos usa e em que quantidade)
- Visualize automaticamente o **custo real**, **lucro** e **margem** de cada produto

---

## 🚀 Funcionalidades

| Módulo        | O que faz                                                    |
|---------------|--------------------------------------------------------------|
| Insumos       | Cadastra ingredientes/materiais com custo e unidade          |
| Produtos      | Cadastra produtos com preço de venda                         |
| Composição    | Define quais insumos compõem cada produto e em que quantidade|
| Resultados    | Calcula custo, lucro e margem de todos os produtos           |

---

## 🖥️ Como Usar

### Pré-requisitos

- Python 3.8 ou superior
- Tkinter (já incluso no Python padrão)
- Nenhuma dependência externa

### Instalação e execução

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/local-erp.git
cd local-erp

# Execute
python main.py
```

O banco de dados `database.db` será criado automaticamente na primeira execução.

---

## 📁 Estrutura do Projeto

```
local-erp/
├── main.py                  # Ponto de entrada
├── database/
│   └── db.py                # Conexão e criação do banco SQLite
├── models/
│   ├── ingredient.py        # CRUD de insumos
│   ├── product.py           # CRUD de produtos
│   └── composition.py       # CRUD de composição + cálculos
├── gui/
│   └── app.py               # Interface gráfica (Tkinter)
└── database.db              # Criado automaticamente
```

---

## 🧪 Exemplo Real — Açaí 500ml

Suponha que você vende **Açaí 500ml** por **R$ 18,00**.

### Insumos cadastrados:

| Insumo      | Custo     | Unidade |
|-------------|-----------|---------|
| Polpa açaí  | R$ 20,00  | kg      |
| Leite       | R$ 4,50   | litro   |
| Granola     | R$ 12,00  | kg      |
| Copo 500ml  | R$ 0,35   | unidade |

### Composição do produto:

| Insumo     | Quantidade | Custo parcial |
|------------|------------|---------------|
| Polpa açaí | 0.150 kg   | R$ 3,00       |
| Leite      | 0.100 L    | R$ 0,45       |
| Granola    | 0.050 kg   | R$ 0,60       |
| Copo 500ml | 1 unidade  | R$ 0,35       |

### Resultado automático:

| Custo Total | Preço Venda | Lucro   | Margem |
|-------------|-------------|---------|--------|
| R$ 4,40     | R$ 18,00    | R$ 13,60| 75,6%  |

Ótima margem! Mas sem o sistema, você talvez nunca soubesse disso com precisão.

---

## 🎨 Interface

- Layout por abas (Insumos / Produtos / Composição / Resultados)
- Feedback visual ao salvar dados
- Linhas com **fundo verde** = lucro / **fundo vermelho** = prejuízo
- Funciona 100% offline, sem internet

---

## ⚙️ Tecnologias

| Tecnologia | Uso                        |
|------------|----------------------------|
| Python     | Linguagem principal        |
| Tkinter    | Interface gráfica          |
| SQLite3    | Banco de dados local       |

---

## 📄 Licença

MIT — use, modifique e distribua livremente.
