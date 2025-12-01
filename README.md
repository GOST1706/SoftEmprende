# SoftEmprende *(Una Aplicación Para Emprendedores)*

<p align="center">
  <img src="/app/ui/images/SoftEmprende.png" width="450">
</p>

Sistema de gestión para pequeños y medianos emprendimientos: ventas, inventario, compras, gastos, clientes, proveedores y reportes.

El propósito es entregar una solución simple, rápida y modular que funcione para cualquier tipo de negocio: tiendas, servicios, comida, productos físicos, etc.

---

## 📁 Estructura del Proyecto

/app  
 ├─ /ui        → Interfaces gráficas (dashboard, POS, formularios, paneles)  
 ├─ /core      → Lógica del negocio (ventas, inventario, compras, usuarios)  
 ├─ /data      → Base de datos local (SQLite) + API remota  
 ├─ /sync      → Sincronización entre datos locales y la nube  
 ├─ /utils     → Funciones auxiliares  
 └─ main.py    → Punto de entrada del sistema  

---

## 🚀 Objetivo del Proyecto

Crear un software flexible que permita administrar cualquier emprendimiento, ofreciendo herramientas como:

- Punto de venta (POS) rápido y fácil de usar.  
- Gestión de productos y servicios.  
- Control de inventario (manual, automático o mixto).  
- Registro de compras y gastos.  
- Reportes detallados de ventas, movimientos y utilidades.  
- Gestión de proveedores, usuarios y roles.  
- Sincronización local ↔ nube para trabajar offline.  

---

## 🛠 Tecnologías previstas

- **Python**  
- **SQLite**  
- **Framework de UI a definir** (Tkinter, PyQt, Flet, etc.)  
- **REST API** para sincronización remota (en segunda fase)  

---

## 📄 Documentación por carpeta

Cada submódulo tendrá su README:

- **app.md**  
- **ui.md**  
- **core.md**  
- **data.md**  
- **sync.md**  
- **utils.md**  

---

## 📌 Estado actual
Etapa de arquitectura y definición de módulos principales.  
Se están diseñando pantallas, flujos y estructura interna del sistema.

---

## 👤 Autor
Desarrollado por **Jaiver Buitrago**, estudiante de Ingeniería Electrónica.  
Proyecto orientado a aprendizaje y aplicación real en negocios.
