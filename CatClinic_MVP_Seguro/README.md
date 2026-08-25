# Cat Clinic UIO — MVP con controles mínimos de seguridad

Aplicación Streamlit que conserva el modelo de Regresión Logística y el
vectorizador TF-IDF versionados, y aplica controles antes y después de la
predicción. La interfaz apoya la clasificación de intención; toda interpretación
y acción posterior corresponde a una persona.

## Controles implementados

- Rechazo de entradas vacías o compuestas solo por símbolos.
- Rechazo de mensajes sin términos reconocidos por TF-IDF.
- Revisión humana cuando el score estimado es menor a 35 %.
- Resultado principal `Clasificación no concluyente` ante score bajo; la
  categoría técnica se conserva en un desplegable de auditoría.
- Revisión humana para categorías clínicas.
- Alerta conservadora ante términos clínicos sensibles.
- Historial temporal con indicador y motivo de revisión.
- Etiqueta `score estimado (no calibrado)` en lugar de confianza.
- Aviso visible de que el prototipo no diagnostica ni asigna prioridad clínica.

El umbral y los patrones de `safety.py` son controles operativos, no una escala
clínica. Deben revisarse con el equipo veterinario antes de cualquier piloto.

## Requisitos

- Python 3.11 o 3.12.
- Dependencias de `requirements.txt`: Streamlit 1.62.0, scikit-learn 1.6.1,
  NumPy, Joblib y pandas.
- `modelo_clasificador.pkl` y `tfidf_vectorizer.pkl` en esta carpeta.

## Ejecución local

Desde esta carpeta:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

En Windows, la activación es `.venv\Scripts\activate`.

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Resultado de referencia: 11 de 11 pruebas aprobadas. Las pruebas cubren entrada
inválida, texto fuera de vocabulario, score bajo, presentación no concluyente,
categorías clínicas, términos sensibles, inicio de la interfaz y equivalencia
de predicciones válidas con la lógica original.

## Demo pública

- URL: <https://catclinic-uio-mvp-seguro-js.streamlit.app>
- Repositorio: `JairoSaltos/proyectoMIA`
- Rama desplegada: `main`
- Punto de entrada: `CatClinic_MVP_Seguro/app.py`
- Entorno registrado: Python 3.12

La demo es pública. Su accesibilidad no implica que el repositorio tenga la
misma visibilidad. Después de cada publicación deben repetirse los casos
manuales descritos en [`VALIDACION.md`](VALIDACION.md).

## Alcance

El sistema clasifica intención y muestra un score estimado no calibrado. No
analiza conversaciones completas, no asigna prioridad veterinaria, no
diagnostica, no prescribe, no recomienda tratamientos y no genera respuestas
automáticas.

Para la visión completa del repositorio, consulte el [README principal](../README.md),
la [arquitectura](../docs/arquitectura.md) y la
[tarjeta del modelo](../MODEL_CARD.md).
