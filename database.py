"""
Módulo de gestión de base de datos SQLite para el sistema de gestión de tienda.
Maneja productos, stock y ventas.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple


class DatabaseManager:
    """Gestor de base de datos para Bro Sublimados"""
    
    def __init__(self, db_path: str = "tienda_bro.db"):
        """
        Inicializa el gestor de base de datos.
        
        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path
        self.create_tables()
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_tables(self):
        """Crea las tablas necesarias si no existen"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                descripcion TEXT,
                precio_base REAL NOT NULL,
                metros_film REAL DEFAULT 0,
                activo INTEGER DEFAULT 1,
                fecha_creacion TEXT NOT NULL
            )
        """)
        
        # Tabla de variantes de productos (talles y colores)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS variantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id INTEGER NOT NULL,
                talle TEXT,
                color TEXT,
                precio_adicional REAL DEFAULT 0,
                stock INTEGER DEFAULT 0,
                FOREIGN KEY (producto_id) REFERENCES productos (id),
                UNIQUE(producto_id, talle, color)
            )
        """)
        
        # Tabla de ventas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                cliente TEXT NOT NULL,
                total REAL NOT NULL,
                total_metros_film REAL DEFAULT 0,
                total_metros_papel REAL DEFAULT 0,
                notas TEXT
            )
        """)
        
        # Tabla de detalles de ventas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_ventas (
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
        """)
        
        conn.commit()
        conn.close()
    
    # ==================== PRODUCTOS ====================
    
    def agregar_producto(self, nombre: str, tipo: str, precio_base: float,
                        descripcion: str = "", metros_film: float = 0) -> int:
        """
        Agrega un nuevo producto a la base de datos.
        
        Args:
            nombre: Nombre del producto
            tipo: Tipo de producto (remera, buzo, taza, etc.)
            precio_base: Precio base del producto
            descripcion: Descripción opcional
            metros_film: Metros de film/papel que usa el producto
            
        Returns:
            ID del producto creado
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute("""
            INSERT INTO productos (nombre, tipo, descripcion, precio_base, metros_film, fecha_creacion)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, tipo, descripcion, precio_base, metros_film, fecha_creacion))
        
        producto_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return producto_id
    
    def obtener_productos(self, solo_activos: bool = True) -> List[Dict]:
        """
        Obtiene todos los productos.
        
        Args:
            solo_activos: Si True, solo devuelve productos activos
            
        Returns:
            Lista de productos como diccionarios
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM productos"
        if solo_activos:
            query += " WHERE activo = 1"
        query += " ORDER BY tipo, nombre"
        
        cursor.execute(query)
        productos = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return productos
    
    def obtener_producto(self, producto_id: int) -> Optional[Dict]:
        """
        Obtiene un producto específico por ID.
        
        Args:
            producto_id: ID del producto
            
        Returns:
            Diccionario con datos del producto o None si no existe
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
        row = cursor.fetchone()
        
        conn.close()
        return dict(row) if row else None
    
    def actualizar_producto(self, producto_id: int, nombre: str = None, tipo: str = None,
                           precio_base: float = None, descripcion: str = None,
                           metros_film: float = None) -> bool:
        """
        Actualiza un producto existente.
        
        Args:
            producto_id: ID del producto a actualizar
            nombre: Nuevo nombre (opcional)
            tipo: Nuevo tipo (opcional)
            precio_base: Nuevo precio base (opcional)
            descripcion: Nueva descripción (opcional)
            metros_film: Nuevos metros de film (opcional)
            
        Returns:
            True si se actualizó correctamente
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if nombre is not None:
            updates.append("nombre = ?")
            params.append(nombre)
        if tipo is not None:
            updates.append("tipo = ?")
            params.append(tipo)
        if precio_base is not None:
            updates.append("precio_base = ?")
            params.append(precio_base)
        if descripcion is not None:
            updates.append("descripcion = ?")
            params.append(descripcion)
        if metros_film is not None:
            updates.append("metros_film = ?")
            params.append(metros_film)
        
        if not updates:
            conn.close()
            return False
        
        params.append(producto_id)
        query = f"UPDATE productos SET {', '.join(updates)} WHERE id = ?"
        
        cursor.execute(query, params)
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        
        return success
    
    def eliminar_producto(self, producto_id: int) -> bool:
        """
        Marca un producto como inactivo (soft delete).
        
        Args:
            producto_id: ID del producto
            
        Returns:
            True si se eliminó correctamente
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE productos SET activo = 0 WHERE id = ?", (producto_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        
        return success
    
    # ==================== VARIANTES ====================
    
    def agregar_variante(self, producto_id: int, talle: str = "", color: str = "",
                        precio_adicional: float = 0, stock: int = 0) -> int:
        """
        Agrega una variante (talle/color) a un producto.
        
        Args:
            producto_id: ID del producto
            talle: Talle de la variante
            color: Color de la variante
            precio_adicional: Precio adicional sobre el precio base
            stock: Stock inicial
            
        Returns:
            ID de la variante creada
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO variantes (producto_id, talle, color, precio_adicional, stock)
                VALUES (?, ?, ?, ?, ?)
            """, (producto_id, talle, color, precio_adicional, stock))
            
            variante_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return variante_id
        except sqlite3.IntegrityError:
            conn.close()
            return -1  # Variante ya existe
    
    def obtener_variantes(self, producto_id: int) -> List[Dict]:
        """
        Obtiene todas las variantes de un producto.
        
        Args:
            producto_id: ID del producto
            
        Returns:
            Lista de variantes
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM variantes
            WHERE producto_id = ?
            ORDER BY talle, color
        """, (producto_id,))
        
        variantes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return variantes
    
    def actualizar_variante(self, variante_id: int, talle: str = None, color: str = None,
                           precio_adicional: float = None, stock: int = None) -> bool:
        """
        Actualiza una variante existente.
        
        Args:
            variante_id: ID de la variante
            talle: Nuevo talle (opcional)
            color: Nuevo color (opcional)
            precio_adicional: Nuevo precio adicional (opcional)
            stock: Nuevo stock (opcional)
            
        Returns:
            True si se actualizó correctamente
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        updates = []
        params = []
        
        if talle is not None:
            updates.append("talle = ?")
            params.append(talle)
        if color is not None:
            updates.append("color = ?")
            params.append(color)
        if precio_adicional is not None:
            updates.append("precio_adicional = ?")
            params.append(precio_adicional)
        if stock is not None:
            updates.append("stock = ?")
            params.append(stock)
        
        if not updates:
            conn.close()
            return False
        
        params.append(variante_id)
        query = f"UPDATE variantes SET {', '.join(updates)} WHERE id = ?"
        
        cursor.execute(query, params)
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        
        return success
    
    def actualizar_stock(self, variante_id: int, cantidad: int) -> bool:
        """
        Actualiza el stock de una variante (incrementa o decrementa).
        
        Args:
            variante_id: ID de la variante
            cantidad: Cantidad a sumar (positivo) o restar (negativo)
            
        Returns:
            True si se actualizó correctamente
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE variantes
            SET stock = stock + ?
            WHERE id = ?
        """, (cantidad, variante_id))
        
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        
        return success
    
    def eliminar_variante(self, variante_id: int) -> bool:
        """
        Elimina una variante.
        
        Args:
            variante_id: ID de la variante
            
        Returns:
            True si se eliminó correctamente
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM variantes WHERE id = ?", (variante_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        
        return success
    
    # ==================== VENTAS ====================
    
    def registrar_venta(self, cliente: str, items: List[Dict], notas: str = "") -> Tuple[int, bool]:
        """
        Registra una nueva venta y actualiza el stock automáticamente.
        
        Args:
            cliente: Nombre del cliente
            items: Lista de items vendidos. Cada item debe tener:
                   - producto_id: ID del producto
                   - variante_id: ID de la variante (opcional)
                   - cantidad: Cantidad vendida
                   - precio_unitario: Precio unitario
            notas: Notas adicionales de la venta
            
        Returns:
            Tupla (venta_id, success)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            total = sum(item['cantidad'] * item['precio_unitario'] for item in items)
            total_metros_film = 0
            total_metros_papel = 0
            
            # Crear la venta
            cursor.execute("""
                INSERT INTO ventas (fecha, cliente, total, total_metros_film, total_metros_papel, notas)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (fecha, cliente, total, 0, 0, notas))
            
            venta_id = cursor.lastrowid
            
            # Agregar detalles de venta y actualizar stock
            for item in items:
                producto_id = item['producto_id']
                variante_id = item.get('variante_id')
                cantidad = item['cantidad']
                precio_unitario = item['precio_unitario']
                subtotal = cantidad * precio_unitario
                
                # Obtener metros de film del producto
                cursor.execute("SELECT metros_film, tipo FROM productos WHERE id = ?", (producto_id,))
                row = cursor.fetchone()
                metros_film = row['metros_film'] if row else 0
                tipo_producto = row['tipo'] if row else ""
                
                metros_item = metros_film * cantidad
                
                # Determinar si es sublimación o DTF basado en el tipo de producto
                if 'sublimacion' in tipo_producto.lower() or 'taza' in tipo_producto.lower():
                    total_metros_papel += metros_item
                else:
                    total_metros_film += metros_item
                
                # Insertar detalle de venta
                cursor.execute("""
                    INSERT INTO detalle_ventas 
                    (venta_id, producto_id, variante_id, cantidad, precio_unitario, subtotal, metros_film)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (venta_id, producto_id, variante_id, cantidad, precio_unitario, subtotal, metros_item))
                
                # Actualizar stock si hay variante
                if variante_id:
                    cursor.execute("""
                        UPDATE variantes
                        SET stock = stock - ?
                        WHERE id = ?
                    """, (cantidad, variante_id))
            
            # Actualizar totales de metros en la venta
            cursor.execute("""
                UPDATE ventas
                SET total_metros_film = ?, total_metros_papel = ?
                WHERE id = ?
            """, (total_metros_film, total_metros_papel, venta_id))
            
            conn.commit()
            conn.close()
            return venta_id, True
            
        except Exception as e:
            conn.rollback()
            conn.close()
            print(f"Error al registrar venta: {e}")
            return -1, False
    
    def obtener_ventas(self, fecha_desde: str = None, fecha_hasta: str = None) -> List[Dict]:
        """
        Obtiene ventas con filtro opcional por fecha.
        
        Args:
            fecha_desde: Fecha inicial (formato YYYY-MM-DD)
            fecha_hasta: Fecha final (formato YYYY-MM-DD)
            
        Returns:
            Lista de ventas
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM ventas"
        params = []
        
        if fecha_desde or fecha_hasta:
            query += " WHERE"
            if fecha_desde:
                query += " fecha >= ?"
                params.append(fecha_desde)
            if fecha_hasta:
                if fecha_desde:
                    query += " AND"
                query += " fecha <= ?"
                params.append(fecha_hasta + " 23:59:59")
        
        query += " ORDER BY fecha DESC"
        
        cursor.execute(query, params)
        ventas = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return ventas
    
    def obtener_venta(self, venta_id: int) -> Optional[Dict]:
        """
        Obtiene una venta específica con sus detalles.
        
        Args:
            venta_id: ID de la venta
            
        Returns:
            Diccionario con la venta y sus detalles
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM ventas WHERE id = ?", (venta_id,))
        venta_row = cursor.fetchone()
        
        if not venta_row:
            conn.close()
            return None
        
        venta = dict(venta_row)
        
        # Obtener detalles
        cursor.execute("""
            SELECT dv.*, p.nombre as producto_nombre, p.tipo as producto_tipo,
                   v.talle, v.color
            FROM detalle_ventas dv
            JOIN productos p ON dv.producto_id = p.id
            LEFT JOIN variantes v ON dv.variante_id = v.id
            WHERE dv.venta_id = ?
        """, (venta_id,))
        
        venta['detalles'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return venta
    
    # ==================== ESTADÍSTICAS ====================
    
    def obtener_stock_bajo(self, limite: int = 5) -> List[Dict]:
        """
        Obtiene productos con stock bajo.
        
        Args:
            limite: Cantidad mínima de stock para considerar "bajo"
            
        Returns:
            Lista de variantes con stock bajo
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT v.*, p.nombre, p.tipo
            FROM variantes v
            JOIN productos p ON v.producto_id = p.id
            WHERE v.stock <= ? AND p.activo = 1
            ORDER BY v.stock ASC
        """, (limite,))
        
        productos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return productos
    
    def obtener_estadisticas_ventas(self, fecha_desde: str = None, fecha_hasta: str = None) -> Dict:
        """
        Obtiene estadísticas de ventas.
        
        Args:
            fecha_desde: Fecha inicial (formato YYYY-MM-DD)
            fecha_hasta: Fecha final (formato YYYY-MM-DD)
            
        Returns:
            Diccionario con estadísticas
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT COUNT(*) as total_ventas, SUM(total) as total_ingresos, " \
                "SUM(total_metros_film) as total_film, SUM(total_metros_papel) as total_papel " \
                "FROM ventas WHERE 1=1"
        params = []
        
        if fecha_desde:
            query += " AND fecha >= ?"
            params.append(fecha_desde)
        if fecha_hasta:
            query += " AND fecha <= ?"
            params.append(fecha_hasta + " 23:59:59")
        
        cursor.execute(query, params)
        row = cursor.fetchone()
        
        stats = dict(row) if row else {}
        conn.close()
        
        return stats
