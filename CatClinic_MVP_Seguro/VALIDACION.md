# Evidencia de validación — controles mínimos de seguridad

Fecha de preparación: 2026-08-19

## Resultado de ejecución

- Pruebas automatizadas aprobadas: **10 de 10**.
- Inicio de Streamlit y endpoint local de salud: **correctos**.
- Predicciones válidas comparadas con la lógica original: **5 de 5 idénticas**.
- Modelo y vectorizador: **idénticos bit a bit a los adjuntos originales**.

Hashes SHA-256 de los artefactos conservados:

- Modelo: `1091cb827f3217b9386843e002de42b041cb3e62570cb5113c43ecbb8a2260a7`
- Vectorizador: `e18dcf27cf658afaf00fc754788761dbd291398fbf067126e85f36a125326c3e`

## Verificaciones automatizadas

Las suites incluidas en `tests/test_safety.py` y `tests/test_app.py` comprueban:

1. Rechazo de mensajes vacíos o formados solo por símbolos.
2. Rechazo de mensajes sin vocabulario reconocido por TF-IDF.
3. Activación de revisión humana con score menor a 35 %.
4. Activación de revisión humana para categorías clínicas.
5. Activación de alerta por términos sensibles incluso si la categoría predicha
   fuera administrativa.
6. Igualdad entre las predicciones del modelo original y la versión protegida
   para cinco mensajes válidos.
7. Inicio de la aplicación Streamlit sin excepciones.
8. Visualización en la interfaz de las alertas de entrada vacía, texto fuera de
   vocabulario y contenido sensible.

El modelo y el vectorizador se copiaron sin modificaciones. Los controles están
implementados en la capa de aplicación.

## Prueba manual posterior al despliegue

| Caso | Entrada | Resultado esperado |
|---|---|---|
| Vacío | Espacios o símbolos | No clasifica y solicita texto válido |
| Fuera de vocabulario | `pizza` | No clasifica y solicita más contexto |
| Baja certeza | Mensaje que obtenga score menor a 35 % | Clasifica y exige revisión humana |
| Contenido sensible | Mensaje de prueba con la palabra `sangre` | Exige revisión humana, independientemente de la categoría |
| Mensaje administrativo | Solicitud clara de horario o cita | Muestra categoría y score estimado |

Esta prueba manual debe repetirse en la nueva URL porque el despliegue y sus
dependencias constituyen un entorno diferente al local.

El archivo `evidencia_guardrails.csv` conserva los resultados de doce mensajes
representativos utilizados durante la verificación local.
