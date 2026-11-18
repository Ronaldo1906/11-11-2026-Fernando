"""
Pruebas unitarias de ALQUILAPC con unittest (equivalente a JUnit en Python).

    TestCajaBlanca  -> cubre cada función y cada rama (if/else) del código.
    TestCajaNegra   -> partición de equivalencia, valores límite y tabla de decisión
                       usando solo entradas/salidas (escenarios S01-S05 del plan).
    TestRegresion   -> resultados "dorados" que no deben cambiar tras una corrección.

Ejecutar:  python -m unittest -v
"""
import unittest

import proyecto1 as p


class TestCajaBlanca(unittest.TestCase):
    # ---- calculo_alquiler / calculo_alquiler_adicional
    def test_cb01_calculo_alquiler(self):
        self.assertEqual(p.calculo_alquiler(2, 1), 70000)

    def test_cb02_calculo_alquiler_adicional_cero(self):
        self.assertEqual(p.calculo_alquiler_adicional(3, 0), 0)

    def test_cb03_calculo_alquiler_adicional(self):
        self.assertEqual(p.calculo_alquiler_adicional(3, 2), 210000)

    # ---- calculo_alquiler_adicional_dto: rama if / rama else
    def test_cb04_dto_adicional_rama_verdadera(self):
        self.assertEqual(p.calculo_alquiler_adicional_dto(210000), 4200)

    def test_cb05_dto_adicional_rama_falsa(self):
        self.assertEqual(p.calculo_alquiler_adicional_dto(0), 0)

    # ---- calculo_dentro_establecimiento: rama if / rama else
    def test_cb06_establecimiento_aplica(self):
        self.assertEqual(p.calculo_dentro_establecimiento(100000, p.ESTABLECIMIENTO), 5000)

    def test_cb07_establecimiento_no_aplica(self):
        for tipo in (p.DENTRO_CIUDAD, p.FUERA_CIUDAD):
            self.assertEqual(p.calculo_dentro_establecimiento(100000, tipo), 0)

    # ---- calculo_domicilio: rama if / rama else
    def test_cb08_domicilio_aplica(self):
        self.assertEqual(p.calculo_domicilio(100000, p.FUERA_CIUDAD), 5000)

    def test_cb09_domicilio_no_aplica(self):
        for tipo in (p.DENTRO_CIUDAD, p.ESTABLECIMIENTO):
            self.assertEqual(p.calculo_domicilio(100000, tipo), 0)

    # ---- calculo_descuento: orden descuentos -> incremento (RN04)
    def test_cb10_domicilio_despues_de_descuentos(self):
        r = p.calculo_descuento(70000, 70000, p.FUERA_CIUDAD)
        self.assertEqual(r["dto_adicional"], 1400)
        self.assertEqual(r["incremento_domicilio"], 6930)  # 5% de 138.600, no de 140.000
        self.assertEqual(r["total"], 145530)

    def test_cb11_porcentaje_redondeo(self):
        self.assertEqual(p.porcentaje(10, 5), 1)   # 0,5 -> 1
        self.assertEqual(p.porcentaje(9, 5), 0)    # 0,45 -> 0

    # ---- validar_datos: cada rama de error
    def test_cb12_validar_sin_errores(self):
        self.assertEqual(p.validar_datos("Ana", 2, 1, 0, 1), [])

    def test_cb13_validar_tipos_no_enteros(self):
        errores = p.validar_datos("Ana", "2", 1.5, None, "1")
        self.assertEqual(len(errores), 4)

    def test_cb14_validar_bool_no_es_entero(self):
        self.assertEqual(len(p.validar_datos("Ana", True, True, False, True)), 4)

    def test_cb15_calcular_valores_lanza_error(self):
        with self.assertRaises(p.ValidacionError) as ctx:
            p.calcular_valores("", 1, 0, -1, 4)
        self.assertEqual(len(ctx.exception.errores), 5)

    def test_cb16_generar_factura_contiene_campos(self):
        liq = p.calcular_valores("Juan", 2, 1, 1, p.FUERA_CIUDAD)
        texto = p.generar_factura(liq)
        for campo in ("Juan", "Fuera de la ciudad", "Equipos alquilados:    2",
                      "Días iniciales:        1", "Días adicionales:      1",
                      "Total descuentos", "Incremento domicilio", "$145.530"):
            self.assertIn(campo, texto)

    def test_cb17_formato_moneda(self):
        self.assertEqual(p.formato_moneda(1662500), "$1.662.500")
        self.assertEqual(p.formato_moneda(0), "$0")


class TestCajaNegra(unittest.TestCase):
    # ---- Escenarios del plan de pruebas
    def test_cn01_S01_2eq_1dia_ciudad(self):
        self.assertEqual(p.calcular_valores("Juan", 2, 1, 0, 1)["total"], 70000)

    def test_cn02_S02_2eq_3dias_fuera(self):
        r = p.calcular_valores("Ana", 2, 3, 0, 2)
        self.assertEqual(r["incremento_domicilio"], 10500)
        self.assertEqual(r["total"], 220500)

    def test_cn03_S03_5eq_10dias_establecimiento(self):
        r = p.calcular_valores("María", 5, 10, 0, 3)
        self.assertEqual(r["dto_establecimiento"], 87500)
        self.assertEqual(r["total"], 1662500)

    def test_cn04_S04_con_dias_adicionales(self):
        r = p.calcular_valores("Pedro", 2, 2, 3, 1)
        self.assertEqual(r["valor_adicional"], 210000)
        self.assertEqual(r["dto_adicional"], 4200)
        self.assertEqual(r["total"], 345800)

    def test_cn05_S05_maximo_descuento_establecimiento_y_adicionales(self):
        r = p.calcular_valores("Pedro", 10, 30, 30, 3)
        # subtotal 21.000.000; dto adic 2% de 10.500.000 = 210.000; dto est 5% = 1.050.000
        self.assertEqual(r["total_descuentos"], 1260000)
        self.assertEqual(r["total"], 19740000)

    # ---- Partición de equivalencia / valores límite: equipos
    def test_cn06_equipos_limites(self):
        self.assertTrue(p.validar_datos("X", 1, 1, 0, 1))      # inválido
        self.assertFalse(p.validar_datos("X", 2, 1, 0, 1))     # límite válido
        self.assertFalse(p.validar_datos("X", 3, 1, 0, 1))     # válido
        self.assertTrue(p.validar_datos("X", 0, 1, 0, 1))      # inválido

    # ---- Días iniciales
    def test_cn07_dias_iniciales_limites(self):
        self.assertTrue(p.validar_datos("X", 2, 0, 0, 1))
        self.assertTrue(p.validar_datos("X", 2, -1, 0, 1))
        self.assertFalse(p.validar_datos("X", 2, 1, 0, 1))

    # ---- Días adicionales
    def test_cn08_dias_adicionales_limites(self):
        self.assertTrue(p.validar_datos("X", 2, 1, -1, 1))
        self.assertFalse(p.validar_datos("X", 2, 1, 0, 1))
        self.assertFalse(p.validar_datos("X", 2, 1, 1, 1))

    # ---- Nombre
    def test_cn09_nombre_vacio_o_espacios(self):
        self.assertTrue(p.validar_datos("", 2, 1, 0, 1))
        self.assertTrue(p.validar_datos("   ", 2, 1, 0, 1))

    def test_cn10_nombre_se_limpia(self):
        self.assertEqual(p.calcular_valores("  Juan  ", 2, 1, 0, 1)["nombre"], "Juan")

    # ---- Tabla de decisión: tipo de servicio
    def test_cn11_tabla_decision_tipo_servicio(self):
        casos = {1: (0, 0), 2: (0, 3500), 3: (3500, 0)}  # (dto_est, incremento) para 70.000
        for tipo, (dto, inc) in casos.items():
            r = p.calcular_valores("X", 2, 1, 0, tipo)
            self.assertEqual((r["dto_establecimiento"], r["incremento_domicilio"]), (dto, inc), tipo)

    def test_cn12_tipo_servicio_invalido(self):
        for tipo in (0, 4, -1):
            self.assertTrue(p.validar_datos("X", 2, 1, 0, tipo))

    def test_cn13_sin_incrementos_valor_cero(self):
        r = p.calcular_valores("X", 2, 1, 0, 1)
        self.assertEqual(r["incremento_domicilio"], 0)
        self.assertEqual(r["total_descuentos"], 0)


class TestRegresion(unittest.TestCase):
    """Valores aprobados. Si alguno falla después de un cambio, hubo regresión."""

    CASOS_DORADOS = [
        # (nombre, equipos, dias_ini, dias_adic, tipo, total_esperado)
        ("Juan", 2, 1, 0, 1, 70000),
        ("María", 5, 5, 0, 1, 875000),
        ("Pedro", 10, 30, 0, 1, 10500000),
        ("Ana", 2, 3, 0, 2, 220500),
        ("Luis", 2, 1, 1, 2, 145530),
        ("Sara", 5, 10, 0, 3, 1662500),
        ("Carlos", 2, 1, 1, 3, 131600),
        ("Pedro", 2, 2, 3, 1, 345800),
    ]

    def test_rg01_casos_dorados(self):
        for nombre, eq, di, da, tipo, esperado in self.CASOS_DORADOS:
            with self.subTest(nombre=nombre, tipo=tipo):
                self.assertEqual(p.calcular_valores(nombre, eq, di, da, tipo)["total"], esperado)

    def test_rg02_constantes_negocio(self):
        self.assertEqual(p.VALOR_DIA, 35000)
        self.assertEqual(p.EQUIPOS_MINIMOS, 2)
        self.assertEqual(len(p.TIPOS_SERVICIO), 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
