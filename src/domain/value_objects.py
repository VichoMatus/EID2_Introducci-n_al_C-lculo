from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ComponentesGPUPredefinidos:
    
    NUCLEOS_CUDA = "Núcleos CUDA"
    MEMORIA_VRAM = "Memoria VRAM" 
    UNIDADES_TEXTURIZADO = "Unidades de texturizado"
    INTERCONEXION_NVLINK = "Interconexión NVLink"
    
    @classmethod
    def obtener_todos(cls) -> List[str]:
        return [
            cls.NUCLEOS_CUDA,
            cls.MEMORIA_VRAM,
            cls.UNIDADES_TEXTURIZADO,
            cls.INTERCONEXION_NVLINK
        ]


@dataclass(frozen=True)
class ConfiguracionGPUPar:
    
    # Datos del problema según el PDF
    NUCLEOS_CUDA_PORCENTAJE = 0.35  # 35%
    NUCLEOS_CUDA_FACTOR = 5
    
    MEMORIA_VRAM_PORCENTAJE = 0.20  # 20%
    MEMORIA_VRAM_FACTOR = 3
    
    UNIDADES_TEXTURIZADO_PORCENTAJE = 0.25  # 25%
    UNIDADES_TEXTURIZADO_FACTOR = 7
    
    INTERCONEXION_NVLINK_PORCENTAJE = 0.20  # 20%
    INTERCONEXION_NVLINK_FACTOR = 10
    
    TIEMPO_RENDERIZADO_ORIGINAL = 50  # 50 ms


@dataclass(frozen=True)
class ConstantesMatematicas:
    
    LIMITE_INFINITO = 1000  # Aproximación para k → ∞
    PRECISION_DECIMAL = 4   # Decimales para redondeo
    PORCENTAJE_ACELERACION_OBJETIVO = 30  # 30% objetivo de aceleración
