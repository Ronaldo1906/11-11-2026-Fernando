"""
Pruebas de integración / sistema de la aplicación web (cliente de pruebas de Flask).
Ejecutar:  python -m unittest -v
"""
import unittest

import app as web


class TestAppWeb(unittest.TestCase):
    def setUp(self):
        web.app.config["TESTING"] = True
        web.SERVICIOS.clear()
        web._siguiente_id[0] = 1
        self.client = web.app.test_client()

    def _liquidar(self, **kw):
        datos = {"nombre": "Juan", "equipos": "2", "dias_iniciales": "1",
                 "dias_adicionales": "0", "tipo_servicio": "1"}
        datos.update(kw)
        return self.client.post("/liquidar", data=datos)

    def test_it01_pagina_principal_responde(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("Liquidar servicio".encode(), r.data)

    def test_it02_liquidar_redirige_a_recibo(self):
        r = self._liquidar(tipo_servicio="2", dias_iniciales="3")
        self.assertEqual(r.status_code, 302)
        self.assertTrue(r.headers["Location"].endswith("/servicios/1"))
        recibo = self.client.get("/servicios/1").get_data(as_text=True)
        for campo in ("Juan", "Fuera de la ciudad", "$220.500", "Imprimir recibo"):
            self.assertIn(campo, recibo)

    def test_it03_consultar_servicios_y_filtrar(self):
        self._liquidar(nombre="Juan")
        self._liquidar(nombre="María")
        todos = self.client.get("/servicios").get_data(as_text=True)
        self.assertIn("Juan", todos)
        self.assertIn("María", todos)
        filtrado = self.client.get("/servicios?nombre=mar").get_data(as_text=True)
        self.assertIn("María", filtrado)
        self.assertNotIn("Juan", filtrado)

    def test_it04_api_json(self):
        self._liquidar(nombre="Ana", equipos="5", dias_iniciales="10", tipo_servicio="3")
        data = self.client.get("/api/servicios/1").get_json()
        self.assertEqual(data["total"], 1662500)

    def test_it05_datos_invalidos_no_genera_recibo(self):
        r = self._liquidar(nombre="", equipos="1", dias_iniciales="0",
                           dias_adicionales="-1", tipo_servicio="")
        self.assertEqual(r.status_code, 400)
        html = r.get_data(as_text=True)
        self.assertIn("obligatorio", html)
        self.assertIn("mínima", html)
        self.assertEqual(web.SERVICIOS, {})

    def test_it06_texto_no_numerico(self):
        r = self._liquidar(equipos="abc")
        self.assertEqual(r.status_code, 400)

    def test_it07_servicio_inexistente_404(self):
        self.assertEqual(self.client.get("/servicios/99").status_code, 404)
        self.assertEqual(self.client.get("/api/servicios/99").status_code, 404)

    def test_it08_dias_adicionales_vacio_es_cero(self):
        r = self._liquidar(dias_adicionales="")
        self.assertEqual(r.status_code, 302)
        self.assertEqual(web.SERVICIOS[1]["dias_adicionales"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
