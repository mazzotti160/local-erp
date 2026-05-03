import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "database.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
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
    """)
    conn.commit()
    conn.close()
