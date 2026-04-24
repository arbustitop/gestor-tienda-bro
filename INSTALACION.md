# Guía de Instalación - Bro Sublimados

## Requisitos del Sistema

### Sistema Operativo
- Windows 10/11
- Linux (Ubuntu 20.04+, Fedora, etc.)
- macOS 10.14+

### Software Requerido
- Python 3.11 o superior (Python 3.12 también es compatible)
- pip (gestor de paquetes de Python)

## Instalación en Windows

### 1. Instalar Python

1. Descargar Python desde [python.org](https://www.python.org/downloads/)
2. Ejecutar el instalador
3. **IMPORTANTE**: Marcar la opción "Add Python to PATH"
4. Click en "Install Now"

### 2. Verificar la instalación

Abrir CMD o PowerShell y ejecutar:

```cmd
python --version
```

Debería mostrar: `Python 3.11.x` o superior

### 3. Instalar el programa

1. Descargar o clonar el repositorio
2. Abrir CMD o PowerShell en la carpeta del proyecto
3. Instalar las dependencias:

```cmd
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```cmd
python main.py
```

## Instalación en Linux

### 1. Instalar Python y tkinter

En Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
```

En Fedora:
```bash
sudo dnf install python3 python3-pip python3-tkinter
```

En Arch Linux:
```bash
sudo pacman -S python python-pip tk
```

### 2. Instalar dependencias del proyecto

```bash
cd gestor-tienda-bro
pip install -r requirements.txt
```

O con pip3:
```bash
pip3 install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
python3 main.py
```

## Instalación en macOS

### 1. Instalar Python

Usando Homebrew (recomendado):
```bash
brew install python@3.11
brew install python-tk@3.11
```

O descargar desde [python.org](https://www.python.org/downloads/)

### 2. Instalar dependencias

```bash
cd gestor-tienda-bro
pip3 install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
python3 main.py
```

## Configuración Inicial

### Primera vez que ejecutas el programa

1. Al ejecutar `python main.py` por primera vez, se creará automáticamente:
   - Base de datos SQLite (`tienda_bro.db`)
   - Tablas necesarias (productos, variantes, ventas, etc.)

2. **Opción A**: Empezar con base de datos vacía
   - Simplemente abre el programa y empieza a agregar tus productos

3. **Opción B**: Cargar datos de ejemplo
   - Ejecuta el script de datos de ejemplo:
   ```bash
   python setup_example_data.py
   ```
   - Esto crea productos, variantes y ventas de ejemplo para familiarizarte con el sistema

## Datos de Ejemplo

El script `setup_example_data.py` crea:

- 7 productos diferentes (remeras, buzos, tazas, etc.)
- 83 variantes (combinaciones de talles y colores)
- 3 ventas de ejemplo con clientes reales
- Stock inicial para todos los productos

Para ejecutarlo:
```bash
python setup_example_data.py
```

## Solución de Problemas

### Error: "No module named 'tkinter'"

**En Windows:**
- Reinstalar Python desde python.org asegurándose de incluir "tcl/tk and IDLE"

**En Linux:**
- Ubuntu/Debian: `sudo apt install python3-tk`
- Fedora: `sudo dnf install python3-tkinter`
- Arch: `sudo pacman -S tk`

**En macOS:**
- `brew install python-tk@3.11`

### Error: "No module named 'customtkinter'"

Instalar las dependencias:
```bash
pip install -r requirements.txt
```

### Error: "Permission denied" en Linux/macOS

Agregar permisos de ejecución:
```bash
chmod +x main.py
./main.py
```

O usar:
```bash
python3 main.py
```

### La ventana se ve borrosa en Windows

- Click derecho en `python.exe`
- Propiedades → Compatibilidad
- Marcar "Invalidar el comportamiento de escala de PPP alto"
- Seleccionar "Aplicación"

## Actualización

Para actualizar el programa:

1. Descargar la nueva versión
2. **IMPORTANTE**: Hacer copia de seguridad de `tienda_bro.db`
3. Reemplazar los archivos del programa (excepto la base de datos)
4. Actualizar dependencias:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

## Respaldo de Datos

### Hacer backup

Simplemente copia el archivo `tienda_bro.db` a una ubicación segura:

```bash
# Linux/macOS
cp tienda_bro.db backup_tienda_$(date +%Y%m%d).db

# Windows (PowerShell)
Copy-Item tienda_bro.db -Destination "backup_tienda_$(Get-Date -Format 'yyyyMMdd').db"
```

### Restaurar backup

Reemplaza `tienda_bro.db` con tu archivo de backup.

## Desinstalación

1. Cerrar la aplicación
2. Eliminar la carpeta del proyecto
3. Opcional: desinstalar paquetes Python:
   ```bash
   pip uninstall customtkinter Pillow
   ```

## Soporte

Para reportar problemas o solicitar ayuda, contactar al desarrollador o crear un issue en el repositorio del proyecto.
