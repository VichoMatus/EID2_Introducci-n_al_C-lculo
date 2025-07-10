"""
Implementación del visualizador de gráficos usando matplotlib
"""
import matplotlib.pyplot as plt
import numpy as np
from typing import List
from ..domain.entities import IVisualizador
from ..infrastructure.calculador_amdahl import CalculadorAmdahl


class VisualizadorMatplotlib(IVisualizador):
    """Implementación del visualizador usando matplotlib"""
    
    def __init__(self):
        self.calculadora = CalculadorAmdahl()
        # Configurar matplotlib para mejor visualización
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 10
    
    def graficar_aceleracion_vs_factor(
        self, 
        porcentajes_mejora: List[float], 
        factores_mejora: List[float]
    ) -> None:
        """
        Gráfica A vs k para diferentes valores de f
        
        Args:
            porcentajes_mejora: Lista de valores f
            factores_mejora: Lista de valores k
        """
        plt.figure(figsize=(12, 8))
        
        for f in porcentajes_mejora:
            aceleraciones = []
            for k in factores_mejora:
                try:
                    a = self.calculadora.calcular_aceleracion_con_parametros(f, k)
                    aceleraciones.append(a)
                except ValueError:
                    aceleraciones.append(None)
            
            # Filtrar valores None
            k_validos = [k for k, a in zip(factores_mejora, aceleraciones) if a is not None]
            a_validos = [a for a in aceleraciones if a is not None]
            
            plt.plot(k_validos, a_validos, marker='o', linewidth=2, 
                    label=f'f = {f:.2f}', markersize=4)
        
        plt.xlabel('Factor de Mejora (k)', fontsize=12)
        plt.ylabel('Aceleración (A)', fontsize=12)
        plt.title('Ley de Amdahl: Aceleración vs Factor de Mejora', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=10)
        plt.xlim(min(factores_mejora), max(factores_mejora))
        
        # Añadir líneas de referencia
        plt.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='Sin mejora (A=1)')
        
        plt.tight_layout()
        plt.show()
        
        # Guardar gráfico
        plt.savefig('aceleracion_vs_factor.png', dpi=300, bbox_inches='tight')
        print("Gráfico guardado como 'aceleracion_vs_factor.png'")
    
    def graficar_aceleracion_vs_porcentaje(
        self, 
        factores_mejora: List[float], 
        porcentajes_mejora: List[float]
    ) -> None:
        """
        Gráfica A vs f para diferentes valores de k
        
        Args:
            factores_mejora: Lista de valores k
            porcentajes_mejora: Lista de valores f
        """
        plt.figure(figsize=(12, 8))
        
        for k in factores_mejora:
            aceleraciones = []
            for f in porcentajes_mejora:
                try:
                    a = self.calculadora.calcular_aceleracion_con_parametros(f, k)
                    aceleraciones.append(a)
                except ValueError:
                    aceleraciones.append(None)
            
            # Filtrar valores None
            f_validos = [f for f, a in zip(porcentajes_mejora, aceleraciones) if a is not None]
            a_validos = [a for a in aceleraciones if a is not None]
            
            plt.plot(f_validos, a_validos, marker='s', linewidth=2, 
                    label=f'k = {k}', markersize=4)
        
        plt.xlabel('Fracción Mejorable (f)', fontsize=12)
        plt.ylabel('Aceleración (A)', fontsize=12)
        plt.title('Ley de Amdahl: Aceleración vs Fracción Mejorable', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=10)
        plt.xlim(0, 1)
        
        # Añadir líneas de referencia
        plt.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='Sin mejora (A=1)')
        
        plt.tight_layout()
        plt.show()
        
        # Guardar gráfico
        plt.savefig('aceleracion_vs_porcentaje.png', dpi=300, bbox_inches='tight')
        print("Gráfico guardado como 'aceleracion_vs_porcentaje.png'")
    
    def graficar_comparacion_componentes(self, componentes_data: List[dict]) -> None:
        """
        Gráfica de barras comparando aceleraciones de componentes
        
        Args:
            componentes_data: Lista de diccionarios con 'nombre' y 'aceleracion'
        """
        plt.figure(figsize=(12, 6))
        
        nombres = [comp['nombre'] for comp in componentes_data]
        aceleraciones = [comp['aceleracion'] for comp in componentes_data]
        
        # Crear gráfico de barras con colores diferentes
        colores = plt.cm.viridis(np.linspace(0, 1, len(nombres)))
        barras = plt.bar(nombres, aceleraciones, color=colores, alpha=0.8)
        
        # Añadir valores sobre las barras
        for barra, aceleracion in zip(barras, aceleraciones):
            altura = barra.get_height()
            plt.text(barra.get_x() + barra.get_width()/2., altura + 0.01,
                    f'{aceleracion:.4f}', ha='center', va='bottom', fontweight='bold')
        
        plt.xlabel('Componentes GPU', fontsize=12)
        plt.ylabel('Aceleración', fontsize=12)
        plt.title('Comparación de Aceleraciones por Componente GPU', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.show()
        
        # Guardar gráfico
        plt.savefig('comparacion_componentes.png', dpi=300, bbox_inches='tight')
        print("Gráfico guardado como 'comparacion_componentes.png'")
    
    def graficar_limite_teorico(self, porcentajes_mejora: List[float]) -> None:
        """
        Gráfica del límite teórico A_max = 1/(1-f)
        
        Args:
            porcentajes_mejora: Lista de valores f
        """
        plt.figure(figsize=(10, 6))
        
        limites = [1/(1-f) if f < 1 else float('inf') for f in porcentajes_mejora]
        
        # Filtrar valores infinitos para visualización
        f_filtrados = [f for f, limite in zip(porcentajes_mejora, limites) if limite < 100]
        limites_filtrados = [limite for limite in limites if limite < 100]
        
        plt.plot(f_filtrados, limites_filtrados, 'r-', linewidth=3, 
                label='Límite Teórico A_max = 1/(1-f)')
        plt.fill_between(f_filtrados, 1, limites_filtrados, alpha=0.2, color='red')
        
        plt.xlabel('Fracción Mejorable (f)', fontsize=12)
        plt.ylabel('Aceleración Máxima Teórica', fontsize=12)
        plt.title('Límite Teórico de la Ley de Amdahl', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=12)
        plt.xlim(0, 0.95)
        plt.ylim(1, 20)
        
        plt.tight_layout()
        plt.show()
        
        # Guardar gráfico
        plt.savefig('limite_teorico.png', dpi=300, bbox_inches='tight')
        print("Gráfico guardado como 'limite_teorico.png'")
