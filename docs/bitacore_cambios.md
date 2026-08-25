# Bitácora de cambios del proyecto

Esta bitácora usa únicamente evidencia observable en el historial Git y en los
pull requests del repositorio. Cuando el historial no permite identificar una
responsabilidad individual, se atribuye el trabajo al **equipo del proyecto**.

## Historial verificable

| Fecha | Evidencia Git | Cambio registrado |
|---|---|---|
| 2026-06-11 | Commits `2733afe`, `0bf41a5`, `7c15985` y PR [#1](https://github.com/JairoSaltos/proyectoMIA/pull/1) | Creación inicial de la bitácora y archivos de arquitectura y validación; actualización inicial del README. |
| 2026-06-12 | Commits `b7b173f`, `5b295a3`, `e9563f6` y `2526893` | Creación y actualización de README y bitácora. El historial disponible no aporta suficiente detalle para ampliar la atribución. |
| 2026-08-20 | Commit `5e0e681` | Incorporación mediante carga de los archivos que conforman el MVP seguro actual. |
| 2026-08-20 | PR [#2](https://github.com/JairoSaltos/proyectoMIA/pull/2), commit `e2e29ef` | Presentación de resultados de score bajo como no concluyentes, salida técnica de auditoría, prueba de regresión fuera de dominio y actualización documental. |
| 2026-08-20 | PR [#3](https://github.com/JairoSaltos/proyectoMIA/pull/3), commit `b3c0539` | Registro de 11/11 pruebas automatizadas, 13/13 casos de guardrails y validación autenticada de Streamlit. |

## Consolidación S10 — 2026-08-25

**Responsable registrado:** equipo del proyecto.

**Rama:** `codex/s10-documentation-hardening`.

**Commit base:** `b3c0539991797fecc3fc779496ccc8017b39a7fa`.

### Alcance

- completar README, arquitectura, datos y estado de validación con usuarios;
- documentar modelo, artefactos, hashes, resultados y trazabilidad pendiente;
- registrar la demo pública confirmada por el propietario;
- proponer la versión 1.0.0 sin publicar un tag ni un release;
- conservar sin cambios la lógica, las pruebas y los artefactos `.pkl`.

### Evidencia de entrada

- 11 de 11 pruebas automatizadas aprobadas;
- 13 de 13 casos de guardrails registrados;
- hashes SHA-256 del modelo y vectorizador coincidentes con la referencia;
- métricas identificadas como resultados reportados en el documento final, no
  como resultados reproducidos desde el repositorio.

El enlace al pull request S10 se añadirá en esta sección inmediatamente después
de abrirlo, antes de solicitar su aprobación.
