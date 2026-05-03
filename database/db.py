import sqlite3
import os
from database.config import get_db_path


def get_connection():
    db_path = get_db_path()
    if not db_path:
        raise RuntimeError("Banco de dados não configurado.")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize():
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            name           TEXT    NOT NULL,
            cost_per_unit  REAL    NOT NULL,
            unit           TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            sale_price  REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS product_ingredients (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id     INTEGER NOT NULL,
            ingredient_id  INTEGER NOT NULL,
            quantity       REAL    NOT NULL,
            FOREIGN KEY (product_id)    REFERENCES products(id)    ON DELETE CASCADE,
            FOREIGN KEY (ingredient_id) REFERENCES ingredients(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS sales (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id  INTEGER NOT NULL,
            quantity    REAL    NOT NULL,
            total_price REAL    NOT NULL,
            date        TEXT    NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS cash_flow (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            type        TEXT NOT NULL,
            description TEXT NOT NULL,
            value       REAL NOT NULL,
            date        TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()
