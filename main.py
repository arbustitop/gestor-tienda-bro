#!/usr/bin/env python3
"""
Gestor de Tienda Bro - Sistema de Gestión de Tienda
Main entry point for the application.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from views.main_window import main

if __name__ == "__main__":
    main()
