import math
from ..domain.entities import ComponenteGPU, ICalculadorAmdahl
from ..domain.value_objects import ConstantesMatematicas


class CalculadorAmdahl(ICalculadorAmdahl):
    #Implementación concreta del calculador de Ley de Amdahl
    
    def calcular_aceleracion(self, componente: ComponenteGPU) -> float:
        f = componente.porcentaje_mejora
        k = componente.factor_mejora
        
        aceleracion = 1 / ((1 - f) + (f / k))
        return round(aceleracion, ConstantesMatematicas.PRECISION_DECIMAL)
    
    def calcular_limite_teorico(self, componente: ComponenteGPU) -> float:
        f = componente.porcentaje_mejora
        limite = 1 / (1 - f)
        return round(limite, ConstantesMatematicas.PRECISION_DECIMAL)
    
    def calcular_tiempo_optimizado(
        self, 
        tiempo_original: float, 
        aceleracion: float
    ) -> float:
        
        tiempo_optimizado = tiempo_original / aceleracion
        return round(tiempo_optimizado, ConstantesMatematicas.PRECISION_DECIMAL)
    
    def calcular_aceleracion_con_parametros(self, f: float, k: float) -> float:
        if not 0 <= f <= 1:
            raise ValueError("f debe estar entre 0 y 1")
        if k <= 1:
            raise ValueError("k debe ser mayor a 1")
            
        aceleracion = 1 / ((1 - f) + (f / k))
        return round(aceleracion, ConstantesMatematicas.PRECISION_DECIMAL)
    
    def calcular_factor_necesario_para_aceleracion(
        self, 
        f: float, 
        aceleracion_objetivo: float
    ) -> float:
        if aceleracion_objetivo <= 1:
            raise ValueError("La aceleración objetivo debe ser mayor a 1")
        
        limite_teorico = 1 / (1 - f)
        if aceleracion_objetivo >= limite_teorico:
            return float('inf')  # Imposible alcanzar
        
        k_necesario = f / (1/aceleracion_objetivo - (1 - f))
        return round(k_necesario, ConstantesMatematicas.PRECISION_DECIMAL)
