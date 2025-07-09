"""
Tests para los componentes GPU predefinidos
"""
import sys
import os

# Agregar el directorio padre al path para importar desde src
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.application.use_cases import CargarComponentesPredefinidosUseCase
from src.domain.value_objects import ComponentesGPUPredefinidos, ConfiguracionGPUPar
from src.infrastructure.calculador_amdahl import CalculadorAmdahl


def test_componentes_predefinidos():
    """Test de los componentes GPU predefinidos"""
    cargar_componentes = CargarComponentesPredefinidosUseCase()
    componentes = cargar_componentes.execute()
    
    # Verificar que se cargan los 4 componentes
    assert len(componentes) == 4
    
    # Verificar nombres
    nombres = [c.nombre for c in componentes]
    assert ComponentesGPUPredefinidos.NUCLEOS_CUDA in nombres
    assert ComponentesGPUPredefinidos.MEMORIA_VRAM in nombres
    assert ComponentesGPUPredefinidos.UNIDADES_TEXTURIZADO in nombres
    assert ComponentesGPUPredefinidos.INTERCONEXION_NVLINK in nombres


def test_aceleraciones_componentes_gpu():
    """Test de las aceleraciones esperadas para componentes GPU"""
    calculador = CalculadorAmdahl()
    cargar_componentes = CargarComponentesPredefinidosUseCase()
    componentes = cargar_componentes.execute()
    
    aceleraciones = {}
    for componente in componentes:
        aceleracion = calculador.calcular_aceleracion(componente)
        aceleraciones[componente.nombre] = aceleracion
    
    # Verificar que las aceleraciones son positivas y mayores a 1
    for nombre, aceleracion in aceleraciones.items():
        assert aceleracion > 1.0, f"{nombre} debe tener aceleración > 1"
        assert aceleracion < 10.0, f"{nombre} tiene aceleración muy alta: {aceleracion}"
    
    # El componente con mayor f*k debería tener mayor aceleración potencial
    # (aunque no siempre es así por la fórmula de Amdahl)
    print("Aceleraciones calculadas:")
    for nombre, aceleracion in sorted(aceleraciones.items(), key=lambda x: x[1], reverse=True):
        print(f"  {nombre}: {aceleracion:.4f}x")


def test_configuracion_gpu_par():
    """Test de la configuración para grupos pares"""
    config = ConfiguracionGPUPar()
    
    # Verificar que los porcentajes suman menos o igual a 100%
    total_porcentaje = (
        config.NUCLEOS_CUDA_PORCENTAJE +
        config.MEMORIA_VRAM_PORCENTAJE +
        config.UNIDADES_TEXTURIZADO_PORCENTAJE +
        config.INTERCONEXION_NVLINK_PORCENTAJE
    )
    assert total_porcentaje == 1.0, f"Los porcentajes deben sumar 100%, actual: {total_porcentaje*100}%"
    
    # Verificar valores específicos del problema
    assert config.NUCLEOS_CUDA_PORCENTAJE == 0.35
    assert config.NUCLEOS_CUDA_FACTOR == 5
    assert config.TIEMPO_RENDERIZADO_ORIGINAL == 50


if __name__ == "__main__":
    test_componentes_predefinidos()
    test_aceleraciones_componentes_gpu()
    test_configuracion_gpu_par()
    print("✅ Todos los tests pasaron correctamente")
