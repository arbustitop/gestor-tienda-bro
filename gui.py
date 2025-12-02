"""
Interfaz gráfica moderna con CustomTkinter para el sistema de gestión de tienda.
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime
from typing import Optional, List, Dict
from database import DatabaseManager


# Configuración de tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    """Aplicación principal de gestión de tienda"""
    
    def __init__(self):
        super().__init__()
        
        self.db = DatabaseManager()
        
        # Configuración de ventana
        self.title("Bro Sublimados - Gestor de Tienda")
        self.geometry("1200x700")
        
        # Grid layout (2 columnas)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Panel lateral de navegación
        self.crear_panel_navegacion()
        
        # Frame principal para contenido
        self.frame_principal = ctk.CTkFrame(self, corner_radius=0)
        self.frame_principal.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Mostrar vista inicial
        self.mostrar_productos()
    
    def crear_panel_navegacion(self):
        """Crea el panel lateral de navegación"""
        self.nav_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky="nsew")
        self.nav_frame.grid_rowconfigure(5, weight=1)
        
        # Logo/Título
        self.label_titulo = ctk.CTkLabel(
            self.nav_frame,
            text="Bro Sublimados",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_titulo.grid(row=0, column=0, padx=20, pady=20)
        
        # Botones de navegación
        self.btn_productos = ctk.CTkButton(
            self.nav_frame,
            text="Productos",
            command=self.mostrar_productos,
            font=ctk.CTkFont(size=14)
        )
        self.btn_productos.grid(row=1, column=0, padx=20, pady=10)
        
        self.btn_stock = ctk.CTkButton(
            self.nav_frame,
            text="Stock",
            command=self.mostrar_stock,
            font=ctk.CTkFont(size=14)
        )
        self.btn_stock.grid(row=2, column=0, padx=20, pady=10)
        
        self.btn_ventas = ctk.CTkButton(
            self.nav_frame,
            text="Ventas",
            command=self.mostrar_ventas,
            font=ctk.CTkFont(size=14)
        )
        self.btn_ventas.grid(row=3, column=0, padx=20, pady=10)
        
        self.btn_nueva_venta = ctk.CTkButton(
            self.nav_frame,
            text="Nueva Venta",
            command=self.mostrar_nueva_venta,
            font=ctk.CTkFont(size=14),
            fg_color="green",
            hover_color="darkgreen"
        )
        self.btn_nueva_venta.grid(row=4, column=0, padx=20, pady=10)
    
    def limpiar_frame_principal(self):
        """Limpia el contenido del frame principal"""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
    
    # ==================== VISTA PRODUCTOS ====================
    
    def mostrar_productos(self):
        """Muestra la vista de gestión de productos"""
        self.limpiar_frame_principal()
        
        # Título
        label_titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Gestión de Productos",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label_titulo.pack(pady=20)
        
        # Frame de botones
        frame_botones = ctk.CTkFrame(self.frame_principal)
        frame_botones.pack(fill="x", padx=20, pady=10)
        
        btn_agregar = ctk.CTkButton(
            frame_botones,
            text="+ Agregar Producto",
            command=self.dialogo_agregar_producto,
            font=ctk.CTkFont(size=14)
        )
        btn_agregar.pack(side="left", padx=10)
        
        btn_actualizar = ctk.CTkButton(
            frame_botones,
            text="⟳ Actualizar",
            command=self.mostrar_productos,
            font=ctk.CTkFont(size=14)
        )
        btn_actualizar.pack(side="left", padx=10)
        
        # Frame para la tabla
        frame_tabla = ctk.CTkFrame(self.frame_principal)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear tabla con Treeview
        self.crear_tabla_productos(frame_tabla)
    
    def crear_tabla_productos(self, parent):
        """Crea la tabla de productos"""
        # Scrollbar
        scrollbar = ctk.CTkScrollbar(parent)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview
        columnas = ("ID", "Nombre", "Tipo", "Precio Base", "Metros Film/Papel", "Variantes")
        self.tree_productos = ttk.Treeview(
            parent,
            columns=columnas,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.configure(command=self.tree_productos.yview)
        
        # Configurar columnas
        self.tree_productos.heading("ID", text="ID")
        self.tree_productos.heading("Nombre", text="Nombre")
        self.tree_productos.heading("Tipo", text="Tipo")
        self.tree_productos.heading("Precio Base", text="Precio Base")
        self.tree_productos.heading("Metros Film/Papel", text="Metros Film/Papel")
        self.tree_productos.heading("Variantes", text="Variantes")
        
        self.tree_productos.column("ID", width=50)
        self.tree_productos.column("Nombre", width=200)
        self.tree_productos.column("Tipo", width=150)
        self.tree_productos.column("Precio Base", width=100)
        self.tree_productos.column("Metros Film/Papel", width=150)
        self.tree_productos.column("Variantes", width=100)
        
        self.tree_productos.pack(fill="both", expand=True)
        
        # Cargar productos
        productos = self.db.obtener_productos()
        for producto in productos:
            variantes = self.db.obtener_variantes(producto['id'])
            self.tree_productos.insert("", "end", values=(
                producto['id'],
                producto['nombre'],
                producto['tipo'],
                f"${producto['precio_base']:.2f}",
                f"{producto['metros_film']:.2f}m",
                len(variantes)
            ))
        
        # Menú contextual
        self.tree_productos.bind("<Button-3>", self.menu_contextual_producto)
        self.tree_productos.bind("<Double-1>", self.editar_producto)
    
    def menu_contextual_producto(self, event):
        """Muestra menú contextual para productos"""
        item = self.tree_productos.identify_row(event.y)
        if item:
            self.tree_productos.selection_set(item)
            menu = ctk.CTkToplevel(self)
            menu.overrideredirect(True)
            menu.geometry(f"+{event.x_root}+{event.y_root}")
            
            btn_editar = ctk.CTkButton(menu, text="Editar", command=lambda: [menu.destroy(), self.editar_producto(None)])
            btn_editar.pack(padx=5, pady=5)
            
            btn_variantes = ctk.CTkButton(menu, text="Gestionar Variantes", command=lambda: [menu.destroy(), self.gestionar_variantes()])
            btn_variantes.pack(padx=5, pady=5)
            
            btn_eliminar = ctk.CTkButton(menu, text="Eliminar", fg_color="red", command=lambda: [menu.destroy(), self.eliminar_producto()])
            btn_eliminar.pack(padx=5, pady=5)
            
            # Cerrar menú al hacer clic fuera
            menu.bind("<FocusOut>", lambda e: menu.destroy())
            menu.focus()
    
    def dialogo_agregar_producto(self):
        """Diálogo para agregar un nuevo producto"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Agregar Producto")
        dialog.geometry("500x500")
        dialog.transient(self)
        dialog.grab_set()
        
        # Campos
        ctk.CTkLabel(dialog, text="Nombre:", font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
        entry_nombre = ctk.CTkEntry(dialog, width=400)
        entry_nombre.pack()
        
        ctk.CTkLabel(dialog, text="Tipo:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        tipos = ["Remera", "Buzo", "Taza", "Sublimación", "DTF", "Otro"]
        combo_tipo = ctk.CTkComboBox(dialog, values=tipos, width=400)
        combo_tipo.pack()
        combo_tipo.set(tipos[0])
        
        ctk.CTkLabel(dialog, text="Descripción:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        entry_descripcion = ctk.CTkEntry(dialog, width=400)
        entry_descripcion.pack()
        
        ctk.CTkLabel(dialog, text="Precio Base:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        entry_precio = ctk.CTkEntry(dialog, width=400)
        entry_precio.pack()
        
        ctk.CTkLabel(dialog, text="Metros de Film/Papel:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        entry_metros = ctk.CTkEntry(dialog, width=400)
        entry_metros.insert(0, "0")
        entry_metros.pack()
        
        # Botones
        frame_botones = ctk.CTkFrame(dialog)
        frame_botones.pack(pady=20)
        
        def guardar():
            try:
                nombre = entry_nombre.get().strip()
                tipo = combo_tipo.get()
                descripcion = entry_descripcion.get().strip()
                precio = float(entry_precio.get())
                metros = float(entry_metros.get())
                
                if not nombre or precio <= 0:
                    messagebox.showerror("Error", "Por favor complete los campos obligatorios correctamente.")
                    return
                
                producto_id = self.db.agregar_producto(nombre, tipo, precio, descripcion, metros)
                messagebox.showinfo("Éxito", f"Producto agregado con ID: {producto_id}")
                dialog.destroy()
                self.mostrar_productos()
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")
        
        btn_guardar = ctk.CTkButton(frame_botones, text="Guardar", command=guardar, width=150)
        btn_guardar.pack(side="left", padx=10)
        
        btn_cancelar = ctk.CTkButton(frame_botones, text="Cancelar", command=dialog.destroy, width=150)
        btn_cancelar.pack(side="left", padx=10)
    
    def editar_producto(self, event):
        """Edita el producto seleccionado"""
        seleccion = self.tree_productos.selection()
        if not seleccion:
            return
        
        item = self.tree_productos.item(seleccion[0])
        producto_id = item['values'][0]
        producto = self.db.obtener_producto(producto_id)
        
        if not producto:
            messagebox.showerror("Error", "Producto no encontrado.")
            return
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Editar Producto")
        dialog.geometry("500x500")
        dialog.transient(self)
        dialog.grab_set()
        
        # Campos con valores actuales
        ctk.CTkLabel(dialog, text="Nombre:", font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
        entry_nombre = ctk.CTkEntry(dialog, width=400)
        entry_nombre.insert(0, producto['nombre'])
        entry_nombre.pack()
        
        ctk.CTkLabel(dialog, text="Tipo:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        tipos = ["Remera", "Buzo", "Taza", "Sublimación", "DTF", "Otro"]
        combo_tipo = ctk.CTkComboBox(dialog, values=tipos, width=400)
        combo_tipo.pack()
        combo_tipo.set(producto['tipo'])
        
        ctk.CTkLabel(dialog, text="Descripción:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        entry_descripcion = ctk.CTkEntry(dialog, width=400)
        entry_descripcion.insert(0, producto['descripcion'] or "")
        entry_descripcion.pack()
        
        ctk.CTkLabel(dialog, text="Precio Base:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        entry_precio = ctk.CTkEntry(dialog, width=400)
        entry_precio.insert(0, str(producto['precio_base']))
        entry_precio.pack()
        
        ctk.CTkLabel(dialog, text="Metros de Film/Papel:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        entry_metros = ctk.CTkEntry(dialog, width=400)
        entry_metros.insert(0, str(producto['metros_film']))
        entry_metros.pack()
        
        # Botones
        frame_botones = ctk.CTkFrame(dialog)
        frame_botones.pack(pady=20)
        
        def guardar():
            try:
                nombre = entry_nombre.get().strip()
                tipo = combo_tipo.get()
                descripcion = entry_descripcion.get().strip()
                precio = float(entry_precio.get())
                metros = float(entry_metros.get())
                
                if not nombre or precio <= 0:
                    messagebox.showerror("Error", "Por favor complete los campos obligatorios correctamente.")
                    return
                
                self.db.actualizar_producto(producto_id, nombre, tipo, precio, descripcion, metros)
                messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
                dialog.destroy()
                self.mostrar_productos()
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")
        
        btn_guardar = ctk.CTkButton(frame_botones, text="Guardar", command=guardar, width=150)
        btn_guardar.pack(side="left", padx=10)
        
        btn_cancelar = ctk.CTkButton(frame_botones, text="Cancelar", command=dialog.destroy, width=150)
        btn_cancelar.pack(side="left", padx=10)
    
    def eliminar_producto(self):
        """Elimina el producto seleccionado"""
        seleccion = self.tree_productos.selection()
        if not seleccion:
            return
        
        item = self.tree_productos.item(seleccion[0])
        producto_id = item['values'][0]
        nombre = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto '{nombre}'?"):
            self.db.eliminar_producto(producto_id)
            messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            self.mostrar_productos()
    
    def gestionar_variantes(self):
        """Gestiona las variantes del producto seleccionado"""
        seleccion = self.tree_productos.selection()
        if not seleccion:
            return
        
        item = self.tree_productos.item(seleccion[0])
        producto_id = item['values'][0]
        producto = self.db.obtener_producto(producto_id)
        
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Variantes - {producto['nombre']}")
        dialog.geometry("800x600")
        dialog.transient(self)
        dialog.grab_set()
        
        # Frame de botones
        frame_botones = ctk.CTkFrame(dialog)
        frame_botones.pack(fill="x", padx=20, pady=10)
        
        btn_agregar = ctk.CTkButton(
            frame_botones,
            text="+ Agregar Variante",
            command=lambda: self.dialogo_agregar_variante(producto_id, dialog)
        )
        btn_agregar.pack(side="left", padx=10)
        
        # Tabla de variantes
        frame_tabla = ctk.CTkFrame(dialog)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = ctk.CTkScrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")
        
        columnas = ("ID", "Talle", "Color", "Precio Adicional", "Stock")
        tree_variantes = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.configure(command=tree_variantes.yview)
        
        for col in columnas:
            tree_variantes.heading(col, text=col)
            tree_variantes.column(col, width=150)
        
        tree_variantes.pack(fill="both", expand=True)
        
        # Cargar variantes
        def cargar_variantes():
            tree_variantes.delete(*tree_variantes.get_children())
            variantes = self.db.obtener_variantes(producto_id)
            for variante in variantes:
                tree_variantes.insert("", "end", values=(
                    variante['id'],
                    variante['talle'] or "-",
                    variante['color'] or "-",
                    f"${variante['precio_adicional']:.2f}",
                    variante['stock']
                ))
        
        cargar_variantes()
        
        # Menú contextual para variantes
        def menu_contextual_variante(event):
            item = tree_variantes.identify_row(event.y)
            if item:
                tree_variantes.selection_set(item)
                menu = ctk.CTkToplevel(dialog)
                menu.overrideredirect(True)
                menu.geometry(f"+{event.x_root}+{event.y_root}")
                
                def editar_variante():
                    selec = tree_variantes.selection()
                    if selec:
                        item_data = tree_variantes.item(selec[0])
                        variante_id = item_data['values'][0]
                        self.dialogo_editar_variante(variante_id, dialog, cargar_variantes)
                    menu.destroy()
                
                def eliminar_variante():
                    selec = tree_variantes.selection()
                    if selec:
                        item_data = tree_variantes.item(selec[0])
                        variante_id = item_data['values'][0]
                        if messagebox.askyesno("Confirmar", "¿Eliminar esta variante?"):
                            self.db.eliminar_variante(variante_id)
                            cargar_variantes()
                    menu.destroy()
                
                btn_editar = ctk.CTkButton(menu, text="Editar", command=editar_variante)
                btn_editar.pack(padx=5, pady=5)
                
                btn_eliminar = ctk.CTkButton(menu, text="Eliminar", fg_color="red", command=eliminar_variante)
                btn_eliminar.pack(padx=5, pady=5)
                
                menu.bind("<FocusOut>", lambda e: menu.destroy())
                menu.focus()
        
        tree_variantes.bind("<Button-3>", menu_contextual_variante)
        
        # Almacenar referencia para actualizar
        dialog.cargar_variantes = cargar_variantes
    
    def dialogo_agregar_variante(self, producto_id: int, parent):
        """Diálogo para agregar una variante"""
        dialog = ctk.CTkToplevel(parent)
        dialog.title("Agregar Variante")
        dialog.geometry("400x400")
        dialog.transient(parent)
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="Talle:", font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
        entry_talle = ctk.CTkEntry(dialog, width=300)
        entry_talle.pack()
        
        ctk.CTkLabel(dialog, text="Color:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        entry_color = ctk.CTkEntry(dialog, width=300)
        entry_color.pack()
        
        ctk.CTkLabel(dialog, text="Precio Adicional:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        entry_precio_adicional = ctk.CTkEntry(dialog, width=300)
        entry_precio_adicional.insert(0, "0")
        entry_precio_adicional.pack()
        
        ctk.CTkLabel(dialog, text="Stock Inicial:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        entry_stock = ctk.CTkEntry(dialog, width=300)
        entry_stock.insert(0, "0")
        entry_stock.pack()
        
        frame_botones = ctk.CTkFrame(dialog)
        frame_botones.pack(pady=20)
        
        def guardar():
            try:
                talle = entry_talle.get().strip()
                color = entry_color.get().strip()
                precio_adicional = float(entry_precio_adicional.get())
                stock = int(entry_stock.get())
                
                variante_id = self.db.agregar_variante(producto_id, talle, color, precio_adicional, stock)
                if variante_id > 0:
                    messagebox.showinfo("Éxito", "Variante agregada correctamente.")
                    dialog.destroy()
                    if hasattr(parent, 'cargar_variantes'):
                        parent.cargar_variantes()
                else:
                    messagebox.showerror("Error", "Esta variante ya existe.")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese valores válidos.")
        
        btn_guardar = ctk.CTkButton(frame_botones, text="Guardar", command=guardar, width=120)
        btn_guardar.pack(side="left", padx=10)
        
        btn_cancelar = ctk.CTkButton(frame_botones, text="Cancelar", command=dialog.destroy, width=120)
        btn_cancelar.pack(side="left", padx=10)
    
    def dialogo_editar_variante(self, variante_id: int, parent, callback):
        """Diálogo para editar una variante"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM variantes WHERE id = ?", (variante_id,))
        variante = dict(cursor.fetchone())
        conn.close()
        
        dialog = ctk.CTkToplevel(parent)
        dialog.title("Editar Variante")
        dialog.geometry("400x400")
        dialog.transient(parent)
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="Talle:", font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
        entry_talle = ctk.CTkEntry(dialog, width=300)
        entry_talle.insert(0, variante['talle'] or "")
        entry_talle.pack()
        
        ctk.CTkLabel(dialog, text="Color:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        entry_color = ctk.CTkEntry(dialog, width=300)
        entry_color.insert(0, variante['color'] or "")
        entry_color.pack()
        
        ctk.CTkLabel(dialog, text="Precio Adicional:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        entry_precio_adicional = ctk.CTkEntry(dialog, width=300)
        entry_precio_adicional.insert(0, str(variante['precio_adicional']))
        entry_precio_adicional.pack()
        
        ctk.CTkLabel(dialog, text="Stock:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
        entry_stock = ctk.CTkEntry(dialog, width=300)
        entry_stock.insert(0, str(variante['stock']))
        entry_stock.pack()
        
        frame_botones = ctk.CTkFrame(dialog)
        frame_botones.pack(pady=20)
        
        def guardar():
            try:
                talle = entry_talle.get().strip()
                color = entry_color.get().strip()
                precio_adicional = float(entry_precio_adicional.get())
                stock = int(entry_stock.get())
                
                self.db.actualizar_variante(variante_id, talle, color, precio_adicional, stock)
                messagebox.showinfo("Éxito", "Variante actualizada correctamente.")
                dialog.destroy()
                callback()
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese valores válidos.")
        
        btn_guardar = ctk.CTkButton(frame_botones, text="Guardar", command=guardar, width=120)
        btn_guardar.pack(side="left", padx=10)
        
        btn_cancelar = ctk.CTkButton(frame_botones, text="Cancelar", command=dialog.destroy, width=120)
        btn_cancelar.pack(side="left", padx=10)
    
    # ==================== VISTA STOCK ====================
    
    def mostrar_stock(self):
        """Muestra la vista de gestión de stock"""
        self.limpiar_frame_principal()
        
        label_titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Gestión de Stock",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label_titulo.pack(pady=20)
        
        # Alertas de stock bajo
        stock_bajo = self.db.obtener_stock_bajo(5)
        if stock_bajo:
            frame_alerta = ctk.CTkFrame(self.frame_principal, fg_color="darkred")
            frame_alerta.pack(fill="x", padx=20, pady=10)
            
            label_alerta = ctk.CTkLabel(
                frame_alerta,
                text=f"⚠️ {len(stock_bajo)} producto(s) con stock bajo",
                font=ctk.CTkFont(size=16, weight="bold")
            )
            label_alerta.pack(pady=10)
        
        # Tabla de stock
        frame_tabla = ctk.CTkFrame(self.frame_principal)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = ctk.CTkScrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")
        
        columnas = ("ID", "Producto", "Tipo", "Talle", "Color", "Stock", "Precio")
        tree_stock = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.configure(command=tree_stock.yview)
        
        for col in columnas:
            tree_stock.heading(col, text=col)
        
        tree_stock.column("ID", width=50)
        tree_stock.column("Producto", width=200)
        tree_stock.column("Tipo", width=100)
        tree_stock.column("Talle", width=80)
        tree_stock.column("Color", width=100)
        tree_stock.column("Stock", width=80)
        tree_stock.column("Precio", width=100)
        
        tree_stock.pack(fill="both", expand=True)
        
        # Cargar datos
        productos = self.db.obtener_productos()
        for producto in productos:
            variantes = self.db.obtener_variantes(producto['id'])
            if variantes:
                for variante in variantes:
                    precio_total = producto['precio_base'] + variante['precio_adicional']
                    # Colorear según stock
                    tags = ()
                    if variante['stock'] <= 5:
                        tags = ('bajo_stock',)
                    
                    tree_stock.insert("", "end", values=(
                        variante['id'],
                        producto['nombre'],
                        producto['tipo'],
                        variante['talle'] or "-",
                        variante['color'] or "-",
                        variante['stock'],
                        f"${precio_total:.2f}"
                    ), tags=tags)
            else:
                tree_stock.insert("", "end", values=(
                    "-",
                    producto['nombre'],
                    producto['tipo'],
                    "-",
                    "-",
                    "Sin variantes",
                    f"${producto['precio_base']:.2f}"
                ))
        
        # Configurar tags
        tree_stock.tag_configure('bajo_stock', background='#ffcccc')
    
    # ==================== VISTA VENTAS ====================
    
    def mostrar_ventas(self):
        """Muestra la vista de historial de ventas"""
        self.limpiar_frame_principal()
        
        label_titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Historial de Ventas",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label_titulo.pack(pady=20)
        
        # Estadísticas
        stats = self.db.obtener_estadisticas_ventas()
        frame_stats = ctk.CTkFrame(self.frame_principal)
        frame_stats.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            frame_stats,
            text=f"Total Ventas: {stats.get('total_ventas', 0)} | "
                 f"Ingresos: ${stats.get('total_ingresos', 0):.2f} | "
                 f"Film DTF: {stats.get('total_film', 0):.2f}m | "
                 f"Papel Sublimación: {stats.get('total_papel', 0):.2f}m",
            font=ctk.CTkFont(size=14)
        ).pack(pady=10)
        
        # Tabla de ventas
        frame_tabla = ctk.CTkFrame(self.frame_principal)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        scrollbar = ctk.CTkScrollbar(frame_tabla)
        scrollbar.pack(side="right", fill="y")
        
        columnas = ("ID", "Fecha", "Cliente", "Total", "Film DTF", "Papel Sublim.")
        tree_ventas = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.configure(command=tree_ventas.yview)
        
        for col in columnas:
            tree_ventas.heading(col, text=col)
        
        tree_ventas.column("ID", width=50)
        tree_ventas.column("Fecha", width=150)
        tree_ventas.column("Cliente", width=200)
        tree_ventas.column("Total", width=100)
        tree_ventas.column("Film DTF", width=100)
        tree_ventas.column("Papel Sublim.", width=120)
        
        tree_ventas.pack(fill="both", expand=True)
        
        # Cargar ventas
        ventas = self.db.obtener_ventas()
        for venta in ventas:
            tree_ventas.insert("", "end", values=(
                venta['id'],
                venta['fecha'],
                venta['cliente'],
                f"${venta['total']:.2f}",
                f"{venta['total_metros_film']:.2f}m",
                f"{venta['total_metros_papel']:.2f}m"
            ))
        
        # Ver detalles al doble clic
        def ver_detalle_venta(event):
            seleccion = tree_ventas.selection()
            if seleccion:
                item = tree_ventas.item(seleccion[0])
                venta_id = item['values'][0]
                self.mostrar_detalle_venta(venta_id)
        
        tree_ventas.bind("<Double-1>", ver_detalle_venta)
    
    def mostrar_detalle_venta(self, venta_id: int):
        """Muestra el detalle de una venta"""
        venta = self.db.obtener_venta(venta_id)
        if not venta:
            messagebox.showerror("Error", "Venta no encontrada.")
            return
        
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Detalle de Venta #{venta_id}")
        dialog.geometry("800x600")
        dialog.transient(self)
        
        # Información de la venta
        frame_info = ctk.CTkFrame(dialog)
        frame_info.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            frame_info,
            text=f"Fecha: {venta['fecha']} | Cliente: {venta['cliente']} | Total: ${venta['total']:.2f}",
            font=ctk.CTkFont(size=14)
        ).pack(pady=10)
        
        ctk.CTkLabel(
            frame_info,
            text=f"Film DTF: {venta['total_metros_film']:.2f}m | Papel Sublimación: {venta['total_metros_papel']:.2f}m",
            font=ctk.CTkFont(size=12)
        ).pack()
        
        if venta['notas']:
            ctk.CTkLabel(
                frame_info,
                text=f"Notas: {venta['notas']}",
                font=ctk.CTkFont(size=12)
            ).pack(pady=5)
        
        # Tabla de detalles
        frame_tabla = ctk.CTkFrame(dialog)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        columnas = ("Producto", "Tipo", "Talle", "Color", "Cantidad", "Precio Unit.", "Subtotal", "Metros")
        tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=90)
        
        tree.pack(fill="both", expand=True)
        
        for detalle in venta['detalles']:
            tree.insert("", "end", values=(
                detalle['producto_nombre'],
                detalle['producto_tipo'],
                detalle['talle'] or "-",
                detalle['color'] or "-",
                detalle['cantidad'],
                f"${detalle['precio_unitario']:.2f}",
                f"${detalle['subtotal']:.2f}",
                f"{detalle['metros_film']:.2f}m"
            ))
    
    # ==================== NUEVA VENTA ====================
    
    def mostrar_nueva_venta(self):
        """Muestra la vista para registrar una nueva venta"""
        self.limpiar_frame_principal()
        
        label_titulo = ctk.CTkLabel(
            self.frame_principal,
            text="Nueva Venta",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        label_titulo.pack(pady=20)
        
        # Frame de información del cliente
        frame_cliente = ctk.CTkFrame(self.frame_principal)
        frame_cliente.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(frame_cliente, text="Cliente:", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        entry_cliente = ctk.CTkEntry(frame_cliente, width=300)
        entry_cliente.pack(side="left", padx=10)
        
        ctk.CTkLabel(frame_cliente, text="Notas:", font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        entry_notas = ctk.CTkEntry(frame_cliente, width=300)
        entry_notas.pack(side="left", padx=10)
        
        # Frame para agregar items
        frame_items = ctk.CTkFrame(self.frame_principal)
        frame_items.pack(fill="x", padx=20, pady=10)
        
        # Lista de items en la venta
        items_venta = []
        
        # Tabla de items
        frame_tabla = ctk.CTkFrame(self.frame_principal)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)
        
        columnas = ("Producto", "Variante", "Cantidad", "Precio", "Subtotal")
        tree_items = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        for col in columnas:
            tree_items.heading(col, text=col)
        
        tree_items.column("Producto", width=200)
        tree_items.column("Variante", width=150)
        tree_items.column("Cantidad", width=100)
        tree_items.column("Precio", width=100)
        tree_items.column("Subtotal", width=100)
        
        tree_items.pack(fill="both", expand=True)
        
        # Total
        frame_total = ctk.CTkFrame(self.frame_principal)
        frame_total.pack(fill="x", padx=20, pady=10)
        
        label_total = ctk.CTkLabel(frame_total, text="Total: $0.00", font=ctk.CTkFont(size=18, weight="bold"))
        label_total.pack(side="right", padx=20)
        
        def actualizar_total():
            total = sum(item['cantidad'] * item['precio_unitario'] for item in items_venta)
            label_total.configure(text=f"Total: ${total:.2f}")
        
        def agregar_item():
            """Diálogo para agregar item a la venta"""
            dialog = ctk.CTkToplevel(self)
            dialog.title("Agregar Item")
            dialog.geometry("500x400")
            dialog.transient(self)
            dialog.grab_set()
            
            # Selección de producto
            ctk.CTkLabel(dialog, text="Producto:", font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
            
            productos = self.db.obtener_productos()
            productos_dict = {f"{p['nombre']} - {p['tipo']}": p for p in productos}
            
            combo_producto = ctk.CTkComboBox(dialog, values=list(productos_dict.keys()), width=400)
            combo_producto.pack()
            if productos_dict:
                combo_producto.set(list(productos_dict.keys())[0])
            
            # Variante
            ctk.CTkLabel(dialog, text="Variante:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
            combo_variante = ctk.CTkComboBox(dialog, values=["Sin variante"], width=400)
            combo_variante.pack()
            combo_variante.set("Sin variante")
            
            variantes_dict = {}
            
            def actualizar_variantes(event=None):
                nonlocal variantes_dict
                producto_key = combo_producto.get()
                if producto_key in productos_dict:
                    producto = productos_dict[producto_key]
                    variantes = self.db.obtener_variantes(producto['id'])
                    if variantes:
                        variantes_dict = {
                            f"{v['talle'] or '-'} / {v['color'] or '-'}": v
                            for v in variantes
                        }
                        combo_variante.configure(values=list(variantes_dict.keys()))
                        combo_variante.set(list(variantes_dict.keys())[0])
                    else:
                        combo_variante.configure(values=["Sin variante"])
                        combo_variante.set("Sin variante")
                        variantes_dict = {}
            
            combo_producto.configure(command=actualizar_variantes)
            actualizar_variantes()
            
            # Cantidad
            ctk.CTkLabel(dialog, text="Cantidad:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
            entry_cantidad = ctk.CTkEntry(dialog, width=400)
            entry_cantidad.insert(0, "1")
            entry_cantidad.pack()
            
            frame_botones = ctk.CTkFrame(dialog)
            frame_botones.pack(pady=20)
            
            def guardar_item():
                try:
                    producto_key = combo_producto.get()
                    producto = productos_dict[producto_key]
                    cantidad = int(entry_cantidad.get())
                    
                    if cantidad <= 0:
                        messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
                        return
                    
                    variante_key = combo_variante.get()
                    variante = None
                    precio = producto['precio_base']
                    variante_str = "Sin variante"
                    
                    if variante_key != "Sin variante" and variante_key in variantes_dict:
                        variante = variantes_dict[variante_key]
                        precio += variante['precio_adicional']
                        variante_str = variante_key
                        
                        # Verificar stock
                        if variante['stock'] < cantidad:
                            if not messagebox.askyesno("Stock Insuficiente", 
                                f"Stock disponible: {variante['stock']}. ¿Continuar de todos modos?"):
                                return
                    
                    item = {
                        'producto_id': producto['id'],
                        'producto_nombre': producto['nombre'],
                        'variante_id': variante['id'] if variante else None,
                        'variante_str': variante_str,
                        'cantidad': cantidad,
                        'precio_unitario': precio
                    }
                    
                    items_venta.append(item)
                    
                    tree_items.insert("", "end", values=(
                        producto['nombre'],
                        variante_str,
                        cantidad,
                        f"${precio:.2f}",
                        f"${cantidad * precio:.2f}"
                    ))
                    
                    actualizar_total()
                    dialog.destroy()
                    
                except ValueError:
                    messagebox.showerror("Error", "Por favor ingrese una cantidad válida.")
            
            btn_guardar = ctk.CTkButton(frame_botones, text="Agregar", command=guardar_item, width=150)
            btn_guardar.pack(side="left", padx=10)
            
            btn_cancelar = ctk.CTkButton(frame_botones, text="Cancelar", command=dialog.destroy, width=150)
            btn_cancelar.pack(side="left", padx=10)
        
        def eliminar_item():
            seleccion = tree_items.selection()
            if seleccion:
                idx = tree_items.index(seleccion[0])
                tree_items.delete(seleccion[0])
                items_venta.pop(idx)
                actualizar_total()
        
        def finalizar_venta():
            cliente = entry_cliente.get().strip()
            notas = entry_notas.get().strip()
            
            if not cliente:
                messagebox.showerror("Error", "Por favor ingrese el nombre del cliente.")
                return
            
            if not items_venta:
                messagebox.showerror("Error", "Debe agregar al menos un item a la venta.")
                return
            
            venta_id, success = self.db.registrar_venta(cliente, items_venta, notas)
            
            if success:
                messagebox.showinfo("Éxito", f"Venta registrada correctamente (ID: {venta_id})")
                self.mostrar_ventas()
            else:
                messagebox.showerror("Error", "No se pudo registrar la venta.")
        
        # Botones
        btn_agregar = ctk.CTkButton(frame_items, text="+ Agregar Item", command=agregar_item)
        btn_agregar.pack(side="left", padx=10)
        
        btn_eliminar = ctk.CTkButton(frame_items, text="- Eliminar Item", command=eliminar_item, fg_color="red")
        btn_eliminar.pack(side="left", padx=10)
        
        btn_finalizar = ctk.CTkButton(
            frame_items,
            text="✓ Finalizar Venta",
            command=finalizar_venta,
            fg_color="green",
            hover_color="darkgreen",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        btn_finalizar.pack(side="right", padx=10)


def main():
    """Función principal"""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
