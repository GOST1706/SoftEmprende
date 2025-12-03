import sqlite3
from core.models import Product

class SQLiteProductRepository:
    def __init__(self, db_path: str):
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
                stock INTEGER
            )
        """)
        self.conn.commit()

    # ------------------------------
    # CREATE
    # ------------------------------
    def add(self, product: Product):
        cur = self.conn.execute("""
            INSERT INTO products (sku, name, price, stock)
            VALUES (?, ?, ?, ?)
        """, (product.sku, product.name, product.price, product.stock))
        self.conn.commit()

        product.id = cur.lastrowid
        return product

    # ------------------------------
    # READ
    # ------------------------------

    # Lista todos los productos
    def list(self):
        cur = self.conn.execute("SELECT * FROM products")
        rows = cur.fetchall()
        return [Product(**row) for row in rows]

    # Buscar por ID, SKU o nombre
    def get_by_any(self, value: str):
        query_value = int(value) if value.isdigit() else -1  # ID válido o -1 si no es número
        cur = self.conn.execute(
            """
            SELECT * FROM products
            WHERE id=:id OR sku=:sku OR name LIKE :name
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
            SET sku = ?, name = ?, price = ?, stock = ?
            WHERE id = ?
        """, (product.sku, product.name, product.price, product.stock, product.id))
        self.conn.commit()
        return product

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
