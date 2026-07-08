# 11. Bitácora de Operaciones (Timeline)

Este documento es un resumen cronológico estructurado de la bitácora operativa original, que contiene más de 260 entradas detallando el progreso diario del equipo.

## Marzo 2026: Despliegue Base
**23 Mar - 31 Mar**
- **Inicio Operativo**: Despliegue de los primeros equipos Ubuntu Server y Windows (WinCLI1, WinCLI2).
- **Redes Fundamentales**: Creación del esquema de direccionamiento IP (10.x.x.x) y configuración inicial de los routers JSBach.
- **Identidad**: Instalación de Windows Server e inicio del despliegue del Active Directory.

## Abril 2026: Servicios, DMZ y Seguridad Inicial
**01 Abr - 15 Abr**
- **Servicios Corporativos**: Despliegue del ERP corporativo Odoo en la VLAN 3 e inicio del servidor Apache para la DMZ.
- **Defensa (Blue Team)**: Despliegue de iptables en JSBach para restringir el tráfico HTTP/SSH. Primera implementación del WAF ModSecurity.
- **Incidentes**: Un fallo de alimentación provocó la caída del Active Directory, obligando al equipo a restaurar las políticas de GPO desde cero (primera lección de DR).

**16 Abr - 30 Abr**
- **SOC & SIEM**: Instalación del servidor Wazuh Manager y despliegue masivo de agentes en los endpoints.
- **OSINT**: Inicio de la fase de inteligencia ofensiva y defensiva. Recopilación de perfiles de la Casa de la Cultura de Benimerda.
- **VPN**: Pruebas de configuración de túneles VPN IPSec entre los pfSense de ambas sedes.

## Mayo 2026: Ataque, Bastionado y Forense Automático
**01 May - 10 May**
- **Forense**: Desarrollo intensivo de scripts de adquisición de memoria por parte de Alfon y Carlos.
- **Desastre Físico (DR)**: La "tormenta eléctrica" destruye la configuración de los pfSense. El equipo ejecuta un rediseño de emergencia moviendo la terminación de la VPN a los routers Linux JSBach.
- **Endpoint Security**: Despliegue de Sysmon en las máquinas Windows y vinculación con Wazuh para telemetría avanzada.

**11 May - 18 May (Fase Roja)**
- **Operaciones Red Team**: El equipo lanza el ataque contra el ayuntamiento rival. Explotación exitosa de la DMZ (phpMyAdmin) y escalada a WordPress. Ejecución de código remoto (RCE) y compromiso final de oot en JSBach.
- **Automatización**: Despliegue funcional del bot de alertas de Telegram.

**19 May - 26 May (Fase de Consolidación)**
- **Hardening Final**: Configuración de reglas estrictas de 2FA por USB y despliegue del sistema de cifrado de archivos gocryptfs.
- **Auditoría Continua**: Generación ininterrumpida de reportes forenses automáticos desde el 13 de mayo, enviando datos horarios al servidor SOC para su escrutinio mediante Volatility.
- **Cierre Normativo**: Redacción de los informes ejecutivos finales, notificación de brecha a la AEPD y consolidación documental (ENS).
