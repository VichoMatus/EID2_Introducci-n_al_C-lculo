"""
Tests para el calculador de Ley de Amdahl
"""
import pytest
import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.domain.entities import ComponenteGPU
from src.infrastructure.calculador_amdahl import CalculadorAmdahl


class TestCalculadorAmdahl:
    """Clase de pruebas para el calculador de Amdahl"""
    
    def setup_method(self):
        """Configuración inicial para cada test"""
        self.calculador = CalculadorAmdahl()
    
    def test_calcular_aceleracion_basico(self):
        """Test básico de cálculo de aceleración"""
        # f = 0.5, k = 2 -> A = 1/((1-0.5) + 0.5/2) = 1/(0.5 + 0.25) = 1/0.75 = 1.3333
        componente = ComponenteGPU("Test", 0.5, 2)
        resultado = self.calculador.calcular_aceleracion(componente)
        assert abs(resultado - 1.3333) < 0.0001
    
    def test_calcular_aceleracion_nucleos_cuda(self):
        """Test con datos reales de núcleos CUDA"""
        # f = 0.35, k = 5 -> A = 1/((1-0.35) + 0.35/5) = 1/(0.65 + 0.07) = 1/0.72 ≈ 1.3889
        componente = ComponenteGPU("Núcleos CUDA", 0.35, 5)
        resultado = self.calculador.calcular_aceleracion(componente)
        assert abs(resultado - 1.3889) < 0.0001
    
    def test_calcular_limite_teorico(self):
        """Test del límite teórico"""
        # f = 0.8 -> A_max = 1/(1-0.8) = 1/0.2 = 5
        componente = ComponenteGPU("Test", 0.8, 10)
        limite = self.calculador.calcular_limite_teorico(componente)
        assert limite == 5.0
    
    def test_calcular_tiempo_optimizado(self):
        """Test del cálculo de tiempo optimizado"""
        tiempo_original = 100.0
        aceleracion = 2.0
        tiempo_optimizado = self.calculador.calcular_tiempo_optimizado(tiempo_original, aceleracion)
        assert tiempo_optimizado == 50.0
    
    def test_componente_gpu_validaciones(self):
        """Test de validaciones de ComponenteGPU"""
        # Porcentaje fuera de rango
        with pytest.raises(ValueError):
            ComponenteGPU("Test", 1.5, 2)  # f > 1
        
        with pytest.raises(ValueError):
            ComponenteGPU("Test", -0.1, 2)  # f < 0
        
        # Factor de mejora inválido
        with pytest.raises(ValueError):
            ComponenteGPU("Test", 0.5, 0.5)  # k <= 1
    
    def test_casos_extremos(self):
        """Test de casos extremos"""
        # f = 0 (nada mejorable) -> A = 1
        componente = ComponenteGPU("Sin mejora", 0.0, 100)
        resultado = self.calculador.calcular_aceleracion(componente)
        assert resultado == 1.0
        
        # f muy cercano a 1
        componente = ComponenteGPU("Casi todo mejorable", 0.99, 100)
        resultado = self.calculador.calcular_aceleracion(componente)
        limite = self.calculador.calcular_limite_teorico(componente)
        assert resultado < limite  # Siempre menor al límite
        assert limite == 100.0  # 1/(1-0.99) = 100
    
    def test_factor_necesario_para_aceleracion(self):
        """Test del cálculo de factor k necesario"""
        f = 0.5
        aceleracion_objetivo = 1.6
        k_necesario = self.calculador.calcular_factor_necesario_para_aceleracion(f, aceleracion_objetivo)
        
        # Verificar que con ese k se obtiene la aceleración objetivo
        componente = ComponenteGPU("Test", f, k_necesario)
        aceleracion_real = self.calculador.calcular_aceleracion(componente)
        assert abs(aceleracion_real - aceleracion_objetivo) < 0.0001
