from dataclasses import dataclass
from typing import Dict, List
from abc import ABC, abstractmethod


@dataclass
class ComponenteGPU:
    nombre: str
    porcentaje_mejora: float  # f en la fórmula (como decimal 0-1)
    factor_mejora: float      # k en la fórmula
    
    def __post_init__(self):
        if not 0 <= self.porcentaje_mejora <= 1:
            raise ValueError("El porcentaje de mejora debe estar entre 0 y 1")
        if self.factor_mejora <= 1:
            raise ValueError("El factor de mejora debe ser mayor a 1")


@dataclass
class ResultadoAmdahl:
    componente: ComponenteGPU
    aceleracion: float
    limite_teorico: float
    tiempo_original: float = None
    tiempo_optimizado: float = None
    porcentaje_mejora_total: float = None
    
    def __post_init__(self):
        if self.tiempo_original and self.tiempo_optimizado:
            self.porcentaje_mejora_total = (
                (self.tiempo_original - self.tiempo_optimizado) / self.tiempo_original * 100
            )


@dataclass
class AnalisisComparativo:
    resultados: List[ResultadoAmdahl]
    mejor_componente: ComponenteGPU
    justificacion: str
    
    def obtener_ranking(self) -> List[tuple]:
        return sorted(
            [(r.componente.nombre, r.aceleracion) for r in self.resultados],
            key=lambda x: x[1],
            reverse=True
        )


class ICalculadorAmdahl(ABC):
    """Interface para el calculador de Ley de Amdahl"""
    
    @abstractmethod
    def calcular_aceleracion(self, componente: ComponenteGPU) -> float:
        pass
    
    @abstractmethod
    def calcular_limite_teorico(self, componente: ComponenteGPU) -> float:
        pass
    
    @abstractmethod
    def calcular_tiempo_optimizado(
        self, 
        tiempo_original: float, 
        aceleracion: float
    ) -> float:
        pass


class IVisualizador(ABC):
    """Interface para el visualizador de gráficos"""
    
    @abstractmethod
    def graficar_aceleracion_vs_factor(
        self, 
        porcentajes_mejora: List[float], 
        factores_mejora: List[float]
    ) -> None:
        pass
    
    @abstractmethod
    def graficar_aceleracion_vs_porcentaje(
        self, 
        factores_mejora: List[float], 
        porcentajes_mejora: List[float]
    ) -> None:
        pass


class IAnalizador(ABC):
    
    @abstractmethod
    def determinar_mejor_componente(
        self, 
        componentes: List[ComponenteGPU]
    ) -> AnalisisComparativo:
        pass
    
    @abstractmethod
    def analizar_ultimos_tres(
        self, 
        componentes: List[ComponenteGPU]
    ) -> AnalisisComparativo:
        pass
