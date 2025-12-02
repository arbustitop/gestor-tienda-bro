"""
Export view for generating CSV reports.
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import os


class ExportView:
    """Export and reporting view."""
    
    def __init__(self, parent, csv_exporter):
        """Initialize export view."""
        self.parent = parent
        self.csv_exporter = csv_exporter
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create and layout widgets."""
        # Configure grid
        self.parent.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            self.parent, 
            text="Exportar Reportes", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Description
        desc = ctk.CTkLabel(
            self.parent, 
            text="Genere reportes en formato CSV para análisis externo",
            font=ctk.CTkFont(size=14)
        )
        desc.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        # Export options frame
        options_frame = ctk.CTkFrame(self.parent)
        options_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        
        # Products export
        self.create_export_card(
            options_frame, 
            0,
            "Exportar Productos",
            "Exporta todos los productos con detalles de stock, precios y materiales",
            self.export_products
        )
        
        # Sales export
        self.create_export_card(
            options_frame, 
            1,
            "Exportar Ventas",
            "Exporta el historial completo de ventas",
            self.export_sales
        )
        
        # Low stock export
        self.create_export_card(
            options_frame, 
            2,
            "Exportar Stock Bajo",
            "Exporta productos con stock bajo (≤5 unidades)",
            self.export_low_stock
        )
        
        # Statistics export
        self.create_export_card(
            options_frame, 
            3,
            "Exportar Estadísticas",
            "Exporta un reporte completo con estadísticas y métricas",
            self.export_statistics
        )
    
    def create_export_card(self, parent, row, title, description, command):
        """Create an export option card."""
        card = ctk.CTkFrame(parent)
        card.grid(row=row, column=0, padx=20, pady=15, sticky="ew")
        
        # Title
        title_label = ctk.CTkLabel(
            card, 
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(padx=20, pady=(15, 5), anchor="w")
        
        # Description
        desc_label = ctk.CTkLabel(
            card, 
            text=description,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        desc_label.pack(padx=20, pady=(0, 10), anchor="w")
        
        # Export button
        export_btn = ctk.CTkButton(
            card, 
            text="📥 Exportar",
            command=command,
            width=120
        )
        export_btn.pack(padx=20, pady=(0, 15), anchor="e")
    
    def export_products(self):
        """Export products to CSV."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="productos.csv"
        )
        
        if not filename:
            return
        
        try:
            success = self.csv_exporter.export_products(filename)
            if success:
                messagebox.showinfo(
                    "Éxito", 
                    f"Productos exportados correctamente a:\n{filename}"
                )
            else:
                messagebox.showwarning("Aviso", "No hay productos para exportar")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def export_sales(self):
        """Export sales to CSV."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="ventas.csv"
        )
        
        if not filename:
            return
        
        try:
            success = self.csv_exporter.export_sales(filename)
            if success:
                messagebox.showinfo(
                    "Éxito", 
                    f"Ventas exportadas correctamente a:\n{filename}"
                )
            else:
                messagebox.showwarning("Aviso", "No hay ventas para exportar")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def export_low_stock(self):
        """Export low stock products to CSV."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="stock_bajo.csv"
        )
        
        if not filename:
            return
        
        try:
            success = self.csv_exporter.export_low_stock(filename, threshold=5)
            if success:
                messagebox.showinfo(
                    "Éxito", 
                    f"Productos con stock bajo exportados a:\n{filename}"
                )
            else:
                messagebox.showwarning("Aviso", "No hay productos con stock bajo")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def export_statistics(self):
        """Export statistics report to CSV."""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="estadisticas.csv"
        )
        
        if not filename:
            return
        
        try:
            success = self.csv_exporter.export_statistics_report(filename)
            if success:
                messagebox.showinfo(
                    "Éxito", 
                    f"Reporte de estadísticas exportado a:\n{filename}"
                )
            else:
                messagebox.showwarning("Aviso", "Error al generar el reporte")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
