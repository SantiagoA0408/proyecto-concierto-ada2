"""
Punto de entrada principal del proyecto: ¿Donde pongo mi concierto?
ADA II - Universidad del Valle

Este archivo inicia la aplicacion con interfaz grafica en Tkinter.
Para ejecutar:
    python main.py
"""

import sys
import os

# Asegurar que el directorio del proyecto este en el PATH para importaciones relativas limpias
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
if DIRECTORIO_ACTUAL not in sys.path:
    sys.path.insert(0, DIRECTORIO_ACTUAL)

try:
    from interfaz import iniciar_interfaz
except ModuleNotFoundError as e:
    if "tkinter" in str(e):
        print("\n" + "=" * 70)
        print(" ERROR: Falta el modulo 'tkinter' en tu instalacion de Python.")
        print("=" * 70)
        print(" En sistemas Linux (Ubuntu/Debian), puedes instalarlo ejecutando:")
        print("     sudo apt update && sudo apt install -y python3-tk\n")
        print(" Luego vuelve a ejecutar:")
        print("     python3 main.py")
        print("=" * 70 + "\n")
        sys.exit(1)
    else:
        raise e


def main():
    """
    Funcion principal que lanza la interfaz grafica de usuario.
    """
    iniciar_interfaz()


if __name__ == "__main__":
    main()
