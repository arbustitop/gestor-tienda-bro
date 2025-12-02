#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos de ejemplo
"""

from database import DatabaseManager
import os

def setup_example_data():
    """Crea datos de ejemplo en la base de datos"""
    
    db = DatabaseManager("tienda_bro.db")
    
    print("Configurando datos de ejemplo para Bro Sublimados...")
    print("="*60)
    
    # Verificar si ya hay datos
    productos_existentes = db.obtener_productos()
    if len(productos_existentes) > 0:
        print(f"⚠️  Ya existen {len(productos_existentes)} productos en la base de datos.")
        respuesta = input("¿Desea continuar y agregar más datos? (s/n): ")
        if respuesta.lower() != 's':
            print("Operación cancelada.")
            return
    
    print("\n1. Agregando productos...")
    
    # Productos de remeras
    remera_dtf_id = db.agregar_producto(
        nombre="Remera DTF Estampada",
        tipo="Remera",
        precio_base=5000.0,
        descripcion="Remera de algodón con estampado DTF de alta calidad",
        metros_film=0.3
    )
    print(f"   ✓ Remera DTF (ID: {remera_dtf_id})")
    
    remera_sublimacion_id = db.agregar_producto(
        nombre="Remera Sublimada Full Print",
        tipo="Sublimación",
        precio_base=6000.0,
        descripcion="Remera con sublimación completa",
        metros_film=0.4
    )
    print(f"   ✓ Remera Sublimación (ID: {remera_sublimacion_id})")
    
    # Buzos
    buzo_dtf_id = db.agregar_producto(
        nombre="Buzo con Capucha DTF",
        tipo="Buzo",
        precio_base=9000.0,
        descripcion="Buzo con capucha y estampado DTF",
        metros_film=0.5
    )
    print(f"   ✓ Buzo DTF (ID: {buzo_dtf_id})")
    
    buzo_canguro_id = db.agregar_producto(
        nombre="Buzo Canguro Premium",
        tipo="Buzo",
        precio_base=10000.0,
        descripcion="Buzo canguro con bolsillo y estampado frontal",
        metros_film=0.6
    )
    print(f"   ✓ Buzo Canguro (ID: {buzo_canguro_id})")
    
    # Tazas
    taza_clasica_id = db.agregar_producto(
        nombre="Taza Sublimada Clásica",
        tipo="Taza",
        precio_base=2000.0,
        descripcion="Taza de cerámica blanca con sublimación",
        metros_film=0.12
    )
    print(f"   ✓ Taza Clásica (ID: {taza_clasica_id})")
    
    taza_magica_id = db.agregar_producto(
        nombre="Taza Mágica Sublimada",
        tipo="Taza",
        precio_base=3000.0,
        descripcion="Taza que cambia de color con calor",
        metros_film=0.12
    )
    print(f"   ✓ Taza Mágica (ID: {taza_magica_id})")
    
    # Otros productos
    musculosa_id = db.agregar_producto(
        nombre="Musculosa DTF",
        tipo="Remera",
        precio_base=4000.0,
        descripcion="Musculosa deportiva con estampado DTF",
        metros_film=0.25
    )
    print(f"   ✓ Musculosa (ID: {musculosa_id})")
    
    print("\n2. Agregando variantes y stock...")
    
    # Variantes para Remera DTF
    talles_remera = ["XS", "S", "M", "L", "XL", "XXL"]
    colores_remera = [
        ("Blanco", 0),
        ("Negro", 200),
        ("Gris", 100),
        ("Azul Marino", 150),
        ("Rojo", 150)
    ]
    
    stocks_base = {"XS": 5, "S": 10, "M": 15, "L": 15, "XL": 8, "XXL": 5}
    
    for talle in talles_remera:
        for color, precio_add in colores_remera:
            stock = stocks_base.get(talle, 10)
            db.agregar_variante(remera_dtf_id, talle, color, precio_add, stock)
    print(f"   ✓ {len(talles_remera) * len(colores_remera)} variantes para Remera DTF")
    
    # Variantes para Remera Sublimación
    for talle in talles_remera:
        stock = stocks_base.get(talle, 10)
        db.agregar_variante(remera_sublimacion_id, talle, "Full Color", 0, stock)
    print(f"   ✓ {len(talles_remera)} variantes para Remera Sublimación")
    
    # Variantes para Buzos
    talles_buzo = ["S", "M", "L", "XL", "XXL"]
    colores_buzo = [
        ("Negro", 0),
        ("Gris Oscuro", 0),
        ("Azul Marino", 200),
        ("Bordo", 200)
    ]
    
    for talle in talles_buzo:
        for color, precio_add in colores_buzo:
            stock = 5 if talle in ["S", "XXL"] else 8
            db.agregar_variante(buzo_dtf_id, talle, color, precio_add, stock)
    print(f"   ✓ {len(talles_buzo) * len(colores_buzo)} variantes para Buzo DTF")
    
    for talle in talles_buzo:
        stock = 4 if talle in ["S", "XXL"] else 6
        db.agregar_variante(buzo_canguro_id, talle, "Negro", 0, stock)
        db.agregar_variante(buzo_canguro_id, talle, "Gris", 0, stock)
    print(f"   ✓ {len(talles_buzo) * 2} variantes para Buzo Canguro")
    
    # Variantes para Musculosa
    for talle in ["S", "M", "L", "XL"]:
        for color in ["Blanco", "Negro", "Gris"]:
            precio_add = 100 if color == "Negro" else 0
            db.agregar_variante(musculosa_id, talle, color, precio_add, 8)
    print(f"   ✓ 12 variantes para Musculosa")
    
    # Variantes para Tazas (solo colores/tipos)
    db.agregar_variante(taza_clasica_id, "", "Blanca", 0, 30)
    db.agregar_variante(taza_clasica_id, "", "Color Interior Rojo", 300, 15)
    db.agregar_variante(taza_clasica_id, "", "Color Interior Azul", 300, 15)
    print(f"   ✓ 3 variantes para Taza Clásica")
    
    db.agregar_variante(taza_magica_id, "", "Negra", 0, 20)
    db.agregar_variante(taza_magica_id, "", "Azul", 0, 20)
    print(f"   ✓ 2 variantes para Taza Mágica")
    
    print("\n3. Registrando ventas de ejemplo...")
    
    # Venta 1
    variantes_remera = db.obtener_variantes(remera_dtf_id)
    var_m_blanco = [v for v in variantes_remera if v['talle'] == 'M' and v['color'] == 'Blanco'][0]
    var_l_negro = [v for v in variantes_remera if v['talle'] == 'L' and v['color'] == 'Negro'][0]
    
    items1 = [
        {
            'producto_id': remera_dtf_id,
            'variante_id': var_m_blanco['id'],
            'cantidad': 5,
            'precio_unitario': 5000.0
        },
        {
            'producto_id': remera_dtf_id,
            'variante_id': var_l_negro['id'],
            'cantidad': 3,
            'precio_unitario': 5200.0
        }
    ]
    
    venta1_id, success = db.registrar_venta(
        cliente="Deportivo San Martín",
        items=items1,
        notas="Remeras para equipo de fútbol juvenil. Entrega: 15/12"
    )
    if success:
        print(f"   ✓ Venta 1 registrada (ID: {venta1_id})")
    
    # Venta 2
    variantes_buzo = db.obtener_variantes(buzo_dtf_id)
    var_buzo_l = [v for v in variantes_buzo if v['talle'] == 'L' and v['color'] == 'Negro'][0]
    
    variantes_taza = db.obtener_variantes(taza_clasica_id)
    var_taza_blanca = [v for v in variantes_taza if v['color'] == 'Blanca'][0]
    
    items2 = [
        {
            'producto_id': buzo_dtf_id,
            'variante_id': var_buzo_l['id'],
            'cantidad': 2,
            'precio_unitario': 9000.0
        },
        {
            'producto_id': taza_clasica_id,
            'variante_id': var_taza_blanca['id'],
            'cantidad': 10,
            'precio_unitario': 2000.0
        }
    ]
    
    venta2_id, success = db.registrar_venta(
        cliente="María González",
        items=items2,
        notas="Regalo empresarial. Diseño corporativo"
    )
    if success:
        print(f"   ✓ Venta 2 registrada (ID: {venta2_id})")
    
    # Venta 3
    variantes_sublim = db.obtener_variantes(remera_sublimacion_id)
    var_sublim_xl = [v for v in variantes_sublim if v['talle'] == 'XL'][0]
    
    items3 = [
        {
            'producto_id': remera_sublimacion_id,
            'variante_id': var_sublim_xl['id'],
            'cantidad': 20,
            'precio_unitario': 6000.0
        }
    ]
    
    venta3_id, success = db.registrar_venta(
        cliente="Eventos Premium S.A.",
        items=items3,
        notas="Remeras para evento corporativo. Diseño full print con logo"
    )
    if success:
        print(f"   ✓ Venta 3 registrada (ID: {venta3_id})")
    
    print("\n" + "="*60)
    print("✓ Datos de ejemplo configurados exitosamente!")
    print("="*60)
    
    # Mostrar estadísticas
    stats = db.obtener_estadisticas_ventas()
    print(f"\n📊 Estadísticas:")
    print(f"   • Total de productos: {len(db.obtener_productos())}")
    print(f"   • Total de ventas: {stats['total_ventas']}")
    print(f"   • Ingresos totales: ${stats['total_ingresos']:.2f}")
    print(f"   • Film DTF usado: {stats['total_film']:.2f} metros")
    print(f"   • Papel sublimación usado: {stats['total_papel']:.2f} metros")
    
    stock_bajo = db.obtener_stock_bajo(5)
    if stock_bajo:
        print(f"\n⚠️  Alertas de stock bajo ({len(stock_bajo)} items):")
        for item in stock_bajo[:5]:  # Mostrar solo los primeros 5
            print(f"   • {item['nombre']} {item['talle']} {item['color']}: {item['stock']} unidades")
    
    print("\n✓ ¡La base de datos está lista para usar!")
    print("  Ejecute 'python main.py' para iniciar la aplicación.\n")

if __name__ == "__main__":
    setup_example_data()
