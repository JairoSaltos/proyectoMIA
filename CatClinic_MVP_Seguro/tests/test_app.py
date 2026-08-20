import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


BASE_DIR = Path(__file__).resolve().parents[1]


class AppIntegrationTests(unittest.TestCase):
    def nueva_app(self):
        app = AppTest.from_file(BASE_DIR / "app.py", default_timeout=15).run()
        self.assertEqual([elemento.value for elemento in app.exception], [])
        return app

    def test_aplicacion_inicia(self):
        app = self.nueva_app()
        self.assertEqual(len(app.text_area), 1)
        self.assertEqual(len(app.button), 2)

    def test_interfaz_rechaza_entrada_vacia(self):
        app = self.nueva_app()
        app.button[0].click().run()
        mensajes = [elemento.value for elemento in app.warning]
        self.assertTrue(any("Ingrese un mensaje" in mensaje for mensaje in mensajes))

    def test_interfaz_rechaza_texto_fuera_del_vocabulario(self):
        app = self.nueva_app()
        app.text_area[0].set_value("pizza")
        app.button[0].click().run()
        mensajes = [elemento.value for elemento in app.warning]
        self.assertTrue(any("no contiene términos reconocidos" in mensaje for mensaje in mensajes))

    def test_interfaz_muestra_alerta_para_contenido_sensible(self):
        app = self.nueva_app()
        app.text_area[0].set_value(
            "mi gato está vomitando sangre y cuánto cuesta la consulta"
        )
        app.button[0].click().run()
        mensajes = [elemento.value for elemento in app.warning]
        self.assertTrue(any("Revisión humana requerida" in mensaje for mensaje in mensajes))
        self.assertTrue(any("sangrado" in mensaje for mensaje in mensajes))


if __name__ == "__main__":
    unittest.main()
