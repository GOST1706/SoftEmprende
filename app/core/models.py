from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# Producto
@dataclass
class Product:
    sku: str
    name: str
    price: float
    stock: int
    id: Optional[int] = None


# Ítem de ventas
@dataclass
class SaleItem:
    id: Optional[int]
    sale_id: int
    product_id: int
    quantity: int
    unit_price: float


# Venta
@dataclass
class Sale:
    id: Optional[int]
    date: datetime
    total: float
