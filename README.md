# 🛍️ Gestor de Tienda Bro

Sistema completo de gestión de tienda para productos personalizados (remeras, buzos, tazas, etc.) con control de stock, ventas y cálculo automático de materiales (DTF y sublimación).

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.1-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 📋 Características Principales

### Gestión de Productos
- ✅ **CRUD completo** de productos con todos los detalles
- 🎨 Soporte para talles, colores y tipos de productos
- 💰 Control de precios y stock
- 📏 Cálculo automático de metros de tela/vinilo por producto
- 🎯 Tipos de impresión (DTF, Sublimación, etc.)
- 🔍 Búsqueda rápida por nombre, color o talle
- ⚠️ Alertas de stock bajo (≤5 unidades)

### Gestión de Ventas
- 📝 Registro completo de ventas con cliente y fecha
- 🛒 Sistema de carrito de compras intuitivo
- 📊 Detalle completo de cada venta
- 🔄 **Actualización automática de stock** al vender
- 📐 **Cálculo automático de materiales usados** (tela DTF y vinilo para sublimación)
- 📅 Filtrado por fecha y cliente
- 💳 Cálculo automático de totales

### Estadísticas y Reportes
- 📈 Dashboard con métricas del día
- 🏆 Productos más vendidos
- 💰 Ingresos diarios y mensuales
- 📊 Valor total del inventario
- 👥 Estadísticas de clientes
- 📉 Ventas de los últimos 7 días
- 🔄 Actualización en tiempo real

### Exportación
- 📥 **Exportar a CSV** todos los reportes
- 📋 Exportar productos, ventas, stock bajo
- 📊 Reporte de estadísticas completo
- 💾 Compatible con Excel y Google Sheets

### Interfaz Gráfica
- 🎨 Interfaz moderna con **CustomTkinter**
- 🌓 Tema oscuro elegante
- 📱 Diseño responsive y adaptable
- ⚡ Navegación rápida e intuitiva
- 🖱️ Controles fáciles de usar

### Base de Datos
- 💾 **SQLite** - Base de datos local (tienda.db)
- 🔄 **Migraciones automáticas**
- 🔒 Transacciones seguras
- 📊 Relaciones entre tablas bien definidas

## 📁 Estructura del Proyecto

```
gestor-tienda-bro/
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Este archivo
├── .gitignore             # Archivos ignorados por Git
├── db/                    # Base de datos (creada automáticamente)
│   └── tienda.db         # Base de datos SQLite
├── src/                   # Código fuente
│   ├── models/           # Modelos de datos
│   │   ├── database.py  # Conexión y migraciones
│   │   ├── product.py   # Modelo de productos
│   │   └── sale.py      # Modelo de ventas
│   ├── views/            # Interfaces gráficas
│   │   ├── main_window.py      # Ventana principal
│   │   ├── products_view.py    # Vista de productos
│   │   ├── sales_view.py       # Vista de ventas
│   │   ├── new_sale_view.py    # Nueva venta
│   │   ├── statistics_view.py  # Estadísticas
│   │   └── export_view.py      # Exportación
│   └── utils/            # Utilidades
│       ├── statistics.py # Cálculos estadísticos
│       └── csv_exporter.py # Exportación a CSV
└── assets/               # Recursos (iconos, imágenes)
    └── icons/           # Iconos de la aplicación
```

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar el Repositorio
```bash
git clone https://github.com/arbustitop/gestor-tienda-bro.git
cd gestor-tienda-bro
```

### Paso 2: Crear Entorno Virtual (Recomendado)
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar la Aplicación
```bash
python main.py
```

¡Listo! La aplicación se abrirá y creará automáticamente la base de datos en la primera ejecución.

## 📖 Guía de Uso

### 1. Dashboard
Al iniciar la aplicación, verás el dashboard con:
- Ventas del día actual
- Metros de tela y vinilo usados hoy
- Productos con stock bajo
- Top 5 productos más vendidos

### 2. Gestión de Productos

#### Agregar Producto
1. Click en "Productos" en el menú lateral
2. Click en "➕ Nuevo Producto"
3. Completa los datos:
   - **Nombre**: Ej: "Remera Lisa"
   - **Tipo**: Ej: "Remera", "Buzo", "Taza"
   - **Talle**: Ej: "M", "L", "XL" (opcional)
   - **Color**: Ej: "Negro", "Blanco" (opcional)
   - **Precio**: Precio de venta
   - **Stock**: Cantidad disponible
   - **Metros Tela**: Metros de tela DTF por unidad
   - **Metros Vinilo**: Metros de vinilo para sublimación
   - **Tipo Impresión**: "DTF", "Sublimación", etc.
4. Click en "Guardar"

#### Editar/Eliminar Producto
- Click en ✏️ para editar
- Click en 🗑️ para eliminar (con confirmación)

#### Buscar Productos
- Usa la barra de búsqueda para filtrar por nombre, color o talle
- Click en "Stock Bajo" para ver productos con ≤5 unidades
- Click en "Todos" para ver el listado completo

### 3. Realizar una Venta

1. Click en "Nueva Venta" (botón verde)
2. Ingresa el nombre del cliente
3. Busca y selecciona productos del lado izquierdo
4. Click en "Agregar" e ingresa la cantidad
5. Revisa el carrito del lado derecho
6. Verifica los totales (dinero, tela, vinilo)
7. Click en "Completar Venta"

**Nota**: El stock se actualiza automáticamente y se calculan los materiales usados.

### 4. Ver Historial de Ventas

1. Click en "Ventas" en el menú
2. Navega por todas las ventas realizadas
3. Usa "Ventas de Hoy" para ver solo las de hoy
4. Busca por nombre de cliente
5. Click en 👁️ "Ver" para ver detalles completos

### 5. Estadísticas

Click en "Estadísticas" para ver:
- Resumen del día y del mes
- Valor total del inventario
- Top 10 productos más vendidos
- Distribución por tipo de producto
- Mejores clientes
- Ventas de los últimos 7 días

### 6. Exportar Reportes

1. Click en "Exportar"
2. Selecciona el tipo de reporte:
   - **Productos**: Listado completo con stock
   - **Ventas**: Historial de ventas
   - **Stock Bajo**: Productos que necesitan reposición
   - **Estadísticas**: Reporte completo de métricas
3. Elige la ubicación y nombre del archivo
4. Abre con Excel, Google Sheets o cualquier editor CSV

## 💡 Casos de Uso

### Ejemplo 1: Vender una Remera
```
Producto: Remera Lisa DTF - Talle M - Color Negro
Precio: $5000
Stock: 10 unidades
Tela DTF: 0.5m por unidad

Al vender 2 unidades:
- Se descuentan 2 del stock (quedan 8)
- Se cobra $10000
- Se registran 1.0m de tela usados
- Se guarda el detalle con cliente y fecha
```

### Ejemplo 2: Control de Stock Bajo
```
1. Dashboard muestra "3 productos con stock bajo"
2. Click en "Productos" → "Stock Bajo"
3. Se muestran todos los productos con ≤5 unidades
4. Exportar a CSV para hacer pedido al proveedor
```

### Ejemplo 3: Reporte Mensual
```
1. Click en "Estadísticas"
2. Ver "Este Mes": Ingresos Mensuales y cantidad de ventas
3. Ver productos más vendidos del período
4. Click en "Exportar" → "Estadísticas"
5. Guardar reporte para contabilidad
```

## 🔧 Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje de programación
- **CustomTkinter 5.2.1**: Framework para GUI moderna
- **SQLite3**: Base de datos embebida
- **Pillow 10.1.0**: Procesamiento de imágenes

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Notas Técnicas

### Base de Datos
La base de datos se crea automáticamente en `db/tienda.db` en la primera ejecución. Las tablas incluyen:
- **products**: Productos con stock y materiales
- **sales**: Registro de ventas
- **sale_items**: Detalle de productos por venta
- **migrations**: Control de versiones de esquema

### Cálculo de Materiales
- **Tela DTF**: Se especifica en metros por producto
- **Vinilo Sublimación**: Se especifica en metros por producto
- En cada venta se multiplica por la cantidad vendida
- Se acumula en el total de la venta

### Stock Bajo
Se considera stock bajo cuando un producto tiene 5 o menos unidades. El threshold se puede ajustar en el código.

## 🐛 Solución de Problemas

### Error: "No module named 'customtkinter'"
```bash
pip install customtkinter
```

### Error: "Database is locked"
Cierra otras instancias de la aplicación que puedan estar usando la base de datos.

### La ventana no se muestra correctamente
Verifica que tengas Python 3.8 o superior y las dependencias instaladas correctamente.

## 📞 Soporte

Para reportar problemas o sugerir mejoras, abre un issue en GitHub.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## ✨ Autor

Desarrollado con ❤️ para gestionar tiendas de productos personalizados.

---

**¡Gracias por usar Gestor de Tienda Bro!** 🚀
