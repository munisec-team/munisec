# 05. Operaciones Red Team (Pentesting)

> **Participantes**: Carlos Delgado, Pau Roig, Jose Luis Oliver
> **Periodo**: 12 de Mayo 2026 - 18 de Mayo 2026

## Descripción General

El equipo de Red Team ejecutó una auditoría de seguridad ofensiva simulando ser un atacante externo. El objetivo principal era comprometer la infraestructura del Ayuntamiento y lograr acceso privilegiado a los sistemas internos para identificar y reportar vulnerabilidades.

El ataque se realizó en una ventana de ~4 horas, logrando acceso completo como administrador (`root`) en el router principal (JSBach).

## Cadena de Ataque (Attack Chain)

El ataque siguió una progresión lineal, escalando privilegios y pivotando entre servicios.

### 1. Reconocimiento y Descubrimiento
Se inició con un escaneo pasivo y activo sobre el rango de IPs públicas.
*   **Vector Inicial**: Se identificó el panel de control de phpMyAdmin en la IP de la DMZ (`10.x.2.10/phpmyadmin`).
*   **Vulnerabilidad**: Panel expuesto a Internet sin restricciones de IP ni WAF.

### 2. Explotación Inicial (Initial Access)
*   **Fuerza Bruta**: Mediante diccionarios construidos en la fase de OSINT y herramientas automáticas, se atacó el panel phpMyAdmin.
*   **Hallazgo**: Se consiguieron credenciales válidas (usuario `root` con contraseña débil/por defecto `alumno`).
*   **Acceso a Base de Datos**: Acceso completo a la base de datos de WordPress (`wp_db`), donde se identificaron hashes de contraseñas de usuarios administradores.

### 3. Escalada a Nivel de Aplicación
*   **Vulnerabilidad en Base de Datos**: La tabla `wp_users` contenía una contraseña almacenada en texto plano para el usuario `adminwp`.
*   **Compromiso CMS**: Autenticación exitosa en el panel de control de WordPress (`/wp-admin`).

### 4. Ejecución de Código Remoto (RCE)
Una vez dentro de WordPress como administradores, el equipo plantó código malicioso.
*   **Técnica**: Inyección de una *Reverse Shell* (shell inversa) modificando el código PHP de una plantilla del tema de WordPress.
*   **Resultado**: Al visitar la página modificada, el servidor Apache devolvió una conexión a la máquina del atacante (Kali Linux), obteniendo una shell como el usuario de servicio `www-data`.

### 5. Escalada de Privilegios Local y Pivotaje
Desde el servidor web de la DMZ, el equipo buscó formas de escalar a `root` y saltar al router principal (JSBach).
*   **Escalada DMZ**: Explotación de vulnerabilidades locales en Ubuntu o malas configuraciones de permisos (SUDO) para obtener `root` en el servidor web.
*   **Pivote (Lateral Movement)**: Acceso al router JSBach, que actúa como puerta de enlace de todas las VLANs.
*   **Impacto Final**: Obtención de acceso `root` en JSBach, logrando el control total del tráfico de la red, capacidad de interceptar comunicaciones (MitM) y acceso irrestricto a la red interna (AD, SOC, Odoo).

## Evidencias
*(Ver capturas de pantalla de la ejecución de comandos y la reverse shell en la carpeta `reports/pentesting/` del repositorio).*

