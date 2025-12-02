# 🚀 Guía Rápida de Inicio

## Instalación en 3 Pasos

### 1. Instalar Python
Si no tienes Python instalado:

**Windows:**
- Descarga desde [python.org](https://www.python.org/downloads/)
- Asegúrate de marcar "Add Python to PATH"

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

**macOS:**
```bash
brew install python3
brew install python-tk
```

### 2. Instalar Dependencias
```bash
cd gestor-tienda-bro
pip install -r requirements.txt
```

### 3. Ejecutar
```bash
python main.py
```

## Primer Uso - Tutorial 5 Minutos

### Paso 1: Agregar tu Primer Producto (1 min)

1. Click en **"Productos"** en el menú lateral
2. Click en **"➕ Nuevo Producto"**
3. Llena el formulario:
   ```
   Nombre: Remera Lisa
   Tipo: Remera
   Talle: M
   Color: Negro
   Precio: 5000
   Stock: 10
   Metros Tela: 0.5
   Tipo Impresión: DTF
   ```
4. Click **"Guardar"**

✅ ¡Primer producto creado!

### Paso 2: Realizar tu Primera Venta (2 min)

1. Click en **"Nueva Venta"** (botón verde)
2. Escribe nombre del cliente: "Juan Pérez"
3. En la lista de productos, busca tu remera
4. Click **"Agregar"**
5. Ingresa cantidad: 2
6. Verifica el carrito:
   - Total: $10000
   - Tela: 1.0m
7. Click **"Completar Venta"**

✅ ¡Primera venta registrada!

### Paso 3: Ver Estadísticas (1 min)

1. Click en **"Dashboard"**
2. Observa:
   - Ventas del día: $10000
   - Tela usada: 1.0m
   - Stock actualizado automáticamente

✅ ¡Sistema funcionando!

### Paso 4: Agregar Más Productos (1 min)

Agrega estos productos comunes:

**Remeras:**
```
Nombre: Remera Estampada
Tipo: Remera
Talle: L
Color: Blanco
Precio: 6500
Stock: 15
Metros Tela: 0.6
Tipo Impresión: DTF
```

**Buzos:**
```
Nombre: Buzo Canguro
Tipo: Buzo
Talle: L
Color: Gris
Precio: 12000
Stock: 8
Metros Tela: 1.2
Tipo Impresión: DTF
```

**Tazas:**
```
Nombre: Taza Sublimada
Tipo: Taza
Talle: (dejar vacío)
Color: Blanco
Precio: 3000
Stock: 20
Metros Vinilo: 0.15
Tipo Impresión: Sublimación
```

## Flujo de Trabajo Diario

### Mañana
1. Abrir aplicación
2. Revisar **Dashboard**
3. Verificar productos con **Stock Bajo**

### Durante el día
1. Hacer ventas con **"Nueva Venta"**
2. Agregar productos nuevos según necesidad
3. Actualizar stock si llegan productos

### Fin del día
1. Ver **"Estadísticas"**
2. Revisar ventas del día
3. Exportar reporte si es necesario:
   - Click **"Exportar"**
   - Elegir **"Exportar Ventas"**
   - Guardar archivo

### Fin de mes
1. **"Estadísticas"** → Ver "Este Mes"
2. **"Exportar"** → **"Exportar Estadísticas"**
3. Guardar para contabilidad

## Atajos y Tips

### ⌨️ Atajos de Teclado
- `Enter` en diálogos = Confirmar
- `Esc` en diálogos = Cancelar
- Búsqueda en tiempo real al escribir

### 💡 Tips Útiles

**Stock Bajo:**
- Revísalo diariamente
- Exporta a CSV para hacer pedidos
- El threshold es 5 unidades

**Materiales:**
- DTF usa "Metros Tela"
- Sublimación usa "Metros Vinilo"
- Se calculan automáticamente en ventas

**Búsqueda:**
- Busca por nombre, color o talle
- No necesitas ser exacto
- Funciona en tiempo real

**Ventas:**
- Siempre ponle nombre al cliente
- Puedes agregar notas opcionales
- El stock se actualiza solo

**Exportación:**
- Los CSV se abren con Excel
- También con Google Sheets
- Guárdalos periódicamente

## Resolución de Problemas Comunes

### No se abre la aplicación
```bash
# Verifica Python instalado
python --version

# Reinstala dependencias
pip install -r requirements.txt --upgrade

# Intenta con python3
python3 main.py
```

### Error "No module named 'customtkinter'"
```bash
pip install customtkinter
```

### Error "Database is locked"
- Cierra otras instancias de la app
- Reinicia la aplicación

### Los cambios no se guardan
- Verifica hacer click en "Guardar"
- Revisa mensajes de error en pantalla

### Stock negativo después de vender
- ¡Eso no debería pasar!
- El sistema valida stock antes de vender
- Si sucede, reporta el bug

## Personalización

### Cambiar Tema
Edita `src/views/main_window.py`:
```python
ctk.set_appearance_mode("dark")  # o "light"
ctk.set_default_color_theme("blue")  # o "green", "dark-blue"
```

### Cambiar Threshold de Stock Bajo
En las funciones de búsqueda, cambia el parámetro:
```python
threshold=5  # Cambiar a tu preferencia
```

### Agregar Campos Personalizados
Modifica las tablas en `src/models/database.py` y los formularios correspondientes.

## Backup y Seguridad

### Hacer Backup
```bash
# Simplemente copia el archivo
cp db/tienda.db db/tienda_backup_$(date +%Y%m%d).db
```

### Restaurar Backup
```bash
# Copia el backup sobre el archivo actual
cp db/tienda_backup_20231215.db db/tienda.db
```

### Backup Automático (Opcional)
Crea un script de backup:

**Linux/Mac (backup.sh):**
```bash
#!/bin/bash
cp db/tienda.db "db/backup/tienda_$(date +%Y%m%d_%H%M%S).db"
```

**Windows (backup.bat):**
```batch
@echo off
copy db\tienda.db "db\backup\tienda_%date:~-4,4%%date:~-7,2%%date:~-10,2%.db"
```

## Recursos Adicionales

- **README.md**: Documentación completa
- **FEATURES.md**: Características detalladas
- **GitHub Issues**: Reportar problemas
- **GitHub Discussions**: Hacer preguntas

## Próximos Pasos

Después de dominar lo básico:

1. Explora todas las **Estadísticas**
2. Prueba todos los **filtros de búsqueda**
3. Exporta diferentes **tipos de reportes**
4. Personaliza para tu negocio específico
5. Contribuye con mejoras al proyecto

---

**¿Listo?** ¡Ejecuta `python main.py` y comienza a gestionar tu tienda! 🎉
