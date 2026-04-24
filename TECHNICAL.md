# Documentación Técnica - Bro Sublimados

## Arquitectura del Sistema

### Tecnologías Utilizadas

- **Python 3.11+**: Lenguaje de programación principal
- **SQLite**: Base de datos embebida (archivo `tienda_bro.db`)
- **CustomTkinter 5.2.1**: Framework para interfaz gráfica moderna
- **tkinter**: Framework GUI base de Python
- **Pillow 10.1.0**: Procesamiento de imágenes (dependencia de CustomTkinter)

### Estructura de Archivos

```
gestor-tienda-bro/
├── main.py                 # Punto de entrada de la aplicación
├── database.py             # Capa de acceso a datos (DAL)
├── gui.py                  # Interfaz gráfica de usuario
├── requirements.txt        # Dependencias Python
├── setup_example_data.py   # Script para datos de ejemplo
├── README.md               # Documentación general
├── INSTALACION.md          # Guía de instalación
├── MANUAL_USUARIO.md       # Manual de usuario
├── TECHNICAL.md            # Este archivo
└── .gitignore              # Archivos ignorados por git
```

## Capa de Datos (database.py)

### Esquema de Base de Datos

#### Tabla: productos
```sql
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    descripcion TEXT,
    precio_base REAL NOT NULL,
    metros_film REAL DEFAULT 0,
    activo INTEGER DEFAULT 1,
    fecha_creacion TEXT NOT NULL
)
```

**Propósito**: Almacena los productos principales (remeras, buzos, tazas, etc.)

**Campos clave**:
- `metros_film`: Metros de material DTF/Sublimación que usa el producto
- `activo`: Soft delete (1 = activo, 0 = eliminado)

#### Tabla: variantes
```sql
CREATE TABLE variantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER NOT NULL,
    talle TEXT,
    color TEXT,
    precio_adicional REAL DEFAULT 0,
    stock INTEGER DEFAULT 0,
    FOREIGN KEY (producto_id) REFERENCES productos (id),
    UNIQUE(producto_id, talle, color)
)
```

**Propósito**: Variantes de productos (combinaciones de talle y color) con stock individual

**Características**:
- Constraint UNIQUE previene duplicados
- Stock se maneja a nivel de variante, no de producto

#### Tabla: ventas
```sql
CREATE TABLE ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    cliente TEXT NOT NULL,
    total REAL NOT NULL,
    total_metros_film REAL DEFAULT 0,
    total_metros_papel REAL DEFAULT 0,
    notas TEXT
)
```

**Propósito**: Registro de ventas con totales agregados

**Características**:
- `total_metros_film`: Total de Film DTF usado en la venta
- `total_metros_papel`: Total de Papel de Sublimación usado
- Separación permite estadísticas de consumo de materiales

#### Tabla: detalle_ventas
```sql
CREATE TABLE detalle_ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venta_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    variante_id INTEGER,
    cantidad INTEGER NOT NULL,
    precio_unitario REAL NOT NULL,
    subtotal REAL NOT NULL,
    metros_film REAL DEFAULT 0,
    FOREIGN KEY (venta_id) REFERENCES ventas (id),
    FOREIGN KEY (producto_id) REFERENCES productos (id),
    FOREIGN KEY (variante_id) REFERENCES variantes (id)
)
```

**Propósito**: Items individuales de cada venta

**Características**:
- Desnormalización: guarda `precio_unitario` y `subtotal` para mantener histórico
- `metros_film`: Metros usados en este item específico

### Clase DatabaseManager

**Ubicación**: `database.py`

#### Métodos Principales

**Productos**:
- `agregar_producto()`: Crea un nuevo producto
- `obtener_productos()`: Lista todos los productos activos
- `obtener_producto(id)`: Obtiene un producto específico
- `actualizar_producto(id, ...)`: Actualiza campos de un producto
- `eliminar_producto(id)`: Soft delete (marca como inactivo)

**Variantes**:
- `agregar_variante()`: Crea variante con stock inicial
- `obtener_variantes(producto_id)`: Lista variantes de un producto
- `actualizar_variante()`: Modifica variante
- `actualizar_stock(variante_id, cantidad)`: Incrementa/decrementa stock
- `eliminar_variante()`: Elimina variante permanentemente

**Ventas**:
- `registrar_venta(cliente, items, notas)`: Registra venta completa (transaccional)
- `obtener_ventas()`: Lista ventas con filtros opcionales
- `obtener_venta(id)`: Obtiene venta con detalles completos

**Estadísticas**:
- `obtener_stock_bajo(limite)`: Lista variantes con stock bajo
- `obtener_estadisticas_ventas()`: Totales de ventas, ingresos y materiales

### Lógica de Negocio Importante

#### Cálculo de Materiales

La función `registrar_venta()` implementa la lógica de cálculo:

```python
# Para cada item vendido:
metros_item = producto.metros_film * cantidad

# Determinar tipo de material basado en el tipo de producto:
if 'sublimacion' in tipo_producto.lower() or 'taza' in tipo_producto.lower():
    total_metros_papel += metros_item
else:
    total_metros_film += metros_item
```

**Regla**: 
- Film DTF → Productos tipo "Remera", "Buzo", "DTF"
- Papel Sublimación → Productos tipo "Taza", "Sublimación"

#### Actualización Automática de Stock

En `registrar_venta()`, después de insertar el detalle:

```python
if variante_id:
    cursor.execute("""
        UPDATE variantes
        SET stock = stock - ?
        WHERE id = ?
    """, (cantidad, variante_id))
```

**Transaccionalidad**: Todo el proceso de venta está en una transacción. Si falla cualquier paso, se hace rollback completo.

## Capa de Presentación (gui.py)

### Clase App (CTk)

**Hereda de**: `customtkinter.CTk`

**Arquitectura**: Single-page application con cambio dinámico de contenido

#### Estructura de Navegación

```
App (ventana principal)
├── nav_frame (panel lateral)
│   ├── Productos
│   ├── Stock
│   ├── Ventas
│   └── Nueva Venta
└── frame_principal (contenido dinámico)
```

#### Vistas Principales

**1. Vista Productos** (`mostrar_productos()`)
- Tabla con todos los productos
- Botones: Agregar, Actualizar
- Menú contextual: Editar, Gestionar Variantes, Eliminar
- Diálogos modales para CRUD

**2. Vista Stock** (`mostrar_stock()`)
- Tabla con todas las variantes
- Alerta visual de stock bajo (≤5 unidades)
- Color rojo para items con stock crítico

**3. Vista Ventas** (`mostrar_ventas()`)
- Panel de estadísticas (totales)
- Tabla de ventas
- Doble click para ver detalle

**4. Nueva Venta** (`mostrar_nueva_venta()`)
- Formulario de cliente y notas
- Sistema de carrito de compras
- Validación de stock en tiempo real
- Cálculo automático de total

#### Componentes CustomTkinter Usados

- `CTkFrame`: Contenedores
- `CTkLabel`: Etiquetas de texto
- `CTkButton`: Botones
- `CTkEntry`: Campos de texto
- `CTkComboBox`: Listas desplegables
- `CTkScrollbar`: Barras de desplazamiento
- `CTkToplevel`: Ventanas modales

**Nota**: Se usa `ttk.Treeview` (tkinter estándar) para las tablas porque CustomTkinter no tiene widget de tabla nativo.

### Flujo de Datos

```
Usuario → GUI (gui.py) → DatabaseManager (database.py) → SQLite
                ↓
         Actualizar Vista
```

**Patrón**: Después de cada operación que modifica datos, se refresca la vista correspondiente.

## Manejo de Errores

### Database Layer

- Try-catch en operaciones de venta (transaccionales)
- Constraint violations → Return -1 o False
- Prints de error para debugging

### GUI Layer

- `messagebox.showerror()` para errores de usuario
- `messagebox.showinfo()` para confirmaciones
- `messagebox.askyesno()` para confirmaciones críticas

## Configuración

### Tema Visual

```python
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
```

**Modificable en**: `gui.py` líneas 11-12

### Límite de Stock Bajo

Definido en llamadas a `obtener_stock_bajo(limite=5)`

**Modificable en**: `gui.py` y lógica de alertas

## Rendimiento

### Consideraciones

- SQLite maneja millones de registros eficientemente
- Índices automáticos en PRIMARY KEY y FOREIGN KEY
- No hay índices personalizados (suficiente para caso de uso)

### Optimizaciones Potenciales

1. Agregar índice en `productos.tipo` si hay muchos productos
2. Agregar índice en `ventas.fecha` para consultas por rango
3. Paginación en vistas con muchos registros

## Seguridad

### Nivel Actual

- **SQL Injection**: Protegido (uso de parámetros preparados)
- **Autenticación**: No implementada
- **Encriptación**: Base de datos sin encriptar

### Recomendaciones para Producción

1. Agregar sistema de usuarios y contraseñas
2. Encriptar base de datos (SQLCipher)
3. Logs de auditoría
4. Backups automáticos

## Extensibilidad

### Agregar Nuevos Tipos de Productos

1. No requiere cambios en esquema
2. Agregar a lista de tipos en diálogos de GUI
3. Ajustar lógica de cálculo de materiales si necesario

### Agregar Campos a Productos

1. Modificar tabla con `ALTER TABLE`
2. Actualizar métodos en `DatabaseManager`
3. Actualizar formularios en GUI

### Reportes y Exportación

Agregar métodos en `DatabaseManager` para:
- Ventas por período
- Productos más vendidos
- Exportación a CSV/Excel

## Testing

### Tests Implementados

- `test_database.py` (temporal): Tests unitarios de capa de datos
- `setup_example_data.py`: Test de integración con datos reales

### Testing Manual

1. Ejecutar `setup_example_data.py`
2. Abrir GUI y verificar funcionalidad
3. Probar CRUD de productos
4. Probar registro de ventas
5. Verificar actualización de stock

## Deployment

### Empaquetado

Usar PyInstaller para crear ejecutable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "BroSublimados" main.py
```

### Distribución

- **Windows**: `.exe` en carpeta `dist/`
- **Linux**: binario en `dist/`
- **macOS**: `.app` bundle

**Incluir**: README.md, MANUAL_USUARIO.md

## Mantenimiento

### Backup de Base de Datos

Estrategia recomendada:
- Backup diario automático
- Rotación de 30 días
- Backup antes de actualizaciones

### Actualización de Versión

1. Hacer backup de `tienda_bro.db`
2. Actualizar código
3. Ejecutar migraciones SQL si necesario
4. Probar con backup

### Log de Cambios

Mantener CHANGELOG.md con:
- Nuevas funcionalidades
- Bugs corregidos
- Cambios en esquema de BD

## Troubleshooting

### Base de datos corrupta

```bash
sqlite3 tienda_bro.db "PRAGMA integrity_check;"
```

### Performance lento

```bash
sqlite3 tienda_bro.db "VACUUM;"
sqlite3 tienda_bro.db "ANALYZE;"
```

### Resetear base de datos

```bash
# Backup primero
cp tienda_bro.db backup_tienda_bro.db
# Eliminar
rm tienda_bro.db
# Ejecutar app para recrear
python main.py
```

## Contribución

Para contribuir al proyecto:

1. Fork del repositorio
2. Crear rama feature
3. Commits descriptivos
4. Pull request con descripción detallada

## Licencia

Proyecto privado - Bro Sublimados

---

**Versión Técnica:** 1.0  
**Última actualización:** Diciembre 2024
