# Manual de Usuario - Bro Sublimados

## Contenido
1. [Introducción](#introducción)
2. [Gestión de Productos](#gestión-de-productos)
3. [Gestión de Stock](#gestión-de-stock)
4. [Registro de Ventas](#registro-de-ventas)
5. [Historial de Ventas](#historial-de-ventas)
6. [Consejos y Mejores Prácticas](#consejos-y-mejores-prácticas)

## Introducción

El Sistema de Gestión de Tienda de Bro Sublimados es una aplicación completa para administrar productos, inventario y ventas de sublimación textil y DTF.

### Características Principales

- ✅ Gestión completa de productos con variantes (talles y colores)
- ✅ Control de stock automático
- ✅ Registro de ventas con cálculo de materiales
- ✅ Alertas de stock bajo
- ✅ Estadísticas de ventas e ingresos
- ✅ Cálculo automático de metros de Film DTF y Papel de Sublimación

## Gestión de Productos

### Ver Productos

1. Click en el botón **"Productos"** en el panel lateral
2. Se mostrará una tabla con todos los productos activos
3. Columnas mostradas:
   - ID
   - Nombre
   - Tipo (Remera, Buzo, Taza, etc.)
   - Precio Base
   - Metros de Film/Papel
   - Cantidad de Variantes

### Agregar un Nuevo Producto

1. En la vista de Productos, click en **"+ Agregar Producto"**
2. Completar los campos:
   - **Nombre**: Nombre descriptivo del producto
   - **Tipo**: Seleccionar de la lista (Remera, Buzo, Taza, Sublimación, DTF, Otro)
   - **Descripción**: Detalles adicionales (opcional)
   - **Precio Base**: Precio en pesos ($)
   - **Metros de Film/Papel**: Cuántos metros usa este producto (importante para calcular consumo)
3. Click en **"Guardar"**

**Ejemplo:**
```
Nombre: Remera Oversize
Tipo: Remera
Descripción: Remera oversize estilo urbano
Precio Base: 6000
Metros de Film/Papel: 0.35
```

### Editar un Producto

**Opción 1:** Doble click sobre el producto en la tabla

**Opción 2:**
1. Click derecho sobre el producto
2. Seleccionar **"Editar"**

3. Modificar los campos necesarios
4. Click en **"Guardar"**

### Gestionar Variantes

Las variantes permiten tener diferentes combinaciones de talles y colores para cada producto.

**Abrir Gestión de Variantes:**
1. Click derecho sobre un producto
2. Seleccionar **"Gestionar Variantes"**

**Agregar Variante:**
1. Click en **"+ Agregar Variante"**
2. Completar:
   - **Talle**: S, M, L, XL, etc. (puede dejarse vacío para productos sin talle)
   - **Color**: Color específico
   - **Precio Adicional**: Monto extra sobre el precio base ($)
   - **Stock Inicial**: Cantidad disponible
3. Click en **"Guardar"**

**Ejemplo de Variantes para Remera:**
```
Talle: M, Color: Blanco, Precio Adicional: 0, Stock: 15
Talle: M, Color: Negro, Precio Adicional: 200, Stock: 10
Talle: L, Color: Blanco, Precio Adicional: 0, Stock: 12
Talle: L, Color: Negro, Precio Adicional: 200, Stock: 8
```

**Editar Variante:**
1. En la ventana de variantes, click derecho sobre una variante
2. Seleccionar **"Editar"**
3. Modificar los campos
4. Click en **"Guardar"**

**Eliminar Variante:**
1. Click derecho sobre la variante
2. Seleccionar **"Eliminar"**
3. Confirmar la eliminación

### Eliminar un Producto

1. Click derecho sobre el producto
2. Seleccionar **"Eliminar"**
3. Confirmar la eliminación

**Nota:** El producto se marca como inactivo (no se borra físicamente) para mantener el historial de ventas.

## Gestión de Stock

### Ver Stock Actual

1. Click en el botón **"Stock"** en el panel lateral
2. Se muestra una tabla con todas las variantes de productos:
   - Producto
   - Tipo
   - Talle
   - Color
   - Stock actual
   - Precio final (base + adicional)

### Alertas de Stock Bajo

- Los productos con stock ≤ 5 unidades aparecen resaltados en rojo
- En la parte superior se muestra un contador de alertas

### Actualizar Stock

El stock se actualiza **automáticamente** al registrar ventas. También puedes:

1. Ir a **Productos** → Click derecho → **Gestionar Variantes**
2. Click derecho en la variante → **Editar**
3. Modificar el campo **Stock**
4. Click en **Guardar**

## Registro de Ventas

### Crear una Nueva Venta

1. Click en **"Nueva Venta"** (botón verde en el panel lateral)
2. Completar datos del cliente:
   - **Cliente**: Nombre del cliente
   - **Notas**: Información adicional (opcional)

### Agregar Items a la Venta

1. Click en **"+ Agregar Item"**
2. Seleccionar:
   - **Producto**: Elegir de la lista desplegable
   - **Variante**: Se muestran las variantes disponibles (talle/color)
   - **Cantidad**: Unidades a vender
3. Click en **"Agregar"**

**El sistema automáticamente:**
- Verifica el stock disponible
- Muestra alerta si no hay stock suficiente
- Calcula el subtotal

**Nota:** Si una variante no tiene stock suficiente, se mostrará una advertencia. Puedes continuar de todos modos si es necesario.

4. Repetir para agregar más items
5. El **Total** se actualiza automáticamente

### Eliminar Item de la Venta

- Click en **"- Eliminar Item"** con el item seleccionado en la tabla

### Finalizar la Venta

1. Verificar que todos los items sean correctos
2. Click en **"✓ Finalizar Venta"** (botón verde)
3. Se mostrará un mensaje de confirmación con el ID de venta

**El sistema automáticamente:**
- Descuenta el stock de cada variante vendida
- Calcula el total de la venta
- Calcula los metros de Film DTF usados
- Calcula los metros de Papel de Sublimación usados
- Registra la fecha y hora

## Historial de Ventas

### Ver Ventas

1. Click en **"Ventas"** en el panel lateral
2. Se muestra:
   - Panel de estadísticas (arriba):
     - Total de ventas
     - Ingresos totales
     - Metros de Film DTF usados
     - Metros de Papel de Sublimación usados
   - Tabla con todas las ventas

### Ver Detalle de una Venta

- **Doble click** sobre cualquier venta en la tabla

Se abrirá una ventana mostrando:
- Información de la venta (fecha, cliente, total)
- Metros de materiales usados
- Notas (si las hay)
- Tabla detallada de items vendidos

## Cálculo de Materiales

### Film DTF

Se usa para:
- Remeras con estampado DTF
- Buzos
- Productos marcados como tipo "DTF"

### Papel de Sublimación

Se usa para:
- Tazas
- Productos de sublimación completa
- Productos marcados como tipo "Sublimación"

**Cálculo:**
```
Metros usados = Metros por producto × Cantidad vendida
```

**Ejemplo:**
- Remera DTF usa 0.3m por unidad
- Se venden 10 remeras
- Total: 10 × 0.3m = 3 metros de Film DTF

## Consejos y Mejores Prácticas

### Organización de Productos

1. **Usa nombres descriptivos:**
   - ✅ "Remera Oversize Urbana"
   - ❌ "Remera 1"

2. **Completa las descripciones:**
   - Incluye material, características especiales, etc.

3. **Configura correctamente los metros de film/papel:**
   - Mide cuánto material usa realmente cada producto
   - Esto te ayudará a calcular costos y consumo

### Gestión de Stock

1. **Revisa regularmente las alertas de stock bajo**
2. **Mantén stock de seguridad** de productos más vendidos
3. **Usa variantes** para diferenciar talles y colores

### Registro de Ventas

1. **Completa siempre el nombre del cliente**
   - Facilita el seguimiento de ventas
   - Útil para estadísticas por cliente

2. **Usa el campo de notas para:**
   - Fechas de entrega
   - Diseños específicos
   - Instrucciones especiales

3. **Revisa el detalle antes de finalizar**
   - Verifica cantidades
   - Confirma precios

### Respaldos

1. **Haz backup regular de `tienda_bro.db`**
   - Diariamente si hay muchas ventas
   - Semanalmente como mínimo

2. **Guarda los backups en diferentes ubicaciones:**
   - Disco duro externo
   - Nube (Google Drive, Dropbox, etc.)
   - Pendrive

### Seguridad

- No compartas la base de datos sin encriptar
- Protege el acceso al equipo donde está instalado
- Mantén backups actualizados

## Atajos de Teclado

| Acción | Método |
|--------|--------|
| Editar producto | Doble click en la tabla |
| Ver detalle de venta | Doble click en la tabla |
| Menú contextual | Click derecho |
| Actualizar vista | Botón "⟳ Actualizar" |

## Preguntas Frecuentes

**¿Puedo tener productos sin variantes?**
- Sí, pero se recomienda crear al menos una variante básica para tener control de stock.

**¿Se pueden modificar ventas ya registradas?**
- No directamente por diseño (para mantener integridad). Si necesitas corregir, contacta al administrador.

**¿Cómo cambio entre tema claro y oscuro?**
- Actualmente solo está disponible el tema oscuro. Se puede modificar en el código.

**¿Puedo exportar los datos?**
- La base de datos SQLite puede abrirse con cualquier visor de SQLite para exportar a Excel/CSV.

**¿Hay límite de productos o ventas?**
- No hay límite práctico. SQLite puede manejar millones de registros.

## Soporte Técnico

Para asistencia técnica o reportar problemas, contactar al desarrollador del sistema.

---

**Versión del Manual:** 1.0  
**Última actualización:** Diciembre 2024
