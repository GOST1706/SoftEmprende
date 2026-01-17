from app.core.sqlite_product_repo import SQLiteProductRepository
from app.core.sqlite_category_repo import SQLiteCategoryRepository
from app.core.sqlite_sale_repo import SQLiteSaleRepository

from app.core.services.product_service import ProductService
from app.core.services.category_service import CategoryService
from app.core.services.sale_service import SaleService

# Prueba actual de funcionamiento de core
def main():
    print("=== INIT REPOS ===")
    product_repo = SQLiteProductRepository("test.db")
    category_repo = SQLiteCategoryRepository("test.db")
    sale_repo = SQLiteSaleRepository("test.db")

    product_service = ProductService(product_repo)
    category_service = CategoryService(category_repo, product_repo)
    sale_service = SaleService(sale_repo, product_repo)

    print("\n=== CREATE CATEGORY ===")
    category = category_service.create("Bebidas")
    print(category)

    print("\n=== CREATE PRODUCT WITH CATEGORY ===")
    product = product_service.create(
        sku="COCA-1L",
        name="Coca Cola 1L",
        price=3500,
        stock=1,
        category_id=category.id
    )
    print(product)

    print("\n=== SALE WITH STOCK (OK) ===")
    items = [
        {"sku": "COCA-1L", "quantity": 1}
    ]
    result_ok = sale_service.create_sale(items)
    print(result_ok)

    print("\n=== SALE WITHOUT STOCK (FAIL) ===")
    result_fail = sale_service.create_sale(items)
    print(result_fail)

    print("\n=== FORCE SALE WITHOUT STOCK ===")
    result_force = sale_service.create_sale(items, force=True)
    print(result_force)

    print("\n=== DELETE CATEGORY (PRODUCT SHOULD KEEP WORKING) ===")
    category_service.delete_category(category.id)

    print("\n=== PRODUCT AFTER CATEGORY DELETE ===")
    prod = product_service.get("COCA-1L")
    print(prod)


if __name__ == "__main__":
    main()
