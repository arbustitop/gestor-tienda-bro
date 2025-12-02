"""
Database module for store management system.
Handles SQLite database connection, schema creation, and migrations.
"""

import sqlite3
import os
from datetime import datetime


class Database:
    """Database manager with automatic migrations."""
    
    def __init__(self, db_path='db/tienda.db'):
        """Initialize database connection."""
        self.db_path = db_path
        self._ensure_db_directory()
        self.connection = None
        self.cursor = None
        self.connect()
        self._initialize_database()
    
    def _ensure_db_directory(self):
        """Ensure the db directory exists."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def connect(self):
        """Establish database connection."""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
    
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
    
    def _initialize_database(self):
        """Create all tables and run migrations."""
        self._create_products_table()
        self._create_sales_table()
        self._create_sale_items_table()
        self._create_migrations_table()
        self._run_migrations()
        self.connection.commit()
    
    def _create_products_table(self):
        """Create products table."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                size TEXT,
                color TEXT,
                price REAL NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                fabric_meters REAL DEFAULT 0,
                vinyl_meters REAL DEFAULT 0,
                print_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    def _create_sales_table(self):
        """Create sales table."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT NOT NULL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_amount REAL NOT NULL,
                total_fabric_meters REAL DEFAULT 0,
                total_vinyl_meters REAL DEFAULT 0,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    def _create_sale_items_table(self):
        """Create sale items table."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                subtotal REAL NOT NULL,
                fabric_meters REAL DEFAULT 0,
                vinyl_meters REAL DEFAULT 0,
                FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')
    
    def _create_migrations_table(self):
        """Create migrations tracking table."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration_name TEXT UNIQUE NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    def _run_migrations(self):
        """Run pending database migrations."""
        # Example migration - can be extended
        migrations = [
            ('initial_schema', self._migration_initial_schema),
        ]
        
        for migration_name, migration_func in migrations:
            if not self._is_migration_applied(migration_name):
                migration_func()
                self._mark_migration_applied(migration_name)
    
    def _is_migration_applied(self, migration_name):
        """Check if a migration has been applied."""
        self.cursor.execute(
            'SELECT COUNT(*) FROM migrations WHERE migration_name = ?',
            (migration_name,)
        )
        return self.cursor.fetchone()[0] > 0
    
    def _mark_migration_applied(self, migration_name):
        """Mark a migration as applied."""
        self.cursor.execute(
            'INSERT INTO migrations (migration_name) VALUES (?)',
            (migration_name,)
        )
    
    def _migration_initial_schema(self):
        """Initial schema migration (already handled in table creation)."""
        pass
    
    def execute(self, query, params=()):
        """Execute a query and return cursor."""
        return self.cursor.execute(query, params)
    
    def fetchall(self):
        """Fetch all results."""
        return self.cursor.fetchall()
    
    def fetchone(self):
        """Fetch one result."""
        return self.cursor.fetchone()
    
    def commit(self):
        """Commit the current transaction."""
        self.connection.commit()
    
    def rollback(self):
        """Rollback the current transaction."""
        self.connection.rollback()
    
    def lastrowid(self):
        """Get last inserted row ID."""
        return self.cursor.lastrowid
