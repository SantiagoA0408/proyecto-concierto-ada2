"""
Modulo generador de codigo MiniZinc.
ADA II - Universidad del Valle

Este modulo se encarga de:
1. Recibir los datos validados del problema (N, M, lista de ciudades).
2. Construir una cadena de texto que contiene un modelo formal de MiniZinc (.mzn).
3. Asegurar que el codigo generado:
   - Sea 100% compatible y ejecutable en MiniZinc IDE (con solvers como Gecode, Coin-BC, Chuffed).
   - Este ampliamente comentado en espanol para facilitar la sustentacion oral ante el profesor.
   - Modele adecuadamente las restricciones del problema (no caer en ciudades, distancia Manhattan).
   - Plantee una funcion objetivo equilibrada (cercania y equidad entre ciudades).
   - Incluya un bloque 'output' amigable y estructurado.
"""


def generar_codigo_minizinc(n: int, m: int, ciudades: list) -> str:
    """
    Genera el script completo de MiniZinc con los parametros inyectados
    a partir de los datos procesados de la entrada.

    Parametros:
        n (int): Tamano del plano cuadrado [0, N] x [0, N].
        m (int): Numero total de ciudades.
        ciudades (list): Lista de diccionarios, donde cada elemento tiene:
                         {'nombre': str, 'x': int, 'y': int}

    Retorna:
        str: Codigo fuente MiniZinc (.mzn) listo para copiar, pegar y ejecutar.
    """
    # 1. Preparar las listas en formato de arreglo MiniZinc
    # Para los nombres, escapamos comillas si existieran por seguridad
    lista_nombres = [f'"{c["nombre"].replace(chr(34), "")}"' for c in ciudades]
    lista_x = [str(c["x"]) for c in ciudades]
    lista_y = [str(c["y"]) for c in ciudades]

    # Convertir a cadenas con formato de arreglo MiniZinc: [item1, item2, ...]
    str_nombres = "[" + ", ".join(lista_nombres) + "]"
    str_x = "[" + ", ".join(lista_x) + "]"
    str_y = "[" + ", ".join(lista_y) + "]"

    # 2. Construir el archivo de MiniZinc con todas sus secciones comentadas
    codigo_mzn = f"""% ==============================================================================
% PROYECTO 2 - ANALISIS Y DISENO DE ALGORITMOS II
% PROBLEMA: ¿Donde pongo mi concierto? (Optimizacion con MiniZinc)
% UNIVERSIDAD DEL VALLE
% ==============================================================================
%
% DESCRIPCION DEL PROBLEMA:
% Se busca ubicar un concierto en una coordenada entera (cx, cy) dentro de un
% plano de dimensiones N x N (donde 0 <= cx <= N y 0 <= cy <= N).
%
% CRITERIOS A CUMPLIR:
% 1. El concierto NO puede coincidir con la ubicacion de ninguna ciudad.
% 2. La distancia entre el concierto y cada ciudad se calcula como distancia
%    Manhattan: d_i = |cx - x_i| + |cy - y_i|.
% 3. Criterio de Cercania y Equidad:
%    - Para que el concierto sea accesible, debe estar cerca en promedio (minimizar max_dist).
%    - Para que no favorezca a una ciudad sobre otra, la diferencia entre la ciudad
%      mas lejana y la mas cercana (diferencia = max_dist - min_dist) debe ser minima.
% ==============================================================================

% ------------------------------------------------------------------------------
% 1. PARAMETROS DEL MODELO (Instancia generada a partir de los datos de entrada)
% ------------------------------------------------------------------------------
int: N = {n};  % Tamano del lado del cuadrado que representa el departamento
int: M = {m};  % Cantidad total de ciudades

% Arreglos que almacenan la informacion de cada una de las ciudades:
array[1..M] of string: nombres = {str_nombres};
array[1..M] of int: pos_x = {str_x};
array[1..M] of int: pos_y = {str_y};

% ------------------------------------------------------------------------------
% 2. VARIABLES DE DECISION
% ------------------------------------------------------------------------------
% Coordenadas del concierto dentro de los limites del plano [0, N]:
var 0..N: cx;  % Coordenada X del concierto
var 0..N: cy;  % Coordenada Y del concierto

% Arreglo con la distancia Manhattan desde el concierto hacia cada ciudad.
% La distancia Manhattan maxima posible en un plano N x N es 2 * N:
array[1..M] of var 0..2*N: dist;

% Variables auxiliares para medir la equidad y cercania:
var 0..2*N: max_dist;    % Distancia a la ciudad mas lejana (peor caso)
var 0..2*N: min_dist;    % Distancia a la ciudad mas cercana (mejor caso)
var 0..2*N: diferencia;  % Brecha de equidad entre extremos (max_dist - min_dist)

% ------------------------------------------------------------------------------
% 3. RESTRICCIONES DEL MODELO
% ------------------------------------------------------------------------------

% Restriccion 1: El concierto NO puede quedar directamente sobre ninguna ciudad.
% Para cada ciudad 'i', la coordenada (cx, cy) no puede ser igual a (pos_x[i], pos_y[i]).
constraint forall(i in 1..M)(
    cx != pos_x[i] \\/ cy != pos_y[i]
);

% Restriccion 2: Calculo de la distancia Manhattan a cada ciudad 'i':
% dist[i] = |cx - pos_x[i]| + |cy - pos_y[i]|
constraint forall(i in 1..M)(
    dist[i] = abs(cx - pos_x[i]) + abs(cy - pos_y[i])
);

% Restriccion 3: Determinacion de las distancias extremas y la brecha de equidad:
constraint max_dist = max(dist);
constraint min_dist = min(dist);
constraint diferencia = max_dist - min_dist;

% ------------------------------------------------------------------------------
% 4. FUNCION OBJETIVO (Equilibrio entre Cercania y Equidad)
% ------------------------------------------------------------------------------
% EXPLICACION PARA LA SUSTENTACION:
% - Si unicamente minimizamos 'diferencia', el solver podria ubicar el concierto
%   en una esquina muy lejana donde todas las ciudades queden a distancias casi
%   identicas pero enormes (lo cual no tendria sentido practico).
% - Si unicamente minimizamos la distancia, podria favorecerse en exceso a un
%   grupo de ciudades dejando a otras aisladas.
% - Por lo tanto, se combinan ambos objetivos ponderando la equidad y la cercania:
%   Minimizamos: max_dist + diferencia
% ------------------------------------------------------------------------------
var int: funcion_objetivo = max_dist + diferencia;

solve minimize funcion_objetivo;

% ------------------------------------------------------------------------------
% 5. SALIDA FORMATEADA
% ------------------------------------------------------------------------------
output [
    "==========================================================\\n",
    "       RESULTADO OPTIMO: UBICACION DEL CONCIERTO          \\n",
    "==========================================================\\n",
    "Ubicacion del Concierto: (X = ", show(cx), ", Y = ", show(cy), ")\\n\\n",
    "Distancias Manhattan a cada ciudad:\\n",
    concat([ "  * " ++ nombres[i] ++ " (" ++ show(pos_x[i]) ++ ", " ++ show(pos_y[i]) ++ "): " ++ show(dist[i]) ++ " km\\n" | i in 1..M ]),
    "\\nMetricas de Optimizacion:\\n",
    "  - Distancia a la ciudad mas cercana (min_dist): ", show(min_dist), " km\\n",
    "  - Distancia a la ciudad mas lejana (max_dist):  ", show(max_dist), " km\\n",
    "  - Brecha de equidad (max_dist - min_dist):      ", show(diferencia), " km\\n",
    "  - Valor de la funcion objetivo:                 ", show(funcion_objetivo), "\\n",
    "==========================================================\\n"
];
"""
    return codigo_mzn
