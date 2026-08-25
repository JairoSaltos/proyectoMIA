# Datos originales — no versionados

Esta carpeta documenta la procedencia y los controles esperados, pero **no
contiene los mensajes originales**. Las conversaciones y exportaciones de la
clínica no se publican para proteger la privacidad de tutores, pacientes y
personal.

## Procedencia reportada

El documento final del proyecto reporta mensajes digitales de WhatsApp
intercambiados con The Cat Clinic UIO. La unidad de análisis fue el mensaje
individual. También indica que la base disponible no contenía un identificador
de conversación suficiente para reconstruir de forma verificable cada
intercambio.

## Estructura general esperada

Una fuente controlada debería mantener, como mínimo:

- un identificador interno no personal del registro;
- el texto del mensaje desidentificado;
- el tipo general de emisor;
- la etiqueta de intención y su versión taxonómica;
- la procedencia, fecha de incorporación y transformaciones aplicadas;
- la relación entre un mensaje original y cualquier variante sintética.

Estos nombres describen requisitos generales y no afirman que exista un esquema
versionado con esos campos.

## Controles éticos y de privacidad

- No incorporar nombres, teléfonos, direcciones, correos, identificaciones,
  comprobantes, datos financieros, fotografías ni antecedentes identificables.
- Aplicar desidentificación y una segunda revisión de identificadores residuales.
- Mantener los originales en un entorno autorizado, con control de acceso,
  registro de cambios y política de conservación.
- Separar los datos de entrenamiento, validación y prueba antes de cualquier
  aumento sintético.
- Mantener las variantes sintéticas únicamente en entrenamiento y evitar que
  derivados de un mismo mensaje aparezcan en particiones diferentes.
- No usar los datos para decisiones clínicas automáticas.

## Condiciones de acceso

El acceso a datos originales requiere autorización del responsable de la
clínica y del equipo del proyecto, una finalidad académica definida y un
procedimiento de protección de datos. El repositorio Git no es un medio
autorizado para distribuirlos.

Para pruebas públicas, use únicamente ejemplos sintéticos o de demostración
descritos en [`../sample/README.md`](../sample/README.md).
