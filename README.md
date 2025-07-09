# EID2 - Introducción al Cálculo: Ley de Amdahl

## 🎯 Descripción del Proyecto

Aplicación desarrollada con **Arquitectura Limpia en Python** para resolver problemas de optimización de componentes GPU usando la **Ley de Amdahl**. Este proyecto está diseñado para grupos pares según las especificaciones del documento EID2.

## 🧮 Ley de Amdahl

La Ley de Amdahl predice la mejora máxima al optimizar un componente de un sistema:

```
A = 1 / ((1-f) + f/k)
```

Donde:
- **A**: Aceleración obtenida
- **f**: Fracción mejorable del sistema (0 ≤ f ≤ 1)  
- **k**: Factor de mejora (k > 1)

**Límite teórico**: Cuando k → ∞: `A_max = 1/(1-f)`

## 🖥️ Componentes GPU (Grupos Pares)

| Componente | Porcentaje Mejora | Factor Mejora |
|------------|-------------------|---------------|
| Núcleos CUDA | 35% | 5 |
| Memoria VRAM | 20% | 3 |
| Unidades de Texturizado | 25% | 7 |
| Interconexión NVLink | 20% | 10 |

## 🏗️ Arquitectura Limpia

El proyecto sigue los principios de Clean Architecture con las siguientes capas:

```
src/
├── domain/              # Entidades y reglas de negocio
│   ├── entities.py      # ComponenteGPU, ResultadoAmdahl, etc.
│   └── value_objects.py # Configuraciones y constantes
├── application/         # Casos de uso
│   └── use_cases.py     # Lógica de aplicación
├── infrastructure/      # Implementaciones concretas
│   ├── calculador_amdahl.py
│   ├── visualizador_matplotlib.py
│   └── analizador_componentes.py
└── presentation/        # Interfaz de usuario
    └── cli.py           # Interfaz de línea de comandos
```

## 🚀 Instalación y Ejecución

### 1. Clonar o Descargar el Proyecto

```bash
# Si estás en el directorio del proyecto
cd "d:\UCT\Tercer Semestre\Introduccion_al_Calculo\EID2_Introducci-n_al_C-lculo"
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la Aplicación

#### 🖥️ Interfaz Gráfica (GUI) - Recomendado

```bash
# Lanzar GUI directamente
python main_gui.py

# O seleccionar GUI desde menú principal
python main.py
```

#### 💻 Línea de Comandos (CLI)

```bash
# Lanzar CLI directamente
python main.py cli

# O seleccionar CLI desde menú principal
python main.py
```

#### 🎯 Demo Automático

```bash
# Ver resolución completa del problema
python demo.py
```

## 🖥️ Interfaz Gráfica (GUI)

La aplicación incluye una **interfaz gráfica moderna** desarrollada con **CustomTkinter**:

### ✨ Características de la GUI:

- **🎨 Diseño Moderno**: Tema oscuro con colores profesionales
- **📱 Responsive**: Se adapta a diferentes tamaños de pantalla
- **🧩 Navegación por Pestañas**: Resultados, Gráficos y Teoría
- **📊 Gráficos Integrados**: Matplotlib embebido en la interfaz
- **⚡ Multihilo**: Procesamiento en segundo plano sin bloqueos
- **🔍 Validación en Tiempo Real**: Verificación automática de datos

### 📋 Funcionalidades GUI:

1. **🎯 Problema Completo**
   - Botón "Resolver Problema Completo"
   - Análisis automático de todos los componentes GPU
   - Resultados formatados profesionalmente

2. **⚙️ Componente Personalizado**
   - Formulario intuitivo para crear componentes
   - Validación automática de datos
   - Cálculo inmediato de aceleraciones

3. **📈 Gráficos Interactivos**
   - A vs k (Aceleración vs Factor de Mejora)
   - A vs f (Aceleración vs Fracción Mejorable)
   - Comparación de componentes
   - Límites teóricos

4. **🔍 Análisis Avanzado**
   - Análisis de últimos 3 componentes
   - Comparaciones automáticas
   - Recomendaciones técnicas

5. **📚 Información Teórica**
   - Documentación completa de la Ley de Amdahl
   - Ejemplos prácticos
   - Aplicaciones industriales

## 📋 Funcionalidades

### 🖥️ Interfaz Gráfica (GUI)
- **🎯 Resolución Completa**: Análisis automático del problema GPU
- **⚙️ Componentes Personalizados**: Crear y evaluar componentes propios
- **📊 Gráficos Interactivos**: Visualizaciones integradas en la aplicación
- **📚 Documentación**: Teoría y ejemplos integrados
- **🔍 Análisis Comparativo**: Evaluación inteligente de componentes

### 💻 Línea de Comandos (CLI)

1. **Resolver problema completo (Grupos Pares - GPU)**
   - Calcula aceleraciones para todos los componentes
   - Determina tiempos optimizados
   - Encuentra componente para 30% de aceleración
   - Genera análisis comparativo completo

2. **Calcular aceleración de componente personalizado**
   - Permite ingresar componentes personalizados
   - Calcula aceleración y límite teórico
   - Guarda componentes para análisis posterior

3. **Mostrar componentes predefinidos**
   - Muestra los 4 componentes GPU del problema
   - Calcula sus aceleraciones automáticamente

4. **Analizar últimos 3 componentes ingresados**
   - Analiza los últimos componentes personalizados
   - Determina cuál es la mejor opción

5. **Generar gráficos**
   - A vs k para diferentes valores de f
   - A vs f para diferentes valores de k
   - Comparación de componentes
   - Límites teóricos

6. **Información teórica**
   - Explicación detallada de la Ley de Amdahl
   - Fórmulas y conceptos clave

## 📊 Resolución del Problema (Grupos Pares)

### Resultados Esperados:

1. **Aceleraciones por componente:**
   - Núcleos CUDA: ~1.3889x
   - Memoria VRAM: ~1.1765x  
   - Unidades Texturizado: ~1.2658x
   - NVLink: ~1.1905x

2. **Tiempo renderizado optimizado (Núcleos CUDA):**
   - Original: 50ms
   - Optimizado: ~36ms
   - Mejora: ~28%

3. **Componente para ≥30% aceleración:**
   - Ningún componente individual logra 30% (1.3x)
   - El mejor es Núcleos CUDA con ~38.9%

## 🧪 Pruebas

Ejecutar tests unitarios:

```bash
# Test básico sin pytest
python tests/test_componentes_gpu.py

# Con pytest (si está instalado)
pytest tests/
```

## 📈 Gráficos Generados

La aplicación genera automáticamente:
- `aceleracion_vs_factor.png`: A vs k para f=0.25 y f=0.35
- `aceleracion_vs_porcentaje.png`: A vs f para diferentes k
- `comparacion_componentes.png`: Comparación de componentes GPU
- `limite_teorico.png`: Límite teórico de Amdahl

## 🔧 Dependencias

- **numpy**: Cálculos numéricos avanzados
- **matplotlib**: Generación de gráficos profesionales
- **customtkinter**: Interfaz gráfica moderna
- **pillow**: Procesamiento de imágenes para GUI
- **pydantic**: Validación de datos (opcional)
- **pytest**: Pruebas unitarias (opcional)

## 💡 Características Técnicas

### ✅ Principios de Clean Architecture
- **Separación de responsabilidades**
- **Inversión de dependencias**
- **Independencia de frameworks**
- **Testeable y mantenible**

### ✅ Funcionalidades Avanzadas
- **Validación automática de datos**
- **Cálculo de límites teóricos**
- **Análisis comparativo inteligente**
- **Interfaz de usuario intuitiva**
- **Generación de gráficos profesionales**

### ✅ Manejo de Errores
- **Validaciones de entrada**
- **Mensajes de error claros**
- **Recuperación graceful de errores**

## 📝 Ejemplo de Uso

```python
# Crear componente personalizado
from src.domain.entities import ComponenteGPU
from src.infrastructure.calculador_amdahl import CalculadorAmdahl

componente = ComponenteGPU("Mi Componente", 0.4, 6)
calculador = CalculadorAmdahl()

aceleracion = calculador.calcular_aceleracion(componente)
limite = calculador.calcular_limite_teorico(componente)

print(f"Aceleración: {aceleracion:.4f}x")
print(f"Límite teórico: {limite:.4f}x")
```

## 🎓 Contexto Académico

- **Materia**: MAT1186 - Introducción al Cálculo
- **Proyecto**: EID2 - Evaluación Integral de Desempeño  
- **Tema**: Ley de Amdahl en optimización de sistemas GPU
- **Enfoque**: Grupos pares (optimización GPU vs CPU)

## 👨‍💻 Arquitectura del Software

Este proyecto demuestra:
- **Diseño orientado al dominio (DDD)**
- **Principios SOLID**
- **Patrón Repository (interfaces)**
- **Casos de uso claramente definidos**
- **Separación de capas lógicas**

¡Perfecto para aprender tanto matemáticas aplicadas como desarrollo de software profesional! 🚀
