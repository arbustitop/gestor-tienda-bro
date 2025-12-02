"""
New sale view for creating sales transactions.
Includes product selection, quantity input, and automatic calculations.
"""

import customtkinter as ctk
from tkinter import messagebox


class NewSaleView:
    """New sale creation view."""
    
    def __init__(self, parent, sale_model, product_model, db, on_complete_callback):
        """Initialize new sale view."""
        self.parent = parent
        self.sale_model = sale_model
        self.product_model = product_model
        self.db = db
        self.on_complete_callback = on_complete_callback
        
        self.sale_items = []  # List of {product, quantity}
        
        self.create_widgets()
        self.load_products()
    
    def create_widgets(self):
        """Create and layout widgets."""
        # Configure grid
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(2, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            self.parent, 
            text="Nueva Venta", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Client info frame
        client_frame = ctk.CTkFrame(self.parent)
        client_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(client_frame, text="Cliente:", font=ctk.CTkFont(size=14)).grid(
            row=0, column=0, padx=10, pady=10
        )
        self.client_entry = ctk.CTkEntry(client_frame, width=300, placeholder_text="Nombre del cliente")
        self.client_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ctk.CTkLabel(client_frame, text="Notas:", font=ctk.CTkFont(size=14)).grid(
            row=0, column=2, padx=10, pady=10
        )
        self.notes_entry = ctk.CTkEntry(client_frame, width=300, placeholder_text="Notas opcionales")
        self.notes_entry.grid(row=0, column=3, padx=10, pady=10)
        
        # Main content frame (products selection and cart)
        content_frame = ctk.CTkFrame(self.parent)
        content_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        content_frame.grid_columnconfigure((0, 1), weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Left side - Products list
        products_label = ctk.CTkLabel(
            content_frame, 
            text="Productos Disponibles", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        products_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Search frame
        search_frame = ctk.CTkFrame(content_frame)
        search_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        self.search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Buscar producto..."
        )
        self.search_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry.bind('<KeyRelease>', lambda e: self.load_products())
        
        # Products scrollable frame
        self.products_frame = ctk.CTkScrollableFrame(content_frame)
        self.products_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        content_frame.grid_rowconfigure(2, weight=1)
        
        # Right side - Shopping cart
        cart_label = ctk.CTkLabel(
            content_frame, 
            text="Carrito de Venta", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        cart_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        self.cart_frame = ctk.CTkScrollableFrame(content_frame)
        self.cart_frame.grid(row=1, column=1, rowspan=2, padx=10, pady=(0, 10), sticky="nsew")
        
        # Totals frame
        totals_frame = ctk.CTkFrame(self.parent)
        totals_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.total_label = ctk.CTkLabel(
            totals_frame, 
            text="Total: $0.00", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.total_label.grid(row=0, column=0, padx=20, pady=10)
        
        self.fabric_label = ctk.CTkLabel(
            totals_frame, 
            text="Tela: 0.00m", 
            font=ctk.CTkFont(size=14)
        )
        self.fabric_label.grid(row=0, column=1, padx=20, pady=10)
        
        self.vinyl_label = ctk.CTkLabel(
            totals_frame, 
            text="Vinilo: 0.00m", 
            font=ctk.CTkFont(size=14)
        )
        self.vinyl_label.grid(row=0, column=2, padx=20, pady=10)
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(self.parent)
        buttons_frame.grid(row=4, column=0, padx=20, pady=10)
        
        complete_btn = ctk.CTkButton(
            buttons_frame, 
            text="Completar Venta", 
            command=self.complete_sale,
            fg_color="green",
            hover_color="darkgreen",
            width=150,
            height=40
        )
        complete_btn.grid(row=0, column=0, padx=10)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame, 
            text="Cancelar", 
            command=self.on_complete_callback,
            width=150,
            height=40
        )
        cancel_btn.grid(row=0, column=1, padx=10)
    
    def load_products(self):
        """Load and display available products."""
        # Clear products list
        for widget in self.products_frame.winfo_children():
            widget.destroy()
        
        search_term = self.search_entry.get()
        products = self.product_model.search(search_term=search_term)
        
        if not products:
            label = ctk.CTkLabel(
                self.products_frame, 
                text="No hay productos disponibles"
            )
            label.pack(pady=20)
            return
        
        # Display products
        for product in products:
            self.create_product_item(product)
    
    def create_product_item(self, product):
        """Create a product item card."""
        item_frame = ctk.CTkFrame(self.products_frame)
        item_frame.pack(fill="x", padx=5, pady=5)
        
        # Product info
        info_text = f"{product['name']}"
        if product['size']:
            info_text += f" - {product['size']}"
        if product['color']:
            info_text += f" - {product['color']}"
        info_text += f"\nPrecio: ${product['price']:.2f} | Stock: {product['stock']}"
        
        info_label = ctk.CTkLabel(
            item_frame, 
            text=info_text,
            justify="left"
        )
        info_label.pack(side="left", padx=10, pady=5)
        
        # Add button
        add_btn = ctk.CTkButton(
            item_frame, 
            text="Agregar", 
            command=lambda p=product: self.add_to_cart(p),
            width=80
        )
        add_btn.pack(side="right", padx=10, pady=5)
    
    def add_to_cart(self, product):
        """Add product to cart with quantity dialog."""
        if product['stock'] <= 0:
            messagebox.showwarning("Sin Stock", "Este producto no tiene stock disponible")
            return
        
        # Show quantity dialog
        QuantityDialog(self.parent, product, self.add_item_to_cart)
    
    def add_item_to_cart(self, product, quantity):
        """Add item to cart with specified quantity."""
        # Check if product already in cart
        for item in self.sale_items:
            if item['product']['id'] == product['id']:
                # Update quantity
                new_quantity = item['quantity'] + quantity
                if new_quantity > product['stock']:
                    messagebox.showwarning(
                        "Stock Insuficiente", 
                        f"Stock disponible: {product['stock']}"
                    )
                    return
                item['quantity'] = new_quantity
                self.update_cart_display()
                return
        
        # Add new item
        self.sale_items.append({
            'product': product,
            'quantity': quantity
        })
        self.update_cart_display()
    
    def update_cart_display(self):
        """Update cart display and totals."""
        # Clear cart
        for widget in self.cart_frame.winfo_children():
            widget.destroy()
        
        if not self.sale_items:
            label = ctk.CTkLabel(
                self.cart_frame, 
                text="Carrito vacío"
            )
            label.pack(pady=20)
            self.update_totals()
            return
        
        # Display cart items
        for idx, item in enumerate(self.sale_items):
            self.create_cart_item(item, idx)
        
        self.update_totals()
    
    def create_cart_item(self, item, index):
        """Create a cart item display."""
        product = item['product']
        quantity = item['quantity']
        subtotal = product['price'] * quantity
        
        item_frame = ctk.CTkFrame(self.cart_frame)
        item_frame.pack(fill="x", padx=5, pady=5)
        
        # Product info
        info_text = f"{product['name']}"
        if product['size']:
            info_text += f" - {product['size']}"
        info_text += f"\n${product['price']:.2f} x {quantity} = ${subtotal:.2f}"
        
        info_label = ctk.CTkLabel(
            item_frame, 
            text=info_text,
            justify="left"
        )
        info_label.pack(side="left", padx=10, pady=5)
        
        # Remove button
        remove_btn = ctk.CTkButton(
            item_frame, 
            text="✖", 
            command=lambda i=index: self.remove_from_cart(i),
            width=40,
            fg_color="red",
            hover_color="darkred"
        )
        remove_btn.pack(side="right", padx=10, pady=5)
    
    def remove_from_cart(self, index):
        """Remove item from cart."""
        if 0 <= index < len(self.sale_items):
            self.sale_items.pop(index)
            self.update_cart_display()
    
    def update_totals(self):
        """Update total amounts display."""
        total_amount = 0
        total_fabric = 0
        total_vinyl = 0
        
        for item in self.sale_items:
            product = item['product']
            quantity = item['quantity']
            
            total_amount += product['price'] * quantity
            total_fabric += product['fabric_meters'] * quantity
            total_vinyl += product['vinyl_meters'] * quantity
        
        self.total_label.configure(text=f"Total: ${total_amount:.2f}")
        self.fabric_label.configure(text=f"Tela: {total_fabric:.2f}m")
        self.vinyl_label.configure(text=f"Vinilo: {total_vinyl:.2f}m")
    
    def complete_sale(self):
        """Complete the sale transaction."""
        client_name = self.client_entry.get().strip()
        
        if not client_name:
            messagebox.showerror("Error", "Ingrese el nombre del cliente")
            return
        
        if not self.sale_items:
            messagebox.showerror("Error", "Agregue productos a la venta")
            return
        
        # Prepare sale items
        items = []
        for item in self.sale_items:
            items.append({
                'product_id': item['product']['id'],
                'quantity': item['quantity']
            })
        
        notes = self.notes_entry.get().strip()
        
        try:
            # Create sale
            sale_id = self.sale_model.create_sale(client_name, items, notes)
            
            if sale_id:
                messagebox.showinfo(
                    "Éxito", 
                    f"Venta completada correctamente\nID: {sale_id}"
                )
                # Call callback to return to sales view
                if self.on_complete_callback:
                    self.on_complete_callback()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al completar la venta: {str(e)}")


class QuantityDialog(ctk.CTkToplevel):
    """Dialog for entering quantity."""
    
    def __init__(self, parent, product, callback):
        """Initialize quantity dialog."""
        super().__init__(parent)
        
        self.product = product
        self.callback = callback
        
        self.title("Cantidad")
        self.geometry("300x200")
        
        # Product info
        info_label = ctk.CTkLabel(
            self, 
            text=f"{product['name']}\nStock disponible: {product['stock']}",
            font=ctk.CTkFont(size=14)
        )
        info_label.pack(padx=20, pady=20)
        
        # Quantity entry
        ctk.CTkLabel(self, text="Cantidad:").pack(padx=20, pady=(10, 5))
        self.quantity_entry = ctk.CTkEntry(self, width=200)
        self.quantity_entry.pack(padx=20, pady=5)
        self.quantity_entry.insert(0, "1")
        self.quantity_entry.focus()
        
        # Buttons
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(padx=20, pady=20)
        
        ok_btn = ctk.CTkButton(
            buttons_frame, 
            text="Agregar", 
            command=self.add_quantity,
            width=100
        )
        ok_btn.grid(row=0, column=0, padx=5)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame, 
            text="Cancelar", 
            command=self.destroy,
            width=100
        )
        cancel_btn.grid(row=0, column=1, padx=5)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        # Bind Enter key
        self.bind('<Return>', lambda e: self.add_quantity())
    
    def add_quantity(self):
        """Validate and add quantity."""
        try:
            quantity = int(self.quantity_entry.get())
            
            if quantity <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return
            
            if quantity > self.product['stock']:
                messagebox.showerror(
                    "Error", 
                    f"Stock insuficiente. Disponible: {self.product['stock']}"
                )
                return
            
            self.callback(self.product, quantity)
            self.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido")
