import sqlite3
import sys
from pathlib import Path
from app.core.models import Category


class SQLiteCategoryRepository:
    def __init__(self, db_name: str = "products.db"):

        # 🔹 PyInstaller / desarrollo
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

    # ------------------------------
    # TABLE
    # ------------------------------
    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)
        self.conn.commit()

    # ------------------------------
    # CREATE
    # ------------------------------
    def add(self, category: Category) -> Category:
        cursor = self.conn.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (category.name,)
        )
        self.conn.commit()
        category.id = cursor.lastrowid
        return category

    # ------------------------------
    # READ
    # ------------------------------
    def list(self) -> list[Category]:
        cursor = self.conn.execute(
            "SELECT id, name FROM categories ORDER BY name"
        )
        return [
            Category(id=row["id"], name=row["name"])
            for row in cursor.fetchall()
        ]

    def get_by_id(self, category_id: int) -> Category | None:
        cursor = self.conn.execute(
            "SELECT id, name FROM categories WHERE id = ?",
            (category_id,)
        )
        row = cursor.fetchone()
        return Category(id=row["id"], name=row["name"]) if row else None

    def get_by_name(self, name: str) -> Category | None:
        cursor = self.conn.execute(
            "SELECT id, name FROM categories WHERE name = ?",
            (name,)
        )
        row = cursor.fetchone()
        return Category(id=row["id"], name=row["name"]) if row else None

    # ------------------------------
    # UPDATE
    # ------------------------------
    def update(self, category: Category):
        self.conn.execute(
            "UPDATE categories SET name = ? WHERE id = ?",
            (category.name, category.id)
        )
        self.conn.commit()
        return category

    # ------------------------------
    # DELETE
    # ------------------------------
    def delete(self, category_id: int):
        # Quitar categoría de productos
        self.conn.execute(
            "UPDATE products SET category_id = NULL WHERE category_id = ?",
            (category_id,)
        )

        # Eliminar categoría
        self.conn.execute(
            "DELETE FROM categories WHERE id = ?",
            (category_id,)
        )

        self.conn.commit()

    # ------------------------------
    # CLOSE
    # ------------------------------
    def close(self):
        self.conn.close()
