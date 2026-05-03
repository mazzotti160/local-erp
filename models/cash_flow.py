from datetime import date
from database.db import get_connection


def add(type_: str, description: str, value: float) -> None:
    conn = get_connection()
    conn.execute(
        "INSERT INTO cash_flow (type, description, value, date) VALUES (?, ?, ?, ?)",
        (type_, description, value, date.today().isoformat()),
    )
    conn.commit()
    conn.close()


def get_today() -> list:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM cash_flow WHERE date = ? ORDER BY id DESC",
        (date.today().isoformat(),),
    ).fetchall()
    conn.close()
    return rows


def get_summary_today() -> dict:
    conn = get_connection()
    row = conn.execute(
        """
        SELECT
            COALESCE(SUM(CASE WHEN type = 'entrada' THEN value ELSE 0 END), 0) AS entradas,
            COALESCE(SUM(CASE WHEN type = 'saida'   THEN value ELSE 0 END), 0) AS saidas
        FROM cash_flow WHERE date = ?
        """,
        (date.today().isoformat(),),
    ).fetchone()
    conn.close()
    return {"entradas": row["entradas"], "saidas": row["saidas"]}


def get_by_date_range(start: str, end: str) -> list:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM cash_flow WHERE date BETWEEN ? AND ? ORDER BY date DESC, id DESC",
        (start, end),
    ).fetchall()
    conn.close()
    return rows


def get_summary_by_date_range(start: str, end: str) -> dict:
    conn = get_connection()
    row = conn.execute(
        """
        SELECT
            COALESCE(SUM(CASE WHEN type = 'entrada' THEN value ELSE 0 END), 0) AS entradas,
            COALESCE(SUM(CASE WHEN type = 'saida'   THEN value ELSE 0 END), 0) AS saidas
        FROM cash_flow WHERE date BETWEEN ? AND ?
        """,
        (start, end),
    ).fetchone()
    conn.close()
    return {"entradas": row["entradas"], "saidas": row["saidas"]}


def delete(entry_id: int) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM cash_flow WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
