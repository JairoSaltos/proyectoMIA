# Sistema inteligente de apoyo a recepción veterinaria

## Descripción del proyecto
Este proyecto desarrolla un prototipo basado en procesamiento de lenguaje natural para clasificar y priorizar solicitudes digitales recibidas por The Cat Clinic UIO.

El sistema utiliza un chat web prototipo para capturar mensajes de tutores, clasifica la intención mediante TF-IDF + Regresión Logística y muestra los resultados en un panel interno para recepción.

## Alcance
El sistema:
- Clasifica intención del mensaje.
- Asigna prioridad baja, media o alta.
- Marca posibles casos que requieren revisión veterinaria.
- Genera una sugerencia de respuesta revisable por recepción.

El sistema no:
- Realiza diagnóstico veterinario.
- Prescribe tratamientos.
- Envía respuestas automáticas.
- Se integra con WhatsApp Business o sistemas clínicos productivos.

## Estructura del repositorio
- `data/`: datos anonimizados o muestras de prueba.
- `notebooks/`: análisis exploratorio, entrenamiento y evaluación.
- `src/`: código fuente del prototipo.
- `models/`: referencia a modelos entrenados.
- `docs/`: documentación, bitácora y decisiones técnicas.

## Instalación
```bash
pip install -r requirements.txt
