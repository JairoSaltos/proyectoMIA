import re
import unittest
from pathlib import Path

import joblib

from safety import (
    MIN_SCORE_REVISION,
    clasificar_mensaje,
    detectar_terminos_sensibles,
    evaluar_revision,
)


BASE_DIR = Path(__file__).resolve().parents[1]


def limpieza_original(texto):
    texto = str(texto).lower()
    texto = re.sub(r"http\S+|www\S+", "", texto)
    texto = re.sub(r"[^a-záéíóúñü\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


class SafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modelo = joblib.load(BASE_DIR / "modelo_clasificador.pkl")
        cls.vectorizador = joblib.load(BASE_DIR / "tfidf_vectorizer.pkl")

    def test_rechaza_mensaje_vacio(self):
        resultado = clasificar_mensaje(self.modelo, self.vectorizador, "   !!!")
        self.assertEqual(resultado.estado, "entrada_invalida")
        self.assertIsNone(resultado.categoria)

    def test_rechaza_texto_fuera_del_vocabulario(self):
        resultado = clasificar_mensaje(self.modelo, self.vectorizador, "pizza")
        self.assertEqual(resultado.estado, "informacion_insuficiente")
        self.assertTrue(resultado.requiere_revision)
        self.assertIsNone(resultado.categoria)

    def test_score_bajo_activa_revision(self):
        requiere_revision, motivos = evaluar_revision(
            "informacion_general", MIN_SCORE_REVISION - 0.01, "consulta de horarios"
        )
        self.assertTrue(requiere_revision)
        self.assertTrue(any("score" in motivo for motivo in motivos))

    def test_categoria_clinica_activa_revision(self):
        requiere_revision, motivos = evaluar_revision(
            "triaje_clinico", 0.90, "mi mascota presenta síntomas"
        )
        self.assertTrue(requiere_revision)
        self.assertTrue(any("categoría clínica" in motivo for motivo in motivos))

    def test_terminos_sensibles_activan_revision(self):
        terminos = detectar_terminos_sensibles(
            "mi gato está vomitando sangre y quiero saber cuánto cuesta"
        )
        self.assertIn("sangrado", terminos)

        resultado = clasificar_mensaje(
            self.modelo,
            self.vectorizador,
            "mi gato está vomitando sangre y quiero saber cuánto cuesta la consulta",
        )
        self.assertEqual(resultado.estado, "clasificado")
        self.assertTrue(resultado.requiere_revision)
        self.assertTrue(any("sangrado" in motivo for motivo in resultado.motivos_revision))

    def test_prediccion_valida_conserva_modelo_original(self):
        casos = [
            "quiero agendar una cita para mañana",
            "cuánto cuesta una consulta",
            "puedo darle el medicamento antes de la cita",
            "dónde queda la clínica y cuál es el horario",
            "quiero cancelar la cita de hoy",
        ]

        for mensaje in casos:
            with self.subTest(mensaje=mensaje):
                texto = limpieza_original(mensaje)
                vector = self.vectorizador.transform([texto])
                prediccion_original = str(self.modelo.predict(vector)[0])
                score_original = float(self.modelo.predict_proba(vector)[0].max())

                resultado = clasificar_mensaje(self.modelo, self.vectorizador, mensaje)

                self.assertEqual(resultado.estado, "clasificado")
                self.assertEqual(resultado.categoria, prediccion_original)
                self.assertAlmostEqual(resultado.score, score_original, places=12)


if __name__ == "__main__":
    unittest.main()
