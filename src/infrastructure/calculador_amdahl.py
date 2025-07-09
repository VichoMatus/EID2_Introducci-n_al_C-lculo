"""
Implementación del calculador de Ley de Amdahl
"""
import math
from ..domain.entities import ComponenteGPU, ICalculadorAmdahl
from ..domain.value_objects import ConstantesMatematicas


class CalculadorAmdahl(ICalculadorAmdahl):
    """Implementación concreta del calculador de Ley de Amdahl"""
    
    def calcular_aceleracion(self, componente: ComponenteGPU) -> float:
        """
        Calcula la aceleración usando la Ley de Amdahl: A = 1 / ((1-f) + f/k)
        
        Args:
            componente: Componente GPU con f (porcentaje_mejora) y k (factor_mejora)
            
        Returns:
            float: Aceleración calculada
        """
        f = componente.porcentaje_mejora
        k = componente.factor_mejora
        
        aceleracion = 1 / ((1 - f) + (f / k))
        return round(aceleracion, ConstantesMatematicas.PRECISION_DECIMAL)
    
    def calcular_limite_teorico(self, componente: ComponenteGPU) -> float:
        """
        Calcula el límite teórico cuando k → ∞: A_max = 1 / (1-f)
        
        Args:
            componente: Componente GPU con f (porcentaje_mejora)
            
        Returns:
            float: Límite teórico máximo
        """
        f = componente.porcentaje_mejora
        limite = 1 / (1 - f)
        return round(limite, ConstantesMatematicas.PRECISION_DECIMAL)
    
    def calcular_tiempo_optimizado(
        self, 
        tiempo_original: float, 
        aceleracion: float
    ) -> float:
        """
        Calcula el tiempo después de la optimización: t_nuevo = t_original / A
        
        Args:
            tiempo_original: Tiempo antes de la optimización
            aceleracion: Factor de aceleración obtenido
            
        Returns:
            float: Tiempo después de la optimización
        """
        tiempo_optimizado = tiempo_original / aceleracion
        return round(tiempo_optimizado, ConstantesMatematicas.PRECISION_DECIMAL)
    
    def calcular_aceleracion_con_parametros(self, f: float, k: float) -> float:
        """
        Calcula aceleración con parámetros directos (útil para gráficos)
        
        Args:
            f: Fracción mejorable (0-1)
            k: Factor de mejora
            
        Returns:
            float: Aceleración calculada
        """
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
        """
        Calcula el factor k necesario para lograr una aceleración objetivo
        Despejando k de la fórmula: k = f / (1/A - (1-f))
        
        Args:
            f: Fracción mejorable
            aceleracion_objetivo: Aceleración que se quiere lograr
            
        Returns:
            float: Factor k necesario
        """
        if aceleracion_objetivo <= 1:
            raise ValueError("La aceleración objetivo debe ser mayor a 1")
        
        limite_teorico = 1 / (1 - f)
        if aceleracion_objetivo >= limite_teorico:
            return float('inf')  # Imposible alcanzar
        
        k_necesario = f / (1/aceleracion_objetivo - (1 - f))
        return round(k_necesario, ConstantesMatematicas.PRECISION_DECIMAL)
