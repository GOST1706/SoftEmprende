import sqlite3
import sys
from pathlib import Path
from app.core.models import Product


class SQLiteProductRepository:
    def __init__(self, db_name: str = "products.db"):

        if getattr(sys, "frozen", False):
            base_dir = Path(sys.executable).parent
        else:
            base_dir = Path(__file__).resolve().parents[1]

        data_dir = base_dir / "data"
        data_dir.mkdir(exist_ok=True)

        db_path = data_dir / db_name

        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku TEXT UNIQUE,
                name TEXT,
                price REAL,
                stock INTEGER,
                category_id INTEGER
            )
        """)
        self.conn.commit()

        # 🔹 Migración simple por si la tabla ya existía sin category_id
        cols = [row["name"] for row in self.conn.execute("PRAGMA table_info(products)")]
        if "category_id" not in cols:
            self.conn.execute("ALTER TABLE products ADD COLUMN category_id INTEGER")
            self.conn.commit()

    # ------------------------------
    # CREATE
    # ------------------------------
    def add(self, product: Product):
        cur = self.conn.execute("""
            INSERT INTO products (sku, name, price, stock, category_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            product.sku,
            product.name,
            product.price,
            product.stock,
            product.category_id
        ))
        self.conn.commit()

        product.id = cur.lastrowid
        return product

    # ------------------------------
    # READ
    # ------------------------------
    def list(self):
        cur = self.conn.execute("SELECT * FROM products")
        rows = cur.fetchall()
        return [Product(**row) for row in rows]

    def list_by_category(self, category_id: int):
        cur = self.conn.execute(
            "SELECT * FROM products WHERE category_id = ?",
            (category_id,)
        )
        rows = cur.fetchall()
        return [Product(**row) for row in rows]

    def get_by_any(self, value: str):
        query_value = int(value) if value.isdigit() else -1
        cur = self.conn.execute(
            """
            SELECT * FROM products
            WHERE id = :id OR sku = :sku OR name LIKE :name
            """,
            {"id": query_value, "sku": value, "name": f"%{value}%"}
        )
        row = cur.fetchone()
        return Product(**row) if row else None

    # ------------------------------
    # UPDATE
    # ------------------------------
    def update(self, product: Product):
        self.conn.execute("""
            UPDATE products
            SET sku = ?, name = ?, price = ?, stock = ?, category_id = ?
            WHERE id = ?
        """, (
            product.sku,
            product.name,
            product.price,
            product.stock,
            product.category_id,
            product.id
        ))
        self.conn.commit()
        return product

    def update_category(self, product_id: int, category_id: int | None):
        self.conn.execute(
            "UPDATE products SET category_id = ? WHERE id = ?",
            (category_id, product_id)
        )
        self.conn.commit()

    # ------------------------------
    # DELETE
    # ------------------------------
    def delete(self, product_id: int):
        self.conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
        self.conn.commit()

    # ------------------------------
    # CLOSE
    # ------------------------------
    def close(self):
        self.conn.close()
