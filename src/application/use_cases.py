"""
Casos de uso para la aplicación de Ley de Amdahl
"""
from typing import List
from ..domain.entities import (
    ComponenteGPU, 
    ResultadoAmdahl, 
    AnalisisComparativo,
    ICalculadorAmdahl,
    IVisualizador,
    IAnalizador
)
from ..domain.value_objects import (
    ConfiguracionGPUPar,
    ComponentesGPUPredefinidos,
    ConstantesMatematicas
)


class CalcularAceleracionUseCase:
    """Caso de uso para calcular aceleración de un componente"""
    
    def __init__(self, calculador: ICalculadorAmdahl):
        self.calculador = calculador
    
    def execute(self, componente: ComponenteGPU) -> ResultadoAmdahl:
        """Ejecuta el cálculo de aceleración"""
        aceleracion = self.calculador.calcular_aceleracion(componente)
        limite_teorico = self.calculador.calcular_limite_teorico(componente)
        
        return ResultadoAmdahl(
            componente=componente,
            aceleracion=aceleracion,
            limite_teorico=limite_teorico
        )


class CalcularTiempoOptimizadoUseCase:
    """Caso de uso para calcular tiempo después de optimización"""
    
    def __init__(self, calculador: ICalculadorAmdahl):
        self.calculador = calculador
    
    def execute(
        self, 
        componente: ComponenteGPU, 
        tiempo_original: float
    ) -> ResultadoAmdahl:
        """Ejecuta el cálculo de tiempo optimizado"""
        aceleracion = self.calculador.calcular_aceleracion(componente)
        limite_teorico = self.calculador.calcular_limite_teorico(componente)
        tiempo_optimizado = self.calculador.calcular_tiempo_optimizado(
            tiempo_original, aceleracion
        )
        
        return ResultadoAmdahl(
            componente=componente,
            aceleracion=aceleracion,
            limite_teorico=limite_teorico,
            tiempo_original=tiempo_original,
            tiempo_optimizado=tiempo_optimizado
        )


class GenerarGraficosUseCase:
    """Caso de uso para generar gráficos"""
    
    def __init__(self, visualizador: IVisualizador):
        self.visualizador = visualizador
    
    def graficar_a_vs_k(self, porcentajes_mejora: List[float]) -> None:
        """Genera gráfico A vs k para diferentes f"""
        factores_mejora = list(range(1, 21))  # k de 1 a 20
        self.visualizador.graficar_aceleracion_vs_factor(
            porcentajes_mejora, factores_mejora
        )
    
    def graficar_a_vs_f(self, factores_mejora: List[float]) -> None:
        """Genera gráfico A vs f para diferentes k"""
        porcentajes_mejora = [i/100 for i in range(5, 96, 5)]  # f de 0.05 a 0.95
        self.visualizador.graficar_aceleracion_vs_porcentaje(
            factores_mejora, porcentajes_mejora
        )


class AnalizarComponentesUseCase:
    """Caso de uso para analizar y comparar componentes"""
    
    def __init__(self, analizador: IAnalizador):
        self.analizador = analizador
    
    def determinar_mejor_optimizacion(
        self, 
        componentes: List[ComponenteGPU]
    ) -> AnalisisComparativo:
        """Determina la mejor optimización entre todos los componentes"""
        return self.analizador.determinar_mejor_componente(componentes)
    
    def analizar_ultimos_tres_componentes(
        self, 
        componentes: List[ComponenteGPU]
    ) -> AnalisisComparativo:
        """Analiza los últimos 3 componentes ingresados"""
        return self.analizador.analizar_ultimos_tres(componentes)


class CargarComponentesPredefinidosUseCase:
    """Caso de uso para cargar componentes GPU predefinidos"""
    
    def execute(self) -> List[ComponenteGPU]:
        """Carga los componentes predefinidos para grupos pares (GPU)"""
        config = ConfiguracionGPUPar()
        
        return [
            ComponenteGPU(
                nombre=ComponentesGPUPredefinidos.NUCLEOS_CUDA,
                porcentaje_mejora=config.NUCLEOS_CUDA_PORCENTAJE,
                factor_mejora=config.NUCLEOS_CUDA_FACTOR
            ),
            ComponenteGPU(
                nombre=ComponentesGPUPredefinidos.MEMORIA_VRAM,
                porcentaje_mejora=config.MEMORIA_VRAM_PORCENTAJE,
                factor_mejora=config.MEMORIA_VRAM_FACTOR
            ),
            ComponenteGPU(
                nombre=ComponentesGPUPredefinidos.UNIDADES_TEXTURIZADO,
                porcentaje_mejora=config.UNIDADES_TEXTURIZADO_PORCENTAJE,
                factor_mejora=config.UNIDADES_TEXTURIZADO_FACTOR
            ),
            ComponenteGPU(
                nombre=ComponentesGPUPredefinidos.INTERCONEXION_NVLINK,
                porcentaje_mejora=config.INTERCONEXION_NVLINK_PORCENTAJE,
                factor_mejora=config.INTERCONEXION_NVLINK_FACTOR
            )
        ]


class ResolverProblemaGPUUseCase:
    """Caso de uso para resolver el problema específico de GPU (grupos pares)"""
    
    def __init__(
        self, 
        calculador: ICalculadorAmdahl,
        analizador: IAnalizador,
        visualizador: IVisualizador
    ):
        self.calculador = calculador
        self.analizador = analizador  
        self.visualizador = visualizador
        self.cargar_componentes = CargarComponentesPredefinidosUseCase()
        self.calcular_aceleracion = CalcularAceleracionUseCase(calculador)
        self.calcular_tiempo = CalcularTiempoOptimizadoUseCase(calculador)
        self.generar_graficos = GenerarGraficosUseCase(visualizador)
        self.analizar_componentes = AnalizarComponentesUseCase(analizador)
    
    def resolver_problema_completo(self) -> dict:
        """Resuelve todo el problema planteado para grupos pares"""
        componentes = self.cargar_componentes.execute()
        
        # 1. Calcular aceleración para cada componente
        resultados = []
        for componente in componentes:
            resultado = self.calcular_aceleracion.execute(componente)
            resultados.append(resultado)
        
        # 2. Calcular límites teóricos (ya incluidos en resultados)
        
        # 3. Calcular tiempo para núcleos CUDA (50ms original)
        nucleos_cuda = next(c for c in componentes 
                           if c.nombre == ComponentesGPUPredefinidos.NUCLEOS_CUDA)
        resultado_tiempo = self.calcular_tiempo.execute(
            nucleos_cuda, 
            ConfiguracionGPUPar.TIEMPO_RENDERIZADO_ORIGINAL
        )
        
        # 4. Determinar componente para 30% de aceleración
        componente_30_porciento = self._encontrar_componente_para_aceleracion(
            componentes, 1.3  # 30% de aceleración = factor 1.3
        )
        
        # 5. Generar gráficos A vs k para f=0.25 y f=0.35
        self.generar_graficos.graficar_a_vs_k([0.25, 0.35])
        
        # 6. Análisis comparativo
        analisis = self.analizar_componentes.determinar_mejor_optimizacion(componentes)
        
        return {
            "resultados_aceleracion": resultados,
            "tiempo_nucleos_cuda": resultado_tiempo,
            "componente_30_porciento": componente_30_porciento,
            "analisis_comparativo": analisis,
            "explicacion_nvlink": self._explicar_limitacion_nvlink(componentes),
            "comparacion_texturizado_vs_vram": self._comparar_texturizado_vs_vram(componentes)
        }
    
    def _encontrar_componente_para_aceleracion(
        self, 
        componentes: List[ComponenteGPU], 
        aceleracion_objetivo: float
    ) -> ComponenteGPU:
        """Encuentra el componente que logra la aceleración objetivo"""
        mejor_componente = None
        mejor_aceleracion = 0
        
        for componente in componentes:
            aceleracion = self.calculador.calcular_aceleracion(componente)
            if aceleracion >= aceleracion_objetivo and aceleracion > mejor_aceleracion:
                mejor_componente = componente
                mejor_aceleracion = aceleracion
        
        return mejor_componente
    
    def _explicar_limitacion_nvlink(self, componentes: List[ComponenteGPU]) -> str:
        """Explica por qué NVLink tiene impacto limitado"""
        nvlink = next(c for c in componentes 
                     if c.nombre == ComponentesGPUPredefinidos.INTERCONEXION_NVLINK)
        aceleracion = self.calculador.calcular_aceleracion(nvlink)
        
        return (
            f"A pesar de que NVLink tiene k={nvlink.factor_mejora} (el más alto), "
            f"su aceleración global es solo {aceleracion:.4f} porque su fracción "
            f"mejorable f={nvlink.porcentaje_mejora} es relativamente baja (20%). "
            f"Según la Ley de Amdahl, A = 1/((1-f) + f/k), el impacto está limitado "
            f"por la porción no mejorable (80% del sistema)."
        )
    
    def _comparar_texturizado_vs_vram(self, componentes: List[ComponenteGPU]) -> dict:
        """Compara unidades de texturizado vs memoria VRAM"""
        texturizado = next(c for c in componentes 
                          if c.nombre == ComponentesGPUPredefinidos.UNIDADES_TEXTURIZADO)
        vram = next(c for c in componentes 
                   if c.nombre == ComponentesGPUPredefinidos.MEMORIA_VRAM)
        
        aceleracion_tex = self.calculador.calcular_aceleracion(texturizado)
        aceleracion_vram = self.calculador.calcular_aceleracion(vram)
        
        return {
            "texturizado": {
                "componente": texturizado,
                "aceleracion": aceleracion_tex
            },
            "vram": {
                "componente": vram,
                "aceleracion": aceleracion_vram
            },
            "mejor": "texturizado" if aceleracion_tex > aceleracion_vram else "vram",
            "diferencia": abs(aceleracion_tex - aceleracion_vram)
        }
