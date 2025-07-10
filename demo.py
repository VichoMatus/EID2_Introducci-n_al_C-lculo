import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.domain.entities import ComponenteGPU
from src.domain.value_objects import ComponentesGPUPredefinidos, ConfiguracionGPUPar
from src.application.use_cases import (
    CargarComponentesPredefinidosUseCase,
    CalcularAceleracionUseCase,
    CalcularTiempoOptimizadoUseCase,
    AnalizarComponentesUseCase
)
from src.infrastructure.calculador_amdahl import CalculadorAmdahl
from src.infrastructure.analizador_componentes import AnalizadorComponentes


def resolver_problema_gpu_automatico():
    
    print("="*80)
    print("           RESOLUCIÓN AUTOMÁTICA - PROBLEMA GPU (GRUPOS PARES)")
    print("="*80)
    
    # Inicializar dependencias
    calculador = CalculadorAmdahl()
    analizador = AnalizadorComponentes(calculador)
    
    # Casos de uso
    cargar_componentes = CargarComponentesPredefinidosUseCase()
    calcular_aceleracion = CalcularAceleracionUseCase(calculador)
    calcular_tiempo = CalcularTiempoOptimizadoUseCase(calculador)
    analizar_componentes = AnalizarComponentesUseCase(analizador)
    
    # Cargar componentes predefinidos
    print("\n1️⃣  COMPONENTES GPU PREDEFINIDOS:")
    print("-" * 60)
    componentes = cargar_componentes.execute()
    
    for componente in componentes:
        print(f"• {componente.nombre}")
        print(f"  - Fracción mejorable (f): {componente.porcentaje_mejora:.1%}")
        print(f"  - Factor de mejora (k): {componente.factor_mejora}")
    
    # Calcular aceleración para cada componente
    print("\n2️⃣  ACELERACIONES CALCULADAS:")
    print("-" * 60)
    resultados = []
    
    for componente in componentes:
        resultado = calcular_aceleracion.execute(componente)
        resultados.append(resultado)
        
        print(f"• {componente.nombre}:")
        print(f"  - Aceleración (A): {resultado.aceleracion:.4f}x")
        print(f"  - Límite teórico (A_max): {resultado.limite_teorico:.4f}x")
        print(f"  - Eficiencia: {(resultado.aceleracion/resultado.limite_teorico)*100:.1f}%")
        print()
    
    # Analisis específico: renderizado de frame (50ms → ?)
    print("3️⃣  ANÁLISIS TIEMPO RENDERIZADO (NÚCLEOS CUDA):")
    print("-" * 60)
    nucleos_cuda = next(c for c in componentes 
                       if c.nombre == ComponentesGPUPredefinidos.NUCLEOS_CUDA)
    
    resultado_tiempo = calcular_tiempo.execute(nucleos_cuda, 50.0)
    
    print(f"• Tiempo original: {resultado_tiempo.tiempo_original} ms")
    print(f"• Tiempo optimizado: {resultado_tiempo.tiempo_optimizado:.2f} ms")
    print(f"• Mejora temporal: {resultado_tiempo.porcentaje_mejora_total:.1f}%")
    print(f"• Reducción: {resultado_tiempo.tiempo_original - resultado_tiempo.tiempo_optimizado:.2f} ms")
    
    # Determinar componente para ≥30% aceleración
    print("\n4️⃣  COMPONENTE PARA ≥30% ACELERACIÓN (A ≥ 1.30):")
    print("-" * 60)
    
    componentes_30_porciento = []
    for resultado in resultados:
        if resultado.aceleracion >= 1.30:
            componentes_30_porciento.append(resultado)
    
    if componentes_30_porciento:
        for resultado in componentes_30_porciento:
            print(f"✅ {resultado.componente.nombre}: {resultado.aceleracion:.4f}x")
    else:
        print("❌ Ningún componente individual logra ≥30% de aceleración")
        print("   El mejor componente es:")
        mejor = max(resultados, key=lambda x: x.aceleracion)
        print(f"   🥇 {mejor.componente.nombre}: {mejor.aceleracion:.4f}x ({(mejor.aceleracion-1)*100:.1f}%)")
    
    # Analisis comparativo completo
    print("\n5️⃣  ANÁLISIS COMPARATIVO:")
    print("-" * 60)
    analisis = analizar_componentes.determinar_mejor_optimizacion(componentes)
    
    print(f"🏆 MEJOR COMPONENTE: {analisis.mejor_componente.nombre}")
    print(f"\n📊 RANKING COMPLETO:")
    for i, (nombre, aceleracion) in enumerate(analisis.obtener_ranking(), 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "4️⃣"
        print(f"   {emoji} {i}°. {nombre}: {aceleracion:.4f}x")
    
    # Explicación técnica NVLink
    print("\n6️⃣  ¿POR QUÉ NVLINK TIENE IMPACTO LIMITADO?")
    print("-" * 60)
    nvlink = next(c for c in componentes 
                 if c.nombre == ComponentesGPUPredefinidos.INTERCONEXION_NVLINK)
    nvlink_resultado = next(r for r in resultados if r.componente == nvlink)
    
    print(f"• NVLink tiene el mayor factor k = {nvlink.factor_mejora}")
    print(f"• Pero su fracción mejorable f = {nvlink.porcentaje_mejora:.1%} es baja")
    print(f"• Aceleración resultante: {nvlink_resultado.aceleracion:.4f}x")
    print(f"• La Ley de Amdahl muestra que el 80% NO mejorable limita el impacto total")
    print(f"• Fórmula: A = 1/((1-{nvlink.porcentaje_mejora}) + {nvlink.porcentaje_mejora}/{nvlink.factor_mejora}) = {nvlink_resultado.aceleracion:.4f}")
    
    # Comparación Texturizado vs VRAM
    print("\n7️⃣  COMPARACIÓN: TEXTURIZADO vs MEMORIA VRAM:")
    print("-" * 60)
    
    texturizado = next(c for c in componentes 
                      if c.nombre == ComponentesGPUPredefinidos.UNIDADES_TEXTURIZADO)
    vram = next(c for c in componentes 
               if c.nombre == ComponentesGPUPredefinidos.MEMORIA_VRAM)
    
    tex_resultado = next(r for r in resultados if r.componente == texturizado)
    vram_resultado = next(r for r in resultados if r.componente == vram)
    
    print(f"• Unidades de Texturizado: f={texturizado.porcentaje_mejora:.1%}, k={texturizado.factor_mejora} → A={tex_resultado.aceleracion:.4f}x")
    print(f"• Memoria VRAM: f={vram.porcentaje_mejora:.1%}, k={vram.factor_mejora} → A={vram_resultado.aceleracion:.4f}x")
    print(f"• Diferencia: {abs(tex_resultado.aceleracion - vram_resultado.aceleracion):.4f}x")
    
    if tex_resultado.aceleracion > vram_resultado.aceleracion:
        print(f"✅ Texturizado es mejor opción ({((tex_resultado.aceleracion - vram_resultado.aceleracion)/vram_resultado.aceleracion*100):.1f}% más aceleración)")
    else:
        print(f"✅ VRAM es mejor opción ({((vram_resultado.aceleracion - tex_resultado.aceleracion)/tex_resultado.aceleracion*100):.1f}% más aceleración)")
    
    # Resumen ejecutivo
    print("\n8️⃣  RESUMEN EJECUTIVO:")
    print("-" * 60)
    print("📋 RESPUESTAS AL PROBLEMA:")
    print(f"   1. Aceleraciones calculadas: ✅ Completado")
    print(f"   2. Límites teóricos: ✅ Completado") 
    print(f"   3. Tiempo renderizado optimizado: {resultado_tiempo.tiempo_optimizado:.2f}ms ✅")
    print(f"   4. Componente ≥30%: {'Encontrado' if componentes_30_porciento else 'No disponible'} ✅")
    print(f"   5. Gráficos A vs k: Funcionalidad disponible ✅")
    print(f"   6. Explicación NVLink: ✅ Completado")
    
    print(f"\n🎯 RECOMENDACIÓN FINAL:")
    print(f"   Optimizar '{analisis.mejor_componente.nombre}' para máxima ganancia global")
    print(f"   Aceleración esperada: {max(r.aceleracion for r in resultados):.4f}x")
    
    print("\n" + "="*80)
    print("                          ✅ ANÁLISIS COMPLETADO")
    print("="*80)


if __name__ == "__main__":
    try:
        resolver_problema_gpu_automatico()
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        sys.exit(1)
