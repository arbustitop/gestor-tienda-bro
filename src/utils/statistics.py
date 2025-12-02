"""
Statistics utilities for store analytics.
Provides functions for calculating store performance metrics.
"""

from datetime import datetime, timedelta


class Statistics:
    """Statistics calculator for store data."""
    
    def __init__(self, db):
        """Initialize statistics with database connection."""
        self.db = db
    
    def get_daily_summary(self):
        """Get summary statistics for today."""
        # Today's sales total
        query_sales = '''
            SELECT 
                COALESCE(SUM(total_amount), 0) as total_sales,
                COUNT(*) as sales_count,
                COALESCE(SUM(total_fabric_meters), 0) as total_fabric,
                COALESCE(SUM(total_vinyl_meters), 0) as total_vinyl
            FROM sales 
            WHERE DATE(sale_date) = DATE('now')
        '''
        self.db.execute(query_sales)
        sales_data = self.db.fetchone()
        
        # Low stock count
        query_low_stock = '''
            SELECT COUNT(*) as low_stock_count
            FROM products
            WHERE stock <= 5
        '''
        self.db.execute(query_low_stock)
        low_stock_data = self.db.fetchone()
        
        return {
            'total_sales': sales_data['total_sales'],
            'sales_count': sales_data['sales_count'],
            'total_fabric': sales_data['total_fabric'],
            'total_vinyl': sales_data['total_vinyl'],
            'low_stock_count': low_stock_data['low_stock_count']
        }
    
    def get_top_products(self, limit=5):
        """Get top selling products."""
        query = '''
            SELECT 
                product_name,
                SUM(quantity) as total_quantity,
                SUM(subtotal) as total_revenue,
                COUNT(*) as sales_count
            FROM sale_items
            GROUP BY product_id, product_name
            ORDER BY total_quantity DESC
            LIMIT ?
        '''
        self.db.execute(query, (limit,))
        return self.db.fetchall()
    
    def get_sales_by_period(self, days=7):
        """Get sales statistics for the last N days."""
        query = '''
            SELECT 
                DATE(sale_date) as date,
                COUNT(*) as sales_count,
                SUM(total_amount) as total_amount
            FROM sales
            WHERE sale_date >= DATE('now', ?)
            GROUP BY DATE(sale_date)
            ORDER BY date DESC
        '''
        self.db.execute(query, (f'-{days} days',))
        return self.db.fetchall()
    
    def get_inventory_value(self):
        """Calculate total inventory value."""
        query = '''
            SELECT 
                SUM(price * stock) as inventory_value,
                SUM(stock) as total_units
            FROM products
        '''
        self.db.execute(query)
        return self.db.fetchone()
    
    def get_product_type_distribution(self):
        """Get distribution of products by type."""
        query = '''
            SELECT 
                type,
                COUNT(*) as product_count,
                SUM(stock) as total_stock
            FROM products
            GROUP BY type
            ORDER BY product_count DESC
        '''
        self.db.execute(query)
        return self.db.fetchall()
    
    def get_monthly_revenue(self):
        """Get revenue for current month."""
        query = '''
            SELECT 
                COALESCE(SUM(total_amount), 0) as monthly_revenue,
                COUNT(*) as monthly_sales
            FROM sales
            WHERE strftime('%Y-%m', sale_date) = strftime('%Y-%m', 'now')
        '''
        self.db.execute(query)
        return self.db.fetchone()
    
    def get_client_statistics(self, limit=10):
        """Get top clients by purchase amount."""
        query = '''
            SELECT 
                client_name,
                COUNT(*) as purchase_count,
                SUM(total_amount) as total_spent
            FROM sales
            GROUP BY client_name
            ORDER BY total_spent DESC
            LIMIT ?
        '''
        self.db.execute(query, (limit,))
        return self.db.fetchall()
