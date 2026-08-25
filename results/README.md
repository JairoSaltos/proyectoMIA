# Resultados y nivel de evidencia

Este archivo separa los resultados **reportados** en el documento final de las
verificaciones que pueden **reproducirse** con el repositorio actual.

## Resumen de procedencia

| Evidencia | Estado | Fuente |
|---|---|---|
| Métricas del modelo final y Naive Bayes | Reportadas, no reproducibles aquí | Documento final compartido para S10 |
| Métricas por categoría | Reportadas, no reproducibles aquí | Documento final compartido para S10 |
| 34 pruebas técnicas de robustez | Reportadas, matriz completa no versionada | Documento final compartido para S10 |
| 11 pruebas automatizadas | Reproducibles | `CatClinic_MVP_Seguro/tests/` |
| 13 casos de guardrails | Versionados y registrados como aprobados | `CatClinic_MVP_Seguro/evidencia_guardrails.csv` y `VALIDACION.md` |
| Hashes de los artefactos | Reproducibles | Archivos `.pkl` versionados |

## Comparación global reportada

| Modelo | Representación | Exactitud | F1 macro | Recall macro |
|---|---|---:|---:|---:|
| Regresión Logística | TF-IDF | 0.534 | 0.452 | 0.49 |
| Naive Bayes Multinomial | TF-IDF | 0.502 | 0.268 | 0.24 |

El documento reporta una diferencia de 0.032 en exactitud y 0.184 en F1 macro a
favor de la Regresión Logística. También reporta 133 clasificaciones correctas
de 249 y un intervalo de Wilson del 95 % para la exactitud entre 0.472 y 0.595.

## Datos de evaluación reportados

- 1.242 mensajes originales etiquetados.
- 993 mensajes originales en entrenamiento.
- 623 variantes sintéticas añadidas solo al entrenamiento.
- 1.616 instancias en el entrenamiento final.
- 249 mensajes originales reservados para prueba antes del aumento.
- 12 categorías.
- Desbalance máximo reportado: 28,8:1 en el corpus original y 8,6:1 en el
  entrenamiento final.

La fuente indica revisión manual del 100 % de las variantes sintéticas, pero el
repositorio no contiene los datos ni el manifiesto para comprobarla.

## Desempeño por categoría reportado

| Categoría | Precisión | Recall | F1 | Soporte |
|---|---:|---:|---:|---:|
| `agendar_cita` | 0.88 | 0.61 | 0.72 | 92 |
| `resultados_examenes` | 0.69 | 0.85 | 0.76 | 13 |
| `costos_cotizacion` | 0.67 | 0.60 | 0.63 | 10 |
| `venta_productos` | 0.50 | 0.60 | 0.55 | 10 |
| `otros_revisar` | 0.48 | 0.59 | 0.53 | 17 |
| `triaje_clinico` | 0.48 | 0.46 | 0.47 | 28 |
| `medicamentos_recetas` | 0.44 | 0.48 | 0.46 | 23 |
| `reprogramar_cancelar_cita` | 0.30 | 0.64 | 0.41 | 11 |
| `indicaciones_previas` | 0.35 | 0.50 | 0.41 | 12 |
| `informacion_general` | 0.25 | 0.38 | 0.30 | 8 |
| `seguimiento_clinico` | 0.18 | 0.18 | 0.18 | 22 |
| `pagos_documentos` | 0.00 | 0.00 | 0.00 | 3 |

Estos números evidencian desempeño desigual. En particular, una exactitud global
de 0.534 no autoriza a ocultar las clases con F1 bajo ni a automatizar
decisiones.

## Robustez y guardrails

El documento final reporta 34 pruebas técnicas. Entre sus conclusiones:

- estabilidad parcial ante cambios de formato;
- degradación por ortografía y variación lingüística;
- comportamiento débil ante entradas límite y fuera de dominio;
- necesidad de abstención y revisión humana.

El repositorio actual conserva 13 casos de guardrails que validan la capa de
presentación y seguridad. Estos casos no reemplazan la evaluación convencional,
no miden exactitud general y no equivalen a validación con usuarios.

## Verificaciones reproducibles

Desde `CatClinic_MVP_Seguro/`:

```bash
python -m unittest discover -s tests -v
python -c "import hashlib, pathlib; [print(hashlib.sha256(p.read_bytes()).hexdigest(), p) for p in map(pathlib.Path, ['modelo_clasificador.pkl', 'tfidf_vectorizer.pkl'])]"
```

Resultado de auditoría S10 antes de cambios:

- pruebas: 11 de 11 aprobadas;
- modelo:
  `1091cb827f3217b9386843e002de42b041cb3e62570cb5113c43ecbb8a2260a7`;
- vectorizador:
  `e18dcf27cf658afaf00fc754788761dbd291398fbf067126e85f36a125326c3e`.

La auditoría se ejecutó con Python 3.12.13 y scikit-learn 1.6.1. El entorno
disponible tenía Streamlit 1.60.0 y las 11 pruebas pasaron; el archivo
`requirements.txt` fija Streamlit 1.62.0. El `devcontainer.json` declara
Python 3.11, por lo que la compatibilidad entre 3.11 y 3.12 debe mantenerse
documentada y verificarse en futuras instalaciones limpias.

## Trazabilidad pendiente

No se puede demostrar todavía que los `.pkl` actuales provengan exactamente
del entrenamiento y la partición descritos arriba. Faltan:

- scripts y configuración del entrenamiento final;
- versión o manifiesto del corpus y de la taxonomía;
- semillas y particiones;
- relación entre originales y variantes sintéticas;
- informe reproducible de métricas;
- identificador de experimento que conecte datos, código y artefactos.

Pregunta al equipo: **¿qué ejecución verificable generó los dos artefactos
versionados y dónde se conserva su manifiesto de datos y resultados?**

Hasta resolverla, todas las métricas de esta página deben citarse como
**reportadas en el documento final**, no como reproducidas.
