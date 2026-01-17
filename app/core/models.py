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
    category_id: Optional[int] = None
    id: Optional[int] = None

# Categoría
@dataclass
class Category:
    name: str
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
