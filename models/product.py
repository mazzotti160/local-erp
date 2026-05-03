from database.db import get_connection


def add(name: str, sale_price: float) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO products (name, sale_price) VALUES (?, ?)",
        (name, sale_price),
    )
    conn.commit()
    conn.close()


def get_all() -> list:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM products ORDER BY name COLLATE NOCASE").fetchall()
    conn.close()
    return rows


def delete(product_id: int) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.execute("DELETE FROM product_ingredients WHERE product_id = ?", (product_id,))
    conn.commit()
    conn.close()
