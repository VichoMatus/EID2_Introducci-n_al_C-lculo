import sys
import os

# Agregar el directorio src al path para las importaciones
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def ejecutar_gui():
    #Ejecuta la interfaz gráfica
    try:
        print("🚀 Iniciando Calculadora Ley de Amdahl - Interfaz Gráfica")
        print("📊 Cargando componentes y configuración...")
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
    try:
        print("💻 Iniciando interfaz de línea de comandos...")
        from src.presentation.cli import main as cli_main
        cli_main()
    except Exception as e:
        print(f"\n❌ Error crítico en CLI: {e}")
        input("\nPresione Enter para salir...")
        sys.exit(1)

def main():
    try:
        # Verificar argumentos de línea de comandos para casos especiales
        if len(sys.argv) > 1:
            modo = sys.argv[1].lower()
            if modo in ["cli", "c", "--cli"]:
                ejecutar_cli()
                return
            elif modo in ["demo", "d", "--demo"]:
                print("🎯 Ejecutando demo automático...")
                import subprocess
                subprocess.run([sys.executable, "demo.py"])
                return
            elif modo in ["help", "h", "--help"]:
                print("""
🎯 CALCULADORA LEY DE AMDAHL - AYUDA

Uso: python main.py [opción]

Opciones:
  (sin argumentos)  Ejecutar interfaz gráfica (por defecto)
  cli               Ejecutar interfaz de línea de comandos
  demo              Ejecutar demostración automática
  help              Mostrar esta ayuda

Ejemplos:
  python main.py         # Interfaz gráfica
  python main.py cli     # Línea de comandos
  python main.py demo    # Demo automático
  python main_gui.py     # Interfaz gráfica directa
                """)
                return
        
        # Ejecutar GUI por defecto
        ejecutar_gui()
        
    except KeyboardInterrupt:
        print("\n👋 ¡Aplicación interrumpida por el usuario!")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        input("\nPresione Enter para salir...")
        sys.exit(1)

if __name__ == "__main__":
    main()
