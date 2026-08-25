# Tarjeta del modelo — Clasificador de intención Cat Clinic UIO

## Resumen

| Campo | Valor |
|---|---|
| Nombre | Clasificador de intención Cat Clinic UIO |
| Estado | Prototipo académico con revisión humana |
| Versión propuesta | 1.0.0, pendiente de aprobación |
| Tarea | Clasificación multiclase de mensajes individuales |
| Modelo | Regresión Logística |
| Representación | TF-IDF con unigramas y bigramas |
| Categorías | 12 |
| Interfaz | Streamlit |

El modelo sugiere una intención comunicacional para apoyar la organización de
mensajes recibidos por la clínica. La predicción no es una decisión automática
y debe revisarse antes de responder o actuar.

## Usuarios y usos previstos

Usuarios previstos:

- equipo académico que evalúa el prototipo;
- equipo del proyecto que revisa su comportamiento;
- personal autorizado de recepción, únicamente dentro de una futura prueba
  controlada y con protocolo aprobado.

Usos permitidos dentro del alcance actual:

- demostración académica;
- pruebas técnicas con ejemplos sintéticos o desidentificados;
- revisión de una categoría sugerida para un mensaje individual;
- análisis de errores y de limitaciones del clasificador.

## Usos no permitidos

El modelo no debe utilizarse para:

- diagnosticar, prescribir o recomendar tratamientos;
- decidir gravedad, urgencia, prioridad u orden de atención;
- ejecutar triaje veterinario automatizado;
- responder a tutores o enviar mensajes automáticamente;
- sustituir al personal de recepción o al equipo veterinario;
- procesar conversaciones reales sin autorización y protección de datos;
- generalizar resultados a otras clínicas, especies, regiones o periodos sin
  una nueva evaluación;
- interpretar el score como certeza clínica.

La categoría `triaje_clinico` es una etiqueta de intención comunicacional, no
una función de triaje.

## Especificación técnica verificada

La inspección de los artefactos versionados con scikit-learn 1.6.1 mostró:

- `LogisticRegression` con `class_weight="balanced"` y solver `lbfgs`;
- `TfidfVectorizer` en minúsculas, con unigramas y bigramas;
- 4.295 características de entrada;
- salida mediante `predict` y distribución estimada mediante
  `predict_proba`.

Categorías:

1. `agendar_cita`
2. `costos_cotizacion`
3. `indicaciones_previas`
4. `informacion_general`
5. `medicamentos_recetas`
6. `otros_revisar`
7. `pagos_documentos`
8. `reprogramar_cancelar_cita`
9. `resultados_examenes`
10. `seguimiento_clinico`
11. `triaje_clinico`
12. `venta_productos`

## Entrada y salida

La entrada es un mensaje individual de texto. La aplicación lo convierte a
minúsculas, elimina URL, caracteres no alfabéticos y espacios repetidos. No se
clasifican entradas vacías ni textos sin términos reconocidos por el
vectorizador.

La salida técnica incluye una categoría y, si está disponible, una distribución
estimada por categoría. El valor máximo de `predict_proba` se muestra como
**score estimado no calibrado**. No debe llamarse confianza ni probabilidad
clínica.

## Artefactos e integridad

| Artefacto | Ruta | SHA-256 |
|---|---|---|
| Clasificador | `CatClinic_MVP_Seguro/modelo_clasificador.pkl` | `1091cb827f3217b9386843e002de42b041cb3e62570cb5113c43ecbb8a2260a7` |
| Vectorizador | `CatClinic_MVP_Seguro/tfidf_vectorizer.pkl` | `e18dcf27cf658afaf00fc754788761dbd291398fbf067126e85f36a125326c3e` |

Los archivos `.pkl` cargan objetos Python y solo deben abrirse desde una fuente
confiable. La verificación S10 confirmó ambos hashes antes de cualquier cambio
documental.

## Desempeño reportado

El documento final compartido para S10 reporta:

| Modelo | Exactitud | F1 macro | Recall macro |
|---|---:|---:|---:|
| Regresión Logística + TF-IDF | 0.534 | 0.452 | 0.49 |
| Naive Bayes Multinomial + TF-IDF | 0.502 | 0.268 | 0.24 |

La fuente reporta 1.616 mensajes de entrenamiento, que incluyen 623 variantes
sintéticas revisadas, y 249 mensajes originales de prueba reservados antes del
aumento. También reporta 1.242 mensajes originales antes de la partición.

Estos valores son **resultados reportados, no reproducidos desde este
repositorio**. No existen aquí los datos, scripts de entrenamiento, particiones,
semillas ni manifiestos necesarios para vincular de forma inequívoca esas
métricas con los dos artefactos actuales. Consulte
[`results/README.md`](results/README.md).

## Comportamiento por categoría reportado

El documento final reporta desempeño desigual. Los F1 más altos fueron
`resultados_examenes` (0.76), `agendar_cita` (0.72) y
`costos_cotizacion` (0.63). Los más bajos fueron
`pagos_documentos` (0.00, con soporte 3), `seguimiento_clinico` (0.18) e
`informacion_general` (0.30).

La disparidad por clase limita el uso operativo y obliga a revisar cada
predicción, especialmente en categorías minoritarias o clínicas.

## Robustez y controles

El documento final reporta 34 pruebas técnicas de robustez ante errores
ortográficos, variación lingüística, ambigüedad y entradas fuera de dominio.
Esas pruebas mostraron vulnerabilidades y no equivalen a validación con
usuarios.

El repositorio contiene además:

- 11 pruebas automatizadas para validación, guardrails e interfaz;
- 13 casos registrados en `evidencia_guardrails.csv`;
- presentación **Clasificación no concluyente** cuando el score es menor a 35 %;
- revisión humana para categorías clínicas y términos sensibles;
- rechazo de entrada vacía o sin vocabulario reconocido.

Los 34 casos del documento y los 13 casos del CSV son conjuntos distintos y no
deben sumarse ni presentarse como una única métrica.

## Limitaciones y riesgos

- **Datos:** corpus pequeño, desbalanceado y procedente de una sola clínica.
- **Trazabilidad:** la correspondencia entre datos, entrenamiento, métricas y
  artefactos no puede verificarse con los archivos versionados.
- **Conversación:** se clasifican mensajes aislados y no existe un identificador
  versionado que permita reconstruir conversaciones.
- **Generalización:** no demostrada fuera de una clínica felina de Quito.
- **Lenguaje:** sensibilidad a ortografía, abreviaturas, otro idioma y cambios
  de redacción.
- **Ambigüedad:** un mensaje puede contener varias intenciones y recibir una
  sola categoría.
- **Score:** `predict_proba` no está calibrado; el umbral de 35 % es un
  guardrail operativo, no un umbral clínico.
- **Guardrails:** las reglas sensibles pueden producir falsos positivos y falsos
  negativos.
- **Privacidad:** los mensajes reales pueden contener identificadores directos
  e indirectos; no deben cargarse al repositorio.
- **Automatización:** una categoría errónea puede generar anclaje. La interfaz
  reduce este riesgo con abstención y revisión humana, pero no lo elimina.
- **Validación humana:** no se realizó una evaluación formal con recepción o
  usuarios finales.

No se incluyen resultados de SHAP, LIME u otras técnicas de explicabilidad
porque el repositorio no contiene evidencia reproducible actual.

## Supervisión y respuesta ante baja confianza

La revisión humana es obligatoria ante score bajo, categorías clínicas,
términos sensibles o información insuficiente. Un resultado no concluyente no
debe reinterpretarse como una categoría confirmada. La persona revisora decide
si solicita contexto, corrige la categoría, escala el mensaje o no utiliza la
salida.

## Trazabilidad pendiente

Antes de afirmar que los artefactos actuales producen las métricas reportadas,
el equipo debe responder y documentar:

1. ¿Qué commit, script, configuración, semilla y partición generaron cada
   archivo `.pkl`?
2. ¿Los artefactos provienen exactamente del entrenamiento con 1.616 mensajes y
   de la evaluación sobre los 249 mensajes reservados?
3. ¿Dónde se conservan de forma controlada el manifiesto de datos, las etiquetas
   y la relación entre originales y variantes sintéticas?
4. ¿Cómo se verificó que mensajes relacionados no cruzaran particiones si no
   existía un identificador de conversación?
5. ¿Qué versión de la taxonomía de 12 clases corresponde a los artefactos?

Hasta resolver estas preguntas, las métricas deben conservar la etiqueta
**reportado en el documento final**.

## Versionado

`VERSION` propone `1.0.0` para la revisión S10. La propuesta no constituye
un release ni un tag y solo debe publicarse después de aprobación del pull
request y confirmación del propietario.
