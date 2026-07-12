# 👥 Contribuyentes y Roles
Este repositorio refleja el trabajo de un equipo de especialistas en ciberseguridad. A continuación se detalla la contribución y especialización de cada miembro a lo largo del ciclo de vida del proyecto.

## 🏅 Miembros del Equipo

### Jose Luis Oliver Herranz (Joselu/Jolu)
**Rol Principal**: Coordinador Técnico, Arquitecto de Red & VPN, Pentester (Red Team).
* **Arquitectura Infraestructura**: Diseño, planificación y despliegue inicial de la topología de red. Implementación de túneles VPN (WireGuard) inter-sedes. Reingeniería y rediseño dinámico de la topología para asegurar la conectividad y alta disponibilidad de los servicios críticos bajo presión.
* **Red Team**: Ejecución de vectores de ataque contra dispositivos de frontera (routers JSBach). Diseño de tácticas de intrusión y movimiento lateral hacia infraestructuras adyacentes, logrando con éxito la escalada de privilegios y el establecimiento de persistencia.
* **Blue Team / Hardening**: Despliegue de políticas estrictas de filtrado de paquetes (`iptables`), bastionado de servicios web mediante WAF (Apache ModSecurity), y centralización de la telemetría configurando el *log forwarding* de los equipos de red al SIEM (SOC).
* **Gestión y Liderazgo**: Liderazgo técnico del equipo, coordinación de tareas, *troubleshooting* avanzado (resolución de bloqueos técnicos del resto de miembros) y orquestación de la respuesta ante caídas masivas de servicio.

### Carlos Delgado
**Rol Principal**: Especialista OSINT y Analista Forense
* **Infraestructura**: Gestión de switches, configuración inicial de VLANs y AD.
* **OSINT**: Investigación exhaustiva de objetivos y recopilación de huella digital.
* **Forense**: Desarrollo de scripts automatizados para la extracción y análisis de memoria/logs.
* **Red Team**: Ejecución de fases de reconocimiento activo y vector de entrada.

### Kike
**Rol Principal**: Arquitecto de Seguridad y Respuesta a Incidentes
* **SOC**: Despliegue de Wazuh-Agent, integraciones y configuración de reglas.
* **Automatización**: Desarrollo del bot de Telegram para alertas tempranas de cambios de estado de servicios.
* **Hardening**: Diseño de GPOs para Windows, implementación de 2FA por USB en servidores y cifrado gocryptfs.
* **Incident Response**: Liderazgo en la recuperación *Bare Metal* tras el fallo eléctrico masivo (Disaster Recovery).

### Pau Roig
**Rol Principal**: Administrador de Sistemas y Web
* **Infraestructura**: Gestión y securización de Active Directory y servicios web corporativos (WordPress).
* **OSINT / Red Team**: Recopilación de inteligencia y ejecución de vectores de ataque web.
* **Automatización**: Soporte en el desarrollo e integración de alertas por Telegram.
* **Documentación**: Elaboración de diagramas y digitalización del inventario de activos.

### Jorge Cortés
**Rol Principal**: Analista SOC (Tier 2/3) y Forense Digital
* **SOC / SIEM**: Configuración avanzada de Wazuh y Suricata. Integración con inteligencia de amenazas (VirusTotal). Corrección de falsos positivos en reglas de detección.
* **Infraestructura**: Configuración física de red, switches y soporte en la conexión de endpoints al dominio.
* **Forense**: Creación de *dumps* de memoria y uso de Volatility para análisis de incidentes.
* **Red Team**: Crackeo de contraseñas offline, fuerza bruta e inteligencia OSINT.

### Alfonso (Alfon)
**Rol Principal**: Analista de Redes Seguras y Forense
* **Infraestructura**: Soporte activo en la configuración y troubleshooting de la VPN inter-sedes y DMZ.
* **Hardening**: Bastionado intensivo de Apache (restricciones VLAN, ofuscación de versiones) y configuración HTTPS para todos los dispositivos de gestión.
* **Blue Team**: Implementación del sistema de logging centralizado (JSBach a SOC) y soporte al equipo forense.

### Luis Fuster
**Rol Principal**: Técnico de Despliegue y Endpoint Security
* **Endpoint**: Despliegue masivo de sistemas operativos base (Windows, Ubuntu Server) e integración en dominio.
* **SOC**: Instalación y configuración de **Sysmon** en endpoints Windows para nutrir de telemetría a Wazuh.
* **Blue Team / Hardening**: Desarrollo de políticas de seguridad locales (GPOs) e impartición de sesiones de concienciación de seguridad al equipo sobre el IDS Suricata.

### Marcos
**Rol Principal**: Administrador Junior Active Directory y SOC
* **Infraestructura**: Configuración básica de Unidades Organizativas y permisos en Windows Server. Despliegue del router JSBach en la Casa de la Cultura.
* **SOC / Red**: Integración del manager de Wazuh e intento de restablecimiento de túneles VPN secundarios.

