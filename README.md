# Cat Clinic UIO — clasificación asistida de mensajes

Prototipo académico de procesamiento de lenguaje natural para apoyar la
recepción digital de The Cat Clinic UIO. El sistema clasifica la intención de
un mensaje individual mediante TF-IDF y Regresión Logística, y presenta el
resultado para revisión humana.

> **Demo pública:** <https://catclinic-uio-mvp-seguro-js.streamlit.app>

La demo puede abrirse mediante el enlace anterior. La visibilidad del
repositorio es independiente de la accesibilidad de la aplicación desplegada.

## Estado del prototipo

| Elemento | Estado |
|---|---|
| Aplicación | MVP funcional en Streamlit |
| Tarea | Clasificación multiclase de intención en 12 categorías |
| Modelo | Regresión Logística con representación TF-IDF |
| Seguridad | Validación de entrada, resultado no concluyente con score bajo, guardrails y revisión humana |
| Pruebas automatizadas | 11 de 11 aprobadas |
| Casos registrados de guardrails | 13 de 13 aprobados |
| Uso | Académico; no autorizado para decisiones clínicas automáticas |
| Versión propuesta | 1.0.0, pendiente de aprobación; no existe todavía un release ni un tag |

## Problema y solución

La recepción debe interpretar manualmente mensajes heterogéneos sobre citas,
costos, indicaciones, resultados, seguimiento, productos y otros asuntos. El
prototipo organiza esa primera lectura mediante una categoría sugerida y una
capa de controles conservadores.

El alcance se limita a **clasificar la intención comunicacional de mensajes
individuales**. El sistema:

- no diagnostica ni prescribe;
- no recomienda tratamientos;
- no determina gravedad, urgencia ni prioridad clínica;
- no reconstruye conversaciones completas;
- no responde a tutores ni envía mensajes automáticamente;
- no sustituye al personal de recepción o al equipo veterinario.

La etiqueta técnica `triaje_clinico` describe una intención comunicacional y
no constituye triaje veterinario automatizado.

## Inicio rápido

### Requisitos

- Python 3.11 o 3.12. El `devcontainer.json` usa Python 3.11; la validación
  registrada se realizó con Python 3.12.
- `pip` y un entorno virtual.
- Dependencias fijadas en
  [`CatClinic_MVP_Seguro/requirements.txt`](CatClinic_MVP_Seguro/requirements.txt),
  incluidos Streamlit 1.62.0 y scikit-learn 1.6.1.

### Instalación

```bash
git clone https://github.com/JairoSaltos/proyectoMIA.git
cd proyectoMIA
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r CatClinic_MVP_Seguro/requirements.txt
```

En Windows, active el entorno con `.venv\Scripts\activate`.

### Ejecución local

Desde la raíz del repositorio:

```bash
streamlit run CatClinic_MVP_Seguro/app.py
```

Streamlit mostrará la URL local, normalmente
`http://localhost:8501`. Los dos archivos `.pkl` deben permanecer junto a
`app.py`.

### Pruebas automatizadas

El comando reproducible que ejecuta las 11 pruebas es:

```bash
cd CatClinic_MVP_Seguro
python -m unittest discover -s tests -v
```

Resultado de referencia: `Ran 11 tests ... OK`. Ejecutar el descubrimiento
desde esta carpeta garantiza que los imports locales de `safety.py` y
`app.py` se resuelvan correctamente.

## Pipeline

```text
mensaje del usuario
  → validación y limpieza
  → vectorización TF-IDF
  → Regresión Logística
  → score no calibrado y guardrails
  → presentación en Streamlit
  → revisión y decisión humana
```

Las entradas vacías o sin vocabulario reconocido no se clasifican. Un score
menor a 35 % se presenta como **Clasificación no concluyente**. También se
solicita revisión humana para categorías clínicas o términos sensibles. Los
detalles técnicos están en la
[`arquitectura`](docs/arquitectura.md).

## Estructura relevante

```text
proyectoMIA/
├── README.md
├── MODEL_CARD.md
├── CHANGELOG.md
├── VERSION
├── CatClinic_MVP_Seguro/
│   ├── app.py
│   ├── safety.py
│   ├── modelo_clasificador.pkl
│   ├── tfidf_vectorizer.pkl
│   ├── requirements.txt
│   ├── VALIDACION.md
│   ├── evidencia_guardrails.csv
│   └── tests/
├── data/
│   ├── raw/README.md
│   └── sample/README.md
├── docs/
│   ├── arquitectura.md
│   ├── bitacore_cambios.md
│   └── validation_usuarios.md
└── results/README.md
```

## Modelo y artefactos

| Archivo | Propósito | SHA-256 |
|---|---|---|
| `CatClinic_MVP_Seguro/modelo_clasificador.pkl` | Regresión Logística multiclase | `1091cb827f3217b9386843e002de42b041cb3e62570cb5113c43ecbb8a2260a7` |
| `CatClinic_MVP_Seguro/tfidf_vectorizer.pkl` | Vectorizador TF-IDF de unigramas y bigramas | `e18dcf27cf658afaf00fc754788761dbd291398fbf067126e85f36a125326c3e` |

Consulte la [tarjeta del modelo](MODEL_CARD.md) para conocer categorías, usos
permitidos, limitaciones y trazabilidad.

## Resultados

Los siguientes valores fueron **reportados en el documento final del
proyecto**. El repositorio actual no incluye los datos ni el pipeline de
entrenamiento necesarios para reproducirlos y vincularlos de forma inequívoca
con los artefactos `.pkl`.

| Modelo | Exactitud | F1 macro | Recall macro |
|---|---:|---:|---:|
| Regresión Logística + TF-IDF | 0.534 | 0.452 | 0.49 |
| Naive Bayes Multinomial + TF-IDF | 0.502 | 0.268 | 0.24 |

El documento final reporta 1.616 mensajes de entrenamiento, incluida ampliación
sintética revisada, y 249 mensajes originales reservados para prueba. La
procedencia exacta de los `.pkl` frente a esa partición permanece como
trazabilidad pendiente. La separación entre resultados reportados y
verificaciones reproducidas se detalla en [`results/README.md`](results/README.md).

## Limitaciones, privacidad y supervisión

- El desempeño reportado es moderado y desigual entre categorías.
- El modelo puede fallar ante errores ortográficos, abreviaturas, otro idioma,
  múltiples intenciones y mensajes fuera de dominio.
- El score de `predict_proba` no está calibrado y no representa certeza
  clínica.
- No se realizó una validación formal con personal de la clínica o usuarios
  finales; existe un [protocolo propuesto](docs/validation_usuarios.md).
- Los datos originales no se versionan por privacidad. No deben incorporarse
  conversaciones reales, identificadores, historiales clínicos, credenciales
  ni secretos al repositorio.
- La revisión humana es obligatoria antes de cualquier respuesta o acción.
- Los artefactos y datos descritos tienen uso académico y no autorizan
  decisiones clínicas automáticas.

## Evidencias para S10

- [x] Descripción del problema, alcance y exclusiones: este README.
- [x] Demo pública e instrucciones de instalación, ejecución y prueba: este README.
- [x] Arquitectura y pipeline real: [`docs/arquitectura.md`](docs/arquitectura.md).
- [x] Modelo, artefactos, hashes y riesgos: [`MODEL_CARD.md`](MODEL_CARD.md).
- [x] Resultados reportados y nivel de trazabilidad: [`results/README.md`](results/README.md).
- [x] Validación automatizada y guardrails: [`CatClinic_MVP_Seguro/VALIDACION.md`](CatClinic_MVP_Seguro/VALIDACION.md).
- [x] Casos técnicos registrados: [`evidencia_guardrails.csv`](CatClinic_MVP_Seguro/evidencia_guardrails.csv).
- [x] Estado de validación con usuarios: [`docs/validation_usuarios.md`](docs/validation_usuarios.md).
- [x] Política para datos privados y muestras seguras: [`data/`](data/).
- [x] Historial verificable y versión propuesta: [`CHANGELOG.md`](CHANGELOG.md), [`docs/bitacore_cambios.md`](docs/bitacore_cambios.md) y [`VERSION`](VERSION).

## Uso académico

Este repositorio documenta un prototipo académico. No se incorpora una licencia
abierta ni se concede autorización para reutilizar los datos o artefactos en
sistemas clínicos, automatizar respuestas o sustituir revisión profesional.
