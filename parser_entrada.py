"""
Modulo de parseo y validacion de entrada.
ADA II - Universidad del Valle

Este modulo se encarga de:
1. Recibir el texto plano ingresado por el usuario (desde la interfaz grafica o un archivo).
2. Procesar y limpiar las lineas de texto.
3. Validar rigurosamente todas las restricciones del problema:
   - Que N y M sean enteros positivos.
   - Que la cantidad de ciudades descritas coincida exactamente con M.
   - Que los nombres de ciudades (incluso con espacios como 'La Union') se lean bien.
   - Que las coordenadas (X, Y) sean numeros enteros y esten dentro del rango [0, N].
   - Detectar coordenadas duplicadas entre ciudades.
4. Retornar los datos estructurados (N, M, lista de ciudades).
"""


class ErrorEntrada(Exception):
    """
    Excepcion personalizada para representar errores en el formato
    o en los valores de los datos de entrada.
    Permite mostrar mensajes amigables y descriptivos en la interfaz grafica.
    """
    pass


def parsear_entrada(texto: str) -> dict:
    """
    Procesa y valida el texto de entrada ingresado por el usuario.

    Parametros:
        texto (str): Texto con el formato:
                     Linea 1: N (tamano del cuadrado del plano)
                     Linea 2: M (numero de ciudades)
                     Siguientes M lineas: NombreCiudad X Y

    Retorna:
        dict: Diccionario con la estructura:
              {
                  'N': int,
                  'M': int,
                  'ciudades': [
                      {'nombre': str, 'x': int, 'y': int},
                      ...
                  ]
              }

    Lanza:
        ErrorEntrada: Si ocurre cualquier inconsistencia con el formato o los valores.
    """
    # 1. Validar que la entrada no sea nula o solo espacios en blanco
    if not texto or not texto.strip():
        raise ErrorEntrada("El area de texto esta vacia. Por favor ingresa los datos de entrada.")

    # 2. Dividir en lineas y descartar lineas totalmente vacias
    lineas = [linea.strip() for linea in texto.strip().splitlines() if linea.strip()]

    # 3. Validar que haya al menos 3 lineas (N, M y minimo una ciudad)
    if len(lineas) < 3:
        raise ErrorEntrada(
            f"Entrada incompleta: se encontraron {len(lineas)} lineas con datos. "
            "Se requiere al menos la linea de N, la linea de M y 1 ciudad."
        )

    # 4. Validar N (tamano del plano)
    linea_n = lineas[0]
    try:
        n = int(linea_n)
    except ValueError:
        raise ErrorEntrada(
            f"El valor de N en la primera linea ('{linea_n}') no es un numero entero valido."
        )

    if n <= 0:
        raise ErrorEntrada(
            f"El tamano del plano N debe ser un entero positivo mayor a 0. Se recibio: {n}."
        )

    # 5. Validar M (numero de ciudades)
    linea_m = lineas[1]
    try:
        m = int(linea_m)
    except ValueError:
        raise ErrorEntrada(
            f"El valor de M en la segunda linea ('{linea_m}') no es un numero entero valido."
        )

    if m <= 0:
        raise ErrorEntrada(
            f"El numero de ciudades M debe ser un entero positivo mayor a 0. Se recibio: {m}."
        )

    # 6. Validar que la cantidad de lineas de ciudades coincida exactamente con M
    lineas_ciudades = lineas[2:]
    total_ciudades_leidas = len(lineas_ciudades)

    if total_ciudades_leidas != m:
        raise ErrorEntrada(
            f"Inconsistencia en la cantidad de ciudades: M indica {m} ciudades, "
            f"pero se proporcionaron {total_ciudades_leidas} lineas de ciudades."
        )

    # 7. Procesar cada ciudad y validar sus coordenadas
    ciudades = []
    # Diccionario para verificar si dos ciudades ocupan exactamente la misma posicion
    posiciones_ocupadas = {}

    for indice, linea in enumerate(lineas_ciudades, start=1):
        partes = linea.split()

        # Cada linea de ciudad debe tener al menos 3 partes: Nombre, X, Y
        if len(partes) < 3:
            raise ErrorEntrada(
                f"Error en la ciudad #{indice} ('{linea}'): "
                "Cada linea debe contener: NombreCiudad X Y (separados por espacio)."
            )

        # Los dos ultimos elementos siempre corresponden a las coordenadas X e Y.
        # Todo lo que este antes se une para formar el nombre de la ciudad
        # (permitiendo nombres compuestos como 'La Union' o 'San Pedro').
        str_x = partes[-2]
        str_y = partes[-1]
        nombre_ciudad = " ".join(partes[:-2]).strip()

        if not nombre_ciudad:
            raise ErrorEntrada(
                f"Error en la ciudad #{indice}: El nombre de la ciudad no puede estar vacio."
            )

        # Validar que X sea un entero
        try:
            x = int(str_x)
        except ValueError:
            raise ErrorEntrada(
                f"Error en la ciudad '{nombre_ciudad}' (linea #{indice}): "
                f"La coordenada X ('{str_x}') no es un numero entero valido."
            )

        # Validar que Y sea un entero
        try:
            y = int(str_y)
        except ValueError:
            raise ErrorEntrada(
                f"Error en la ciudad '{nombre_ciudad}' (linea #{indice}): "
                f"La coordenada Y ('{str_y}') no es un numero entero valido."
            )

        # Validar que X este dentro del rango permitido [0, N]
        if not (0 <= x <= n):
            raise ErrorEntrada(
                f"Error en la ciudad '{nombre_ciudad}': "
                f"La coordenada X={x} esta fuera del rango permitido [0, {n}]."
            )

        # Validar que Y este dentro del rango permitido [0, N]
        if not (0 <= y <= n):
            raise ErrorEntrada(
                f"Error en la ciudad '{nombre_ciudad}': "
                f"La coordenada Y={y} esta fuera del rango permitido [0, {n}]."
            )

        # Validar coordenadas duplicadas entre ciudades distintas
        coord = (x, y)
        if coord in posiciones_ocupadas:
            ciudad_previa = posiciones_ocupadas[coord]
            raise ErrorEntrada(
                f"Coordenada duplicada ({x}, {y}): la ciudad '{nombre_ciudad}' "
                f"se encuentra en la misma posicion que '{ciudad_previa}'."
            )
        posiciones_ocupadas[coord] = nombre_ciudad

        # Agregar la ciudad validada a la lista
        ciudades.append({
            "nombre": nombre_ciudad,
            "x": x,
            "y": y
        })

    # 8. Retornar los datos completamente validados y estructurados
    return {
        "N": n,
        "M": m,
        "ciudades": ciudades
    }
