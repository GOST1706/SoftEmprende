# Core SoftEmprende

Este documento describe **la arquitectura y responsabilidades del núcleo (core)** del sistema.

---

## 📁 Estructura del core

```
core/
├─ models.py
├─ sqlite_product_repo.py
├─ sqlite_sale_repo.py
└─ services/
   ├─ product_service.py
   └─ sale_service.py
```

---

## 🧱 MODELOS (`models.py`)

### Product

Representa un producto del inventario.

Campos:

* `id` (int | None): autoincrement, asignado por la DB
* `sku` (str): código único del producto
* `name` (str): nombre del producto
* `price` (float): precio unitario
* `stock` (int): cantidad disponible

---

### Sale

Representa una venta (cabecera).

Campos:

* `id` (int | None): autoincrement
* `date` (datetime): fecha de la venta
* `total` (float): total de la venta

---

### SaleItem

Representa un ítem dentro de una venta.

Campos:

* `id` (int | None): autoincrement
* `sale_id` (int): referencia a la venta
* `product_id` (int): referencia al producto
* `quantity` (int): cantidad vendida
* `unit_price` (float): precio unitario al momento de la venta

---

## 🗄️ REPOSITORIOS (SQLite)

Los repositorios **son la única capa que toca la base de datos**.

---

### SQLiteProductRepository

Responsable de **productos e inventario**.

Funciones:

* Crear tabla `products`
* Insertar productos
* Buscar productos por:

  * id
  * sku
  * nombre (LIKE)
* Listar productos
* Actualizar productos
* Eliminar productos

Notas:

* Guarda la base de datos en `/data/products.db`
* Compatible con ejecución normal y `.exe` (PyInstaller)

---

### SQLiteSaleRepository

Responsable de **ventas y sus ítems**.

Funciones:

* Crear tabla `sales`
* Crear tabla `sale_items`
* Insertar una venta
* Insertar ítems de venta

No maneja lógica de negocio, solo persistencia.

---

## 🧠 SERVICIOS (Lógica de negocio)

Los servicios **no conocen SQLite**, solo trabajan con repositorios.

---

### ProductService

Encapsula la lógica de productos.

Funciones:

* `create()` → crear producto
* `get(value)` → buscar por id / sku / nombre
* `get_all()` → listar productos
* `update()` → actualizar producto
* `delete()` → eliminar producto

---

### SaleService

Encapsula toda la lógica de ventas.

#### preview_sale(items)

Valida una venta **sin guardarla**.

Hace:

* Verifica existencia del producto
* Valida stock
* Calcula total

Retorna:

```python
{
  "total": float,
  "warnings": list[str],
  "can_continue": bool
}
```

---

#### create_sale(items, force=False)

Crea una venta real.

Comportamiento:

* Si `force=False` y hay warnings → no vende
* Si `force=True` → vende aunque el stock quede negativo
* Descuenta stock
* Registra venta
* Registra ítems

Retorna:

```python
{
  "sale": Sale,
  "warnings": list[str]
}
```

---

## 📌 Principios usados

* Separación de responsabilidades
* Arquitectura por capas
* Repositorios desacoplados
* Servicios reutilizables
* Preparado para UI, API o CLI


