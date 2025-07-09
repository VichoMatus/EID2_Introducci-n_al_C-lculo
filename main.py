#!/usr/bin/env python3
"""
Aplicación principal para el cálculo de la Ley de Amdahl
Proyecto: EID2 - Introducción al Cálculo
Autor: Aplicación con Arquitectura Limpia
Fecha: Julio 2025

Esta aplicación resuelve el problema de optimización de GPU usando la Ley de Amdahl
para grupos pares según el documento del proyecto.

Modos disponibles:
- GUI: Interfaz gráfica moderna con CustomTkinter
- CLI: Interfaz de línea de comandos
"""

import sys
import os

# Agregar el directorio src al path para las importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def mostrar_banner():
    """Muestra el banner de la aplicación"""
    print("""
    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │           CALCULADORA LEY DE AMDAHL - GPU                  │
    │                                                             │
    │  Proyecto: EID2 - Introducción al Cálculo                  │
    │  Tema: Optimización de componentes GPU                     │
    │  Aplicación: Arquitectura Limpia en Python                │
    │                                                             │
    │  🎯 Funcionalidades:                                        │
    │     • Cálculo automático de aceleraciones                  │
    │     • Análisis de componentes GPU                          │
    │     • Generación de gráficos                               │
    │     • Resolución problema completo                         │
    │                                                             │
    │  🖥️  Modos disponibles:                                     │
    │     • GUI: Interfaz gráfica moderna                        │
    │     • CLI: Línea de comandos                               │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
    """)

def seleccionar_modo():
    """Permite al usuario seleccionar el modo de ejecución"""
    print("Seleccione el modo de ejecución:")
    print("1. 🖥️  GUI - Interfaz Gráfica (Recomendado)")
    print("2. 💻 CLI - Línea de Comandos")
    print("0. ❌ Salir")
    
    while True:
        try:
            opcion = input("\nIngrese su opción (1/2/0): ").strip()
            
            if opcion == "1":
                return "gui"
            elif opcion == "2":
                return "cli"
            elif opcion == "0":
                print("👋 ¡Hasta luego!")
                return None
            else:
                print("❌ Opción no válida. Ingrese 1, 2 o 0.")
                
        except (KeyboardInterrupt, EOFError):
            print("\n👋 ¡Hasta luego!")
            return None

def ejecutar_gui():
    """Ejecuta la interfaz gráfica"""
    try:
        print("🚀 Iniciando interfaz gráfica...")
        from src.presentation.gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"\n❌ Error: No se pueden importar las dependencias de GUI: {e}")
        print("\n💡 Solución: Instale las dependencias faltantes:")
        print("   pip install customtkinter matplotlib pillow")
        print("\n🔄 Cambiando automáticamente a modo CLI...")
        ejecutar_cli()
    except Exception as e:
        print(f"\n❌ Error en GUI: {e}")
        print("🔄 Cambiando a modo CLI como respaldo...")
        ejecutar_cli()

def ejecutar_cli():
    """Ejecuta la interfaz de línea de comandos"""
    try:
        print("💻 Iniciando interfaz de línea de comandos...")
        from src.presentation.cli import main as cli_main
        cli_main()
    except Exception as e:
        print(f"\n❌ Error crítico en CLI: {e}")
        sys.exit(1)

def main():
    """Función principal"""
    try:
        mostrar_banner()
        
        # Si se pasa argumento de línea de comandos
        if len(sys.argv) > 1:
            modo = sys.argv[1].lower()
            if modo in ["gui", "g", "--gui"]:
                ejecutar_gui()
                return
            elif modo in ["cli", "c", "--cli"]:
                ejecutar_cli()
                return
            else:
                print(f"❌ Argumento no válido: {sys.argv[1]}")
                print("💡 Uso: python main.py [gui|cli]")
                return
        
        # Selección interactiva
        modo = seleccionar_modo()
        
        if modo == "gui":
            ejecutar_gui()
        elif modo == "cli":
            ejecutar_cli()
        
    except KeyboardInterrupt:
        print("\n👋 ¡Aplicación interrumpida por el usuario!")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
