# Cat Clinic UIO — Clasificador de mensajes con revisión humana

Prototipo académico de procesamiento de lenguaje natural para apoyar la recepción
de The Cat Clinic UIO. La aplicación clasifica la intención de mensajes escritos
por tutores de mascotas mediante TF-IDF y Regresión Logística.

## Funcionalidad actual

- Clasifica la intención del mensaje.
- Muestra un score estimado no calibrado y la distribución estimada por categoría.
- Presenta como `No concluyente` los resultados con score inferior a 35 %; la
  salida técnica queda disponible solo como detalle de auditoría.
- Rechaza entradas vacías, compuestas solo por símbolos o sin vocabulario
  reconocido por el vectorizador.
- Solicita revisión humana ante score bajo, categorías clínicas o términos
  sensibles.
- Mantiene un historial temporal durante la sesión.

## Alcance y limitaciones

El prototipo no asigna prioridad clínica, no diagnostica, no prescribe
tratamientos y no genera ni envía respuestas automáticas. Las alertas son
controles conservadores de derivación a una persona; no constituyen triaje
veterinario. Los patrones sensibles deben ser revisados por la veterinaria antes
de considerar un uso distinto al académico.

## Estructura actual

```text
proyectoMIA/
├── README.md
├── CatClinic_MVP_Seguro/
│   ├── app.py
│   ├── safety.py
│   ├── modelo_clasificador.pkl
│   ├── tfidf_vectorizer.pkl
│   ├── requirements.txt
│   ├── VALIDACION.md
│   ├── evidencia_guardrails.csv
│   └── tests/
│       ├── test_app.py
│       └── test_safety.py
├── data/
└── docs/
```

La aplicación desplegable se encuentra en `CatClinic_MVP_Seguro/app.py`.

## Ejecución local

```bash
cd CatClinic_MVP_Seguro
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

En Windows, la activación del entorno es `.venv\Scripts\activate`.

## Pruebas

```bash
cd CatClinic_MVP_Seguro
python -m unittest discover -s tests -v
```

## Despliegue en Streamlit Community Cloud

- URL: <https://catclinic-uio-mvp-seguro-js.streamlit.app>
- Repositorio: `JairoSaltos/proyectoMIA`
- Rama: `main`
- Main file path: `CatClinic_MVP_Seguro/app.py`
- Python: `3.12`

El archivo de dependencias está ubicado junto al punto de entrada de la
aplicación: `CatClinic_MVP_Seguro/requirements.txt`.

## Integridad del modelo

La capa de seguridad no reentrena ni modifica los artefactos `.pkl`. La
validación técnica y los casos de guardrails están documentados en
`CatClinic_MVP_Seguro/VALIDACION.md`.
