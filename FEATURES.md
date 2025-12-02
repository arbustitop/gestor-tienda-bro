# 🎯 Características Detalladas

## Funcionalidades Implementadas

### 1. Sistema de Base de Datos SQLite

#### Tablas Principales
- **products**: Almacena información completa de productos
  - ID, nombre, tipo, talle, color
  - Precio, stock actual
  - Metros de tela DTF y vinilo para sublimación
  - Tipo de impresión
  - Timestamps de creación y actualización

- **sales**: Registro de ventas
  - ID, nombre del cliente
  - Fecha de venta
  - Total de la venta
  - Total de metros de tela y vinilo utilizados
  - Notas adicionales

- **sale_items**: Detalle de productos en cada venta
  - Relación con venta y producto
  - Cantidad, precio unitario, subtotal
  - Metros de materiales por item

- **migrations**: Control de versiones de esquema
  - Sistema de migraciones automáticas
  - Permite actualizaciones sin pérdida de datos

#### Características de la Base de Datos
- ✅ Creación automática en primera ejecución
- ✅ Migraciones automáticas
- ✅ Transacciones seguras con rollback
- ✅ Relaciones foreign key
- ✅ Índices para búsquedas rápidas

### 2. Gestión de Productos (CRUD Completo)

#### Crear Producto
- Formulario completo con validación
- Campos: nombre, tipo, talle, color, precio, stock
- Campos especiales: metros de tela, metros de vinilo, tipo de impresión
- Validación de datos obligatorios
- Precios y stock no pueden ser negativos

#### Leer/Listar Productos
- Vista de tabla con todos los productos
- Columnas: ID, nombre, tipo, talle, color, precio, stock, materiales
- Indicador visual de stock bajo (rojo)
- Paginación eficiente

#### Actualizar Producto
- Formulario pre-llenado con datos actuales
- Actualización de stock sin crear nuevo producto
- Actualización de precios y materiales
- Timestamp de última actualización

#### Eliminar Producto
- Confirmación antes de eliminar
- Previene eliminación accidental
- Manejo de errores

#### Búsqueda y Filtros
- Búsqueda por nombre, color o talle
- Filtro de productos con stock bajo (≤5 unidades)
- Búsqueda en tiempo real
- Resultados instantáneos

### 3. Sistema de Ventas

#### Proceso de Venta
1. **Selección de Cliente**: Entrada de nombre del cliente
2. **Carrito de Compras**: 
   - Búsqueda de productos disponibles
   - Selección con validación de stock
   - Entrada de cantidad por producto
   - Vista previa del carrito
3. **Cálculos Automáticos**:
   - Subtotal por producto
   - Total de la venta
   - Metros de tela DTF utilizados
   - Metros de vinilo para sublimación
4. **Confirmación y Registro**:
   - Actualización automática de stock
   - Registro de la transacción
   - Generación de ID de venta

#### Validaciones de Venta
- ✅ Cliente obligatorio
- ✅ Al menos un producto en el carrito
- ✅ Verificación de stock disponible
- ✅ Prevención de sobreventa
- ✅ Transacciones atómicas (todo o nada)

#### Historial de Ventas
- Vista completa de todas las ventas
- Información: cliente, fecha, total, materiales
- Contador de items por venta
- Detalle expandible de cada venta

#### Detalles de Venta
- Ventana modal con información completa
- Lista de productos vendidos
- Cantidades, precios, subtotales
- Materiales utilizados por producto
- Total de tela y vinilo

#### Filtros de Ventas
- Ver todas las ventas
- Filtrar por fecha de hoy
- Buscar por nombre de cliente
- Ordenamiento cronológico

### 4. Cálculo de Materiales

#### DTF (Direct to Film)
- Se especifica metros de tela por producto
- Cálculo automático: `metros_tela * cantidad`
- Acumulación en venta: suma de todos los productos
- Reporte en estadísticas diarias y mensuales

#### Sublimación
- Se especifica metros de vinilo por producto
- Cálculo automático: `metros_vinilo * cantidad`
- Acumulación en venta: suma de todos los productos
- Ideal para tazas, gorras, etc.

#### Usos del Cálculo
- Control de inventario de materiales
- Proyección de compras
- Costeo por venta
- Estadísticas de consumo

### 5. Estadísticas y Métricas

#### Dashboard Principal
- **Ventas de Hoy**: Total en pesos y cantidad
- **Materiales Usados Hoy**: Tela y vinilo en metros
- **Productos con Stock Bajo**: Contador con alerta
- **Top 5 Productos**: Los más vendidos con métricas

#### Estadísticas Detalladas
- **Resumen Diario**:
  - Ventas totales del día
  - Cantidad de transacciones
  - Materiales consumidos
  - Alertas de stock

- **Resumen Mensual**:
  - Ingresos del mes
  - Número de ventas
  - Tendencias

- **Inventario**:
  - Valor total en stock
  - Unidades totales
  - Distribución por tipo

- **Top 10 Productos Más Vendidos**:
  - Nombre del producto
  - Cantidad vendida
  - Ingresos generados
  - Número de ventas

- **Distribución por Tipo**:
  - Remeras, Buzos, Tazas, etc.
  - Cantidad de SKUs
  - Stock total por tipo

- **Mejores Clientes**:
  - Top 10 por gasto
  - Cantidad de compras
  - Total gastado

- **Ventas por Período**:
  - Últimos 7 días
  - Ventas por fecha
  - Totales diarios

### 6. Exportación de Reportes (CSV)

#### Exportar Productos
- Archivo CSV con todos los productos
- Columnas: ID, nombre, tipo, talle, color, precio, stock, materiales
- Compatible con Excel y Google Sheets
- Encoding UTF-8 para caracteres especiales

#### Exportar Ventas
- Historial completo de ventas
- Columnas: ID, cliente, fecha, total, materiales, notas
- Filtros opcionales por fecha
- Ideal para contabilidad

#### Exportar Stock Bajo
- Lista de productos que necesitan reposición
- Threshold configurable (default: ≤5 unidades)
- Para pedidos a proveedores
- Columnas relevantes para compras

#### Exportar Estadísticas
- Reporte completo con métricas
- Ventas del día y período
- Top productos
- Valor de inventario
- Formato profesional

#### Exportar Detalle de Venta
- Exportación individual por venta
- Header con datos del cliente
- Lista detallada de productos
- Totales de materiales
- Como recibo o comprobante

### 7. Interfaz Gráfica (CustomTkinter)

#### Diseño General
- **Sidebar de Navegación**:
  - Logo/título de la aplicación
  - Botones para cada sección
  - Nueva Venta destacada en verde
  - Navegación intuitiva

- **Área de Contenido Principal**:
  - Cambia según la sección activa
  - Layout responsive
  - Scrollbars cuando es necesario
  - Títulos claros por sección

#### Tema Visual
- Modo oscuro elegante
- Colores consistentes
- Tema azul (configurable)
- Contraste adecuado
- Tipografía legible

#### Componentes Interactivos
- **Botones**:
  - Estados hover
  - Colores semánticos (verde=crear, rojo=eliminar)
  - Iconos emoji para claridad
  - Ancho y alto consistentes

- **Tablas**:
  - Headers con texto en bold
  - Filas alternadas visualmente
  - Scroll vertical
  - Botones de acción inline

- **Formularios**:
  - Labels claros
  - Placeholders informativos
  - Validación en tiempo real
  - Mensajes de error descriptivos

- **Diálogos Modales**:
  - Para crear/editar
  - Para ver detalles
  - Para ingresar cantidades
  - Bloqueo de ventana padre

#### Experiencia de Usuario
- Confirmaciones para acciones destructivas
- Mensajes de éxito/error claros
- Feedback visual inmediato
- Shortcuts de teclado (Enter en diálogos)
- Navegación fluida entre secciones

### 8. Arquitectura del Código

#### Estructura Modular
```
src/
├── models/          # Lógica de negocio y datos
│   ├── database.py  # Conexión y migraciones
│   ├── product.py   # Operaciones de productos
│   └── sale.py      # Operaciones de ventas
├── views/           # Interfaces gráficas
│   ├── main_window.py      # Ventana principal
│   ├── products_view.py    # Vista de productos
│   ├── sales_view.py       # Vista de ventas
│   ├── new_sale_view.py    # Crear venta
│   ├── statistics_view.py  # Estadísticas
│   └── export_view.py      # Exportación
└── utils/           # Utilidades
    ├── statistics.py       # Cálculos estadísticos
    └── csv_exporter.py     # Exportación CSV
```

#### Principios de Diseño
- **Separación de Responsabilidades**: Models, Views, Utils
- **DRY (Don't Repeat Yourself)**: Funciones reutilizables
- **Código Documentado**: Docstrings en todas las clases y métodos
- **Manejo de Errores**: Try-except con rollback
- **Transacciones Seguras**: Commits y rollbacks apropiados

#### Comentarios en Código
- Docstrings de módulos
- Docstrings de clases
- Docstrings de métodos
- Comentarios inline cuando es necesario
- Español para mejor comprensión

### 9. Características de Calidad

#### Robustez
- Validación de entrada en todos los formularios
- Manejo de excepciones
- Transacciones de base de datos seguras
- Rollback automático en errores

#### Mantenibilidad
- Código modular y organizado
- Nombres descriptivos
- Funciones pequeñas y enfocadas
- Fácil de extender

#### Usabilidad
- Interfaz intuitiva
- Mensajes claros
- Feedback visual
- Prevención de errores

#### Performance
- Consultas SQL optimizadas
- Índices en tablas
- Carga eficiente de datos
- UI responsive

### 10. Casos de Uso Cubiertos

1. **Dueño de tienda pequeña**: Gestionar productos y ventas diarias
2. **Control de inventario**: Saber qué reponer
3. **Cálculo de materiales**: Cuánta tela/vinilo se usa
4. **Contabilidad**: Exportar ventas a CSV
5. **Análisis de ventas**: Ver qué productos funcionan mejor
6. **Gestión de clientes**: Histórico de compras
7. **Proyecciones**: Estadísticas para decisiones de negocio

## Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal
- **SQLite3**: Base de datos embebida
- **CustomTkinter 5.2.1**: Framework de GUI moderna
- **Pillow 10.1.0**: Manejo de imágenes (requerido por CustomTkinter)
- **CSV (estándar)**: Exportación de datos

## Ventajas del Sistema

1. **Sin costo de licencias**: Todo open source
2. **No requiere internet**: Funciona offline
3. **Portable**: Un solo archivo de base de datos
4. **Fácil de respaldar**: Solo copiar tienda.db
5. **Escalable**: Se puede migrar a sistema más grande
6. **Personalizable**: Código fuente disponible
7. **Multiplataforma**: Windows, Linux, macOS

## Limitaciones Conocidas

1. **Un usuario a la vez**: SQLite no maneja concurrencia alta
2. **Requiere GUI**: No funciona en servidores sin X11
3. **Local**: No es multi-tienda por defecto
4. **Sin facturación electrónica**: Para AFIP/SUNAT requiere integración

## Posibles Extensiones Futuras

- [ ] Integración con facturación electrónica
- [ ] Sistema de usuarios y permisos
- [ ] Backup automático a la nube
- [ ] Reportes en PDF
- [ ] Gráficos de ventas
- [ ] Sistema de descuentos y promociones
- [ ] Gestión de proveedores
- [ ] Control de gastos
- [ ] App móvil complementaria
- [ ] API REST para integraciones
