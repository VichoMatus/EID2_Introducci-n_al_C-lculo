"""
Entidades del dominio para la aplicación de Ley de Amdahl
"""
from dataclasses import dataclass
from typing import Dict, List
from abc import ABC, abstractmethod


@dataclass
class ComponenteGPU:
    """Entidad que representa un componente de GPU"""
    nombre: str
    porcentaje_mejora: float  # f en la fórmula (como decimal 0-1)
    factor_mejora: float      # k en la fórmula
    
    def __post_init__(self):
        """Validaciones después de la inicialización"""
        if not 0 <= self.porcentaje_mejora <= 1:
            raise ValueError("El porcentaje de mejora debe estar entre 0 y 1")
        if self.factor_mejora <= 1:
            raise ValueError("El factor de mejora debe ser mayor a 1")


@dataclass
class ResultadoAmdahl:
    """Entidad que representa el resultado de calcular la Ley de Amdahl"""
    componente: ComponenteGPU
    aceleracion: float
    limite_teorico: float
    tiempo_original: float = None
    tiempo_optimizado: float = None
    porcentaje_mejora_total: float = None
    
    def __post_init__(self):
        """Cálculos automáticos después de la inicialización"""
        if self.tiempo_original and self.tiempo_optimizado:
            self.porcentaje_mejora_total = (
                (self.tiempo_original - self.tiempo_optimizado) / self.tiempo_original * 100
            )


@dataclass
class AnalisisComparativo:
    """Entidad para el análisis comparativo de componentes"""
    resultados: List[ResultadoAmdahl]
    mejor_componente: ComponenteGPU
    justificacion: str
    
    def obtener_ranking(self) -> List[tuple]:
        """Obtiene ranking de componentes por aceleración"""
        return sorted(
            [(r.componente.nombre, r.aceleracion) for r in self.resultados],
            key=lambda x: x[1],
            reverse=True
        )


class ICalculadorAmdahl(ABC):
    """Interface para el calculador de Ley de Amdahl"""
    
    @abstractmethod
    def calcular_aceleracion(self, componente: ComponenteGPU) -> float:
        """Calcula la aceleración usando la Ley de Amdahl"""
        pass
    
    @abstractmethod
    def calcular_limite_teorico(self, componente: ComponenteGPU) -> float:
        """Calcula el límite teórico cuando k tiende a infinito"""
        pass
    
    @abstractmethod
    def calcular_tiempo_optimizado(
        self, 
        tiempo_original: float, 
        aceleracion: float
    ) -> float:
        """Calcula el tiempo después de la optimización"""
        pass


class IVisualizador(ABC):
    """Interface para el visualizador de gráficos"""
    
    @abstractmethod
    def graficar_aceleracion_vs_factor(
        self, 
        porcentajes_mejora: List[float], 
        factores_mejora: List[float]
    ) -> None:
        """Gráfica A vs k para diferentes valores de f"""
        pass
    
    @abstractmethod
    def graficar_aceleracion_vs_porcentaje(
        self, 
        factores_mejora: List[float], 
        porcentajes_mejora: List[float]
    ) -> None:
        """Gráfica A vs f para diferentes valores de k"""
        pass


class IAnalizador(ABC):
    """Interface para el analizador de componentes"""
    
    @abstractmethod
    def determinar_mejor_componente(
        self, 
        componentes: List[ComponenteGPU]
    ) -> AnalisisComparativo:
        """Determina cuál componente es mejor optimizar"""
        pass
    
    @abstractmethod
    def analizar_ultimos_tres(
        self, 
        componentes: List[ComponenteGPU]
    ) -> AnalisisComparativo:
        """Analiza los últimos 3 componentes ingresados"""
        pass
