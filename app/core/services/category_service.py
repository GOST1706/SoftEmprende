from typing import List, Optional
from app.core.models import Category
from app.core.sqlite_category_repo import SQLiteCategoryRepository
from app.core.sqlite_product_repo import SQLiteProductRepository


class CategoryService:
    def __init__(
        self,
        category_repo: SQLiteCategoryRepository,
        product_repo: SQLiteProductRepository
    ):
        self.category_repo = category_repo
        self.product_repo = product_repo

    # -------- CREAR --------
    def create(self, name: str) -> Category:
        name = name.strip()

        if not name:
            raise ValueError("El nombre de la categoría no puede estar vacío")

        existing = self.category_repo.get_by_name(name)
        if existing:
            raise ValueError("Ya existe una categoría con ese nombre")

        category = Category(name=name)
        return self.category_repo.add(category)

    # -------- LISTAR --------
    def list_categories(self) -> List[Category]:
        return self.category_repo.list()

    # -------- EDITAR --------
    def rename_category(self, category_id: int, new_name: str) -> Category:
        new_name = new_name.strip()

        if not new_name:
            raise ValueError("El nombre no puede estar vacío")

        existing = self.category_repo.get_by_name(new_name)
        if existing and existing.id != category_id:
            raise ValueError("Ya existe otra categoría con ese nombre")

        return self.category_repo.update_name(category_id, new_name)

    # -------- ELIMINAR --------
    def delete_category(self, category_id: int):
        """
        Elimina la categoría y quita la relación
        con todos los productos que la usaban
        """
        products = self.product_repo.list_by_category(category_id)

        for product in products:
            self.product_repo.update_category(product.id, None)

        self.category_repo.delete(category_id)

    # -------- PRODUCTOS DE UNA CATEGORÍA --------
    def get_products(self, category_id: int):
        return self.product_repo.list_by_category(category_id)

    # -------- ASIGNAR / QUITAR PRODUCTO --------
    def add_product_to_category(self, product_id: int, category_id: int):
        self.product_repo.update_category(product_id, category_id)

    def remove_product_from_category(self, product_id: int):
        self.product_repo.update_category(product_id, None)
