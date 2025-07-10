#!/usr/bin/env python3
"""
Aplicación GUI principal para el cálculo de la Ley de Amdahl
Proyecto: EID2 - Introducción al Cálculo
Interfaz: CustomTkinter (GUI Moderna)
"""

import sys
import os

# Agregar el directorio src al path para las importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.presentation.gui import main

if __name__ == "__main__":
    print("🚀 Iniciando Calculadora Ley de Amdahl - Interfaz Gráfica")
    print("📊 Cargando componentes y configuración...")
    
    try:
        main()
    except ImportError as e:
        print(f"\n❌ Error de dependencias: {e}")
        print("\n💡 Solución: Instale las dependencias faltantes:")
        print("   pip install customtkinter matplotlib pillow")
        input("\nPresione Enter para salir...")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        input("\nPresione Enter para salir...")
