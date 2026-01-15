import sqlite3
import sys
from pathlib import Path
from datetime import datetime
from app.core.models import Sale, SaleItem

class SQLiteSaleRepository:
    def __init__(self, db_name: str = "products.db"):

        # Path base (dev / exe)
        if getattr(sys, "frozen", False):
            base_dir = Path(sys.executable).parent
        else:
            base_dir = Path(__file__).resolve().parents[1]

        data_dir = base_dir / "data"
        data_dir.mkdir(exist_ok=True)

        db_path = data_dir / db_name

        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                total REAL
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                unit_price REAL,
                FOREIGN KEY (sale_id) REFERENCES sales(id)
            )
        """)
        self.conn.commit()

    def add_sale(self, sale: Sale):
        cur = self.conn.execute(
            "INSERT INTO sales (date, total) VALUES (?, ?)",
            (sale.date.isoformat(), sale.total)
        )
        self.conn.commit()
        sale.id = cur.lastrowid
        return sale

    def add_item(self, item: SaleItem):
        cur = self.conn.execute(
            """
            INSERT INTO sale_items (sale_id, product_id, quantity, unit_price)
            VALUES (?, ?, ?, ?)
            """,
            (item.sale_id, item.product_id, item.quantity, item.unit_price)
        )
        self.conn.commit()
        item.id = cur.lastrowid
        return item
