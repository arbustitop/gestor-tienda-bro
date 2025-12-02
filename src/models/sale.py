"""
Sale model for managing store sales and transactions.
Handles sales recording, stock updates, and sales history.
"""

from datetime import datetime


class Sale:
    """Sale model with transaction handling."""
    
    def __init__(self, db):
        """Initialize sale model with database connection."""
        self.db = db
    
    def create_sale(self, client_name, items, notes=''):
        """
        Create a new sale with items.
        
        Args:
            client_name: Name of the client
            items: List of dicts with keys: product_id, quantity
            notes: Optional notes
            
        Returns:
            sale_id if successful, None otherwise
        """
        try:
            # Calculate totals
            total_amount = 0
            total_fabric = 0
            total_vinyl = 0
            sale_items_data = []
            
            for item in items:
                # Get product details
                self.db.execute('SELECT * FROM products WHERE id = ?', 
                              (item['product_id'],))
                product = self.db.fetchone()
                
                if not product:
                    raise ValueError(f"Product {item['product_id']} not found")
                
                quantity = item['quantity']
                
                # Check stock
                if product['stock'] < quantity:
                    raise ValueError(
                        f"Insufficient stock for {product['name']}. "
                        f"Available: {product['stock']}, Requested: {quantity}"
                    )
                
                # Calculate subtotal and materials
                subtotal = product['price'] * quantity
                fabric_used = product['fabric_meters'] * quantity
                vinyl_used = product['vinyl_meters'] * quantity
                
                total_amount += subtotal
                total_fabric += fabric_used
                total_vinyl += vinyl_used
                
                sale_items_data.append({
                    'product_id': product['id'],
                    'product_name': product['name'],
                    'quantity': quantity,
                    'unit_price': product['price'],
                    'subtotal': subtotal,
                    'fabric_meters': fabric_used,
                    'vinyl_meters': vinyl_used
                })
            
            # Create sale record
            sale_query = '''
                INSERT INTO sales (client_name, total_amount, 
                                 total_fabric_meters, total_vinyl_meters, notes)
                VALUES (?, ?, ?, ?, ?)
            '''
            self.db.execute(sale_query, (client_name, total_amount, 
                                        total_fabric, total_vinyl, notes))
            sale_id = self.db.lastrowid()
            
            # Create sale items and update stock
            for item_data in sale_items_data:
                item_query = '''
                    INSERT INTO sale_items (sale_id, product_id, product_name,
                                          quantity, unit_price, subtotal,
                                          fabric_meters, vinyl_meters)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                '''
                self.db.execute(item_query, (
                    sale_id, item_data['product_id'], item_data['product_name'],
                    item_data['quantity'], item_data['unit_price'], 
                    item_data['subtotal'], item_data['fabric_meters'],
                    item_data['vinyl_meters']
                ))
                
                # Update stock
                stock_query = '''
                    UPDATE products 
                    SET stock = stock - ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                '''
                self.db.execute(stock_query, (item_data['quantity'], 
                                             item_data['product_id']))
            
            self.db.commit()
            return sale_id
            
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_all_sales(self):
        """Get all sales ordered by date (most recent first)."""
        query = '''
            SELECT s.*, COUNT(si.id) as items_count
            FROM sales s
            LEFT JOIN sale_items si ON s.id = si.sale_id
            GROUP BY s.id
            ORDER BY s.sale_date DESC
        '''
        self.db.execute(query)
        return self.db.fetchall()
    
    def get_sale_by_id(self, sale_id):
        """Get sale details by ID."""
        query = 'SELECT * FROM sales WHERE id = ?'
        self.db.execute(query, (sale_id,))
        return self.db.fetchone()
    
    def get_sale_items(self, sale_id):
        """Get all items for a specific sale."""
        query = '''
            SELECT * FROM sale_items 
            WHERE sale_id = ?
            ORDER BY id
        '''
        self.db.execute(query, (sale_id,))
        return self.db.fetchall()
    
    def get_sales_by_date_range(self, start_date, end_date):
        """Get sales within a date range."""
        query = '''
            SELECT * FROM sales 
            WHERE DATE(sale_date) BETWEEN DATE(?) AND DATE(?)
            ORDER BY sale_date DESC
        '''
        self.db.execute(query, (start_date, end_date))
        return self.db.fetchall()
    
    def get_today_sales(self):
        """Get today's sales."""
        query = '''
            SELECT * FROM sales 
            WHERE DATE(sale_date) = DATE('now')
            ORDER BY sale_date DESC
        '''
        self.db.execute(query)
        return self.db.fetchall()
    
    def get_today_total(self):
        """Get total sales amount for today."""
        query = '''
            SELECT COALESCE(SUM(total_amount), 0) as total
            FROM sales 
            WHERE DATE(sale_date) = DATE('now')
        '''
        self.db.execute(query)
        return self.db.fetchone()['total']
    
    def get_most_sold_product(self, limit=10):
        """Get the most sold products."""
        query = '''
            SELECT product_name, SUM(quantity) as total_sold,
                   COUNT(*) as times_sold
            FROM sale_items
            GROUP BY product_id
            ORDER BY total_sold DESC
            LIMIT ?
        '''
        self.db.execute(query, (limit,))
        return self.db.fetchall()
    
    def search_sales(self, search_term='', start_date=None, end_date=None):
        """Search sales by client name or date range."""
        query = 'SELECT * FROM sales WHERE 1=1'
        params = []
        
        if search_term:
            query += ' AND client_name LIKE ?'
            params.append(f'%{search_term}%')
        
        if start_date:
            query += ' AND DATE(sale_date) >= DATE(?)'
            params.append(start_date)
        
        if end_date:
            query += ' AND DATE(sale_date) <= DATE(?)'
            params.append(end_date)
        
        query += ' ORDER BY sale_date DESC'
        
        self.db.execute(query, params)
        return self.db.fetchall()
