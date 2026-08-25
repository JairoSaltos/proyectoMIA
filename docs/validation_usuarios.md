# Estado de validación con usuarios

## Situación actual

No se ha realizado una validación formal del prototipo con personal de la
clínica ni con usuarios finales. Tampoco se ha demostrado utilidad operativa,
aceptación, reducción de tiempos, seguridad percibida o mejora del proceso.

Esta ausencia debe distinguirse de otras verificaciones:

| Evidencia | Estado | Qué demuestra | Qué no demuestra |
|---|---|---|---|
| 11 pruebas automatizadas | Aprobadas | Comportamiento del código y guardrails incluidos | Utilidad o aceptación por personas |
| 13 casos de `evidencia_guardrails.csv` | Registrados como aprobados | Respuesta técnica ante entradas de prueba | Precisión general o validación clínica |
| 34 pruebas técnicas de robustez reportadas en el documento final | Reportadas, no reproducibles desde este repositorio | Vulnerabilidades ante variación y casos límite | Validación con usuarios |
| Validación con recepción o equipo veterinario | No realizada | — | No debe afirmarse que ocurrió |

## Protocolo propuesto

El documento final recomienda una evaluación futura independiente de las
pruebas técnicas. Un protocolo mínimo puede ejecutarse así:

1. Obtener aprobación del responsable de la clínica y definir participantes,
   finalidad, tratamiento de datos y criterio de interrupción.
2. Preparar al menos 80 casos nuevos y desidentificados que cubran las 12
   categorías, incluyendo mensajes claros, ambiguos y fuera de dominio.
3. Evitar datos personales y no reutilizar el conjunto de prueba empleado para
   medir el modelo.
4. Pedir a cada participante que lea el mensaje, observe la categoría sugerida
   y registre acuerdo o desacuerdo.
5. Ante desacuerdo, registrar la categoría esperada y una razón breve, sin
   convertir el ejercicio en diagnóstico o evaluación de prioridad clínica.
6. Evaluar por separado la comprensión de las alertas, el resultado no
   concluyente y la facilidad para escalar el caso a una persona.
7. Analizar resultados globales y por categoría, documentar incidentes y
   mantener toda decisión final bajo responsabilidad humana.

## Criterios sugeridos

- claridad de las categorías y de los mensajes de la interfaz;
- utilidad percibida para organizar la revisión;
- frecuencia y tipo de errores de clasificación;
- comprensión del score como estimación no calibrada;
- seguridad percibida de los guardrails;
- facilidad de corrección y escalamiento a una persona;
- casos en los que el sistema debería abstenerse.

## Resultados a reportar

Se deben reportar la proporción de acuerdo, el acuerdo por categoría, el número
y tipo de correcciones, las causas de desacuerdo, los incidentes y la percepción
de utilidad. Estos resultados no deben confundirse con exactitud clínica ni
con autorización para responder automáticamente.

Hasta ejecutar y documentar este protocolo, el estado seguirá siendo:
**validación con usuarios no realizada**.
