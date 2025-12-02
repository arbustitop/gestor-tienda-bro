#!/usr/bin/env python3
"""
Sistema de Gestión de Tienda - Bro Sublimados
Punto de entrada principal de la aplicación
"""

import sys
import os

# Asegurar que el directorio actual está en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui import main

if __name__ == "__main__":
    main()
