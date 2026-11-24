"""
Script de pruebas para el modulo generador_minizinc.py.
ADA II - Universidad del Valle
"""

import unittest
from generador_minizinc import generar_codigo_minizinc

class TestGeneradorMiniZinc(unittest.TestCase):

    def setUp(self):
        self.ciudades = [
            {"nombre": "Palmira", "x": 2, "y": 3},
            {"nombre": "Cali", "x": 10, "y": 2},
            {"nombre": "Buga", "x": 11, "y": 0},
            {"nombre": "Tulua", "x": 0, "y": 3},
            {"nombre": "RioFrio", "x": 1, "y": 2}
        ]
        self.n = 12
        self.m = 5
        self.codigo = generar_codigo_minizinc(self.n, self.m, self.ciudades)

    def test_parametros_presentes(self):
        self.assertIn("int: N = 12;", self.codigo)
        self.assertIn("int: M = 5;", self.codigo)
        self.assertIn('["Palmira", "Cali", "Buga", "Tulua", "RioFrio"]', self.codigo)
        self.assertIn("[2, 10, 11, 0, 1]", self.codigo)
        self.assertIn("[3, 2, 0, 3, 2]", self.codigo)

    def test_variables_decision(self):
        self.assertIn("var 0..N: cx;", self.codigo)
        self.assertIn("var 0..N: cy;", self.codigo)
        self.assertIn("array[1..M] of var 0..2*N: dist;", self.codigo)
        self.assertIn("var 0..2*N: max_dist;", self.codigo)
        self.assertIn("var 0..2*N: min_dist;", self.codigo)
        self.assertIn("var 0..2*N: diferencia;", self.codigo)

    def test_restricciones(self):
        # Restriccion no coincidir con ciudades
        self.assertIn("cx != pos_x[i] \\/ cy != pos_y[i]", self.codigo)
        # Restriccion distancia Manhattan
        self.assertIn("dist[i] = abs(cx - pos_x[i]) + abs(cy - pos_y[i])", self.codigo)
        # Restriccion maximo y minimo
        self.assertIn("constraint max_dist = max(dist);", self.codigo)
        self.assertIn("constraint min_dist = min(dist);", self.codigo)
        self.assertIn("constraint diferencia = max_dist - min_dist;", self.codigo)

    def test_funcion_objetivo(self):
        self.assertIn("solve minimize funcion_objetivo;", self.codigo)

    def test_seccion_output(self):
        self.assertIn("output [", self.codigo)
        self.assertIn("show(cx)", self.codigo)
        self.assertIn("show(cy)", self.codigo)

    def test_ciudades_con_espacios(self):
        ciudades_compuestas = [
            {"nombre": "La Union", "x": 1, "y": 9},
            {"nombre": "San Pedro", "x": 1, "y": 4}
        ]
        codigo = generar_codigo_minizinc(10, 2, ciudades_compuestas)
        self.assertIn('"La Union"', codigo)
        self.assertIn('"San Pedro"', codigo)


if __name__ == "__main__":
    unittest.main()
