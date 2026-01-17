from app.core.models import Product

class ProductService:
    def __init__(self, repo):
        self.repo = repo

    # ------------------------------
    # CREATE
    # ------------------------------
    def create(
        self,
        sku: str,
        name: str,
        price: float,
        stock: int = 0,
        category_id: int | None = None
    ):
        product = Product(
            id=None,
            sku=sku,
            name=name,
            price=price,
            stock=stock,
            category_id=category_id
        )
        return self.repo.add(product)

    # ------------------------------
    # READ
    # ------------------------------
    def get_all(self):
        return self.repo.list()

    def get(self, value: str):
        product = self.repo.get_by_any(value)
        if not product:
            raise ValueError("Product not found")
        return product

    def get_by_category(self, category_id: int):
        return self.repo.list_by_category(category_id)

    # ------------------------------
    # UPDATE
    # ------------------------------
    def update(
        self,
        product_id: int,
        sku: str,
        name: str,
        price: float,
        stock: int,
        category_id: int | None
    ):
        product = self.repo.get_by_any(str(product_id))
        if not product:
            raise ValueError("Product not found")

        product.sku = sku
        product.name = name
        product.price = price
        product.stock = stock
        product.category_id = category_id

        return self.repo.update(product)

    # 👉 helpers limpios para UI
    def assign_category(self, product_id: int, category_id: int):
        self.repo.update_category(product_id, category_id)

    def remove_category(self, product_id: int):
        self.repo.update_category(product_id, None)

    # ------------------------------
    # DELETE
    # ------------------------------
    def delete(self, product_id: int):
        return self.repo.delete(product_id)
