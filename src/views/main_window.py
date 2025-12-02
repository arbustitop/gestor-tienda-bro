"""
Main window for the store management system.
CustomTkinter-based responsive GUI application.
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import Database
from models.product import Product
from models.sale import Sale
from utils.statistics import Statistics
from utils.csv_exporter import CSVExporter


class MainWindow(ctk.CTk):
    """Main application window."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        # Window configuration
        self.title("Gestor de Tienda Bro")
        self.geometry("1200x700")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialize database
        self.db = Database('db/tienda.db')
        self.product_model = Product(self.db)
        self.sale_model = Sale(self.db)
        self.statistics = Statistics(self.db)
        self.csv_exporter = CSVExporter(self.db)
        
        # Create UI
        self.create_widgets()
        self.load_dashboard_data()
    
    def create_widgets(self):
        """Create and layout all widgets."""
        # Main container with sidebar
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)
        
        # Logo/Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="Gestor Tienda", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Navigation buttons
        self.btn_dashboard = ctk.CTkButton(
            self.sidebar, 
            text="Dashboard", 
            command=self.show_dashboard
        )
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=10)
        
        self.btn_products = ctk.CTkButton(
            self.sidebar, 
            text="Productos", 
            command=self.show_products
        )
        self.btn_products.grid(row=2, column=0, padx=20, pady=10)
        
        self.btn_sales = ctk.CTkButton(
            self.sidebar, 
            text="Ventas", 
            command=self.show_sales
        )
        self.btn_sales.grid(row=3, column=0, padx=20, pady=10)
        
        self.btn_new_sale = ctk.CTkButton(
            self.sidebar, 
            text="Nueva Venta", 
            command=self.show_new_sale,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.btn_new_sale.grid(row=4, column=0, padx=20, pady=10)
        
        self.btn_statistics = ctk.CTkButton(
            self.sidebar, 
            text="Estadísticas", 
            command=self.show_statistics
        )
        self.btn_statistics.grid(row=5, column=0, padx=20, pady=10)
        
        self.btn_export = ctk.CTkButton(
            self.sidebar, 
            text="Exportar", 
            command=self.show_export
        )
        self.btn_export.grid(row=6, column=0, padx=20, pady=10)
        
        # Main content frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Content container (will hold different views)
        self.content_frame = None
        
    def clear_content(self):
        """Clear current content frame."""
        if self.content_frame:
            self.content_frame.destroy()
        
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        return self.content_frame
    
    def show_dashboard(self):
        """Show dashboard view."""
        frame = self.clear_content()
        
        # Title
        title = ctk.CTkLabel(
            frame, 
            text="Dashboard", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Load and display dashboard data
        self.load_dashboard_data(frame)
    
    def load_dashboard_data(self, frame=None):
        """Load and display dashboard statistics."""
        if frame is None:
            return
        
        summary = self.statistics.get_daily_summary()
        
        # Stats cards container
        stats_frame = ctk.CTkFrame(frame)
        stats_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Sales today card
        sales_card = self.create_stat_card(
            stats_frame, 
            "Ventas Hoy", 
            f"${summary['total_sales']:.2f}",
            f"{summary['sales_count']} ventas"
        )
        sales_card.grid(row=0, column=0, padx=10, pady=10)
        
        # Fabric used card
        fabric_card = self.create_stat_card(
            stats_frame, 
            "Tela Usada Hoy", 
            f"{summary['total_fabric']:.2f}m",
            "Total metros"
        )
        fabric_card.grid(row=0, column=1, padx=10, pady=10)
        
        # Vinyl used card
        vinyl_card = self.create_stat_card(
            stats_frame, 
            "Vinilo Usado Hoy", 
            f"{summary['total_vinyl']:.2f}m",
            "Total metros"
        )
        vinyl_card.grid(row=0, column=2, padx=10, pady=10)
        
        # Low stock card
        low_stock_card = self.create_stat_card(
            stats_frame, 
            "Stock Bajo", 
            str(summary['low_stock_count']),
            "productos",
            fg_color="darkred" if summary['low_stock_count'] > 0 else None
        )
        low_stock_card.grid(row=0, column=3, padx=10, pady=10)
        
        # Top products section
        top_products_label = ctk.CTkLabel(
            frame, 
            text="Productos Más Vendidos", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        top_products_label.grid(row=2, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Top products table
        top_products = self.statistics.get_top_products(5)
        
        if top_products:
            products_frame = ctk.CTkFrame(frame)
            products_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
            
            # Headers
            headers = ["Producto", "Cantidad", "Ingresos", "Ventas"]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(
                    products_frame, 
                    text=header, 
                    font=ctk.CTkFont(weight="bold")
                )
                label.grid(row=0, column=i, padx=10, pady=5)
            
            # Data rows
            for idx, product in enumerate(top_products, start=1):
                ctk.CTkLabel(products_frame, text=product['product_name']).grid(
                    row=idx, column=0, padx=10, pady=5, sticky="w"
                )
                ctk.CTkLabel(products_frame, text=str(product['total_quantity'])).grid(
                    row=idx, column=1, padx=10, pady=5
                )
                ctk.CTkLabel(products_frame, text=f"${product['total_revenue']:.2f}").grid(
                    row=idx, column=2, padx=10, pady=5
                )
                ctk.CTkLabel(products_frame, text=str(product['sales_count'])).grid(
                    row=idx, column=3, padx=10, pady=5
                )
    
    def create_stat_card(self, parent, title, value, subtitle, fg_color=None):
        """Create a statistics card widget."""
        card = ctk.CTkFrame(parent, fg_color=fg_color)
        
        title_label = ctk.CTkLabel(
            card, 
            text=title, 
            font=ctk.CTkFont(size=12)
        )
        title_label.pack(padx=20, pady=(10, 5))
        
        value_label = ctk.CTkLabel(
            card, 
            text=value, 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        value_label.pack(padx=20, pady=5)
        
        subtitle_label = ctk.CTkLabel(
            card, 
            text=subtitle, 
            font=ctk.CTkFont(size=10)
        )
        subtitle_label.pack(padx=20, pady=(5, 10))
        
        return card
    
    def show_products(self):
        """Show products management view."""
        from views.products_view import ProductsView
        frame = self.clear_content()
        ProductsView(frame, self.product_model, self.db)
    
    def show_sales(self):
        """Show sales history view."""
        from views.sales_view import SalesView
        frame = self.clear_content()
        SalesView(frame, self.sale_model, self.db)
    
    def show_new_sale(self):
        """Show new sale form."""
        from views.new_sale_view import NewSaleView
        frame = self.clear_content()
        NewSaleView(frame, self.sale_model, self.product_model, self.db, 
                   self.show_sales)
    
    def show_statistics(self):
        """Show statistics view."""
        from views.statistics_view import StatisticsView
        frame = self.clear_content()
        StatisticsView(frame, self.statistics, self.db)
    
    def show_export(self):
        """Show export options view."""
        from views.export_view import ExportView
        frame = self.clear_content()
        ExportView(frame, self.csv_exporter)
    
    def on_closing(self):
        """Handle window closing."""
        self.db.close()
        self.destroy()


def main():
    """Run the application."""
    app = MainWindow()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()
