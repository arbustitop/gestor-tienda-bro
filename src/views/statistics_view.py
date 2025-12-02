"""
Statistics view for displaying store analytics and metrics.
"""

import customtkinter as ctk


class StatisticsView:
    """Statistics and analytics view."""
    
    def __init__(self, parent, statistics, db):
        """Initialize statistics view."""
        self.parent = parent
        self.statistics = statistics
        self.db = db
        
        self.create_widgets()
        self.load_statistics()
    
    def create_widgets(self):
        """Create and layout widgets."""
        # Configure grid
        self.parent.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            self.parent, 
            text="Estadísticas", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Scrollable content
        self.content_frame = ctk.CTkScrollableFrame(self.parent)
        self.content_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.parent.grid_rowconfigure(1, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
    
    def load_statistics(self):
        """Load and display statistics."""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        row = 0
        
        # Daily summary
        self.create_section_title(row, "Resumen de Hoy")
        row += 1
        
        daily = self.statistics.get_daily_summary()
        daily_frame = self.create_stats_grid(row)
        
        self.add_stat_item(daily_frame, 0, 0, "Ventas", f"${daily['total_sales']:.2f}")
        self.add_stat_item(daily_frame, 0, 1, "Número de Ventas", str(daily['sales_count']))
        self.add_stat_item(daily_frame, 1, 0, "Tela Usada", f"{daily['total_fabric']:.2f}m")
        self.add_stat_item(daily_frame, 1, 1, "Vinilo Usado", f"{daily['total_vinyl']:.2f}m")
        self.add_stat_item(daily_frame, 2, 0, "Productos Stock Bajo", str(daily['low_stock_count']))
        
        row += 1
        
        # Monthly revenue
        monthly = self.statistics.get_monthly_revenue()
        self.create_section_title(row, "Este Mes")
        row += 1
        
        monthly_frame = self.create_stats_grid(row)
        self.add_stat_item(monthly_frame, 0, 0, "Ingresos Mensuales", f"${monthly['monthly_revenue']:.2f}")
        self.add_stat_item(monthly_frame, 0, 1, "Ventas del Mes", str(monthly['monthly_sales']))
        
        row += 1
        
        # Inventory
        inventory = self.statistics.get_inventory_value()
        self.create_section_title(row, "Inventario")
        row += 1
        
        inventory_frame = self.create_stats_grid(row)
        self.add_stat_item(inventory_frame, 0, 0, "Valor Total", f"${inventory['inventory_value']:.2f}")
        self.add_stat_item(inventory_frame, 0, 1, "Unidades Totales", str(inventory['total_units']))
        
        row += 1
        
        # Top products
        self.create_section_title(row, "Productos Más Vendidos")
        row += 1
        
        top_products = self.statistics.get_top_products(10)
        if top_products:
            products_frame = ctk.CTkFrame(self.content_frame)
            products_frame.grid(row=row, column=0, padx=10, pady=10, sticky="ew")
            
            # Headers
            headers = ["#", "Producto", "Cantidad", "Ingresos", "Ventas"]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(
                    products_frame, 
                    text=header, 
                    font=ctk.CTkFont(weight="bold")
                )
                label.grid(row=0, column=i, padx=10, pady=5)
            
            # Products
            for idx, product in enumerate(top_products, start=1):
                ctk.CTkLabel(products_frame, text=str(idx)).grid(
                    row=idx, column=0, padx=10, pady=5
                )
                ctk.CTkLabel(products_frame, text=product['product_name']).grid(
                    row=idx, column=1, padx=10, pady=5, sticky="w"
                )
                ctk.CTkLabel(products_frame, text=str(product['total_quantity'])).grid(
                    row=idx, column=2, padx=10, pady=5
                )
                ctk.CTkLabel(products_frame, text=f"${product['total_revenue']:.2f}").grid(
                    row=idx, column=3, padx=10, pady=5
                )
                ctk.CTkLabel(products_frame, text=str(product['sales_count'])).grid(
                    row=idx, column=4, padx=10, pady=5
                )
        
        row += 1
        
        # Product types distribution
        self.create_section_title(row, "Distribución por Tipo")
        row += 1
        
        types = self.statistics.get_product_type_distribution()
        if types:
            types_frame = ctk.CTkFrame(self.content_frame)
            types_frame.grid(row=row, column=0, padx=10, pady=10, sticky="ew")
            
            # Headers
            headers = ["Tipo", "Cantidad de Productos", "Stock Total"]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(
                    types_frame, 
                    text=header, 
                    font=ctk.CTkFont(weight="bold")
                )
                label.grid(row=0, column=i, padx=10, pady=5)
            
            # Types
            for idx, ptype in enumerate(types, start=1):
                ctk.CTkLabel(types_frame, text=ptype['type']).grid(
                    row=idx, column=0, padx=10, pady=5, sticky="w"
                )
                ctk.CTkLabel(types_frame, text=str(ptype['product_count'])).grid(
                    row=idx, column=1, padx=10, pady=5
                )
                ctk.CTkLabel(types_frame, text=str(ptype['total_stock'])).grid(
                    row=idx, column=2, padx=10, pady=5
                )
        
        row += 1
        
        # Top clients
        self.create_section_title(row, "Mejores Clientes")
        row += 1
        
        clients = self.statistics.get_client_statistics(10)
        if clients:
            clients_frame = ctk.CTkFrame(self.content_frame)
            clients_frame.grid(row=row, column=0, padx=10, pady=10, sticky="ew")
            
            # Headers
            headers = ["#", "Cliente", "Compras", "Total Gastado"]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(
                    clients_frame, 
                    text=header, 
                    font=ctk.CTkFont(weight="bold")
                )
                label.grid(row=0, column=i, padx=10, pady=5)
            
            # Clients
            for idx, client in enumerate(clients, start=1):
                ctk.CTkLabel(clients_frame, text=str(idx)).grid(
                    row=idx, column=0, padx=10, pady=5
                )
                ctk.CTkLabel(clients_frame, text=client['client_name']).grid(
                    row=idx, column=1, padx=10, pady=5, sticky="w"
                )
                ctk.CTkLabel(clients_frame, text=str(client['purchase_count'])).grid(
                    row=idx, column=2, padx=10, pady=5
                )
                ctk.CTkLabel(clients_frame, text=f"${client['total_spent']:.2f}").grid(
                    row=idx, column=3, padx=10, pady=5
                )
        
        row += 1
        
        # Sales by period
        self.create_section_title(row, "Últimos 7 Días")
        row += 1
        
        period = self.statistics.get_sales_by_period(7)
        if period:
            period_frame = ctk.CTkFrame(self.content_frame)
            period_frame.grid(row=row, column=0, padx=10, pady=10, sticky="ew")
            
            # Headers
            headers = ["Fecha", "Ventas", "Total"]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(
                    period_frame, 
                    text=header, 
                    font=ctk.CTkFont(weight="bold")
                )
                label.grid(row=0, column=i, padx=10, pady=5)
            
            # Days
            for idx, day in enumerate(period, start=1):
                ctk.CTkLabel(period_frame, text=day['date']).grid(
                    row=idx, column=0, padx=10, pady=5
                )
                ctk.CTkLabel(period_frame, text=str(day['sales_count'])).grid(
                    row=idx, column=1, padx=10, pady=5
                )
                ctk.CTkLabel(period_frame, text=f"${day['total_amount']:.2f}").grid(
                    row=idx, column=2, padx=10, pady=5
                )
    
    def create_section_title(self, row, text):
        """Create a section title."""
        title = ctk.CTkLabel(
            self.content_frame, 
            text=text, 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=row, column=0, padx=10, pady=(20, 10), sticky="w")
    
    def create_stats_grid(self, row):
        """Create a grid frame for stats."""
        frame = ctk.CTkFrame(self.content_frame)
        frame.grid(row=row, column=0, padx=10, pady=10, sticky="ew")
        return frame
    
    def add_stat_item(self, parent, row, col, label, value):
        """Add a stat item to grid."""
        item_frame = ctk.CTkFrame(parent)
        item_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        label_widget = ctk.CTkLabel(
            item_frame, 
            text=label,
            font=ctk.CTkFont(size=12)
        )
        label_widget.pack(padx=20, pady=(10, 5))
        
        value_widget = ctk.CTkLabel(
            item_frame, 
            text=value,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        value_widget.pack(padx=20, pady=(5, 10))
