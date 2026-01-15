from app.core.services.product_service import ProductService
from app.core.services.sale_service import SaleService
from app.core.sqlite_product_repo import SQLiteProductRepository
from app.core.sqlite_sale_repo import SQLiteSaleRepository

product_repo = SQLiteProductRepository()
sale_repo = SQLiteSaleRepository()

product_service = ProductService(product_repo)
sale_service = SaleService(sale_repo, product_repo)

# 1️⃣ Crear producto con stock = 1
product = product_service.create(
    sku="SKU_TEST",
    name="Producto Test",
    price=1000,
    stock=1
)

print("Producto creado:", product)

# 2️⃣ Primera venta (stock OK)
items_1 = [
    {"sku": "SKU_TEST", "quantity": 1}
]

print("\n--- Venta 1 ---")
preview_1 = sale_service.preview_sale(items_1)
print("Preview:", preview_1)

sale_1 = sale_service.create_sale(items_1)
print("Venta creada:", sale_1)

# 3️⃣ Segunda venta (sin stock)
items_2 = [
    {"sku": "SKU_TEST", "quantity": 1}
]

print("\n--- Venta 2 (sin stock) ---")
preview_2 = sale_service.preview_sale(items_2)
print("Preview:", preview_2)

sale_2 = sale_service.create_sale(items_2, force=True)
print("Venta creada forzada:", sale_2)
