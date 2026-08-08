# 👥 Contribuyentes y Roles

Este repositorio refleja el trabajo de un equipo de especialistas en ciberseguridad que diseñaron, desplegaron, atacaron y defendieron la infraestructura del Ayuntamiento de Guarromán.

A continuación se presenta un índice con los roles principales de cada miembro, seguido de un desglose técnico de sus aportaciones en las distintas fases del proyecto (Infraestructura, SOC, Red Team, Forense, etc.).

## 📌 Estructura y División del Equipo

El proyecto se estructuró inicialmente dividiendo a los integrantes en dos equipos principales, con apoyo transversal:

* **🔴 Red Team (Equipo Ofensivo)**: **Jose Luis Oliver (Joselu)**, **Carlos Delgado** y **Pau Roig**. (Responsables de intrusión, pentesting, OSINT y explotación).
* **🔵 Blue Team (Equipo Defensivo)**: **Jorge Cortés**, **Enrique Cebrián (Kike)**, **Luis Fuster** y **Marcos Bori**. (Responsables de infraestructura, bastionado, Active Directory, SOC/SIEM, DFIR y respuesta a incidentes/legal).
* **🟣 Apoyo Transversal**: **Alfonso Garrido (Alfon)**. (Apoyo técnico activo tanto en tareas ofensivas como defensivas, desarrollo forense y redes).

> *Nota: Aunque miembros del Red Team apoyaron puntualmente en tareas de configuración o infraestructura (y viceversa), la responsabilidad y función principal se mantuvo según la división indicada.*

## 📌 Índice de Contribuyentes

| Miembro del Equipo | Equipo Principal | Rol Principal en el Proyecto | Enlace al Perfil |
| :--- | :--- | :--- | :--- |
| **Jose Luis Oliver (Joselu)** | 🔴 Red Team | Coordinador, Arquitecto de Red & Pentester | [Ver Perfil](#jose-luis-oliver-herranz-joselujolu) |
| **Carlos Delgado** | 🔴 Red Team | Especialista OSINT & Pentester | [Ver Perfil](#carlos-delgado) |
| **Pau Roig** | 🔴 Red Team | Pentester Web (DMZ) & OSINT | [Ver Perfil](#pau-roig) |
| **Jorge Cortés** | 🔵 Blue Team | Analista SOC (Tier 2/3) & Forense Digital | [Ver Perfil](#jorge-cortés) |
| **Enrique Cebrián (Kike)** | 🔵 Blue Team | Arquitecto de Seguridad & Respuesta a Incidentes | [Ver Perfil](#enrique-cebrián-kike) |
| **Luis Fuster** | 🔵 Blue Team | Técnico de Despliegue & Endpoint Security | [Ver Perfil](#luis-fuster) |
| **Marcos Bori** | 🔵 Blue Team | Administrador Active Directory & SOC | [Ver Perfil](#marcos-bori) |
| **Alfonso Garrido (Alfon)** | 🟣 Transversal | Analista de Redes Seguras, Desarrollador & Forense | [Ver Perfil](#alfonso-garrido-alfon) |

---

## 🏅 Desglose Técnico de Perfiles

### Jose Luis Oliver Herranz (Joselu/Jolu)
**Rol Principal**: Coordinador Técnico, Arquitecto de Red & VPN, Pentester (Red Team).
* **Arquitectura Infraestructura**: Diseño, planificación y despliegue inicial de la topología de red. Implementación y enrutamiento de túneles VPN (WireGuard) inter-sedes y teletrabajo.
* **JSBach y Contingencia**: Desarrollo y ejecución de los scripts de recuperación de emergencia (`backupJSBACH.sh` y `restoreJSBACH.sh`) durante el desastre eléctrico, rediseñando dinámicamente la topología para garantizar alta disponibilidad. Orquestación del Portal Cautivo para el WiFi público de la biblioteca.
* **Red Team**: Ejecución de vectores de ataque contra dispositivos de frontera (routers JSBach). Diseño de tácticas de intrusión y movimiento lateral hacia infraestructuras adyacentes, logrando con éxito la escalada de privilegios y el establecimiento de persistencia.
* **Blue Team / Hardening**: Despliegue de políticas estrictas de filtrado de paquetes (`iptables`), bastionado de servicios web mediante WAF (Apache ModSecurity), y apoyo a Alfonso en la finalización de las funciones de logging e integración del módulo VPN en `jsbach-logger.sh`.

### Carlos Delgado
**Rol Principal**: Especialista OSINT y Analista Forense
* **Infraestructura y AD**: Gestión de switches y configuración inicial de VLANs. Responsable de la integración y adición de múltiples equipos cliente (ej. PC-13, PC-25, PC-29) al dominio corporativo `guarroman.local`, asegurando su conectividad DNS.
* **SOC / Agentes**: Despliegue e instalación de agentes **Wazuh-Agent** en los equipos cliente de la red y configuración del servicio *Remote Log* (Syslog) en los switches TP-Link para enviar telemetría de conmutación al SIEM.
* **OSINT**: Investigación exhaustiva de objetivos y recopilación de huella digital, auditando los perfiles ficticios para identificar fugas en brechas de datos de terceros.
* **Forense**: Desarrollo de scripts automatizados para la extracción y análisis de memoria/logs.
* **Red Team**: Ejecución de fases de reconocimiento activo y vector de entrada.

### Enrique Cebrián (Kike)
**Rol Principal**: Arquitecto de Seguridad y Respuesta a Incidentes
* **Infraestructura y ERP**: Liderazgo en el despliegue e instalación del ERP **Odoo** en la red interna. Co-diseño estratégico de la estructura organizativa (OUs) del dominio Active Directory.
* **SOC**: Despliegue de Wazuh-Agent, integraciones y configuración de reglas.
* **Automatización**: Desarrollo del bot de Telegram para alertas tempranas de cambios de estado de servicios.
* **Hardening**: Diseño y aplicación de Directivas de Grupo (GPOs) críticas en Windows, implementación de 2FA por USB en servidores y cifrado gocryptfs.
* **Incident Response**: Liderazgo en la recuperación *Bare Metal* tras el fallo eléctrico masivo.

### Pau Roig
**Rol Principal**: Administrador de Sistemas y Web
* **Infraestructura Web (DMZ)**: Provisión e instalación del entorno Ubuntu para la DMZ. Despliegue del portal institucional en **WordPress** y blindaje inicial mediante la instalación de plugins de seguridad específicos.
* **OSINT / Red Team**: Recopilación de inteligencia y ejecución de vectores de ataque web.
* **Automatización**: Soporte en el desarrollo e integración de alertas por Telegram.
* **Documentación**: Elaboración de diagramas y digitalización del inventario de activos.

### Jorge Cortés
**Rol Principal**: Analista SOC (Tier 2/3) y Forense Digital
* **SOC / SIEM**: Configuración avanzada de Wazuh y Suricata. Integración con inteligencia de amenazas (VirusTotal). Corrección de falsos positivos en reglas de detección y depuración de la ingesta de Syslog remoto proveniente de los switches TP-Link junto a Carlos, Pau y Joselu.
* **Infraestructura**: Configuración física de red, cableado de switches, adición conjunta de endpoints al dominio y toma de decisiones para aplicar las directivas de seguridad (GPOs).
* **Forense**: Creación de *dumps* de memoria y uso de Volatility para análisis de incidentes.
* **Red Team**: Crackeo de contraseñas offline, fuerza bruta e inteligencia OSINT.

### Alfonso Garrido (Alfon)
**Rol Principal**: Analista de Redes Seguras y Forense
* **Infraestructura**: Soporte activo en la configuración y troubleshooting de la VPN inter-sedes. Apoyo a Joselu en la configuración de accesos HTTP/HTTPS del Portal Cautivo.
* **Hardening**: Bastionado intensivo de Apache (restricciones VLAN, ofuscación de versiones) y configuración HTTPS para todos los dispositivos de gestión.
* **Blue Team**: Investigación, diseño y creación del script de logging centralizado (`jsbach-logger.sh`) en JSBach para reenvío Syslog al SOC, y soporte al equipo forense.

### Luis Fuster
**Rol Principal**: Técnico de Despliegue y Endpoint Security
* **Endpoint e Infraestructura**: Despliegue masivo y desatendido de los sistemas operativos de los equipos cliente (Windows, Ubuntu Server) utilizando herramientas automatizadas (Ventoy).
* **SOC**: Instalación y configuración de **Sysmon** en endpoints Windows para nutrir de telemetría a Wazuh.
* **Blue Team / Hardening**: Participación activa en el debate, diseño y aplicación de las políticas de seguridad (GPOs) del Active Directory. Impartición de sesiones de concienciación de seguridad al equipo sobre el IDS Suricata.

### Marcos Bori
**Rol Principal**: Administrador Active Directory y SOC
* **Implementación AD Core**: Responsable de la instalación base de Windows Server 2016 y levantamiento del bosque inicial de Active Directory. Configuración de DNS, DHCP y creación de los grupos principales (`FUNCIONARIOS`, `ADMINISTRACION`) junto con sus recursos compartidos.
* **Mantenimiento**: Ejecución de tareas de limpieza y reestructuración del AD, eliminando configuraciones innecesarias para estabilizar el entorno.
* **Infraestructura Física**: Despliegue del router JSBach en la Casa de la Cultura.
* **SOC / Red**: Integración del manager de Wazuh, backup de normas y depuración/corrección de reglas de Wazuh y Suricata junto a Jorge, e intento de restablecimiento de túneles VPN secundarios.
