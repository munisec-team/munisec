# 02. SOC, SIEM y Monitorización

> **Participantes**: Jorge Cortés, Kike, Luis Fuster, Marcos
> **Periodo**: Abril 2026 - Mayo 2026

## Descripción General

El Centro de Operaciones de Seguridad (SOC) fue alojado de forma aislada en la VLAN 4, con el objetivo de monitorizar, detectar y alertar sobre actividades anómalas en ambas sedes del Ayuntamiento. El *stack* de seguridad se basó en herramientas Open Source líderes en la industria.

## Arquitectura de Monitorización

### ?? Wazuh (SIEM & XDR)
El núcleo del SOC es el servidor Wazuh Manager. Se instalaron agentes de Wazuh en los servidores críticos (AD, WordPress, Odoo, JSBach) y en los endpoints de los funcionarios.

*   **Recolección de Logs**: Se centralizaron logs de sistema, autenticación (Event Log de Windows, `/var/log/auth.log` en Linux) y aplicaciones.
*   **Ajuste de Reglas (Tuning)**: Jorge Cortés lideró la corrección de reglas de detección por defecto que estaban generando una alta tasa de Falsos Positivos, adaptándolas a la casuística de tráfico legítimo del Ayuntamiento.

### ??? Suricata (NIDS/IPS)
Se integró el Sistema de Detección de Intrusos de Red (NIDS) Suricata para inspeccionar el tráfico inter-VLAN. Suricata alertaba directamente a Wazuh cuando detectaba firmas de ataques conocidos (ej. escaneos de Nmap, intentos de fuerza bruta, firmas de exploits web).

### ??? Sysmon (Endpoint Detection)
Luis Fuster configuró **Sysmon** (System Monitor de Sysinternals) en los endpoints Windows. Esta telemetría granular enriqueció los logs de Wazuh, permitiendo detectar:
*   Creación de procesos sospechosos.
*   Modificaciones en el registro de Windows.
*   Conexiones de red originadas por procesos anómalos.

### ?? Integración con VirusTotal
Se activó la integración nativa de Wazuh con la API de VirusTotal. Esto permitió que cualquier archivo nuevo modificado en los servidores clave (FIM - File Integrity Monitoring) fuera escaneado automáticamente contra la base de datos de VT en busca de malware.

## ?? Alertas y Automatización Temprana

Para reducir el *Time to Detect* (TTD), Kike y Pau desarrollaron un **bot de Telegram**.

*   El bot fue programado para realizar *health checks* continuos de los servicios críticos (Ping a JSBach, HTTP GET a WordPress).
*   En caso de pérdida de conectividad, el bot enviaba notificaciones Push inmediatas al grupo de administradores, lo que fue vital durante la simulación de caída de red (tormenta).

## Configuración Técnica

### Wazuh Manager (`ossec.conf`)

- **IP del SOC**: `10.1.4.138`
- **Recepción de logs**: syslog UDP 514 + secure TCP 1514
- **Integración VirusTotal**: activa para eventos FIM (syscheck), API key configurada
- **Integración Suricata**: lectura de `/var/log/suricata/eve.json` en formato JSON
- **SCA (Security Configuration Assessment)**: habilitado, perfil CIS Ubuntu 24.04 activo
- **Vulnerability Detection**: habilitado, actualización cada 60min
- **File Integrity Monitoring**: directorios `/etc`, `/usr/bin`, `/usr/sbin`, `/bin`, `/sbin`, `/boot` con frecuencia 12h; `/home/soc/Descargas` en tiempo real con `check_all` y `report_changes`
- **Rootcheck**: habilitado cada 12h (rootkits, trojans, puertos, procesos)
- **Syscollector**: inventario hardware, SO, red, paquetes, puertos, procesos, usuarios, servicios
- **Active response**: comandos definidos (`disable-account`, `firewall-drop`, `host-deny`, `route-null`) aunque sin reglas activas configuradas
- **Reglas personalizadas**: directorio `etc/rules/` y decoders en `etc/decoders/`

### Suricata — Reglas Personalizadas (21)

El equipo desarrolló reglas `local.rules` (SID 1200001-1200021) para detección específica:

| SID | Tipo | Descripción |
|-----|------|-------------|
| 1200001 | TCP | SYN scan (30 paq/3s) |
| 1200002 | TCP | FIN scan (20 paq/3s) |
| 1200003 | TCP | NULL/XMAS scan (20 paq/3s) |
| 1200004 | UDP | UDP scan (30 paq/5s) |
| 1200005 | ICMP | ICMP sweep (15 paq/3s) |
| 1200006 | TCP | Escaneo interno (movimiento lateral, 40 paq/5s) |
| 1200007 | HTTP | Fuerza bruta web (60 req/10s) |
| 1200008 | HTTP | Acceso a `/admin` (10 req/30s) |
| 1200009 | HTTP | Acceso a `/backup` (10 req/30s) |
| 1200010 | HTTP | Exposición de ficheros sensibles (`.env`, `.bak`, `.sql`, etc.) |
| 1200011 | HTTP | User-Agent curl/wget (10 req/60s) |
| 1200012 | HTTP | User-Agent de fuzzing (gobuster, ffuf, etc.) |
| 1200013 | TCP | Reverse shell `/dev/tcp` |
| 1200014 | TCP | Actividad Netcat |
| 1200015 | TCP | Ejecución de shell (`bash -i`, `/bin/sh`) |
| 1200016 | TCP | Posible beaconing (25 SYN/15s) |
| 1200017 | UDP | DNS tunneling (60 consultas/10s) |
| 1200018 | UDP | Consulta DNS anómala (>180 bytes) |
| 1200019 | TCP | Fuerza bruta SSH (20 intentos/60s) |
| 1200020 | TCP | Fuerza bruta RDP (25 intentos/60s) |
| 1200021 | TCP | Fuerza bruta SMB (25 intentos/60s) |

## Lecciones Aprendidas

1. **La ceguera de red es fatal**: Sin Suricata, el tráfico de reconocimiento inicial del Red Team pasó completamente inadvertido para el SOC.
2. **Alert Fatigue**: Antes del *tuning* de reglas realizado por Jorge, el volumen de alertas irrelevantes impedía a los analistas ver los eventos críticos reales.

