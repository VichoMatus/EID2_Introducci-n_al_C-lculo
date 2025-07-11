import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from typing import List, Optional

from ..domain.entities import ComponenteGPU, ResultadoAmdahl
from ..application.use_cases import (
    ResolverProblemaGPUUseCase,
    CalcularAceleracionUseCase,
    CargarComponentesPredefinidosUseCase,
    AnalizarComponentesUseCase
)
from ..infrastructure.calculador_amdahl import CalculadorAmdahl
from ..infrastructure.analizador_componentes import AnalizadorComponentes
from ..infrastructure.visualizador_matplotlib import VisualizadorMatplotlib


class AmdahlGUIApp:
    """Aplicación principal con interfaz gráfica"""
    
    def __init__(self):
        # Configurar CustomTkinter
        ctk.set_appearance_mode("dark")  # "light" o "dark"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
        
        # Ventana principal
        self.root = ctk.CTk()
        self.root.title("Calculadora Ley de Amdahl - Optimización GPU")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Dependencias
        self.calculador = CalculadorAmdahl()
        self.analizador = AnalizadorComponentes(self.calculador)
        self.visualizador = VisualizadorMatplotlib()
        
        # Casos de uso
        self.cargar_componentes = CargarComponentesPredefinidosUseCase()
        self.calcular_aceleracion = CalcularAceleracionUseCase(self.calculador)
        self.analizar_componentes = AnalizarComponentesUseCase(self.analizador)
        
        # Variables
        self.componentes_usuario: List[ComponenteGPU] = []
        self.resultados_actuales: List[ResultadoAmdahl] = []
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Cargar componentes predefinidos al inicio
        self.cargar_componentes_predefinidos()
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica principal"""
        # Configurar grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Panel lateral izquierdo (controles)
        self.crear_panel_controles()
        
        # Panel principal derecho (resultados y gráficos)
        self.crear_panel_principal()
        
        # Barra de estado
        self.crear_barra_estado()
    
    def crear_panel_controles(self):
        # Frame principal izquierdo
        self.frame_controles = ctk.CTkFrame(self.root, width=350)
        self.frame_controles.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")
        self.frame_controles.grid_propagate(False)
        
        # Título
        titulo = ctk.CTkLabel(
            self.frame_controles, 
            text="🎯 Ley de Amdahl - GPU", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        titulo.pack(pady=(20, 10))
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(
            self.frame_controles, 
            text="Optimización de Componentes", 
            font=ctk.CTkFont(size=14)
        )
        subtitulo.pack(pady=(0, 20))
        
        # Sección: Problema Predefinido
        self.crear_seccion_predefinido()
        
        # Sección: Componente Personalizado
        self.crear_seccion_personalizado()
        
        # Sección: Gráficos
        self.crear_seccion_graficos()
        
        # Sección: Análisis
        self.crear_seccion_analisis()
    
    def crear_seccion_predefinido(self):
        # Marco
        frame_pred = ctk.CTkFrame(self.frame_controles)
        frame_pred.pack(fill="x", padx=10, pady=(0, 15))
        
        # Título sección
        ctk.CTkLabel(
            frame_pred, 
            text="📊 Problema GPU (Grupo Par)", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # Botón resolver problema completo
        self.btn_resolver = ctk.CTkButton(
            frame_pred,
            text="🚀 Resolver Problema Completo",
            command=self.resolver_problema_completo,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_resolver.pack(pady=(0, 10), padx=15, fill="x")
        
        # Botón mostrar componentes
        self.btn_mostrar_comp = ctk.CTkButton(
            frame_pred,
            text="📋 Mostrar Componentes",
            command=self.mostrar_componentes_predefinidos,
            height=35
        )
        self.btn_mostrar_comp.pack(pady=(0, 15), padx=15, fill="x")
    
    def crear_seccion_personalizado(self):
        # Marco
        frame_pers = ctk.CTkFrame(self.frame_controles)
        frame_pers.pack(fill="x", padx=10, pady=(0, 15))
        
        # Título sección
        ctk.CTkLabel(
            frame_pers, 
            text="⚙️ Componente Personalizado", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # Nombre
        ctk.CTkLabel(frame_pers, text="Nombre:").pack(anchor="w", padx=15)
        self.entry_nombre = ctk.CTkEntry(frame_pers, placeholder_text="Ej: Mi Componente")
        self.entry_nombre.pack(fill="x", padx=15, pady=(0, 10))
        
        # Porcentaje mejorable
        ctk.CTkLabel(frame_pers, text="Porcentaje Mejorable (%):").pack(anchor="w", padx=15)
        self.entry_porcentaje = ctk.CTkEntry(frame_pers, placeholder_text="Ej: 25")
        self.entry_porcentaje.pack(fill="x", padx=15, pady=(0, 10))
        
        # Factor de mejora
        ctk.CTkLabel(frame_pers, text="Factor de Mejora (k):").pack(anchor="w", padx=15)
        self.entry_factor = ctk.CTkEntry(frame_pers, placeholder_text="Ej: 5")
        self.entry_factor.pack(fill="x", padx=15, pady=(0, 10))
        
        # Botón calcular
        self.btn_calcular = ctk.CTkButton(
            frame_pers,
            text="📐 Calcular Aceleración",
            command=self.calcular_componente_personalizado,
            height=35
        )
        self.btn_calcular.pack(pady=(0, 15), padx=15, fill="x")
    
    def crear_seccion_graficos(self):
        frame_graf = ctk.CTkFrame(self.frame_controles)
        frame_graf.pack(fill="x", padx=10, pady=(0, 15))
        
        ctk.CTkLabel(
            frame_graf, 
            text="📈 Gráficos", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # Botones de gráficos
        self.btn_graf_avsk = ctk.CTkButton(
            frame_graf,
            text="📊 A vs k (f=0.25, 0.35)",
            command=self.graficar_a_vs_k,
            height=30
        )
        self.btn_graf_avsk.pack(pady=(0, 5), padx=15, fill="x")
        
        self.btn_graf_avsf = ctk.CTkButton(
            frame_graf,
            text="📈 A vs f (k=4, 8)",
            command=self.graficar_a_vs_f,
            height=30
        )
        self.btn_graf_avsf.pack(pady=(0, 5), padx=15, fill="x")
        
        self.btn_graf_comp = ctk.CTkButton(
            frame_graf,
            text="🏆 Comparar Componentes",
            command=self.graficar_comparacion,
            height=30
        )
        self.btn_graf_comp.pack(pady=(0, 15), padx=15, fill="x")
    
    def crear_seccion_analisis(self):
        frame_anal = ctk.CTkFrame(self.frame_controles)
        frame_anal.pack(fill="x", padx=10, pady=(0, 15))
        
        ctk.CTkLabel(
            frame_anal, 
            text="🔍 Análisis", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # Botón analizar últimos 3
        self.btn_analizar = ctk.CTkButton(
            frame_anal,
            text="🎯 Analizar Últimos 3",
            command=self.analizar_ultimos_tres,
            height=35
        )
        self.btn_analizar.pack(pady=(0, 15), padx=15, fill="x")
    
    def crear_panel_principal(self):
        # Frame principal derecho
        self.frame_principal = ctk.CTkFrame(self.root)
        self.frame_principal.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")
        
        # Configurar grid
        self.frame_principal.grid_rowconfigure(1, weight=1)
        self.frame_principal.grid_columnconfigure(0, weight=1)
        
        # Título del panel
        titulo_panel = ctk.CTkLabel(
            self.frame_principal, 
            text="📊 Resultados y Análisis", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        titulo_panel.grid(row=0, column=0, pady=(20, 10))
        
        # Notebook para pestañas
        self.notebook = ctk.CTkTabview(self.frame_principal)
        self.notebook.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # Crear pestañas
        self.crear_pestana_resultados()
        self.crear_pestana_graficos()
        self.crear_pestana_teoria()
    
    def crear_pestana_resultados(self):
        self.tab_resultados = self.notebook.add("📋 Resultados")
        
        # Área de texto para resultados
        self.text_resultados = ctk.CTkTextbox(
            self.tab_resultados,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.text_resultados.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Mensaje inicial
        self.text_resultados.insert("0.0", 
            "🎯 Bienvenido a la Calculadora de Ley de Amdahl\n\n"
            "Seleccione una opción del panel izquierdo para comenzar:\n\n"
            "• 🚀 Resolver Problema Completo: Calcula todas las aceleraciones para GPU\n"
            "• 📋 Mostrar Componentes: Ve los componentes predefinidos\n"
            "• ⚙️ Componente Personalizado: Crea y calcula tu propio componente\n"
            "• 📈 Gráficos: Visualiza las relaciones de Amdahl\n"
            "• 🔍 Análisis: Compara componentes ingresados\n\n"
            "💡 La Ley de Amdahl: A = 1 / ((1-f) + f/k)\n"
            "   Donde A=aceleración, f=fracción mejorable, k=factor de mejora\n"
        )
    
    def crear_pestana_graficos(self):
        self.tab_graficos = self.notebook.add("📈 Gráficos")
        
        # Frame para el gráfico
        self.frame_grafico = ctk.CTkFrame(self.tab_graficos)
        self.frame_grafico.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Label inicial
        self.label_grafico = ctk.CTkLabel(
            self.frame_grafico,
            text="📊 Seleccione un gráfico del panel izquierdo\n\n"
                 "Opciones disponibles:\n"
                 "• A vs k: Aceleración vs Factor de Mejora\n"
                 "• A vs f: Aceleración vs Fracción Mejorable\n"
                 "• Comparación: Barras de componentes GPU",
            font=ctk.CTkFont(size=14)
        )
        self.label_grafico.pack(expand=True)
    
    def crear_pestana_teoria(self):
        self.tab_teoria = self.notebook.add("📚 Teoría")
        
        # Área de texto para teoría
        self.text_teoria = ctk.CTkTextbox(
            self.tab_teoria,
            font=ctk.CTkFont(size=12)
        )
        self.text_teoria.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Contenido teórico
        contenido_teoria = """
📚 LEY DE AMDAHL - FUNDAMENTOS TEÓRICOS

🎯 DEFINICIÓN:
La Ley de Amdahl predice la mejora máxima al optimizar un componente de un sistema.

📐 FÓRMULA PRINCIPAL:
    A = 1 / ((1-f) + f/k)

Donde:
• A: Aceleración obtenida (speedup)
• f: Fracción mejorable del sistema (0 ≤ f ≤ 1)
• k: Factor de mejora del componente (k > 1)

🔄 LÍMITE TEÓRICO:
Cuando k → ∞: A_max = 1/(1-f)

📊 INTERPRETACIÓN:
• f = 0.5 → A_max = 2x (máximo posible)
• f = 0.9 → A_max = 10x (máximo posible)
• La fracción NO mejorable (1-f) limita la aceleración total

🖥️ APLICACIÓN EN GPU (GRUPOS PARES):

🔧 Componentes Analizados:
1. Núcleos CUDA (35%, k=5):
   • Paralelización de cálculos
   • Procesamiento en paralelo masivo

2. Memoria VRAM (20%, k=3):
   • Acceso rápido a datos
   • Ancho de banda de memoria

3. Unidades de Texturizado (25%, k=7):
   • Procesamiento de texturas
   • Filtrado y muestreo

4. Interconexión NVLink (20%, k=10):
   • Comunicación entre GPUs
   • Transferencia de datos

📈 CASOS PRÁCTICOS:

Ejemplo 1: Núcleos CUDA
• f = 0.35, k = 5
• A = 1/((1-0.35) + 0.35/5) = 1/(0.65 + 0.07) = 1/0.72 ≈ 1.39x
• Mejora del 39%

Ejemplo 2: NVLink
• f = 0.20, k = 10
• A = 1/((1-0.20) + 0.20/10) = 1/(0.80 + 0.02) = 1/0.82 ≈ 1.22x
• Solo 22% de mejora a pesar de k=10

💡 CONCLUSIONES CLAVE:

1. La fracción mejorable (f) es MÁS importante que el factor k
2. Optimizar componentes con mayor f da mejores resultados
3. Aumentar k indefinidamente tiene rendimientos decrecientes
4. El límite teórico nunca se puede superar en la práctica

🏭 APLICACIONES INDUSTRIALES:

• Intel: Optimización de instrucciones de punto flotante vs control
• NVIDIA: Balance entre núcleos vs velocidad de memoria
• Google: Optimización de centros de datos (CPU vs red)
• AMD: Diseño de arquitecturas híbridas CPU-GPU

🎓 IMPORTANCIA ACADÉMICA:
La Ley de Amdahl es fundamental para:
• Diseño de sistemas computacionales
• Toma de decisiones en optimización
• Análisis costo-beneficio de mejoras
• Predicción de rendimiento del sistema
"""
        
        self.text_teoria.insert("0.0", contenido_teoria)
    
    def crear_barra_estado(self):
        self.barra_estado = ctk.CTkLabel(
            self.root,
            text="✅ Listo - Seleccione una opción para comenzar",
            font=ctk.CTkFont(size=11)
        )
        self.barra_estado.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 5))
    
    def actualizar_estado(self, mensaje: str):
        self.barra_estado.configure(text=mensaje)
        self.root.update()
    
    def cargar_componentes_predefinidos(self):
        try:
            componentes = self.cargar_componentes.execute()
            self.actualizar_estado(f"✅ Cargados {len(componentes)} componentes predefinidos")
        except Exception as e:
            self.actualizar_estado(f"❌ Error al cargar componentes: {e}")
    
    def resolver_problema_completo(self):
        self.actualizar_estado("🔄 Resolviendo problema completo...")
        
        def resolver():
            try:
                # Resolver problema
                resolver_problema = ResolverProblemaGPUUseCase(
                    self.calculador, self.analizador, self.visualizador
                )
                resultados = resolver_problema.resolver_problema_completo()
                
                # Mostrar resultados en la interfaz
                self.root.after(0, lambda: self.mostrar_resultados_completos(resultados))
                
            except Exception as e:
                self.root.after(0, lambda: self.mostrar_error(f"Error al resolver problema: {e}"))
        
        # Ejecutar en hilo separado para no bloquear la UI
        threading.Thread(target=resolver, daemon=True).start()
    
    def mostrar_resultados_completos(self, resultados: dict):
        try:
            # Limpiar área de resultados
            self.text_resultados.delete("0.0", "end")
            
            # Formatear y mostrar resultados
            output = "🎯 RESULTADOS PROBLEMA COMPLETO - GRUPOS PARES (GPU)\n"
            output += "=" * 60 + "\n\n"
            
            # 1. Aceleraciones por componente
            output += "1️⃣ ACELERACIONES POR COMPONENTE:\n"
            output += "-" * 40 + "\n"
            for resultado in resultados["resultados_aceleracion"]:
                comp = resultado.componente
                output += f"• {comp.nombre}:\n"
                output += f"  - f = {comp.porcentaje_mejora:.1%}, k = {comp.factor_mejora}\n"
                output += f"  - Aceleración: {resultado.aceleracion:.4f}x\n"
                output += f"  - Límite teórico: {resultado.limite_teorico:.4f}x\n\n"
            
            # 2. Tiempo núcleos CUDA
            output += "2️⃣ ANÁLISIS TIEMPO NÚCLEOS CUDA (50ms):\n"
            output += "-" * 40 + "\n"
            tiempo_resultado = resultados["tiempo_nucleos_cuda"]
            output += f"• Tiempo original: {tiempo_resultado.tiempo_original}ms\n"
            output += f"• Tiempo optimizado: {tiempo_resultado.tiempo_optimizado:.2f}ms\n"
            output += f"• Mejora total: {tiempo_resultado.porcentaje_mejora_total:.1f}%\n\n"
            
            # 3. Componente para 30% aceleración
            output += "3️⃣ COMPONENTE PARA ≥30% ACELERACIÓN:\n"
            output += "-" * 40 + "\n"
            comp_30 = resultados["componente_30_porciento"]
            if comp_30:
                aceleracion_30 = self.calculador.calcular_aceleracion(comp_30)
                output += f"✅ {comp_30.nombre}: {aceleracion_30:.4f}x (≥ 1.30x)\n\n"
            else:
                output += "❌ Ningún componente individual logra ≥30% de aceleración\n\n"
            
            # 4. Mejor componente
            output += "4️⃣ ANÁLISIS COMPARATIVO:\n"
            output += "-" * 40 + "\n"
            analisis = resultados["analisis_comparativo"]
            output += f"🏆 Mejor componente: {analisis.mejor_componente.nombre}\n\n"
            output += "📊 Ranking de aceleraciones:\n"
            for i, (nombre, aceleracion) in enumerate(analisis.obtener_ranking(), 1):
                emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
                output += f"   {emoji} {i}. {nombre}: {aceleracion:.4f}x\n"
            
            # 5. Explicación NVLink
            output += "\n5️⃣ LIMITACIÓN DE NVLINK:\n"
            output += "-" * 40 + "\n"
            output += resultados["explicacion_nvlink"] + "\n\n"
            
            # 6. Comparación texturizado vs VRAM
            output += "6️⃣ TEXTURIZADO vs MEMORIA VRAM:\n"
            output += "-" * 40 + "\n"
            comparacion = resultados["comparacion_texturizado_vs_vram"]
            tex_data = comparacion["texturizado"]
            vram_data = comparacion["vram"]
            output += f"• Unidades de Texturizado: {tex_data['aceleracion']:.4f}x\n"
            output += f"• Memoria VRAM: {vram_data['aceleracion']:.4f}x\n"
            output += f"• Mejor opción: {comparacion['mejor'].upper()}\n"
            output += f"• Diferencia: {comparacion['diferencia']:.4f}x\n\n"
            
            output += "✅ Análisis completo finalizado"
            
            # Mostrar en el área de texto
            self.text_resultados.insert("0.0", output)
            
            # Cambiar a pestaña de resultados
            self.notebook.set("📋 Resultados")
            
            self.actualizar_estado("✅ Problema completo resuelto exitosamente")
            
        except Exception as e:
            self.mostrar_error(f"Error al mostrar resultados: {e}")
    
    def mostrar_componentes_predefinidos(self):
        try:
            self.actualizar_estado("📋 Mostrando componentes predefinidos...")
            
            componentes = self.cargar_componentes.execute()
            
            # Limpiar y mostrar
            self.text_resultados.delete("0.0", "end")
            
            output = "📋 COMPONENTES GPU PREDEFINIDOS (GRUPOS PARES)\n"
            output += "=" * 50 + "\n\n"
            
            for i, componente in enumerate(componentes, 1):
                resultado = self.calcular_aceleracion.execute(componente)
                
                output += f"{i}. {componente.nombre}\n"
                output += "-" * 30 + "\n"
                output += f"   • Porcentaje mejorable (f): {componente.porcentaje_mejora:.1%}\n"
                output += f"   • Factor de mejora (k): {componente.factor_mejora}\n"
                output += f"   • Aceleración obtenida: {resultado.aceleracion:.4f}x\n"
                output += f"   • Límite teórico: {resultado.limite_teorico:.4f}x\n"
                output += f"   • Eficiencia: {(resultado.aceleracion/resultado.limite_teorico)*100:.1f}%\n\n"
            
            self.text_resultados.insert("0.0", output)
            self.notebook.set("📋 Resultados")
            
            self.actualizar_estado("✅ Componentes predefinidos mostrados")
            
        except Exception as e:
            self.mostrar_error(f"Error al mostrar componentes: {e}")
    
    def calcular_componente_personalizado(self):
        try:
            # Obtener datos del formulario
            nombre = self.entry_nombre.get().strip()
            porcentaje_str = self.entry_porcentaje.get().strip()
            factor_str = self.entry_factor.get().strip()
            
            # Validaciones
            if not nombre:
                messagebox.showerror("Error", "El nombre del componente no puede estar vacío")
                return
            
            try:
                porcentaje = float(porcentaje_str) / 100
                factor = float(factor_str)
            except ValueError:
                messagebox.showerror("Error", "Porcentaje y factor deben ser números válidos")
                return
            
            # Crear componente
            componente = ComponenteGPU(nombre, porcentaje, factor)
            
            # Calcular
            resultado = self.calcular_aceleracion.execute(componente)
            
            # Agregar a lista de usuario
            self.componentes_usuario.append(componente)
            
            # Mostrar resultado
            self.text_resultados.delete("0.0", "end")
            
            output = f"⚙️ COMPONENTE PERSONALIZADO: {nombre}\n"
            output += "=" * 50 + "\n\n"
            output += f"📊 PARÁMETROS:\n"
            output += f"• Fracción mejorable (f): {porcentaje:.1%}\n"
            output += f"• Factor de mejora (k): {factor}\n\n"
            output += f"📈 RESULTADOS:\n"
            output += f"• Aceleración obtenida: {resultado.aceleracion:.4f}x\n"
            output += f"• Límite teórico (k→∞): {resultado.limite_teorico:.4f}x\n"
            output += f"• Eficiencia actual: {(resultado.aceleracion/resultado.limite_teorico)*100:.1f}%\n"
            output += f"• Mejora de rendimiento: {(resultado.aceleracion-1)*100:.1f}%\n\n"
            
            # Análisis adicional
            if resultado.aceleracion >= 1.3:
                output += "✅ ¡Excelente! Logra más del 30% de aceleración\n"
            elif resultado.aceleracion >= 1.2:
                output += "✅ Buena aceleración (20-30%)\n"
            elif resultado.aceleracion >= 1.1:
                output += "⚠️  Aceleración moderada (10-20%)\n"
            else:
                output += "❌ Aceleración baja (<10%)\n"
            
            output += f"\n📝 Total de componentes ingresados: {len(self.componentes_usuario)}\n"
            output += "(Use 'Analizar Últimos 3' para comparar con otros componentes)"
            
            self.text_resultados.insert("0.0", output)
            self.notebook.set("📋 Resultados")
            
            # Limpiar formulario
            self.entry_nombre.delete(0, "end")
            self.entry_porcentaje.delete(0, "end")
            self.entry_factor.delete(0, "end")
            
            self.actualizar_estado(f"✅ Componente '{nombre}' calculado: {resultado.aceleracion:.4f}x")
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            self.mostrar_error(f"Error al calcular componente: {e}")
    
    def analizar_ultimos_tres(self):
        try:
            if len(self.componentes_usuario) == 0:
                messagebox.showwarning(
                    "Sin Componentes", 
                    "No hay componentes personalizados ingresados.\n\n"
                    "Primero agregue algunos componentes usando la sección 'Componente Personalizado'."
                )
                return
            
            self.actualizar_estado("🔍 Analizando últimos componentes...")
            
            # Analizar
            analisis = self.analizar_componentes.analizar_ultimos_tres_componentes(
                self.componentes_usuario
            )
            
            # Mostrar resultados
            self.text_resultados.delete("0.0", "end")
            
            ultimos_tres = self.componentes_usuario[-3:]
            
            output = f"🔍 ANÁLISIS ÚLTIMOS {len(ultimos_tres)} COMPONENTE(S)\n"
            output += "=" * 50 + "\n\n"
            output += f"📝 Total de componentes ingresados: {len(self.componentes_usuario)}\n\n"
            
            output += "📊 COMPONENTES ANALIZADOS:\n"
            output += "-" * 30 + "\n"
            for i, componente in enumerate(ultimos_tres, 1):
                resultado = next(r for r in analisis.resultados if r.componente == componente)
                output += f"{i}. {componente.nombre}\n"
                output += f"   • f={componente.porcentaje_mejora:.1%}, k={componente.factor_mejora}\n"
                output += f"   • Aceleración: {resultado.aceleracion:.4f}x\n\n"
            
            output += f"🏆 MEJOR OPCIÓN: {analisis.mejor_componente.nombre}\n\n"
            
            output += "📊 RANKING DE ACELERACIONES:\n"
            output += "-" * 30 + "\n"
            for i, (nombre, aceleracion) in enumerate(analisis.obtener_ranking(), 1):
                emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
                output += f"   {emoji} {i}. {nombre}: {aceleracion:.4f}x\n"
            
            output += f"\n📋 JUSTIFICACIÓN TÉCNICA:\n"
            output += "-" * 30 + "\n"
            output += analisis.justificacion
            
            self.text_resultados.insert("0.0", output)
            self.notebook.set("📋 Resultados")
            
            self.actualizar_estado("✅ Análisis de componentes completado")
            
        except Exception as e:
            self.mostrar_error(f"Error al analizar componentes: {e}")
    
    def graficar_a_vs_k(self):
        try:
            self.actualizar_estado("📊 Generando gráfico A vs k...")
            
            # Crear figura
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Datos
            k_values = np.arange(1, 21)
            f_values = [0.25, 0.35]
            
            for f in f_values:
                a_values = [self.calculador.calcular_aceleracion_con_parametros(f, k) for k in k_values]
                ax.plot(k_values, a_values, marker='o', linewidth=2, 
                       label=f'f = {f:.2f}', markersize=4)
            
            ax.set_xlabel('Factor de Mejora (k)', fontsize=12)
            ax.set_ylabel('Aceleración (A)', fontsize=12)
            ax.set_title('Ley de Amdahl: Aceleración vs Factor de Mejora', 
                        fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=11)
            ax.axhline(y=1, color='red', linestyle='--', alpha=0.5)
            
            # Mostrar en interfaz
            self.mostrar_grafico_en_interfaz(fig)
            
            self.actualizar_estado("✅ Gráfico A vs k generado")
            
        except Exception as e:
            self.mostrar_error(f"Error al generar gráfico A vs k: {e}")
    
    def graficar_a_vs_f(self):
        try:
            self.actualizar_estado("📈 Generando gráfico A vs f...")
            
            # Crear figura
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Datos
            f_values = np.arange(0.05, 0.96, 0.05)
            k_values = [4, 8]
            
            for k in k_values:
                a_values = [self.calculador.calcular_aceleracion_con_parametros(f, k) for f in f_values]
                ax.plot(f_values, a_values, marker='s', linewidth=2, 
                       label=f'k = {k}', markersize=4)
            
            ax.set_xlabel('Fracción Mejorable (f)', fontsize=12)
            ax.set_ylabel('Aceleración (A)', fontsize=12)
            ax.set_title('Ley de Amdahl: Aceleración vs Fracción Mejorable', 
                        fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=11)
            ax.axhline(y=1, color='red', linestyle='--', alpha=0.5)
            
            # Mostrar en interfaz
            self.mostrar_grafico_en_interfaz(fig)
            
            self.actualizar_estado("✅ Gráfico A vs f generado")
            
        except Exception as e:
            self.mostrar_error(f"Error al generar gráfico A vs f: {e}")
    
    def graficar_comparacion(self):
        try:
            self.actualizar_estado("🏆 Generando comparación de componentes...")
            
            # Obtener componentes
            componentes = self.cargar_componentes.execute()
            
            # Crear figura
            fig, ax = plt.subplots(figsize=(12, 6))
            
            nombres = [comp.nombre for comp in componentes]
            aceleraciones = [self.calculador.calcular_aceleracion(comp) for comp in componentes]
            
            # Crear gráfico de barras
            colores = plt.cm.viridis(np.linspace(0, 1, len(nombres)))
            barras = ax.bar(nombres, aceleraciones, color=colores, alpha=0.8)
            
            # Añadir valores sobre las barras
            for barra, aceleracion in zip(barras, aceleraciones):
                altura = barra.get_height()
                ax.text(barra.get_x() + barra.get_width()/2., altura + 0.01,
                       f'{aceleracion:.4f}x', ha='center', va='bottom', fontweight='bold')
            
            ax.set_xlabel('Componentes GPU', fontsize=12)
            ax.set_ylabel('Aceleración', fontsize=12)
            ax.set_title('Comparación de Aceleraciones por Componente GPU', 
                        fontsize=14, fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            ax.grid(True, alpha=0.3, axis='y')
            
            # Mostrar en interfaz
            self.mostrar_grafico_en_interfaz(fig)
            
            self.actualizar_estado("✅ Comparación de componentes generada")
            
        except Exception as e:
            self.mostrar_error(f"Error al generar comparación: {e}")
    
    def mostrar_grafico_en_interfaz(self, fig):
        try:
            # Limpiar frame de gráfico
            for widget in self.frame_grafico.winfo_children():
                widget.destroy()
            
            # Crear canvas para matplotlib
            canvas = FigureCanvasTkAgg(fig, self.frame_grafico)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
            # Cambiar a pestaña de gráficos
            self.notebook.set("📈 Gráficos")
            
            plt.close(fig)  # Cerrar figura para liberar memoria
            
        except Exception as e:
            self.mostrar_error(f"Error al mostrar gráfico: {e}")
    
    def mostrar_error(self, mensaje: str):
        messagebox.showerror("Error", mensaje)
        self.actualizar_estado(f"❌ {mensaje}")
    
    def ejecutar(self):
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Error crítico en la aplicación: {e}")


def main():
    try:
        app = AmdahlGUIApp()
        app.ejecutar()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")


if __name__ == "__main__":
    main()
