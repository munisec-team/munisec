# 03. SOC, SIEM y Monitorización

> **Participantes**: Jorge Cortés, Kike, Luis Fuster, Marcos
> **Periodo**: Abril 2026 - Mayo 2026

## Descripción General

El Centro de Operaciones de Seguridad (SOC) fue alojado de forma aislada en la VLAN 4, con el objetivo de monitorizar, detectar y alertar sobre actividades anómalas en ambas sedes del Ayuntamiento. El *stack* de seguridad se basó en herramientas Open Source líderes en la industria.

## Arquitectura de Monitorización

### 🦅 Wazuh (SIEM & XDR)
El núcleo del SOC es el servidor Wazuh Manager. Se instalaron agentes de Wazuh en los servidores críticos (AD, WordPress, Odoo, JSBach) y en los endpoints de los funcionarios.

*   **Recolección de Logs**: Se centralizaron logs de sistema, autenticación (Event Log de Windows, `/var/log/auth.log` en Linux) y aplicaciones.
*   **Ajuste de Reglas (Tuning)**: Jorge Cortés lideró la corrección de reglas de detección por defecto que estaban generando una alta tasa de Falsos Positivos, adaptándolas a la casuística de tráfico legítimo del Ayuntamiento.

### 🛡️ Suricata (NIDS/IPS)
Se integró el Sistema de Detección de Intrusos de Red (NIDS) Suricata para inspeccionar el tráfico inter-VLAN. Suricata alertaba directamente a Wazuh cuando detectaba firmas de ataques conocidos (ej. escaneos de Nmap, intentos de fuerza bruta, firmas de exploits web).

### 👁️ Sysmon (Endpoint Detection)
Luis Fuster configuró **Sysmon** (System Monitor de Sysinternals) en los endpoints Windows. Esta telemetría granular enriqueció los logs de Wazuh, permitiendo detectar:
*   Creación de procesos sospechosos.
*   Modificaciones en el registro de Windows.
*   Conexiones de red originadas por procesos anómalos.

### 🦠 Integración con VirusTotal
Se activó la integración nativa de Wazuh con la API de VirusTotal. Esto permitió que cualquier archivo nuevo modificado en los servidores clave (FIM - File Integrity Monitoring) fuera escaneado automáticamente contra la base de datos de VT en busca de malware.

## 🤖 Alertas y Automatización Temprana

Para reducir el *Time to Detect* (TTD), Kike y Pau desarrollaron un **bot de Telegram**.

*   El bot fue programado para realizar *health checks* continuos de los servicios críticos (Ping a JSBach, HTTP GET a WordPress).
*   En caso de pérdida de conectividad, el bot enviaba notificaciones Push inmediatas al grupo de administradores, lo que fue vital durante la simulación de caída de red (tormenta).

## Lecciones Aprendidas

1. **La ceguera de red es fatal**: Sin Suricata, el tráfico de reconocimiento inicial del Red Team pasó completamente inadvertido para el SOC.
2. **Alert Fatigue**: Antes del *tuning* de reglas realizado por Jorge, el volumen de alertas irrelevantes impedía a los analistas ver los eventos críticos reales.

