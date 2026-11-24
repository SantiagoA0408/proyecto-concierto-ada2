"""
Modulo de interfaz grafica de usuario (GUI) con Tkinter.
ADA II - Universidad del Valle

Este modulo implementa la ventana de la aplicacion que permite:
1. Escribir o pegar la entrada del problema (N, M y ciudades).
2. Cargar ejemplos predefinidos o desde un archivo .txt.
3. Validar los datos y generar el codigo fuente de MiniZinc correspondiente.
4. Visualizar y copiar el codigo MiniZinc al portapapeles para llevarlo al IDE de MiniZinc.

IMPORTANTE (Restricciones del Enunciado):
- NO resuelve el problema en Python (no calcula coordenadas finales del concierto).
- NO dibuja planos cartesianos ni mapas en la GUI.
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from parser_entrada import parsear_entrada, ErrorEntrada
from generador_minizinc import generar_codigo_minizinc


# Texto del ejemplo oficial del enunciado para precargar o restaurar facilmente
EJEMPLO_POR_DEFECTO = """12
5
Palmira 2 3
Cali 10 2
Buga 11 0
Tulua 0 3
RioFrio 1 2"""

EJEMPLO_NOMBRES_COMPUESTOS = """10
4
La Union 1 9
Cali 3 9
Tulua 2 7
San Pedro 1 4"""


class AplicacionConcierto:
    """
    Clase principal que gestiona la ventana y los componentes graficos.
    """

    def __init__(self, ventana_raiz: tk.Tk):
        """
        Inicializa la ventana principal y todos los widgets.
        """
        self.raiz = ventana_raiz
        self.raiz.title("ADA II - Optimizacion: ¿Donde pongo mi concierto?")
        self.raiz.geometry("980x740")
        self.raiz.minsize(800, 600)

        # Configuracion general de estilos
        self._configurar_estilos()

        # Construccion de la interfaz
        self._crear_encabezado()
        self._crear_paneles_principales()
        self._crear_barra_estado()

        # Precargar el ejemplo del enunciado al iniciar
        self.cargar_ejemplo(EJEMPLO_POR_DEFECTO)

    def _configurar_estilos(self):
        """
        Configura fuentes y colores sencillos y legibles.
        """
        self.fuente_titulo = ("Helvetica", 14, "bold")
        self.fuente_subtitulo = ("Helvetica", 10)
        self.fuente_etiquetas = ("Helvetica", 10, "bold")
        self.fuente_codigo = ("Courier New", 10)
        self.fuente_botones = ("Helvetica", 10)

    def _crear_encabezado(self):
        """
        Crea el marco superior con el titulo y la explicacion del problema.
        """
        frame_header = ttk.Frame(self.raiz, padding="10")
        frame_header.pack(fill=tk.X)

        lbl_titulo = ttk.Label(
            frame_header,
            text="Optimizacion: ¿Donde pongo mi concierto?",
            font=self.fuente_titulo,
            foreground="#1a365d"
        )
        lbl_titulo.pack(anchor=tk.W)

        lbl_descripcion = ttk.Label(
            frame_header,
            text="Herramienta para generar el modelo MiniZinc de localizacion equitativa "
                 "con distancia Manhattan en el Valle del Cauca.\n"
                 "Ingresa los datos o carga un ejemplo, presiona 'Solucionar problema' y copia el modelo generado a MiniZinc IDE.",
            font=self.fuente_subtitulo,
            foreground="#4a5568"
        )
        lbl_descripcion.pack(anchor=tk.W, pady=(4, 0))

    def _crear_paneles_principales(self):
        """
        Crea el cuerpo central con dos areas de texto:
        - Panel superior/izquierdo: Entrada de datos.
        - Boton de accion central.
        - Panel inferior/derecho: Salida de MiniZinc.
        """
        frame_cuerpo = ttk.Frame(self.raiz, padding="10")
        frame_cuerpo.pack(fill=tk.BOTH, expand=True)

        # -------------------------------------------------------------
        # 1. Panel de Entrada
        # -------------------------------------------------------------
        frame_entrada = ttk.LabelFrame(
            frame_cuerpo,
            text=" 1. Datos de Entrada (N, M y Coordenadas de Ciudades) ",
            padding="8"
        )
        frame_entrada.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

        lbl_guia_formato = ttk.Label(
            frame_entrada,
            text="Formato esperado: Linea 1: N (tamano) | Linea 2: M (ciudades) | Lineas 3+: NombreCiudad X Y",
            font=("Helvetica", 9, "italic"),
            foreground="#2d3748"
        )
        lbl_guia_formato.pack(anchor=tk.W, pady=(0, 4))

        # Area de texto de entrada con barra de desplazamiento
        frame_txt_in = ttk.Frame(frame_entrada)
        frame_txt_in.pack(fill=tk.BOTH, expand=True)

        scroll_in = ttk.Scrollbar(frame_txt_in, orient=tk.VERTICAL)
        self.txt_entrada = tk.Text(
            frame_txt_in,
            wrap=tk.WORD,
            yscrollcommand=scroll_in.set,
            font=self.fuente_codigo,
            height=7
        )
        scroll_in.config(command=self.txt_entrada.yview)
        scroll_in.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_entrada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Botonera para el area de entrada
        frame_botones_in = ttk.Frame(frame_entrada, padding="4")
        frame_botones_in.pack(fill=tk.X, pady=(4, 0))

        btn_ejemplo1 = ttk.Button(
            frame_botones_in,
            text="Ejemplo Enunciado (N=12)",
            command=lambda: self.cargar_ejemplo(EJEMPLO_POR_DEFECTO)
        )
        btn_ejemplo1.pack(side=tk.LEFT, padx=3)

        btn_ejemplo2 = ttk.Button(
            frame_botones_in,
            text="Ejemplo Nombres Compuestos",
            command=lambda: self.cargar_ejemplo(EJEMPLO_NOMBRES_COMPUESTOS)
        )
        btn_ejemplo2.pack(side=tk.LEFT, padx=3)

        btn_cargar_archivo = ttk.Button(
            frame_botones_in,
            text="Cargar Archivo .txt...",
            command=self.cargar_desde_archivo
        )
        btn_cargar_archivo.pack(side=tk.LEFT, padx=3)

        btn_limpiar_in = ttk.Button(
            frame_botones_in,
            text="Limpiar Entrada",
            command=self.limpiar_entrada
        )
        btn_limpiar_in.pack(side=tk.RIGHT, padx=3)

        # -------------------------------------------------------------
        # 2. Boton Principal de Accion: "Solucionar problema"
        # -------------------------------------------------------------
        frame_accion = ttk.Frame(frame_cuerpo, padding="4")
        frame_accion.pack(fill=tk.X, pady=4)

        self.btn_solucionar = tk.Button(
            frame_accion,
            text="▶ Solucionar problema (Generar Codigo MiniZinc)",
            command=self.solucionar_problema,
            font=("Helvetica", 11, "bold"),
            bg="#2b6cb0",
            fg="white",
            activebackground="#2c5282",
            activeforeground="white",
            padx=12,
            pady=6,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.btn_solucionar.pack(fill=tk.X)

        # -------------------------------------------------------------
        # 3. Panel de Salida: Codigo MiniZinc Generado
        # -------------------------------------------------------------
        frame_salida = ttk.LabelFrame(
            frame_cuerpo,
            text=" 2. Codigo MiniZinc Generado (.mzn) ",
            padding="8"
        )
        frame_salida.pack(fill=tk.BOTH, expand=True, pady=(6, 0))

        lbl_guia_salida = ttk.Label(
            frame_salida,
            text="Este codigo contiene el modelo matematico formal, restricciones y funcion objetivo listo para MiniZinc IDE.",
            font=("Helvetica", 9, "italic"),
            foreground="#2d3748"
        )
        lbl_guia_salida.pack(anchor=tk.W, pady=(0, 4))

        # Area de texto de salida con barra de desplazamiento
        frame_txt_out = ttk.Frame(frame_salida)
        frame_txt_out.pack(fill=tk.BOTH, expand=True)

        scroll_out = ttk.Scrollbar(frame_txt_out, orient=tk.VERTICAL)
        self.txt_salida = tk.Text(
            frame_txt_out,
            wrap=tk.WORD,
            yscrollcommand=scroll_out.set,
            font=self.fuente_codigo,
            height=12,
            bg="#f7fafc"
        )
        scroll_out.config(command=self.txt_salida.yview)
        scroll_out.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_salida.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Botonera para el area de salida
        frame_botones_out = ttk.Frame(frame_salida, padding="4")
        frame_botones_out.pack(fill=tk.X, pady=(4, 0))

        btn_copiar = tk.Button(
            frame_botones_out,
            text="📋 Copiar codigo MiniZinc",
            command=self.copiar_codigo,
            font=self.fuente_botones,
            bg="#38a169",
            fg="white",
            activebackground="#276749",
            activeforeground="white",
            padx=8,
            pady=3,
            cursor="hand2"
        )
        btn_copiar.pack(side=tk.LEFT, padx=3)

        btn_guardar_mzn = ttk.Button(
            frame_botones_out,
            text="💾 Guardar como archivo .mzn...",
            command=self.guardar_archivo_mzn
        )
        btn_guardar_mzn.pack(side=tk.LEFT, padx=3)

        btn_limpiar_out = ttk.Button(
            frame_botones_out,
            text="Limpiar Salida",
            command=self.limpiar_salida
        )
        btn_limpiar_out.pack(side=tk.RIGHT, padx=3)

    def _crear_barra_estado(self):
        """
        Crea una barra de estado inferior para informar al usuario de las operaciones.
        """
        self.lbl_estado = ttk.Label(
            self.raiz,
            text="Estado: Listo.",
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding="4"
        )
        self.lbl_estado.pack(side=tk.BOTTOM, fill=tk.X)

    # -----------------------------------------------------------------
    # Metodos de Interaccion y Logica de la GUI
    # -----------------------------------------------------------------

    def cargar_ejemplo(self, texto_ejemplo: str):
        """
        Carga un texto de ejemplo en el TextArea de entrada.
        """
        self.txt_entrada.delete("1.0", tk.END)
        self.txt_entrada.insert(tk.END, texto_ejemplo.strip() + "\n")
        self.lbl_estado.config(text="Estado: Ejemplo cargado en el area de entrada.")

    def limpiar_entrada(self):
        """
        Limpia el contenido del TextArea de entrada.
        """
        self.txt_entrada.delete("1.0", tk.END)
        self.lbl_estado.config(text="Estado: Area de entrada vaciada.")

    def limpiar_salida(self):
        """
        Limpia el contenido del TextArea de salida.
        """
        self.txt_salida.delete("1.0", tk.END)
        self.lbl_estado.config(text="Estado: Area de salida vaciada.")

    def cargar_desde_archivo(self):
        """
        Permite seleccionar un archivo de texto .txt y carga su contenido en la entrada.
        """
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de entrada",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if ruta_archivo:
            try:
                with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                    contenido = archivo.read()
                self.cargar_ejemplo(contenido)
                nombre_base = os.path.basename(ruta_archivo)
                self.lbl_estado.config(text=f"Estado: Archivo '{nombre_base}' cargado correctamente.")
            except Exception as e:
                messagebox.showerror(
                    "Error al leer archivo",
                    f"No se pudo leer el archivo seleccionado:\n{str(e)}"
                )

    def solucionar_problema(self):
        """
        Accion principal del boton 'Solucionar problema'.
        1. Lee el contenido del TextArea de entrada.
        2. Llama a parsear_entrada(...) para validar los datos.
        3. Si la entrada es valida, llama a generar_codigo_minizinc(...)
           y muestra el codigo en el TextArea de salida.
        4. Si hay algun error, muestra una ventana de alerta amigable.
        """
        texto_ingresado = self.txt_entrada.get("1.0", tk.END)

        try:
            # Validar y estructurar datos de entrada
            datos = parsear_entrada(texto_ingresado)

            # Generar el modelo MiniZinc
            codigo_mzn = generar_codigo_minizinc(
                datos["N"],
                datos["M"],
                datos["ciudades"]
            )

            # Mostrar en el TextArea de salida
            self.txt_salida.delete("1.0", tk.END)
            self.txt_salida.insert(tk.END, codigo_mzn)

            self.lbl_estado.config(
                text=f"Estado: ¡Exito! Codigo MiniZinc generado para N={datos['N']} y M={datos['M']} ciudades."
            )

        except ErrorEntrada as error:
            # Error de formato o validacion de restricciones de entrada
            messagebox.showerror("Error en los datos de entrada", str(error))
            self.lbl_estado.config(text="Estado: Error de validacion en la entrada.")

        except Exception as error_inesperado:
            # Error imprevisto
            messagebox.showerror(
                "Error inesperado",
                f"Ocurrio un error imprevisto al procesar los datos:\n{str(error_inesperado)}"
            )
            self.lbl_estado.config(text="Estado: Ocurrio un error imprevisto.")

    def copiar_codigo(self):
        """
        Copia el codigo del TextArea de salida al portapapeles del sistema operativo.
        """
        codigo = self.txt_salida.get("1.0", tk.END).strip()
        if not codigo:
            messagebox.showwarning(
                "Salida vacia",
                "No hay codigo generado para copiar. Primero presiona 'Solucionar problema'."
            )
            return

        self.raiz.clipboard_clear()
        self.raiz.clipboard_append(codigo)
        self.raiz.update()  # Necesario en algunos sistemas para asegurar que se guarde en clipboard

        messagebox.showinfo(
            "Copiado al portapapeles",
            "¡El codigo MiniZinc ha sido copiado al portapapeles!\n"
            "Ya puedes pegarlo (Ctrl+V) en MiniZinc IDE para resolverlo."
        )
        self.lbl_estado.config(text="Estado: Codigo MiniZinc copiado al portapapeles.")

    def guardar_archivo_mzn(self):
        """
        Permite guardar el codigo generado directamente en un archivo .mzn.
        """
        codigo = self.txt_salida.get("1.0", tk.END).strip()
        if not codigo:
            messagebox.showwarning(
                "Salida vacia",
                "No hay codigo para guardar. Primero presiona 'Solucionar problema'."
            )
            return

        ruta_destino = filedialog.asksaveasfilename(
            title="Guardar modelo MiniZinc",
            defaultextension=".mzn",
            filetypes=[("Archivos MiniZinc", "*.mzn"), ("Todos los archivos", "*.*")]
        )
        if ruta_destino:
            try:
                with open(ruta_destino, "w", encoding="utf-8") as archivo:
                    archivo.write(codigo + "\n")
                messagebox.showinfo(
                    "Archivo guardado",
                    f"El archivo se guardo exitosamente en:\n{ruta_destino}"
                )
                self.lbl_estado.config(text=f"Estado: Archivo guardado como '{os.path.basename(ruta_destino)}'.")
            except Exception as e:
                messagebox.showerror(
                    "Error al guardar archivo",
                    f"No se pudo guardar el archivo:\n{str(e)}"
                )


def iniciar_interfaz():
    """
    Funcion que inicializa la ventana de Tkinter y lanza el bucle de eventos.
    """
    ventana = tk.Tk()
    app = AplicacionConcierto(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    iniciar_interfaz()
