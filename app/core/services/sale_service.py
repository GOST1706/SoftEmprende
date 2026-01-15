from datetime import datetime
from app.core.models import Sale, SaleItem

class SaleService:
    def __init__(self, sale_repo, product_repo):
        self.sale_repo = sale_repo
        self.product_repo = product_repo

    def preview_sale(self, items: list):
        """
        Valida la venta SIN guardarla.
        Retorna total y warnings si hay stock insuficiente.
        """
        total = 0
        warnings = []

        for it in items:
            product = self.product_repo.get_by_any(str(it["sku"]))
            if not product:
                warnings.append(f"Producto {it['sku']} no existe")
                continue

            if product.stock < it["quantity"]:
                warnings.append(
                    f"Stock insuficiente para {product.name} (hay {product.stock})"
                )

            total += product.price * it["quantity"]

        return {
            "total": total,
            "warnings": warnings,
            "can_continue": len(warnings) > 0
        }

    def create_sale(self, items: list, force: bool = False):
        """
        force=False → no vende si hay stock insuficiente
        force=True  → vende aunque quede stock negativo
        """
        preview = self.preview_sale(items)
        if preview["warnings"] and not force:
            return preview  # la UI decide

        sale = Sale(date=datetime.now(), total=0)
        sale = self.sale_repo.add_sale(sale)

        total = 0
        for it in items:
            product = self.product_repo.get_by_any(str(it["sku"]))
            if not product:
                continue

            # Descontar stock (puede quedar negativo)
            product.stock -= it["quantity"]
            self.product_repo.update(product)

            subtotal = product.price * it["quantity"]
            total += subtotal

            item = SaleItem(
                sale_id=sale.id,
                product_id=product.id,
                quantity=it["quantity"],
                unit_price=product.price
            )
            self.sale_repo.add_item(item)

        sale.total = total
        self.sale_repo.conn.execute(
            "UPDATE sales SET total=? WHERE id=?",
            (total, sale.id)
        )
        self.sale_repo.conn.commit()

        return {"sale": sale, "warnings": preview["warnings"]}
