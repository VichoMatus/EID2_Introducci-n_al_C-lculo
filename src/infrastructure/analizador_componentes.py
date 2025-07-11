from typing import List
from ..domain.entities import (
    ComponenteGPU, 
    ResultadoAmdahl, 
    AnalisisComparativo,
    IAnalizador,
    ICalculadorAmdahl
)


class AnalizadorComponentes(IAnalizador):
    #Implementación del analizador de componentes GPU
    
    def __init__(self, calculador: ICalculadorAmdahl):
        self.calculador = calculador
    
    def determinar_mejor_componente(
        self, 
        componentes: List[ComponenteGPU]
    ) -> AnalisisComparativo:
        resultados = []
        mejor_aceleracion = 0
        mejor_componente = None
        
        for componente in componentes:
            aceleracion = self.calculador.calcular_aceleracion(componente)
            limite_teorico = self.calculador.calcular_limite_teorico(componente)
            
            resultado = ResultadoAmdahl(
                componente=componente,
                aceleracion=aceleracion,
                limite_teorico=limite_teorico
            )
            resultados.append(resultado)
            
            if aceleracion > mejor_aceleracion:
                mejor_aceleracion = aceleracion
                mejor_componente = componente
        
        justificacion = self._generar_justificacion(mejor_componente, resultados)
        
        return AnalisisComparativo(
            resultados=resultados,
            mejor_componente=mejor_componente,
            justificacion=justificacion
        )
    
    def analizar_ultimos_tres(
        self, 
        componentes: List[ComponenteGPU]
    ) -> AnalisisComparativo:
        ultimos_tres = componentes[-3:] if len(componentes) >= 3 else componentes
        return self.determinar_mejor_componente(ultimos_tres)
    
    def _generar_justificacion(
        self, 
        mejor_componente: ComponenteGPU, 
        resultados: List[ResultadoAmdahl]
    ) -> str:
        if not mejor_componente:
            return "No se pudo determinar un mejor componente"
        
        mejor_resultado = next(r for r in resultados if r.componente == mejor_componente)
        
        justificacion = (
            f"El componente '{mejor_componente.nombre}' es la mejor opción para optimizar "
            f"porque ofrece la mayor aceleración global: {mejor_resultado.aceleracion:.4f}x. "
            f"\n\nAnálisis técnico:\n"
            f"- Fracción mejorable (f): {mejor_componente.porcentaje_mejora:.1%}\n"
            f"- Factor de mejora (k): {mejor_componente.factor_mejora}\n"
            f"- Aceleración real: {mejor_resultado.aceleracion:.4f}x\n"
            f"- Límite teórico: {mejor_resultado.limite_teorico:.4f}x\n"
            f"- Eficiencia: {(mejor_resultado.aceleracion/mejor_resultado.limite_teorico)*100:.1f}% del límite teórico\n\n"
        )
        
        # Añadir comparación con otros componentes
        otros_resultados = [r for r in resultados if r.componente != mejor_componente]
        if otros_resultados:
            justificacion += "Comparación con otros componentes:\n"
            for resultado in sorted(otros_resultados, key=lambda x: x.aceleracion, reverse=True):
                diferencia = mejor_resultado.aceleracion - resultado.aceleracion
                justificacion += (
                    f"- {resultado.componente.nombre}: {resultado.aceleracion:.4f}x "
                    f"(diferencia: +{diferencia:.4f}x)\n"
                )
        
        return justificacion
    
    def calcular_eficiencia_optimizacion(
        self, 
        componente: ComponenteGPU
    ) -> dict:
        aceleracion = self.calculador.calcular_aceleracion(componente)
        limite_teorico = self.calculador.calcular_limite_teorico(componente)
        
        eficiencia = (aceleracion / limite_teorico) * 100
        margen_mejora = limite_teorico - aceleracion
        
        return {
            "aceleracion": aceleracion,
            "limite_teorico": limite_teorico,
            "eficiencia_porcentaje": round(eficiencia, 2),
            "margen_mejora": round(margen_mejora, 4),
            "factor_escalabilidad": round(componente.factor_mejora / aceleracion, 2)
        }
    
    def encontrar_componente_objetivo(
        self, 
        componentes: List[ComponenteGPU], 
        aceleracion_minima: float
    ) -> List[ComponenteGPU]:
        componentes_validos = []
        
        for componente in componentes:
            aceleracion = self.calculador.calcular_aceleracion(componente)
            if aceleracion >= aceleracion_minima:
                componentes_validos.append(componente)
        
        # Ordenar por aceleración descendente
        componentes_validos.sort(
            key=lambda c: self.calculador.calcular_aceleracion(c), 
            reverse=True
        )
        
        return componentes_validos
