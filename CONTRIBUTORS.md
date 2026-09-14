# 👥 Contribuyentes y Roles

Este repositorio refleja el trabajo de un equipo de estudiantes y recién titulados en ciberseguridad que diseñaron, desplegaron, auditaron y defendieron la infraestructura simulada del Ayuntamiento de Guarromán.

A continuación se presenta un índice con la distribución de equipos de cada miembro, seguido de un desglose técnico de sus aportaciones reales en las distintas fases del proyecto (Infraestructura, SOC, Red Team, Forense, etc.).

## 📌 Estructura y División del Equipo

El proyecto se estructuró inicialmente dividiendo a los integrantes en dos equipos principales, con apoyo transversal:

* **🔴 Red Team (Equipo Ofensivo)**: **Jose Luis Oliver (Joselu)**, **Carlos Delgado** y **Pau Roig**. (Auditoría de seguridad, pentesting, OSINT y vectores de ataque).
* **🔵 Blue Team (Equipo Defensivo)**: **Jorge Cortés**, **Enrique Cebrián (Kike)**, **Luis Fuster** y **Marcos Bori**. (Infraestructura, Active Directory, protección de equipos, monitorización SOC/SIEM, DFIR y documentación legal).
* **🟣 Apoyo Transversal**: **Alfonso Garrido (Alfon)**. (Apoyo técnico activo en configuración de redes, protección de equipos, scripting y desarrollo de la herramienta forense).

> *Nota: Aunque miembros del Red Team apoyaron en momentos puntuales en tareas de infraestructura o configuración (y viceversa), la responsabilidad y función principal se mantuvo según la división indicada.*

## 📌 Índice de Contribuyentes

| Miembro del Equipo | Equipo Principal | Rol Principal en el Proyecto | Enlace al Perfil |
| :--- | :--- | :--- | :--- |
| **Jose Luis Oliver (Joselu)** | 🔴 Red Team | Coordinación Técnica, Redes & Pentesting | [Ver Perfil](#jose-luis-oliver-herranz-joselujolu) |
| **Carlos Delgado** | 🔴 Red Team | Reconocimiento OSINT & Pentesting | [Ver Perfil](#carlos-delgado) |
| **Pau Roig** | 🔴 Red Team | Pentesting Web (DMZ), Bot de Telegram & OSINT | [Ver Perfil](#pau-roig) |
| **Jorge Cortés** | 🔵 Blue Team | Monitorización SOC (Wazuh/Suricata) & Análisis Forense | [Ver Perfil](#jorge-cortés) |
| **Enrique Cebrián (Kike)** | 🔵 Blue Team | Servicios (Odoo), Protecciones & Respuesta a Incidentes | [Ver Perfil](#enrique-cebrián-kike) |
| **Luis Fuster** | 🔵 Blue Team | Despliegue de Equipos, Supervisión de Ordenadores & Concienciación | [Ver Perfil](#luis-fuster) |
| **Marcos Bori** | 🔵 Blue Team | Despliegue Active Directory & Soporte SOC | [Ver Perfil](#marcos-bori) |
| **Alfonso Garrido (Alfon)** | 🟣 Transversal | Configuración de Redes, Scripting & Software Forense | [Ver Perfil](#alfonso-garrido-alfon) |

---

## 🏅 Desglose Técnico de Perfiles

### Jose Luis Oliver Herranz (Joselu/Jolu)
**Rol Principal**: Coordinación Técnica, Redes & Pentesting (Red Team).
* **Arquitectura de Red**: Diseño y planificación de la topología de red inter-sedes. Configuración de enrutamiento y túneles VPN (WireGuard) para comunicación entre sedes y accesos remotos.
* **JSBach y Contingencia**: Desarrollo del script de respaldo (`backupJSBach.sh`) y reconfiguración de contingencia del enrutador JSBach tras el fallo de los firewalls pfSense. Configuración del Portal Cautivo para el acceso WiFi de la biblioteca.
* **Red Team**: Ejecución de vías de acceso e intrusión interna. Pruebas de concepto para desplazamiento entre equipos internos, escalada de privilegios y persistencia.
* **Protección de Red**: Aplicación de políticas de filtrado `iptables`, refuerzo de seguridad en Apache mediante WAF ModSecurity y soporte en el script de registro centralizado de actividad (`jsbach-logger.sh`).

### Carlos Delgado
**Rol Principal**: Reconocimiento OSINT & Pentesting (Red Team).
* **OSINT**: Investigación de objetivos, recopilación de huella digital y auditoría de credenciales expuestas en brechas de datos de terceros para la fase ofensiva.
* **Red Team**: Ejecución de reconocimiento activo y apoyo en la entrada inicial.
* **Soporte de Red e Integración**: Configuración de switches TP-Link, incorporación de ordenadores de trabajo (PC-13, PC-25, PC-29) al dominio `guarroman.local` e instalación inicial de agentes `wazuh-agent`.

### Enrique Cebrián (Kike)
**Rol Principal**: Servicios, Protecciones & Respuesta a Incidentes (Blue Team).
* **Servicios e Infraestructura**: Instalación y despliegue del ERP **Odoo** en la red interna. Co-diseño de las Unidades Organizativas (OUs) en Active Directory.
* **Protecciones y Seguridad**: Configuración de Directivas de Grupo (GPOs) en Windows, autenticación 2FA en servidores y cifrado de volúmenes con `gocryptfs`.
* **Respuesta a Incidentes y Legal**: Desarrollo de notificaciones automáticas en Bash (prototipo del bot), reinstalación del Wazuh Manager tras corrupción de API y redacción de los documentos formales de notificación a la AEPD e informes de incidentes.

### Pau Roig
**Rol Principal**: Servicios Web DMZ, Bot de Telegram & Pentesting (Red Team).
* **Servicios Web DMZ**: Instalación del servidor Ubuntu en la DMZ, despliegue del portal institucional en **WordPress** y configuración inicial del servicio web.
* **OSINT & Red Team**: Apoyo en la recopilación de inteligencia de fuentes abiertas y ejecución de pruebas de intrusión web.
* **Bot de Telegram**: Desarrollo del **Bot de Telegram en Python (`GuarromanBot`)** para unificar el monitoreo del estado de servicios y el parseo en tiempo real de las alertas JSON de Wazuh.

### Jorge Cortés
**Rol Principal**: Monitorización SOC & Análisis Forense (Blue Team).
* **SOC / SIEM**: Despliegue de agentes **wazuh-agent** en ordenadores de trabajo junto a Carlos Delgado, configuración de Wazuh Manager y del IDS Suricata. Integración de la API de VirusTotal para análisis automático de muestras y ajuste de reglas personalizadas (`local.rules`) para reducción de falsos positivos.
* **Análisis Forense**: Inspección de volcados de memoria RAM con Volatility Framework para la detección de procesos ocultos y conexiones anómalas.
* **Infraestructura y Red Team**: Cableado y configuración física de switches, adición de ordenadores al dominio y pruebas de fuerza bruta/crackeo de contraseñas.

### Alfonso Garrido (Alfon)
**Rol Principal**: Configuración de Redes, Scripting & Software Forense (Transversal).
* **Redes y Protección**: Apoyo en la configuración de la VPN inter-sedes y refuerzo de seguridad en servidores web (Apache HTTPS, ocultación de versiones).
* **Scripting**: Desarrollo del script centralizado de registro de actividad `jsbach-logger.sh` en el router JSBach para el envío de eventos Syslog a Wazuh.
* **Software Forense**: Desarrollo y creación de la herramienta propia **[Forensic Suite Dashboard](software/forensic-suite-dashboard/)** (Flask/Python + Volatility 3) para automatizar el análisis forense y la generación de reportes HTML. Disponible en la carpeta local **[`software/forensic-suite-dashboard/`](software/forensic-suite-dashboard/)** y en su repositorio oficial de GitHub: **[alfgarpen/Forensic-Suite-dashboard](https://github.com/alfgarpen/Forensic-Suite-dashboard)**.

### Luis Fuster
**Rol Principal**: Despliegue de Equipos, Supervisión de Ordenadores & Concienciación (Blue Team).
* **Despliegue de Sistemas**: Instalación y aprovisionamiento de sistemas operativos en estaciones de trabajo y servidores mediante imágenes automatizadas.
* **Supervisión de Ordenadores**: Despliegue y configuración de **Sysmon** en ordenadores Windows para enviar eventos de ejecución y red al SIEM Wazuh.
* **Concienciación y GPOs**: Aplicación de Directivas de Grupo en Active Directory e impartición de sesiones de concienciación en ciberseguridad sobre alertas del SIEM/IDS para el personal.

### Marcos Bori
**Rol Principal**: Despliegue Active Directory & Soporte SOC (Blue Team).
* **Active Directory**: Instalación inicial de Windows Server 2016, promoción del controlador de dominio (`guarroman.local`), servicios DNS/DHCP y creación de cuentas de usuario y recursos compartidos.
* **Mantenimiento y SOC**: Tareas de mantenimiento en Active Directory, soporte en la integración de reglas de Wazuh y Suricata junto a Jorge, y despliegue del router JSBach en la Casa de la Cultura.
