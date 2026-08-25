# Registro de cambios

Este registro se basa en commits y pull requests observables. La versión 1.0.0
es una propuesta para revisión; no se ha publicado un release ni creado un tag.

## [1.0.0] — propuesta pendiente de aprobación

### Documentación S10

- amplía el README con alcance, exclusiones, demo pública, instalación,
  ejecución, pruebas, pipeline, estructura y evidencias;
- documenta arquitectura, entradas, salidas, artefactos y límites;
- añade la tarjeta del modelo y separa resultados reportados de verificaciones
  reproducibles;
- documenta privacidad de datos originales y uso de ejemplos seguros;
- registra que no se realizó validación formal con usuarios y propone un
  protocolo futuro;
- reemplaza fechas y atribuciones no verificables de la bitácora por evidencia
  del historial Git;
- registra compatibilidad observada entre Python 3.11 y 3.12 sin modificar
  dependencias;
- actualiza el estado de la demo como pública por confirmación del propietario.

### Integridad

- no cambia `app.py`, `safety.py`, las pruebas ni los artefactos `.pkl`;
- no reentrena el modelo ni modifica clases o umbrales;
- no incorpora datos privados, conversaciones reales, secretos o credenciales;
- no añade una licencia abierta;
- no crea un release ni el tag `v1.0.0`.

## Historial anterior verificable

### 2026-08-20 — validación de guardrails

- PR [#3](https://github.com/JairoSaltos/proyectoMIA/pull/3).
- Commit `b3c0539991797fecc3fc779496ccc8017b39a7fa`.
- Registra 11/11 pruebas automatizadas, 13/13 casos de guardrails y validación
  autenticada de Streamlit.

### 2026-08-20 — resultados no concluyentes

- PR [#2](https://github.com/JairoSaltos/proyectoMIA/pull/2).
- Commit `e2e29ef7090136f4c2d31c13c2db8f2f358a089b`.
- Presenta scores bajos como no concluyentes, conserva salida técnica para
  auditoría y añade una prueba fuera de dominio.

### 2026-08-20 — incorporación del MVP seguro

- Commit `5e0e68177b7b28c6c6ae04b97f1dc2dda8341b5b`.
- El mensaje del commit registra una carga de archivos; no se atribuyen detalles
  adicionales que el historial no permita verificar.

### 2026-06-11 a 2026-06-12 — documentación inicial

- Creación y actualización inicial de README, arquitectura, validación de
  usuarios y bitácora.
- PR [#1](https://github.com/JairoSaltos/proyectoMIA/pull/1).
