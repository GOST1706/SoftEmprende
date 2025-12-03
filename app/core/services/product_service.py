from core.models import Product

class ProductService:
    def __init__(self, repo):
        self.repo = repo

    def create(self, sku: str, name: str, price: float, stock: int = 0):
        product = Product(
            sku=sku,
            name=name,
            price=price,
            stock=stock
        )
        return self.repo.add(product)

    def get_all(self):
        return self.repo.list()

    # Buscar por ID, SKU o nombre
    def get(self, value: str):
        product = self.repo.get_by_any(value)
        if not product:
            raise ValueError("Product not found")
        return product

    # Actualiza todos los campos del producto
    def update(self, product_id: int, sku: str, name: str, price: float, stock: int):
        product = self.repo.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        product.sku = sku
        product.name = name
        product.price = price
        product.stock = stock
        
        return self.repo.update(product)

    def delete(self, product_id: int):
        return self.repo.delete(product_id)