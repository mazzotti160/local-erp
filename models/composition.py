from database.db import get_connection


def add(product_id: int, ingredient_id: int, quantity: float) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO product_ingredients (product_id, ingredient_id, quantity) VALUES (?, ?, ?)",
        (product_id, ingredient_id, quantity),
    )
    conn.commit()
    conn.close()


def get_by_product(product_id: int) -> list:
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT
            pi.id,
            i.name,
            i.unit,
            pi.quantity,
            i.cost_per_unit,
            (pi.quantity * i.cost_per_unit) AS total_cost
        FROM product_ingredients pi
        JOIN ingredients i ON i.id = pi.ingredient_id
        WHERE pi.product_id = ?
        ORDER BY i.name COLLATE NOCASE
        """,
        (product_id,),
    ).fetchall()
    conn.close()
    return rows


def delete(composition_id: int) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM product_ingredients WHERE id = ?", (composition_id,))
    conn.commit()
    conn.close()


def get_all_results() -> list:
    conn = get_connection()
    products = conn.execute("SELECT * FROM products ORDER BY name COLLATE NOCASE").fetchall()
    results = []
    for p in products:
        row = conn.execute(
            """
            SELECT COALESCE(SUM(pi.quantity * i.cost_per_unit), 0) AS total
            FROM product_ingredients pi
            JOIN ingredients i ON i.id = pi.ingredient_id
            WHERE pi.product_id = ?
            """,
            (p["id"],),
        ).fetchone()
        cost = row["total"]
        price = p["sale_price"]
        profit = price - cost
        margin = (profit / price * 100) if price > 0 else 0.0
        results.append({
            "name": p["name"],
            "cost": cost,
            "price": price,
            "profit": profit,
            "margin": margin,
        })
    conn.close()
    return results
