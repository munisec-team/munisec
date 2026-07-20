# 👥 Contribuyentes y Roles

Este repositorio refleja el trabajo de un equipo de especialistas en ciberseguridad que diseñaron, desplegaron, atacaron y defendieron la infraestructura del Ayuntamiento de Guarromán.

A continuación se presenta un índice con los roles principales de cada miembro, seguido de un desglose técnico de sus aportaciones en las distintas fases del proyecto (Infraestructura, SOC, Red Team, Forense, etc.).

## 📌 Índice de Contribuyentes

| Miembro del Equipo | Rol Principal en el Proyecto | Enlace al Perfil |
| :--- | :--- | :--- |
| **Jose Luis Oliver (Joselu)** | Coordinador, Arquitecto de Red & Pentester | [Ver Perfil](#jose-luis-oliver-herranz-joselujolu) |
| **Carlos Delgado** | Especialista OSINT & Analista Forense | [Ver Perfil](#carlos-delgado) |
| **Enrique Cebrián (Kike)** | Arquitecto de Seguridad & Respuesta a Incidentes | [Ver Perfil](#enrique-cebrián-kike) |
| **Pau Roig** | Administrador de Sistemas y Web (DMZ) | [Ver Perfil](#pau-roig) |
| **Jorge Cortés** | Analista SOC (Tier 2/3) & Forense Digital | [Ver Perfil](#jorge-cortés) |
| **Alfonso Garrido (Alfon)** | Analista de Redes Seguras & Forense | [Ver Perfil](#alfonso-garrido-alfon) |
| **Luis Fuster** | Técnico de Despliegue masivo & Endpoint Security | [Ver Perfil](#luis-fuster) |
| **Marcos Bori** | Administrador Active Directory & SOC | [Ver Perfil](#marcos-bori) |

---

## 🏅 Desglose Técnico de Perfiles

### Jose Luis Oliver Herranz (Joselu/Jolu)
**Rol Principal**: Coordinador Técnico, Arquitecto de Red & VPN, Pentester (Red Team).
* **Arquitectura Infraestructura**: Diseño, planificación y despliegue inicial de la topología de red. Implementación y enrutamiento de túneles VPN (WireGuard) inter-sedes y teletrabajo.
* **JSBach y Contingencia**: Desarrollo y ejecución de los scripts de recuperación de emergencia (`backupJSBACH.sh` y `restoreJSBACH.sh`) durante el desastre eléctrico, rediseñando dinámicamente la topología para garantizar alta disponibilidad. Orquestación del Portal Cautivo para el WiFi público de la biblioteca.
* **Red Team**: Ejecución de vectores de ataque contra dispositivos de frontera (routers JSBach). Diseño de tácticas de intrusión y movimiento lateral hacia infraestructuras adyacentes, logrando con éxito la escalada de privilegios y el establecimiento de persistencia.
* **Blue Team / Hardening**: Despliegue de políticas estrictas de filtrado de paquetes (`iptables`), bastionado de servicios web mediante WAF (Apache ModSecurity), y centralización de la telemetría configurando el *log forwarding* de los equipos de red al SIEM (SOC).

### Carlos Delgado
**Rol Principal**: Especialista OSINT y Analista Forense
* **Infraestructura y AD**: Gestión de switches y configuración inicial de VLANs. Responsable de la integración y adición de múltiples equipos cliente (ej. PC-13, PC-25, PC-29) al dominio corporativo `guarroman.local`, asegurando su conectividad DNS.
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
* **SOC / SIEM**: Configuración avanzada de Wazuh y Suricata. Integración con inteligencia de amenazas (VirusTotal). Corrección de falsos positivos en reglas de detección.
* **Infraestructura**: Configuración física de red, cableado de switches, adición conjunta de endpoints al dominio y toma de decisiones para aplicar las directivas de seguridad (GPOs).
* **Forense**: Creación de *dumps* de memoria y uso de Volatility para análisis de incidentes.
* **Red Team**: Crackeo de contraseñas offline, fuerza bruta e inteligencia OSINT.

### Alfonso Garrido (Alfon)
**Rol Principal**: Analista de Redes Seguras y Forense
* **Infraestructura**: Soporte activo en la configuración y troubleshooting de la VPN inter-sedes. Apoyo a Joselu en la configuración de accesos HTTP/HTTPS del Portal Cautivo.
* **Hardening**: Bastionado intensivo de Apache (restricciones VLAN, ofuscación de versiones) y configuración HTTPS para todos los dispositivos de gestión.
* **Blue Team**: Implementación del sistema de logging centralizado (JSBach a SOC) y soporte al equipo forense.

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
* **SOC / Red**: Integración del manager de Wazuh e intento de restablecimiento de túneles VPN secundarios.
