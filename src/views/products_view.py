"""
Products view for managing store products.
Includes CRUD operations and search functionality.
"""

import customtkinter as ctk
from tkinter import messagebox


class ProductsView:
    """Products management view."""
    
    def __init__(self, parent, product_model, db):
        """Initialize products view."""
        self.parent = parent
        self.product_model = product_model
        self.db = db
        self.selected_product_id = None
        
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
            text="Gestión de Productos", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Search and filter frame
        search_frame = ctk.CTkFrame(self.parent)
        search_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Buscar producto...",
            width=300
        )
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)
        
        self.search_btn = ctk.CTkButton(
            search_frame, 
            text="Buscar", 
            command=self.search_products,
            width=100
        )
        self.search_btn.grid(row=0, column=1, padx=5, pady=10)
        
        self.low_stock_btn = ctk.CTkButton(
            search_frame, 
            text="Stock Bajo", 
            command=self.show_low_stock,
            width=100
        )
        self.low_stock_btn.grid(row=0, column=2, padx=5, pady=10)
        
        self.reset_btn = ctk.CTkButton(
            search_frame, 
            text="Todos", 
            command=self.load_products,
            width=100
        )
        self.reset_btn.grid(row=0, column=3, padx=5, pady=10)
        
        self.add_btn = ctk.CTkButton(
            search_frame, 
            text="➕ Nuevo Producto", 
            command=self.show_add_product,
            fg_color="green",
            hover_color="darkgreen",
            width=150
        )
        self.add_btn.grid(row=0, column=4, padx=10, pady=10)
        
        # Products list frame with scrollbar
        list_frame = ctk.CTkFrame(self.parent)
        list_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        
        self.products_scrollable = ctk.CTkScrollableFrame(list_frame)
        self.products_scrollable.grid(row=0, column=0, sticky="nsew")
        self.products_scrollable.grid_columnconfigure(0, weight=1)
    
    def load_products(self):
        """Load and display all products."""
        # Clear current list
        for widget in self.products_scrollable.winfo_children():
            widget.destroy()
        
        products = self.product_model.get_all()
        
        if not products:
            label = ctk.CTkLabel(
                self.products_scrollable, 
                text="No hay productos registrados",
                font=ctk.CTkFont(size=14)
            )
            label.grid(row=0, column=0, pady=20)
            return
        
        # Headers
        headers = ["ID", "Nombre", "Tipo", "Talle", "Color", "Precio", 
                  "Stock", "Tela(m)", "Vinilo(m)", "Acciones"]
        header_frame = ctk.CTkFrame(self.products_scrollable)
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=ctk.CTkFont(weight="bold"),
                width=80
            )
            label.grid(row=0, column=i, padx=5, pady=5)
        
        # Product rows
        for idx, product in enumerate(products, start=1):
            self.create_product_row(idx, product)
    
    def create_product_row(self, row_num, product):
        """Create a row for a product."""
        row_frame = ctk.CTkFrame(self.products_scrollable)
        row_frame.grid(row=row_num, column=0, sticky="ew", padx=5, pady=2)
        
        # Determine stock color
        stock_color = "red" if product['stock'] <= 5 else None
        
        # ID
        ctk.CTkLabel(row_frame, text=str(product['id']), width=80).grid(
            row=0, column=0, padx=5, pady=5
        )
        
        # Name
        ctk.CTkLabel(row_frame, text=product['name'], width=150).grid(
            row=0, column=1, padx=5, pady=5
        )
        
        # Type
        ctk.CTkLabel(row_frame, text=product['type'], width=100).grid(
            row=0, column=2, padx=5, pady=5
        )
        
        # Size
        ctk.CTkLabel(row_frame, text=product['size'] or '-', width=80).grid(
            row=0, column=3, padx=5, pady=5
        )
        
        # Color
        ctk.CTkLabel(row_frame, text=product['color'] or '-', width=80).grid(
            row=0, column=4, padx=5, pady=5
        )
        
        # Price
        ctk.CTkLabel(row_frame, text=f"${product['price']:.2f}", width=80).grid(
            row=0, column=5, padx=5, pady=5
        )
        
        # Stock
        stock_label = ctk.CTkLabel(
            row_frame, 
            text=str(product['stock']), 
            width=80,
            text_color=stock_color
        )
        stock_label.grid(row=0, column=6, padx=5, pady=5)
        
        # Fabric meters
        ctk.CTkLabel(row_frame, text=f"{product['fabric_meters']:.2f}", width=80).grid(
            row=0, column=7, padx=5, pady=5
        )
        
        # Vinyl meters
        ctk.CTkLabel(row_frame, text=f"{product['vinyl_meters']:.2f}", width=80).grid(
            row=0, column=8, padx=5, pady=5
        )
        
        # Actions
        actions_frame = ctk.CTkFrame(row_frame)
        actions_frame.grid(row=0, column=9, padx=5, pady=5)
        
        edit_btn = ctk.CTkButton(
            actions_frame, 
            text="✏️", 
            command=lambda p=product: self.show_edit_product(p),
            width=40
        )
        edit_btn.grid(row=0, column=0, padx=2)
        
        delete_btn = ctk.CTkButton(
            actions_frame, 
            text="🗑️", 
            command=lambda pid=product['id']: self.delete_product(pid),
            width=40,
            fg_color="red",
            hover_color="darkred"
        )
        delete_btn.grid(row=0, column=1, padx=2)
    
    def search_products(self):
        """Search products by term."""
        search_term = self.search_entry.get()
        
        # Clear current list
        for widget in self.products_scrollable.winfo_children():
            widget.destroy()
        
        products = self.product_model.search(search_term=search_term)
        
        if not products:
            label = ctk.CTkLabel(
                self.products_scrollable, 
                text="No se encontraron productos",
                font=ctk.CTkFont(size=14)
            )
            label.grid(row=0, column=0, pady=20)
            return
        
        # Display headers and products
        self._display_products_list(products)
    
    def show_low_stock(self):
        """Show products with low stock."""
        # Clear current list
        for widget in self.products_scrollable.winfo_children():
            widget.destroy()
        
        products = self.product_model.get_low_stock_products(threshold=5)
        
        if not products:
            label = ctk.CTkLabel(
                self.products_scrollable, 
                text="No hay productos con stock bajo",
                font=ctk.CTkFont(size=14)
            )
            label.grid(row=0, column=0, pady=20)
            return
        
        self._display_products_list(products)
    
    def _display_products_list(self, products):
        """Helper to display list of products."""
        # Headers
        headers = ["ID", "Nombre", "Tipo", "Talle", "Color", "Precio", 
                  "Stock", "Tela(m)", "Vinilo(m)", "Acciones"]
        header_frame = ctk.CTkFrame(self.products_scrollable)
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=ctk.CTkFont(weight="bold"),
                width=80
            )
            label.grid(row=0, column=i, padx=5, pady=5)
        
        # Product rows
        for idx, product in enumerate(products, start=1):
            self.create_product_row(idx, product)
    
    def show_add_product(self):
        """Show add product dialog."""
        ProductFormDialog(self.parent, self.product_model, None, self.load_products)
    
    def show_edit_product(self, product):
        """Show edit product dialog."""
        ProductFormDialog(self.parent, self.product_model, product, self.load_products)
    
    def delete_product(self, product_id):
        """Delete a product."""
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?"):
            try:
                self.product_model.delete(product_id)
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                self.load_products()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")


class ProductFormDialog(ctk.CTkToplevel):
    """Dialog for adding/editing products."""
    
    def __init__(self, parent, product_model, product=None, callback=None):
        """Initialize product form dialog."""
        super().__init__(parent)
        
        self.product_model = product_model
        self.product = product
        self.callback = callback
        
        self.title("Editar Producto" if product else "Nuevo Producto")
        self.geometry("500x600")
        
        self.create_form()
        
        if product:
            self.fill_form(product)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
    
    def create_form(self):
        """Create form fields."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Title
        title_text = "Editar Producto" if self.product else "Nuevo Producto"
        title = ctk.CTkLabel(
            self, 
            text=title_text, 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=20)
        
        # Form frame
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Name
        ctk.CTkLabel(form_frame, text="Nombre:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(form_frame, width=300)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Type
        ctk.CTkLabel(form_frame, text="Tipo:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.type_entry = ctk.CTkEntry(form_frame, width=300)
        self.type_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Size
        ctk.CTkLabel(form_frame, text="Talle:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.size_entry = ctk.CTkEntry(form_frame, width=300)
        self.size_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Color
        ctk.CTkLabel(form_frame, text="Color:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.color_entry = ctk.CTkEntry(form_frame, width=300)
        self.color_entry.grid(row=3, column=1, padx=10, pady=10)
        
        # Price
        ctk.CTkLabel(form_frame, text="Precio:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.price_entry = ctk.CTkEntry(form_frame, width=300)
        self.price_entry.grid(row=4, column=1, padx=10, pady=10)
        
        # Stock
        ctk.CTkLabel(form_frame, text="Stock:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.stock_entry = ctk.CTkEntry(form_frame, width=300)
        self.stock_entry.grid(row=5, column=1, padx=10, pady=10)
        
        # Fabric meters
        ctk.CTkLabel(form_frame, text="Metros Tela:").grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.fabric_entry = ctk.CTkEntry(form_frame, width=300)
        self.fabric_entry.grid(row=6, column=1, padx=10, pady=10)
        self.fabric_entry.insert(0, "0")
        
        # Vinyl meters
        ctk.CTkLabel(form_frame, text="Metros Vinilo:").grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.vinyl_entry = ctk.CTkEntry(form_frame, width=300)
        self.vinyl_entry.grid(row=7, column=1, padx=10, pady=10)
        self.vinyl_entry.insert(0, "0")
        
        # Print type
        ctk.CTkLabel(form_frame, text="Tipo Impresión:").grid(row=8, column=0, padx=10, pady=10, sticky="w")
        self.print_type_entry = ctk.CTkEntry(form_frame, width=300, placeholder_text="DTF, Sublimación, etc.")
        self.print_type_entry.grid(row=8, column=1, padx=10, pady=10)
        
        # Buttons
        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.grid(row=2, column=0, padx=20, pady=20)
        
        save_btn = ctk.CTkButton(
            buttons_frame, 
            text="Guardar", 
            command=self.save_product,
            width=120
        )
        save_btn.grid(row=0, column=0, padx=10)
        
        cancel_btn = ctk.CTkButton(
            buttons_frame, 
            text="Cancelar", 
            command=self.destroy,
            width=120
        )
        cancel_btn.grid(row=0, column=1, padx=10)
    
    def fill_form(self, product):
        """Fill form with product data."""
        self.name_entry.insert(0, product['name'])
        self.type_entry.insert(0, product['type'])
        self.size_entry.insert(0, product['size'] or '')
        self.color_entry.insert(0, product['color'] or '')
        self.price_entry.insert(0, str(product['price']))
        self.stock_entry.insert(0, str(product['stock']))
        self.fabric_entry.delete(0, 'end')
        self.fabric_entry.insert(0, str(product['fabric_meters']))
        self.vinyl_entry.delete(0, 'end')
        self.vinyl_entry.insert(0, str(product['vinyl_meters']))
        self.print_type_entry.insert(0, product['print_type'] or '')
    
    def save_product(self):
        """Save product data."""
        try:
            # Validate inputs
            name = self.name_entry.get().strip()
            product_type = self.type_entry.get().strip()
            size = self.size_entry.get().strip()
            color = self.color_entry.get().strip()
            price = float(self.price_entry.get())
            stock = int(self.stock_entry.get())
            fabric_meters = float(self.fabric_entry.get() or 0)
            vinyl_meters = float(self.vinyl_entry.get() or 0)
            print_type = self.print_type_entry.get().strip()
            
            if not name or not product_type:
                messagebox.showerror("Error", "Nombre y Tipo son obligatorios")
                return
            
            if price < 0 or stock < 0:
                messagebox.showerror("Error", "Precio y Stock deben ser mayores o iguales a 0")
                return
            
            # Save or update
            if self.product:
                self.product_model.update(
                    self.product['id'], name, product_type, size, color, 
                    price, stock, fabric_meters, vinyl_meters, print_type
                )
                messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            else:
                self.product_model.create(
                    name, product_type, size, color, price, stock, 
                    fabric_meters, vinyl_meters, print_type
                )
                messagebox.showinfo("Éxito", "Producto creado correctamente")
            
            if self.callback:
                self.callback()
            
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Error", "Verifique que los valores numéricos sean correctos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar producto: {str(e)}")
