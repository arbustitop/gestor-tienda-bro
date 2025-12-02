"""
CSV export utilities for generating reports.
Exports products, sales, and statistics to CSV format.
"""

import csv
import os
from datetime import datetime


class CSVExporter:
    """CSV exporter for store data."""
    
    def __init__(self, db):
        """Initialize CSV exporter with database connection."""
        self.db = db
    
    def export_products(self, filename='products_export.csv'):
        """Export all products to CSV."""
        query = 'SELECT * FROM products ORDER BY type, name'
        self.db.execute(query)
        products = self.db.fetchall()
        
        if not products:
            return False
        
        headers = ['ID', 'Nombre', 'Tipo', 'Talle', 'Color', 'Precio', 
                  'Stock', 'Metros Tela', 'Metros Vinilo', 'Tipo Impresión']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            for product in products:
                writer.writerow([
                    product['id'],
                    product['name'],
                    product['type'],
                    product['size'] or '',
                    product['color'] or '',
                    product['price'],
                    product['stock'],
                    product['fabric_meters'],
                    product['vinyl_meters'],
                    product['print_type'] or ''
                ])
        
        return True
    
    def export_sales(self, filename='sales_export.csv', start_date=None, end_date=None):
        """Export sales to CSV with optional date range."""
        query = 'SELECT * FROM sales WHERE 1=1'
        params = []
        
        if start_date:
            query += ' AND DATE(sale_date) >= DATE(?)'
            params.append(start_date)
        
        if end_date:
            query += ' AND DATE(sale_date) <= DATE(?)'
            params.append(end_date)
        
        query += ' ORDER BY sale_date DESC'
        
        self.db.execute(query, params)
        sales = self.db.fetchall()
        
        if not sales:
            return False
        
        headers = ['ID', 'Cliente', 'Fecha', 'Total', 'Metros Tela', 
                  'Metros Vinilo', 'Notas']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            for sale in sales:
                writer.writerow([
                    sale['id'],
                    sale['client_name'],
                    sale['sale_date'],
                    sale['total_amount'],
                    sale['total_fabric_meters'],
                    sale['total_vinyl_meters'],
                    sale['notes'] or ''
                ])
        
        return True
    
    def export_sale_details(self, sale_id, filename=None):
        """Export detailed sale with items."""
        if not filename:
            filename = f'sale_{sale_id}_detail.csv'
        
        # Get sale header
        self.db.execute('SELECT * FROM sales WHERE id = ?', (sale_id,))
        sale = self.db.fetchone()
        
        if not sale:
            return False
        
        # Get sale items
        self.db.execute('SELECT * FROM sale_items WHERE sale_id = ?', (sale_id,))
        items = self.db.fetchall()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Sale header
            writer.writerow(['DETALLE DE VENTA'])
            writer.writerow(['ID Venta:', sale['id']])
            writer.writerow(['Cliente:', sale['client_name']])
            writer.writerow(['Fecha:', sale['sale_date']])
            writer.writerow(['Total:', f"${sale['total_amount']:.2f}"])
            writer.writerow([])
            
            # Items
            writer.writerow(['Producto', 'Cantidad', 'Precio Unitario', 
                           'Subtotal', 'Metros Tela', 'Metros Vinilo'])
            
            for item in items:
                writer.writerow([
                    item['product_name'],
                    item['quantity'],
                    f"${item['unit_price']:.2f}",
                    f"${item['subtotal']:.2f}",
                    item['fabric_meters'],
                    item['vinyl_meters']
                ])
            
            writer.writerow([])
            writer.writerow(['Total Metros Tela:', sale['total_fabric_meters']])
            writer.writerow(['Total Metros Vinilo:', sale['total_vinyl_meters']])
        
        return True
    
    def export_low_stock(self, filename='low_stock.csv', threshold=5):
        """Export low stock products."""
        query = '''
            SELECT * FROM products 
            WHERE stock <= ? 
            ORDER BY stock, name
        '''
        self.db.execute(query, (threshold,))
        products = self.db.fetchall()
        
        if not products:
            return False
        
        headers = ['ID', 'Nombre', 'Tipo', 'Talle', 'Color', 'Stock Actual', 'Precio']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            for product in products:
                writer.writerow([
                    product['id'],
                    product['name'],
                    product['type'],
                    product['size'] or '',
                    product['color'] or '',
                    product['stock'],
                    product['price']
                ])
        
        return True
    
    def export_statistics_report(self, filename='statistics_report.csv'):
        """Export comprehensive statistics report."""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            writer.writerow(['REPORTE DE ESTADÍSTICAS'])
            writer.writerow(['Fecha de generación:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow([])
            
            # Daily summary
            query_daily = '''
                SELECT 
                    COALESCE(SUM(total_amount), 0) as total,
                    COUNT(*) as count
                FROM sales 
                WHERE DATE(sale_date) = DATE('now')
            '''
            self.db.execute(query_daily)
            daily = self.db.fetchone()
            
            writer.writerow(['VENTAS DE HOY'])
            writer.writerow(['Total ventas:', f"${daily['total']:.2f}"])
            writer.writerow(['Cantidad de ventas:', daily['count']])
            writer.writerow([])
            
            # Top products
            writer.writerow(['PRODUCTOS MÁS VENDIDOS'])
            writer.writerow(['Producto', 'Cantidad Vendida', 'Ingresos'])
            
            query_top = '''
                SELECT 
                    product_name,
                    SUM(quantity) as total_qty,
                    SUM(subtotal) as revenue
                FROM sale_items
                GROUP BY product_id, product_name
                ORDER BY total_qty DESC
                LIMIT 10
            '''
            self.db.execute(query_top)
            top_products = self.db.fetchall()
            
            for product in top_products:
                writer.writerow([
                    product['product_name'],
                    product['total_qty'],
                    f"${product['revenue']:.2f}"
                ])
            
            writer.writerow([])
            
            # Inventory value
            query_inventory = '''
                SELECT 
                    COALESCE(SUM(price * stock), 0) as value,
                    COALESCE(SUM(stock), 0) as units
                FROM products
            '''
            self.db.execute(query_inventory)
            inventory = self.db.fetchone()
            
            writer.writerow(['INVENTARIO'])
            writer.writerow(['Valor total:', f"${inventory['value']:.2f}"])
            writer.writerow(['Unidades totales:', inventory['units']])
        
        return True
