# Proyecto 2 - Optimización: "¿Dónde pongo mi concierto?"
**Curso:** Análisis y Diseño de Algoritmos II (ADA II)  
**Profesor:** Miguel Ángel Askar Rodríguez, Mg.  
**Universidad del Valle - Cali, Colombia**

---

## 1. Descripción del Proyecto

La aplicación permite resolver el problema de localización del concierto de *Benito-Bad* en el departamento del Valle del Cauca, modelado como una grilla discreta de tamaño $N \times N$ ($0 \le x \le N$, $0 \le y \le N$).

El programa lee la información de entrada desde una interfaz gráfica sencilla en Tkinter, valida minuciosamente todas las restricciones del problema y genera el modelo formal de programación con restricciones en **MiniZinc (.mzn)** listo para ser resuelto en **MiniZinc IDE**.

> **Nota de diseño ético y de cumplimiento:**
> Conforme al enunciado oficial del curso:
> 1. La aplicación en Python **NO** resuelve el problema internamente (no calcula ni dibuja la posición del concierto). Su función es validar y construir el modelo matemático para MiniZinc.
> 2. La interfaz gráfica **NO** incluye planos cartesianos ni mapas gráficos innecesarios.

---

## 2. Estructura de Archivos

```text
proyecto_concierto/
├── main.py                  # Punto de entrada de la aplicación
├── interfaz.py              # Interfaz gráfica de usuario en Tkinter
├── parser_entrada.py        # Lectura, limpieza y validación exhaustiva de la entrada
├── generador_minizinc.py    # Generador del modelo formal MiniZinc (.mzn) comentado
├── test_parser.py           # Suite de pruebas unitarias para el validador
├── test_generador.py        # Suite de pruebas unitarias para el generador MiniZinc
├── ejemplos/                # Casos de prueba en formato .txt
│   ├── ejemplo_enunciado.txt           # Caso base del enunciado (N=12, M=5)
│   ├── ejemplo_nombres_compuestos.txt  # Ciudades con espacios (La Unión, San Pedro)
│   ├── caso_ciudades_agrupadas.txt     # Ciudades concentradas en un sector
│   └── caso_extremos.txt               # Ciudades situadas en las 4 esquinas del plano
└── README.md                # Documentación del proyecto y guía para sustentación
```

---

## 3. Requisitos y Ejecución

### Requisitos previos
- **Python 3.8+**
- En sistemas Linux (Ubuntu / Debian), asegurarse de contar con `tkinter`:
  ```bash
  sudo apt update && sudo apt install -y python3-tk
  ```
- **MiniZinc IDE** (descargable libremente desde [minizinc.org](https://www.minizinc.org/)).

### Cómo ejecutar la aplicación
Desde la terminal, ubícate en la carpeta del proyecto y ejecuta:

```bash
cd proyecto_concierto
python3 main.py
```

### Ejecutar las pruebas unitarias
```bash
python3 test_parser.py
python3 test_generador.py
```

---

## 4. Guía de Uso de la Interfaz Gráfica

1. **Ingreso de datos:**
   - Escribe o pega en el primer `TextArea` los datos con el formato:
     ```text
     N
     M
     Ciudad_1 X_1 Y_1
     ...
     Ciudad_M X_M Y_M
     ```
   - O bien, usa los botones rápidos:
     - **Ejemplo Enunciado:** Carga el caso del PDF ($N=12, M=5$).
     - **Ejemplo Nombres Compuestos:** Carga el caso con `La Union` y `San Pedro`.
     - **Cargar Archivo .txt...:** Selecciona cualquier archivo de prueba en tu equipo.
2. **Generación del código:**
   - Presiona el botón azul **"▶ Solucionar problema (Generar Código MiniZinc)"**.
   - Si los datos son válidos, el modelo de MiniZinc aparecerá en el segundo `TextArea`. Si hay errores (valores fuera de rango, no enteros, etc.), se mostrará una ventana con el mensaje descriptivo en español.
3. **Resolución en MiniZinc IDE:**
   - Presiona el botón verde **"📋 Copiar código MiniZinc"** (o guárdalo con *"Guardar como archivo .mzn"*).
   - Abre **MiniZinc IDE**, crea un nuevo archivo, pega el código (`Ctrl+V`) y presiona el botón **Run** (con solver Gecode, Chuffed o Coin-BC).
   - MiniZinc mostrará las coordenadas óptimas $(cx, cy)$, la distancia a cada ciudad y las métricas de equidad.

---

## 5. Modelo Matemático Formal (Para el Informe IEEE y Sustentación)

### 5.1. Definición Formal del Problema
- **Plano discreto:** Coordenadas enteras dentro de $[0, N] \times [0, N]$.
- **Entrada:**
  - $N \in \mathbb{Z}^+$: Dimensión del plano.
  - $M \in \mathbb{Z}^+$: Número de ciudades.
  - Posiciones de ciudades: $(x_i, y_i) \in [0, N] \times [0, N]$ para cada $i \in \{1, \dots, M\}$.
- **Variables de Decisión:**
  - $cx, cy \in [0, N]$: Coordenadas enteras del concierto.
  - $d_i \in [0, 2N]$: Distancia Manhattan desde el concierto a la ciudad $i$, dada por:
    $$d_i = |cx - x_i| + |cy - y_i|$$
  - $d_{\text{max}} = \max_{i} (d_i)$: Distancia a la ciudad más alejada (criterio Minimax).
  - $d_{\text{min}} = \min_{i} (d_i)$: Distancia a la ciudad más favorecida.
  - $\Delta = d_{\text{max}} - d_{\text{min}}$: Brecha de inequidad entre los extremos.

### 5.2. Restricciones
1. **No colisión con ciudades:**
   $$\forall i \in \{1, \dots, M\}, \quad (cx \neq x_i) \lor (cy \neq y_i)$$
   Garantiza que el concierto no se ubique directamente sobre ninguna ciudad.
2. **Cálculo de Distancia Manhattan:**
   $$\forall i \in \{1, \dots, M\}, \quad d_i = |cx - x_i| + |cy - y_i|$$
3. **Límites de variables:**
   $$0 \le cx \le N, \quad 0 \le cy \le N, \quad 0 \le d_i \le 2N$$

### 5.3. Función Objetivo: ¿Cómo evitar "favorecer" a una ciudad sobre otra?
Uno de los puntos clave a defender en la sustentación oral es el diseño de la función objetivo:

$$\text{Minimizar } \quad Z = d_{\text{max}} + \Delta = d_{\text{max}} + (d_{\text{max}} - d_{\text{min}})$$

#### Justificación Técnica:
- **¿Por qué NO minimizar únicamente $\Delta = d_{\text{max}} - d_{\text{min}}$?**  
  Si solo se minimiza la brecha, el solver podría enviar el concierto a una esquina extrema lejana fuera del centro geográfico (por ejemplo, a una distancia de 15 km de todas las ciudades). En ese caso, $\Delta = 0$ (perfectamente equitativo), pero todas las ciudades tendrían que viajar distancias absurdas.
- **¿Por qué NO minimizar únicamente $d_{\text{max}}$ o la suma $\sum d_i$?**  
  Minimizar únicamente la suma de distancias puede ubicar el concierto pegado a un grupo de ciudades densamente pobladas (dejándolas a distancia 1), pero perjudicando gravemente a una ciudad lejana aislada (dejándola a distancia 11), lo que generaría un conflicto político entre alcaldes.
- **La solución de compromiso ($d_{\text{max}} + \Delta$):**  
  El término $d_{\text{max}}$ actúa como fuerza de atracción (cercanía global), mientras que $\Delta$ actúa como penalización contra el favoritismo desmedido (equidad).

---

## 6. Análisis de Casos Especiales (Recomendados por el Profesor)

Durante la sustentación se pueden evaluar casos límite:

1. **Ciudades en las 4 esquinas del plano (`caso_extremos.txt`):**
   - Coordenadas: $(0,0)$, $(0,N)$, $(N,0)$, $(N,N)$.
   - *Comportamiento esperado:* Por simetría de la distancia Manhattan, el concierto se sitúa en el centro exacto $(\lfloor N/2 \rfloor, \lfloor N/2 \rfloor)$, donde todas las distancias son idénticas y $\Delta = 0$.
2. **Ciudades alineadas en una sola fila o columna:**
   - En distancia Manhattan unidimensional, la distancia total se minimiza en la **mediana** de las posiciones, pero la equidad ($\Delta$) busca el **punto medio** entre los extremos. El modelo encuentra el balance exacto entre el centroide y los bordes.
3. **Ciudades agrupadas con una ciudad solitaria lejana:**
   - Tres ciudades en un clúster pequeño y una ciudad distante. El término $\Delta$ evita que el concierto se quede dentro del clúster olvidando a la ciudad solitaria, desplazando el concierto hacia un punto intermedio prudente.
4. **Espacio saturado o $N$ muy pequeño:**
   - Si $N=1$ y todas las 4 coordenadas están ocupadas por ciudades, el solver de MiniZinc reportará inmediatamente `=====UNSATISFIABLE=====`, demostrando formalmente que no existe ninguna coordenada entera libre.
