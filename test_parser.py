"""
Script de pruebas unitarias para el modulo parser_entrada.py.
ADA II - Universidad del Valle
"""

import os
import unittest
from parser_entrada import parsear_entrada, ErrorEntrada

RUTA_EJEMPLOS = os.path.join(os.path.dirname(__file__), "ejemplos")

class TestParserEntrada(unittest.TestCase):

    def test_ejemplo_enunciado(self):
        with open(os.path.join(RUTA_EJEMPLOS, "ejemplo_enunciado.txt"), "r", encoding="utf-8") as f:
            texto = f.read()
        datos = parsear_entrada(texto)
        self.assertEqual(datos["N"], 12)
        self.assertEqual(datos["M"], 5)
        self.assertEqual(len(datos["ciudades"]), 5)
        self.assertEqual(datos["ciudades"][0], {"nombre": "Palmira", "x": 2, "y": 3})
        self.assertEqual(datos["ciudades"][4], {"nombre": "RioFrio", "x": 1, "y": 2})

    def test_nombres_compuestos(self):
        with open(os.path.join(RUTA_EJEMPLOS, "ejemplo_nombres_compuestos.txt"), "r", encoding="utf-8") as f:
            texto = f.read()
        datos = parsear_entrada(texto)
        self.assertEqual(datos["N"], 10)
        self.assertEqual(datos["M"], 4)
        self.assertEqual(datos["ciudades"][0]["nombre"], "La Union")
        self.assertEqual(datos["ciudades"][3]["nombre"], "San Pedro")

    def test_entrada_vacia(self):
        with self.assertRaises(ErrorEntrada) as ctx:
            parsear_entrada("   \n  \t  ")
        self.assertIn("vacia", str(ctx.exception))

    def test_n_invalido(self):
        with self.assertRaises(ErrorEntrada) as ctx:
            parsear_entrada("abc\n2\nCali 1 2\nBuga 2 3")
        self.assertIn("N en la primera linea", str(ctx.exception))

        with self.assertRaises(ErrorEntrada) as ctx:
            parsear_entrada("-5\n2\nCali 1 2\nBuga 2 3")
        self.assertIn("mayor a 0", str(ctx.exception))

    def test_m_invalido(self):
        with self.assertRaises(ErrorEntrada) as ctx:
            parsear_entrada("10\nxyz\nCali 1 2")
        self.assertIn("M en la segunda linea", str(ctx.exception))

        with self.assertRaises(ErrorEntrada) as ctx:
            parsear_entrada("10\n0\nCali 1 2")
        self.assertIn("mayor a 0", str(ctx.exception))

    def test_cantidad_ciudades_no_coincide(self):
        with self.assertRaises(ErrorEntrada) as ctx:
            parsear_entrada("10\n3\nCali 1 2\nBuga 2 3")
        self.assertIn("Inconsistencia en la cantidad de ciudades", str(ctx.exception))

    def test_coordenadas_fuera_de_rango(self):
        # X > N
        with self.assertRaises(ErrorEntrada) as ctx:
            parsear_entrada("10\n1\nCali 11 5")
        self.assertIn("fuera del rango", str(ctx.exception))

        # Y < 0
        with self.assertRaises(ErrorEntrada) as ctx:
            parsear_entrada("10\n1\nCali 5 -1")
        self.assertIn("fuera del rango", str(ctx.exception))

    def test_coordenada_duplicada(self):
        with self.assertRaises(ErrorEntrada) as ctx:
            parsear_entrada("10\n2\nCali 5 5\nPalmira 5 5")
        self.assertIn("Coordenada duplicada", str(ctx.exception))

    def test_coordenada_no_entera(self):
        with self.assertRaises(ErrorEntrada) as ctx:
            parsear_entrada("10\n1\nCali 5.5 5")
        self.assertIn("no es un numero entero valido", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
