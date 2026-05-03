from database.db import get_connection


def add(name: str, cost_per_unit: float, unit: str) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO ingredients (name, cost_per_unit, unit) VALUES (?, ?, ?)",
        (name, cost_per_unit, unit),
    )
    conn.commit()
    conn.close()


def get_all() -> list:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM ingredients ORDER BY name COLLATE NOCASE").fetchall()
    conn.close()
    return rows


def delete(ingredient_id: int) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM ingredients WHERE id = ?", (ingredient_id,))
    conn.commit()
    conn.close()
