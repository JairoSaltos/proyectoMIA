# Cat Clinic UIO — MVP con controles mínimos de seguridad

Esta aplicación independiente conserva sin cambios el modelo de Regresión
Logística y el vectorizador TF-IDF, y agrega controles antes y después de la
predicción.

## Controles implementados

- Rechazo de entradas vacías o compuestas solo por símbolos.
- Rechazo de mensajes sin términos reconocidos por TF-IDF.
- Revisión humana cuando el score estimado es menor a 35 %.
- Resultado principal `Clasificación no concluyente` ante score bajo; la
  categoría técnica se conserva en un desplegable de auditoría.
- Revisión humana para categorías clínicas.
- Alerta conservadora ante términos clínicos sensibles.
- Historial con indicador y motivo de revisión; los scores bajos se registran
  como `No concluyente`.
- Etiqueta `score estimado (no calibrado)` en lugar de `confianza`.
- Aviso visible de que el prototipo no diagnostica ni asigna prioridad clínica.
- Versión de scikit-learn fijada en 1.6.1, correspondiente a los artefactos.

El umbral y los patrones sensibles son controles operativos del prototipo, no
una escala clínica. La veterinaria debe revisar la lista de patrones de
`safety.py` antes de considerar un uso distinto al académico.

## Ejecución local

Desde esta carpeta:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

En Windows, la activación del entorno es `.venv\Scripts\activate`.

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas verifican entradas vacías, texto fuera del vocabulario, score bajo,
la presentación no concluyente, categorías clínicas, términos sensibles, inicio
de la interfaz y equivalencia de las predicciones válidas con la lógica original.

## Publicación independiente

La aplicación se publica en Streamlit Community Cloud con estos datos:

- URL: <https://catclinic-uio-mvp-seguro-js.streamlit.app>
- Repositorio: `JairoSaltos/proyectoMIA`
- Rama: `main`
- Main file path: `CatClinic_MVP_Seguro/app.py`
- Python: `3.12`

Después de cada publicación se deben repetir los casos manuales indicados en
`VALIDACION.md`.

## Alcance

El sistema clasifica intención y muestra un score estimado. Las alertas
agregadas solo derivan casos a una persona. No asignan prioridad veterinaria,
no diagnostican y no generan tratamientos ni respuestas clínicas.
