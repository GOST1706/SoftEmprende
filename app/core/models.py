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


# Ítem de venta
@dataclass
class SaleItem:
    sale_id: int
    product_id: int
    quantity: int
    unit_price: float
    id: Optional[int] = None


# Venta
@dataclass
class Sale:
    date: datetime
    total: float
    id: Optional[int] = None
