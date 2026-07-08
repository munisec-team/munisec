# 05. OSINT e Inteligencia de Fuentes Abiertas

> **Participantes**: Carlos Delgado, Pau Roig, Jorge Cortés
> **Periodo**: Abril 2026 - Mayo 2026

## Descripción General

La fase de inteligencia (OSINT - *Open Source Intelligence*) fue el primer paso crítico tanto para la defensa (evaluar la exposición propia) como para el ataque (obtener información del equipo rival, el Ayuntamiento de Benimerda). 

## Metodología

La investigación se centró en la huella digital dejada por los perfiles ficticios en plataformas reales de la web (redes sociales, foros, repositorios públicos).

### Objetivos Ofensivos (Reconocimiento del objetivo)
Se recabó información técnica y organizativa para preparar vectores de ataque:

1.  **Enumeración de Dominios e IPs**: Identificación de los puntos de entrada públicos (`172.29.230.x`).
2.  **Identificación de Personal Clave**: Se buscaron perfiles simulados (ej. administradores de sistemas, concejales) para crear diccionarios personalizados de fuerza bruta o correos de *spear-phishing*.
3.  **Filtración de Credenciales**: Búsqueda en bases de datos públicas de correos y contraseñas filtradas que hubieran sido reutilizadas por los administradores en el entorno del laboratorio. (El equipo logró obtener credenciales de acceso crítico mediante esta técnica).

### Inteligencia Defensiva (Autoprotección)
Carlos Delgado lideró una auditoría de la propia huella digital del Ayuntamiento de Guarromán:

*   Se analizaron los correos de los personajes ficticios (ej. `Baltasar Cañete`, `Dolores Expósito`) para identificar si habían sido comprometidos en brechas de datos de terceros (ej. HaveIBeenPwned).
*   Se limitó la información expuesta en el CMS público (WordPress) para mitigar la enumeración de usuarios (una vulnerabilidad común que facilita ataques de fuerza bruta).

## Resultados y Reportes

Se generaron informes formales detallando los hallazgos y proponiendo medidas de mitigación (concienciación de usuarios, políticas de contraseñas robustas). 

*Por razones de confidencialidad y respeto a la privacidad de los ejercicios del equipo rival, los informes PDF originales (que contienen nombres de alumnos) no se muestran públicamente, pero obran en poder del equipo para su consulta en entrevistas.*

