"""
Sales view for viewing sales history and details.
"""

import customtkinter as ctk
from tkinter import messagebox


class SalesView:
    """Sales history view."""
    
    def __init__(self, parent, sale_model, db):
        """Initialize sales view."""
        self.parent = parent
        self.sale_model = sale_model
        self.db = db
        
        self.create_widgets()
        self.load_sales()
    
    def create_widgets(self):
        """Create and layout widgets."""
        # Configure grid
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_rowconfigure(2, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            self.parent, 
            text="Historial de Ventas", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Search frame
        search_frame = ctk.CTkFrame(self.parent)
        search_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Buscar por cliente...",
            width=300
        )
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)
        
        self.search_btn = ctk.CTkButton(
            search_frame, 
            text="Buscar", 
            command=self.search_sales,
            width=100
        )
        self.search_btn.grid(row=0, column=1, padx=5, pady=10)
        
        self.reset_btn = ctk.CTkButton(
            search_frame, 
            text="Todas", 
            command=self.load_sales,
            width=100
        )
        self.reset_btn.grid(row=0, column=2, padx=5, pady=10)
        
        self.today_btn = ctk.CTkButton(
            search_frame, 
            text="Ventas de Hoy", 
            command=self.show_today_sales,
            width=120
        )
        self.today_btn.grid(row=0, column=3, padx=5, pady=10)
        
        # Sales list frame
        list_frame = ctk.CTkFrame(self.parent)
        list_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        
        self.sales_scrollable = ctk.CTkScrollableFrame(list_frame)
        self.sales_scrollable.grid(row=0, column=0, sticky="nsew")
        self.sales_scrollable.grid_columnconfigure(0, weight=1)
    
    def load_sales(self):
        """Load and display all sales."""
        # Clear current list
        for widget in self.sales_scrollable.winfo_children():
            widget.destroy()
        
        sales = self.sale_model.get_all_sales()
        
        if not sales:
            label = ctk.CTkLabel(
                self.sales_scrollable, 
                text="No hay ventas registradas",
                font=ctk.CTkFont(size=14)
            )
            label.grid(row=0, column=0, pady=20)
            return
        
        # Headers
        headers = ["ID", "Cliente", "Fecha", "Total", "Tela (m)", "Vinilo (m)", "Items", "Acciones"]
        header_frame = ctk.CTkFrame(self.sales_scrollable)
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=ctk.CTkFont(weight="bold"),
                width=100
            )
            label.grid(row=0, column=i, padx=5, pady=5)
        
        # Sales rows
        for idx, sale in enumerate(sales, start=1):
            self.create_sale_row(idx, sale)
    
    def create_sale_row(self, row_num, sale):
        """Create a row for a sale."""
        row_frame = ctk.CTkFrame(self.sales_scrollable)
        row_frame.grid(row=row_num, column=0, sticky="ew", padx=5, pady=2)
        
        # ID
        ctk.CTkLabel(row_frame, text=str(sale['id']), width=100).grid(
            row=0, column=0, padx=5, pady=5
        )
        
        # Client
        ctk.CTkLabel(row_frame, text=sale['client_name'], width=150).grid(
            row=0, column=1, padx=5, pady=5
        )
        
        # Date
        date_str = sale['sale_date'].split('.')[0] if '.' in sale['sale_date'] else sale['sale_date']
        ctk.CTkLabel(row_frame, text=date_str, width=150).grid(
            row=0, column=2, padx=5, pady=5
        )
        
        # Total
        ctk.CTkLabel(row_frame, text=f"${sale['total_amount']:.2f}", width=100).grid(
            row=0, column=3, padx=5, pady=5
        )
        
        # Fabric
        ctk.CTkLabel(row_frame, text=f"{sale['total_fabric_meters']:.2f}", width=100).grid(
            row=0, column=4, padx=5, pady=5
        )
        
        # Vinyl
        ctk.CTkLabel(row_frame, text=f"{sale['total_vinyl_meters']:.2f}", width=100).grid(
            row=0, column=5, padx=5, pady=5
        )
        
        # Items count
        ctk.CTkLabel(row_frame, text=str(sale['items_count']), width=100).grid(
            row=0, column=6, padx=5, pady=5
        )
        
        # Actions
        view_btn = ctk.CTkButton(
            row_frame, 
            text="👁️ Ver", 
            command=lambda s=sale: self.show_sale_details(s),
            width=80
        )
        view_btn.grid(row=0, column=7, padx=5, pady=5)
    
    def search_sales(self):
        """Search sales by client name."""
        search_term = self.search_entry.get()
        
        # Clear current list
        for widget in self.sales_scrollable.winfo_children():
            widget.destroy()
        
        sales = self.sale_model.search_sales(search_term=search_term)
        
        if not sales:
            label = ctk.CTkLabel(
                self.sales_scrollable, 
                text="No se encontraron ventas",
                font=ctk.CTkFont(size=14)
            )
            label.grid(row=0, column=0, pady=20)
            return
        
        self._display_sales_list(sales)
    
    def show_today_sales(self):
        """Show today's sales."""
        # Clear current list
        for widget in self.sales_scrollable.winfo_children():
            widget.destroy()
        
        sales = self.sale_model.get_today_sales()
        
        if not sales:
            label = ctk.CTkLabel(
                self.sales_scrollable, 
                text="No hay ventas hoy",
                font=ctk.CTkFont(size=14)
            )
            label.grid(row=0, column=0, pady=20)
            return
        
        self._display_sales_list(sales)
    
    def _display_sales_list(self, sales):
        """Helper to display list of sales."""
        # Headers
        headers = ["ID", "Cliente", "Fecha", "Total", "Tela (m)", "Vinilo (m)", "Items", "Acciones"]
        header_frame = ctk.CTkFrame(self.sales_scrollable)
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=ctk.CTkFont(weight="bold"),
                width=100
            )
            label.grid(row=0, column=i, padx=5, pady=5)
        
        # Sales rows with items count
        for idx, sale in enumerate(sales, start=1):
            # Get items count
            self.db.execute(
                'SELECT COUNT(*) as count FROM sale_items WHERE sale_id = ?',
                (sale['id'],)
            )
            items_count = self.db.fetchone()['count']
            
            # Create extended sale dict
            sale_dict = dict(sale)
            sale_dict['items_count'] = items_count
            
            self.create_sale_row(idx, sale_dict)
    
    def show_sale_details(self, sale):
        """Show sale details dialog."""
        SaleDetailsDialog(self.parent, sale, self.sale_model)


class SaleDetailsDialog(ctk.CTkToplevel):
    """Dialog for viewing sale details."""
    
    def __init__(self, parent, sale, sale_model):
        """Initialize sale details dialog."""
        super().__init__(parent)
        
        self.sale = sale
        self.sale_model = sale_model
        
        self.title(f"Detalle de Venta #{sale['id']}")
        self.geometry("700x600")
        
        self.create_widgets()
        self.load_details()
        
        # Make modal
        self.transient(parent)
        self.grab_set()
    
    def create_widgets(self):
        """Create dialog widgets."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            self, 
            text=f"Venta #{self.sale['id']}", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=20)
        
        # Info frame
        info_frame = ctk.CTkFrame(self)
        info_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Sale info
        date_str = self.sale['sale_date'].split('.')[0] if '.' in self.sale['sale_date'] else self.sale['sale_date']
        
        info_text = f"Cliente: {self.sale['client_name']}\n"
        info_text += f"Fecha: {date_str}\n"
        info_text += f"Total: ${self.sale['total_amount']:.2f}\n"
        info_text += f"Tela usada: {self.sale['total_fabric_meters']:.2f}m\n"
        info_text += f"Vinilo usado: {self.sale['total_vinyl_meters']:.2f}m"
        if self.sale['notes']:
            info_text += f"\nNotas: {self.sale['notes']}"
        
        info_label = ctk.CTkLabel(
            info_frame, 
            text=info_text,
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        info_label.pack(padx=20, pady=10)
        
        # Items label
        items_label = ctk.CTkLabel(
            self, 
            text="Productos", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        items_label.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="w")
        
        # Items frame
        items_frame = ctk.CTkScrollableFrame(self)
        items_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
        self.grid_rowconfigure(3, weight=1)
        
        self.items_frame = items_frame
        
        # Close button
        close_btn = ctk.CTkButton(
            self, 
            text="Cerrar", 
            command=self.destroy,
            width=120
        )
        close_btn.grid(row=4, column=0, padx=20, pady=20)
    
    def load_details(self):
        """Load and display sale items."""
        items = self.sale_model.get_sale_items(self.sale['id'])
        
        if not items:
            label = ctk.CTkLabel(
                self.items_frame, 
                text="No hay items"
            )
            label.pack(pady=20)
            return
        
        # Headers
        headers = ["Producto", "Cantidad", "Precio Unit.", "Subtotal", "Tela (m)", "Vinilo (m)"]
        header_frame = ctk.CTkFrame(self.items_frame)
        header_frame.pack(fill="x", padx=5, pady=5)
        
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame, 
                text=header, 
                font=ctk.CTkFont(weight="bold"),
                width=100
            )
            label.grid(row=0, column=i, padx=5, pady=5)
        
        # Items rows
        for item in items:
            item_frame = ctk.CTkFrame(self.items_frame)
            item_frame.pack(fill="x", padx=5, pady=2)
            
            ctk.CTkLabel(item_frame, text=item['product_name'], width=150).grid(
                row=0, column=0, padx=5, pady=5
            )
            ctk.CTkLabel(item_frame, text=str(item['quantity']), width=100).grid(
                row=0, column=1, padx=5, pady=5
            )
            ctk.CTkLabel(item_frame, text=f"${item['unit_price']:.2f}", width=100).grid(
                row=0, column=2, padx=5, pady=5
            )
            ctk.CTkLabel(item_frame, text=f"${item['subtotal']:.2f}", width=100).grid(
                row=0, column=3, padx=5, pady=5
            )
            ctk.CTkLabel(item_frame, text=f"{item['fabric_meters']:.2f}", width=100).grid(
                row=0, column=4, padx=5, pady=5
            )
            ctk.CTkLabel(item_frame, text=f"{item['vinyl_meters']:.2f}", width=100).grid(
                row=0, column=5, padx=5, pady=5
            )
