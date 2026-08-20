# Cat Clinic UIO — MVP con controles mínimos de seguridad

Esta es una copia independiente de la aplicación original. Conserva sin cambios
el modelo de Regresión Logística y el vectorizador TF-IDF, pero agrega controles
antes y después de la predicción.

## Cambios implementados

- Rechazo de entradas vacías o compuestas solo por símbolos.
- Rechazo de mensajes sin términos reconocidos por TF-IDF.
- Revisión humana cuando el score estimado es menor a 35 %.
- Revisión humana para categorías clínicas.
- Alerta conservadora ante términos clínicos sensibles.
- Historial con indicador y motivo de revisión.
- Etiqueta `score estimado (no calibrado)` en lugar de `confianza`.
- Aviso visible de que el prototipo no diagnostica ni asigna prioridad clínica.
- Versión de scikit-learn fijada en 1.6.1, correspondiente a los artefactos.

El umbral y los patrones sensibles son controles operativos del prototipo, no
una escala clínica. La veterinaria debe revisar la lista de patrones de
`safety.py` antes de considerar un uso distinto al académico.

## Ejecución local

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
categorías clínicas, términos sensibles y equivalencia de las predicciones
válidas con la lógica original.

## Publicación independiente

1. Crear un repositorio nuevo, por ejemplo `catclinic-mvp-seguro`.
2. Subir únicamente el contenido de esta carpeta.
3. En Streamlit Community Cloud, crear una app nueva apuntando a `app.py`.
4. No cambiar la aplicación ni el repositorio de la versión de la compañera.
5. Ejecutar la prueba manual indicada en `VALIDACION.md` después del despliegue.

## Alcance

El sistema clasifica intención y muestra un score estimado. Las alertas agregadas
solo derivan casos a una persona. No asignan prioridad veterinaria, no diagnostican
y no generan tratamientos o respuestas clínicas.
