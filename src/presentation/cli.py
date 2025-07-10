"""
Interfaz de línea de comandos para la aplicación de Ley de Amdahl
"""
import sys
from typing import List, Optional
from ..domain.entities import ComponenteGPU
from ..domain.value_objects import ComponentesGPUPredefinidos, ConfiguracionGPUPar
from ..application.use_cases import (
    ResolverProblemaGPUUseCase,
    CalcularAceleracionUseCase,
    CalcularTiempoOptimizadoUseCase,
    GenerarGraficosUseCase,
    AnalizarComponentesUseCase,
    CargarComponentesPredefinidosUseCase
)
from ..infrastructure.calculador_amdahl import CalculadorAmdahl
from ..infrastructure.analizador_componentes import AnalizadorComponentes


class CLIAmdahl:
    """Interfaz de línea de comandos para la aplicación"""
    
    def __init__(self):
        # Dependencias
        self.calculador = CalculadorAmdahl()
        self.analizador = AnalizadorComponentes(self.calculador)
        
        # Casos de uso
        self.cargar_componentes = CargarComponentesPredefinidosUseCase()
        self.calcular_aceleracion = CalcularAceleracionUseCase(self.calculador)
        self.calcular_tiempo = CalcularTiempoOptimizadoUseCase(self.calculador)
        self.analizar_componentes = AnalizarComponentesUseCase(self.analizador)
        
        # Lista de componentes ingresados por el usuario
        self.componentes_usuario: List[ComponenteGPU] = []
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal de la aplicación"""
        print("\n" + "="*70)
        print("    CALCULADORA LEY DE AMDAHL - OPTIMIZACIÓN GPU")
        print("="*70)
        print("1. Resolver problema completo (Grupos Pares - GPU)")
        print("2. Calcular aceleración de componente personalizado")
        print("3. Mostrar componentes predefinidos")
        print("4. Analizar últimos 3 componentes ingresados")
        print("5. Generar gráficos") 
        print("6. Mostrar información teórica")
        print("0. Salir")
        print("="*70)
    
    def ejecutar(self):
        """Ejecuta la aplicación principal"""
        while True:
            try:
                self.mostrar_menu_principal()
                opcion = input("Seleccione una opción: ").strip()
                
                if opcion == "0":
                    print("\n¡Gracias por usar la Calculadora de Ley de Amdahl!")
                    break
                elif opcion == "1":
                    self.resolver_problema_completo()
                elif opcion == "2":
                    self.calcular_componente_personalizado()
                elif opcion == "3":
                    self.mostrar_componentes_predefinidos()
                elif opcion == "4":
                    self.analizar_ultimos_tres()
                elif opcion == "5":
                    self.generar_graficos_menu()
                elif opcion == "6":
                    self.mostrar_informacion_teorica()
                else:
                    print("❌ Opción no válida. Intente nuevamente.")
                    
            except KeyboardInterrupt:
                print("\n\n¡Aplicación interrumpida por el usuario!")
                break
            except Exception as e:
                print(f"❌ Error inesperado: {e}")
                input("Presione Enter para continuar...")
    
    def resolver_problema_completo(self):
        """Resuelve el problema completo para grupos pares (GPU)"""
        print("\n" + "="*60)
        print("  RESOLUCIÓN PROBLEMA COMPLETO - GRUPOS PARES (GPU)")
        print("="*60)
        
        try:
            # Importar aquí para evitar errores si matplotlib no está instalado
            from ..infrastructure.visualizador_matplotlib import VisualizadorMatplotlib
            visualizador = VisualizadorMatplotlib()
            
            resolver_problema = ResolverProblemaGPUUseCase(
                self.calculador, self.analizador, visualizador
            )
            
            print("Resolviendo problema...")
            resultados = resolver_problema.resolver_problema_completo()
            
            self._mostrar_resultados_completos(resultados)
            
        except ImportError:
            print("⚠️  Matplotlib no disponible. Resolviendo sin gráficos...")
            self._resolver_sin_graficos()
        except Exception as e:
            print(f"❌ Error al resolver problema: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _resolver_sin_graficos(self):
        """Resuelve el problema sin generar gráficos"""
        componentes = self.cargar_componentes.execute()
        
        print("\n1. ACELERACIÓN PARA CADA COMPONENTE:")
        print("-" * 50)
        
        resultados = []
        for componente in componentes:
            resultado = self.calcular_aceleracion.execute(componente)
            resultados.append(resultado)
            
            print(f"• {componente.nombre}:")
            print(f"  - f = {componente.porcentaje_mejora:.1%}, k = {componente.factor_mejora}")
            print(f"  - Aceleración: {resultado.aceleracion:.4f}x")
            print(f"  - Límite teórico: {resultado.limite_teorico:.4f}x")
            print()
        
        print("2. ANÁLISIS TIEMPO NÚCLEOS CUDA (50ms → ? ms):")
        print("-" * 50)
        nucleos_cuda = next(c for c in componentes 
                           if c.nombre == ComponentesGPUPredefinidos.NUCLEOS_CUDA)
        resultado_tiempo = self.calcular_tiempo.execute(nucleos_cuda, 50.0)
        
        print(f"• Tiempo original: {resultado_tiempo.tiempo_original}ms")
        print(f"• Tiempo optimizado: {resultado_tiempo.tiempo_optimizado}ms")
        print(f"• Mejora total: {resultado_tiempo.porcentaje_mejora_total:.1f}%")
        
        print("\n3. COMPONENTE PARA 30% DE ACELERACIÓN:")
        print("-" * 50)
        for resultado in sorted(resultados, key=lambda x: x.aceleracion, reverse=True):
            if resultado.aceleracion >= 1.3:
                print(f"✅ {resultado.componente.nombre} logra {resultado.aceleracion:.4f}x (≥ 1.30x)")
                break
        else:
            print("❌ Ningún componente individual logra 30% de aceleración")
        
        print("\n4. ANÁLISIS COMPARATIVO:")
        print("-" * 50)
        analisis = self.analizar_componentes.determinar_mejor_optimizacion(componentes)
        print(f"🏆 Mejor componente: {analisis.mejor_componente.nombre}")
        print(f"📊 Ranking de aceleraciones:")
        for i, (nombre, aceleracion) in enumerate(analisis.obtener_ranking(), 1):
            print(f"   {i}. {nombre}: {aceleracion:.4f}x")
    
    def calcular_componente_personalizado(self):
        """Permite calcular aceleración para un componente personalizado"""
        print("\n" + "="*50)
        print("  CÁLCULO COMPONENTE PERSONALIZADO")
        print("="*50)
        
        try:
            nombre = input("Nombre del componente: ").strip()
            if not nombre:
                print("❌ El nombre no puede estar vacío")
                return
            
            porcentaje_str = input("Porcentaje mejorable (ejemplo: 25 para 25%): ").strip()
            porcentaje = float(porcentaje_str) / 100
            
            factor_str = input("Factor de mejora (k): ").strip()
            factor = float(factor_str)
            
            componente = ComponenteGPU(nombre, porcentaje, factor)
            resultado = self.calcular_aceleracion.execute(componente)
            
            # Agregar a la lista de componentes del usuario
            self.componentes_usuario.append(componente)
            
            print(f"\n📊 RESULTADOS PARA '{nombre}':")
            print("-" * 40)
            print(f"• Fracción mejorable (f): {porcentaje:.1%}")
            print(f"• Factor de mejora (k): {factor}")
            print(f"• Aceleración obtenida: {resultado.aceleracion:.4f}x")
            print(f"• Límite teórico (k→∞): {resultado.limite_teorico:.4f}x")
            print(f"• Eficiencia: {(resultado.aceleracion/resultado.limite_teorico)*100:.1f}%")
            
            # Preguntar si quiere calcular tiempo optimizado
            calcular_tiempo = input("\n¿Calcular tiempo optimizado? (s/n): ").lower().startswith('s')
            if calcular_tiempo:
                tiempo_original = float(input("Tiempo original (ms/s): "))
                resultado_tiempo = self.calcular_tiempo.execute(componente, tiempo_original)
                print(f"\n⏱️  ANÁLISIS TEMPORAL:")
                print(f"• Tiempo original: {resultado_tiempo.tiempo_original}")
                print(f"• Tiempo optimizado: {resultado_tiempo.tiempo_optimizado}")
                print(f"• Mejora total: {resultado_tiempo.porcentaje_mejora_total:.1f}%")
            
        except ValueError as e:
            print(f"❌ Error en los valores ingresados: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def mostrar_componentes_predefinidos(self):
        """Muestra los componentes GPU predefinidos"""
        print("\n" + "="*60)
        print("  COMPONENTES GPU PREDEFINIDOS (GRUPOS PARES)")
        print("="*60)
        
        componentes = self.cargar_componentes.execute()
        
        for i, componente in enumerate(componentes, 1):
            resultado = self.calcular_aceleracion.execute(componente)
            
            print(f"\n{i}. {componente.nombre}")
            print("-" * 40)
            print(f"   • Porcentaje mejorable: {componente.porcentaje_mejora:.1%}")
            print(f"   • Factor de mejora: {componente.factor_mejora}")
            print(f"   • Aceleración: {resultado.aceleracion:.4f}x")
            print(f"   • Límite teórico: {resultado.limite_teorico:.4f}x")
        
        input("\nPresione Enter para continuar...")
    
    def analizar_ultimos_tres(self):
        """Analiza los últimos 3 componentes ingresados por el usuario"""
        print("\n" + "="*50)
        print("  ANÁLISIS ÚLTIMOS 3 COMPONENTES")
        print("="*50)
        
        if len(self.componentes_usuario) == 0:
            print("❌ No hay componentes ingresados por el usuario.")
            print("   Primero ingrese algunos componentes usando la opción 2.")
            input("\nPresione Enter para continuar...")
            return
        
        print(f"📝 Total de componentes ingresados: {len(self.componentes_usuario)}")
        
        ultimos_tres = self.componentes_usuario[-3:]
        analisis = self.analizar_componentes.analizar_ultimos_tres_componentes(
            self.componentes_usuario
        )
        
        print(f"\n🔍 Analizando últimos {len(ultimos_tres)} componente(s):")
        print("-" * 50)
        
        for i, componente in enumerate(ultimos_tres, 1):
            resultado = next(r for r in analisis.resultados if r.componente == componente)
            print(f"{i}. {componente.nombre}")
            print(f"   • f={componente.porcentaje_mejora:.1%}, k={componente.factor_mejora}")
            print(f"   • Aceleración: {resultado.aceleracion:.4f}x")
        
        print(f"\n🏆 MEJOR OPCIÓN: {analisis.mejor_componente.nombre}")
        print(f"📊 Ranking:")
        for i, (nombre, aceleracion) in enumerate(analisis.obtener_ranking(), 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
            print(f"   {emoji} {i}. {nombre}: {aceleracion:.4f}x")
        
        print(f"\n📋 JUSTIFICACIÓN:")
        print(analisis.justificacion)
        
        input("\nPresione Enter para continuar...")
    
    def generar_graficos_menu(self):
        """Menú para generar gráficos (requiere matplotlib)"""
        print("\n" + "="*50)
        print("  GENERACIÓN DE GRÁFICOS")
        print("="*50)
        
        try:
            from ..infrastructure.visualizador_matplotlib import VisualizadorMatplotlib
            visualizador = VisualizadorMatplotlib()
            generar_graficos = GenerarGraficosUseCase(visualizador)
            
            print("1. Gráfico A vs k (para f=0.25 y f=0.35)")
            print("2. Gráfico A vs f (para diferentes k)")
            print("3. Comparación de componentes predefinidos")
            print("4. Límite teórico")
            print("0. Volver")
            
            opcion = input("\nSeleccione opción: ").strip()
            
            if opcion == "1":
                print("Generando gráfico A vs k...")
                generar_graficos.graficar_a_vs_k([0.25, 0.35])
            elif opcion == "2":
                print("Generando gráfico A vs f...")
                generar_graficos.graficar_a_vs_f([4, 8])
            elif opcion == "3":
                self._graficar_comparacion_componentes(visualizador)
            elif opcion == "4":
                self._graficar_limite_teorico(visualizador)
            elif opcion == "0":
                return
            else:
                print("❌ Opción no válida")
                
        except ImportError:
            print("❌ Matplotlib no está instalado.")
            print("   Instale con: pip install matplotlib")
        except Exception as e:
            print(f"❌ Error al generar gráficos: {e}")
        
        input("\nPresione Enter para continuar...")
    
    def _graficar_comparacion_componentes(self, visualizador):
        """Genera gráfico de comparación de componentes"""
        componentes = self.cargar_componentes.execute()
        datos = []
        
        for componente in componentes:
            resultado = self.calcular_aceleracion.execute(componente)
            datos.append({
                'nombre': componente.nombre,
                'aceleracion': resultado.aceleracion
            })
        
        visualizador.graficar_comparacion_componentes(datos)
    
    def _graficar_limite_teorico(self, visualizador):
        """Genera gráfico del límite teórico"""
        porcentajes = [i/100 for i in range(5, 96, 5)]
        visualizador.graficar_limite_teorico(porcentajes)
    
    def mostrar_informacion_teorica(self):
        """Muestra información teórica sobre la Ley de Amdahl"""
        print("\n" + "="*70)
        print("  INFORMACIÓN TEÓRICA - LEY DE AMDAHL")
        print("="*70)
        
        info = """
📚 LA LEY DE AMDAHL

La Ley de Amdahl predice la mejora máxima al optimizar un componente:

    A = 1 / ((1-f) + f/k)

Donde:
• A: Aceleración obtenida
• f: Fracción mejorable del sistema (0 ≤ f ≤ 1)
• k: Factor de mejora del componente (k > 1)

🔍 LÍMITE TEÓRICO:
Cuando k → ∞: A_max = 1/(1-f)

📊 INTERPRETACIÓN:
• f=0.5, k=∞ → A_max = 2x (máximo posible)
• f=0.9, k=∞ → A_max = 10x (máximo posible)
• La fracción NO mejorable (1-f) limita la aceleración total

🎯 APLICACIÓN EN GPU:
• Núcleos CUDA: Paralelización de cálculos
• Memoria VRAM: Acceso a datos
• Unidades Texturizado: Procesamiento de texturas
• NVLink: Comunicación entre GPUs

💡 CONCLUSIÓN CLAVE:
Es más efectivo optimizar componentes con mayor fracción 
mejorable (f) que aumentar indefinidamente el factor k.
"""
        print(info)
        input("Presione Enter para continuar...")
    
    def _mostrar_resultados_completos(self, resultados: dict):
        """Muestra los resultados completos del problema"""
        print("\n🎯 RESULTADOS PROBLEMA COMPLETO:")
        print("="*60)
        
        # Mostrar aceleraciones
        print("\n1️⃣  ACELERACIONES POR COMPONENTE:")
        for resultado in resultados["resultados_aceleracion"]:
            print(f"• {resultado.componente.nombre}: {resultado.aceleracion:.4f}x")
        
        # Mostrar tiempo núcleos CUDA
        print(f"\n2️⃣  TIEMPO NÚCLEOS CUDA:")
        tiempo_resultado = resultados["tiempo_nucleos_cuda"]
        print(f"• Original: {tiempo_resultado.tiempo_original}ms")
        print(f"• Optimizado: {tiempo_resultado.tiempo_optimizado}ms")
        print(f"• Mejora: {tiempo_resultado.porcentaje_mejora_total:.1f}%")
        
        # Componente para 30%
        print(f"\n3️⃣  COMPONENTE PARA ≥30% ACELERACIÓN:")
        comp_30 = resultados["componente_30_porciento"]
        if comp_30:
            aceleracion_30 = self.calculador.calcular_aceleracion(comp_30)
            print(f"✅ {comp_30.nombre}: {aceleracion_30:.4f}x")
        else:
            print("❌ Ningún componente individual logra ≥30%")
        
        # Mejor componente
        print(f"\n4️⃣  MEJOR COMPONENTE GENERAL:")
        analisis = resultados["analisis_comparativo"]
        print(f"🏆 {analisis.mejor_componente.nombre}")
        
        # Explicación NVLink
        print(f"\n5️⃣  LIMITACIÓN DE NVLINK:")
        print(resultados["explicacion_nvlink"])
        
        # Comparación
        print(f"\n6️⃣  TEXTURIZADO vs VRAM:")
        comparacion = resultados["comparacion_texturizado_vs_vram"]
        tex_data = comparacion["texturizado"]
        vram_data = comparacion["vram"]
        print(f"• Texturizado: {tex_data['aceleracion']:.4f}x")
        print(f"• VRAM: {vram_data['aceleracion']:.4f}x")
        print(f"• Mejor: {comparacion['mejor'].upper()}")


def main():
    """Función principal de la aplicación"""
    try:
        cli = CLIAmdahl()
        cli.ejecutar()
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
