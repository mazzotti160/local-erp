from datetime import date
from database.db import get_connection


def add(product_id: int, quantity: float, total_price: float) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO sales (product_id, quantity, total_price, date) VALUES (?, ?, ?, ?)",
        (product_id, quantity, total_price, date.today().isoformat()),
    )
    conn.commit()
    conn.close()


def get_today() -> list:
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT s.id, p.name, s.quantity, s.total_price, s.date
        FROM sales s
        JOIN products p ON p.id = s.product_id
        WHERE s.date = ?
        ORDER BY s.id DESC
        """,
        (date.today().isoformat(),),
    ).fetchall()
    conn.close()
    return rows


def get_total_today() -> float:
    conn = get_connection()
    row = conn.execute(
        "SELECT COALESCE(SUM(total_price), 0) AS total FROM sales WHERE date = ?",
        (date.today().isoformat(),),
    ).fetchone()
    conn.close()
    return row["total"]


def get_by_date_range(start: str, end: str) -> list:
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT s.date, p.name,
               SUM(s.quantity)    AS qty,
               SUM(s.total_price) AS total
        FROM sales s
        JOIN products p ON p.id = s.product_id
        WHERE s.date BETWEEN ? AND ?
        GROUP BY s.date, p.id
        ORDER BY s.date DESC, p.name COLLATE NOCASE
        """,
        (start, end),
    ).fetchall()
    conn.close()
    return rows


def get_total_by_date_range(start: str, end: str) -> float:
    conn = get_connection()
    row = conn.execute(
        "SELECT COALESCE(SUM(total_price), 0) AS total FROM sales WHERE date BETWEEN ? AND ?",
        (start, end),
    ).fetchone()
    conn.close()
    return row["total"]


def delete(sale_id: int) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
    conn.commit()
    conn.close()
