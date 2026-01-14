from app.core.models import Product
from app.core.sqlite_repo import SQLiteProductRepository

class ProductService:
    def __init__(self, repo):
        self.repo = repo

    def create(self, sku: str, name: str, price: float, stock: int = 0):
        product = Product(
            id = None,
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
        product = self.repo.get_by_any(str(product_id))
        if not product:
            raise ValueError("Product not found")

        product.sku = sku
        product.name = name
        product.price = price
        product.stock = stock
        
        return self.repo.update(product)

    def delete(self, product_id: int):
        return self.repo.delete(product_id)


#'''    
if __name__ == "__main__":
    repo = SQLiteProductRepository("products.db")
    service = ProductService(repo)

    # Crear producto de prueba
    p = service.create("SKU121", "Producto de prueba 4", 12.5, 10)
    print("Creado:", p)

    # Listar
    print("Lista:", service.get_all())

    # Buscar
    print("Buscar SKU:", service.get("Producto"))
#'''
