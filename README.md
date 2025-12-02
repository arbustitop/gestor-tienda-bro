# Bro Sublimados - Sistema de Gestión de Tienda

Sistema completo de gestión de tienda y stock para Bro Sublimados (sublimación textil y DTF).

## Características

### Gestión de Productos
- CRUD completo de productos (remeras, buzos, tazas, etc.)
- Soporte para múltiples variantes por producto (talles y colores)
- Gestión de precios base y precios adicionales por variante
- Configuración de metros de film/papel por producto

### Gestión de Stock
- Control de inventario por variante
- Actualización automática de stock al registrar ventas
- Alertas de stock bajo
- Vista consolidada de todo el inventario

### Registro de Ventas
- Registro completo de ventas con fecha y cliente
- Detalle de productos vendidos con cantidades y precios
- Cálculo automático de metros de Film DTF y Papel de Sublimación usados
- Historial completo de ventas con filtros
- Estadísticas de ventas e ingresos

## Tecnologías

- **Python 3.11+**: Lenguaje principal
- **SQLite**: Base de datos embebida
- **CustomTkinter**: Interfaz gráfica moderna y atractiva
- **tkinter**: Framework GUI base

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/arbustitop/gestor-tienda-bro.git
cd gestor-tienda-bro
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Para ejecutar la aplicación:

```bash
python main.py
```

O en sistemas Unix/Linux:
```bash
python3 main.py
```

## Estructura del Proyecto

```
gestor-tienda-bro/
├── main.py          # Punto de entrada de la aplicación
├── database.py      # Gestión de base de datos SQLite
├── gui.py           # Interfaz gráfica con CustomTkinter
├── requirements.txt # Dependencias del proyecto
└── README.md        # Este archivo
```

## Base de Datos

La aplicación utiliza SQLite con las siguientes tablas:

- **productos**: Productos principales con precios base y metros de film/papel
- **variantes**: Variantes de productos (talles y colores) con stock individual
- **ventas**: Registro de ventas con totales y metros utilizados
- **detalle_ventas**: Items individuales de cada venta

## Funcionalidades Principales

### 1. Gestión de Productos
- Agregar nuevos productos con tipo, precio y metros de film/papel
- Editar información de productos existentes
- Eliminar productos (soft delete)
- Gestionar variantes (talles y colores) con precios adicionales

### 2. Control de Stock
- Ver inventario completo con todas las variantes
- Alertas automáticas para stock bajo
- Actualización automática al registrar ventas

### 3. Registro de Ventas
- Interfaz intuitiva para registrar nuevas ventas
- Selección de productos y variantes
- Verificación de stock disponible
- Cálculo automático de totales
- Cálculo automático de metros de Film DTF y Papel de Sublimación

### 4. Historial y Estadísticas
- Ver todas las ventas registradas
- Ver detalles completos de cada venta
- Estadísticas de ventas totales, ingresos y materiales usados

## Cálculo de Materiales

El sistema calcula automáticamente los metros de material usado en cada venta:

- **Film DTF**: Para productos de tipo DTF, remeras y buzos
- **Papel de Sublimación**: Para productos de sublimación y tazas

El cálculo se basa en los metros configurados por producto multiplicados por la cantidad vendida.

## Licencia

Este proyecto es privado y pertenece a Bro Sublimados.

## Autor

Desarrollado para Bro Sublimados
