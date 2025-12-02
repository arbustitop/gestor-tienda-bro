"""
Product model for managing store products.
Handles CRUD operations for products with sizes, colors, prices, and stock.
"""

from datetime import datetime


class Product:
    """Product model with CRUD operations."""
    
    def __init__(self, db):
        """Initialize product model with database connection."""
        self.db = db
    
    def create(self, name, product_type, size, color, price, stock=0, 
               fabric_meters=0, vinyl_meters=0, print_type=''):
        """Create a new product."""
        query = '''
            INSERT INTO products (name, type, size, color, price, stock,
                                fabric_meters, vinyl_meters, print_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.db.execute(query, (name, product_type, size, color, price, 
                               stock, fabric_meters, vinyl_meters, print_type))
        self.db.commit()
        return self.db.lastrowid()
    
    def get_all(self):
        """Get all products."""
        query = 'SELECT * FROM products ORDER BY name, size'
        self.db.execute(query)
        return self.db.fetchall()
    
    def get_by_id(self, product_id):
        """Get a product by ID."""
        query = 'SELECT * FROM products WHERE id = ?'
        self.db.execute(query, (product_id,))
        return self.db.fetchone()
    
    def search(self, search_term='', product_type='', low_stock=False, 
               low_stock_threshold=5):
        """Search products with filters."""
        query = 'SELECT * FROM products WHERE 1=1'
        params = []
        
        if search_term:
            query += ' AND (name LIKE ? OR color LIKE ? OR size LIKE ?)'
            search_pattern = f'%{search_term}%'
            params.extend([search_pattern, search_pattern, search_pattern])
        
        if product_type:
            query += ' AND type = ?'
            params.append(product_type)
        
        if low_stock:
            query += ' AND stock <= ?'
            params.append(low_stock_threshold)
        
        query += ' ORDER BY name, size'
        
        self.db.execute(query, params)
        return self.db.fetchall()
    
    def update(self, product_id, name, product_type, size, color, price, 
               stock, fabric_meters=0, vinyl_meters=0, print_type=''):
        """Update a product."""
        query = '''
            UPDATE products 
            SET name = ?, type = ?, size = ?, color = ?, price = ?, 
                stock = ?, fabric_meters = ?, vinyl_meters = ?, 
                print_type = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        '''
        self.db.execute(query, (name, product_type, size, color, price, 
                               stock, fabric_meters, vinyl_meters, 
                               print_type, product_id))
        self.db.commit()
    
    def delete(self, product_id):
        """Delete a product."""
        query = 'DELETE FROM products WHERE id = ?'
        self.db.execute(query, (product_id,))
        self.db.commit()
    
    def update_stock(self, product_id, quantity_change):
        """Update product stock (positive to add, negative to subtract)."""
        query = '''
            UPDATE products 
            SET stock = stock + ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        '''
        self.db.execute(query, (quantity_change, product_id))
        self.db.commit()
    
    def get_product_types(self):
        """Get all unique product types."""
        query = 'SELECT DISTINCT type FROM products ORDER BY type'
        self.db.execute(query)
        return [row['type'] for row in self.db.fetchall()]
    
    def get_low_stock_products(self, threshold=5):
        """Get products with low stock."""
        query = 'SELECT * FROM products WHERE stock <= ? ORDER BY stock, name'
        self.db.execute(query, (threshold,))
        return self.db.fetchall()
    
    def get_total_count(self):
        """Get total number of products."""
        query = 'SELECT COUNT(*) as count FROM products'
        self.db.execute(query)
        return self.db.fetchone()['count']
    
    def check_stock_available(self, product_id, quantity):
        """Check if enough stock is available."""
        product = self.get_by_id(product_id)
        if product and product['stock'] >= quantity:
            return True
        return False
