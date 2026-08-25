# Evidencia de validación — controles mínimos de seguridad

Fecha de preparación: 2026-08-20

## Resultado de ejecución

- Pruebas automatizadas aprobadas: **11 de 11**.
- Inicio de Streamlit y endpoint local de salud: **correctos**.
- Casos del CSV de guardrails reproducidos: **13 de 13**.
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
9. Presentación de los scores menores a 35 % como `Clasificación no concluyente`,
   sin mostrar una categoría como resultado principal.
10. Conservación de la salida técnica de baja certeza dentro de un desplegable
    de auditoría.

El modelo y el vectorizador se copiaron sin modificaciones. Los controles están
implementados en la capa de aplicación.

## Despliegue independiente

- URL: <https://catclinic-uio-mvp-seguro-js.streamlit.app>
- Repositorio: `JairoSaltos/proyectoMIA`
- Rama: `main`
- Punto de entrada: `CatClinic_MVP_Seguro/app.py`
- Commit publicado: `e2e29ef7090136f4c2d31c13c2db8f2f358a089b`
- Pull request: `#2`
- Entorno validado localmente: Python 3.12, Streamlit 1.62.0 y
  scikit-learn 1.6.1.
- Salud en producción después de la fusión: `GET /healthz` respondió HTTP 200
  con `{"status":"ok"}` el 2026-08-20.

### Estado de acceso

La verificación del 2026-08-20 se realizó con una sesión autenticada. En ese
momento, una solicitud sin sesión redirigía al inicio de sesión de Streamlit.
Este dato se conserva como contexto histórico de aquella validación.

Por confirmación del propietario el 2026-08-24, la aplicación está actualmente
disponible de forma pública en
<https://catclinic-uio-mvp-seguro-js.streamlit.app>. Esta actualización
documental no equivale a una nueva validación funcional en producción ni
modifica la configuración, la URL o los secretos del despliegue.

La validación visual autenticada se completó el 2026-08-20 a las 20:32:11,
según la hora mostrada en el historial de la aplicación. Para la entrada
`como se come una pizza`, la interfaz mostró primero `Clasificación no
concluyente`, mantuvo cerrada la salida técnica y registró `No concluyente` en
el historial con score 20,8 %. El caso cumplió el comportamiento esperado.

## Prueba manual posterior al despliegue

| Caso | Entrada | Resultado esperado |
|---|---|---|
| Vacío | Espacios o símbolos | No clasifica y solicita texto válido |
| Fuera de vocabulario | `pizza` | No clasifica y solicita más contexto |
| Baja certeza | `como se come una pizza` | Muestra primero `Clasificación no concluyente` y exige revisión humana; la categoría técnica solo aparece en el desplegable |
| Contenido sensible | Mensaje de prueba con la palabra `sangre` | Muestra primero la revisión humana, independientemente de la categoría |
| Mensaje administrativo | Solicitud clara de horario o cita | Muestra categoría y score estimado |

Esta prueba manual debe repetirse en la nueva URL porque el despliegue y sus
dependencias constituyen un entorno diferente al local.

El caso de baja certeza fue repetido y aprobado en la URL desplegada durante la
validación autenticada del 2026-08-20. Los demás casos permanecen cubiertos por
las 11 pruebas automatizadas y deben repetirse en la demo pública antes de
cualquier prueba piloto con personal de recepción.

El caso fuera de dominio `como se come una pizza` obtuvo técnicamente
`triaje_clinico` con score 0,208381. El guardrail evitó presentarlo como una
clasificación confirmada: la salida principal fue `Clasificación no concluyente`
y la categoría se conservó únicamente para auditoría.

El archivo `evidencia_guardrails.csv` conserva los resultados de trece mensajes
representativos utilizados durante la verificación local.
