# 02. SOC, SIEM y Monitorización

> 👉 Para consultar el desglose exacto de tareas técnicas realizadas por cada miembro, revisa el **[Registro de Contribuyentes](../CONTRIBUTORS.md)**.<br>
> **Periodo**: Abril 2026 - Mayo 2026

## Descripción General

El Centro de Operaciones de Seguridad (SOC) se estableció como el núcleo de visibilidad y defensa del Ayuntamiento de Guarromán. Alojado de forma aislada en la **VLAN 4 (SOC / Seguridad)** (subred `10.1.4.0/24`), su función principal fue recibir, correlacionar y analizar en tiempo real la información de actividad generada por servidores, dispositivos de red y ordenadores de trabajo de ambas sedes (Ayuntamiento y Casa de la Cultura).

El conjunto de herramientas defensivas combinó soluciones de código abierto líderes en el sector: **Wazuh** como SIEM/XDR central, **Suricata** como sistema de detección de intrusiones perimetral e inter-VLAN, **Sysmon** para supervisión avanzada en ordenadores Windows, la **API de VirusTotal** para análisis automático de archivos y un **Bot de Telegram** propio para notificaciones instantáneas.

---

## 🛰️ Recolección de Datos y Fuentes de Información

La eficacia del SIEM dependió directamente del alcance y la granularidad de las fuentes de datos integradas en el Wazuh Manager (`10.1.4.138`):

### 1. Wazuh Agents (Servidores y Equipos de Trabajo)
- **Instalación y Provisión**: **Carlos Delgado** y **Jorge Cortés** ejecutaron el despliegue del paquete `wazuh-agent` en los ordenadores de trabajo Windows y servidores Ubuntu de la red corporativa, configurando el parámetro `WAZUH_MANAGER="10.1.4.138"` para establecer la conexión cifrada por el puerto `1514/TCP`.
- **Recolección de Logs de Autenticación**: A través del agente se auditaron de forma nativa los registros de autenticación del sistema (como los intentos de acceso SSH en `/var/log/auth.log` en Linux y los Event Logs en Windows).
- **Gestión de Agentes y Grupos**: Jorge Cortés centralizó el alta y la vinculación de claves (`manage_agents`) en el servidor central, organizando los equipos en grupos lógicos (`servidores-core`, `dmz-web`, `equipos-funcionarios`) para aplicar políticas de supervisión diferenciadas.

### 2. Sysmon (Supervisión Avanzada en Windows)
- Luis Fuster desplegó el ejecutable `Sysmon64.exe` (System Monitor de Sysinternals) junto a la plantilla de reglas `sysmonconfig.xml` en los sistemas Windows 10/Server del dominio.
- El registro de actividad de Sysmon se reenvió a Wazuh a través del canal de eventos de Windows (`Microsoft-Windows-Sysmon/Operational`), permitiendo auditar:
  - **Event ID 1**: Creación de procesos sospechosos (ej. `cmd.exe` o `powershell.exe` ejecutados por procesos no habituales).
  - **Event ID 3**: Conexiones de red originadas por programas locales.
  - **Event ID 13**: Modificaciones en claves críticas del Registro de Windows (`HKLM\Software\Microsoft\Windows\CurrentVersion\Run`).

### 3. Log Forwarding Centralizado desde JSBach
- **Script Global de Log**: Alfonso Garrido diseñó e implementó el script **[jsbach-logger.sh](../software/jsbach/jsbach-logger.sh)** para estandarizar el registro de eventos del router Linux. Jose Luis Oliver colaboró en la integración del registro de actividad en los módulos de VPN WireGuard (`vpn_wg`) y scripts de backup.

```bash
# Muestra de jsbach-logger.sh:
log_action() {
    local module="${1:-SYSTEM}"
    local action="${2:-UNKNOWN}"
    local details="${3:-}"
    local level="${4:-INFO}"

    local log_msg="[JSBACH][$module][$level] $action"
    logger -p "local0.$priority_level" "$log_msg" 2>/dev/null || true
}
```

- **Reenvío Syslog (`rsyslog`)**: Se desplegó el fichero de configuración **[60-custom-log.conf](../software/rsyslog/60-custom-log.conf)** en rsyslog para monitorizar `/var/log/jsbach/user-actions.log` mediante el módulo `imfile` y reenviar las alertas al Wazuh Manager (`10.1.4.138:514/UDP`).

```conf
# Muestra de 60-custom-log.conf:
input(type="imfile"
      File="/var/log/jsbach/user-actions.log"
      Tag="jsbach-actions:"
      Facility="local7")

local7.* @10.1.4.138:514
```

### 4. Syslog Remoto desde Switches TP-Link (Infraestructura Física)
- **Configuración de Hardware**: Carlos Delgado habilitó la transmisión de logs en los switches gestionables TP-Link hacia la IP del Wazuh Manager (`10.1.4.138:514/UDP`). Las configuraciones de respaldo de los switches se encuentran estructuradas por sede y función en **[`ayto-principal/sysConfigBackup.cfg`](../software/switch-tplink/ayto-principal/sysConfigBackup.cfg)**, **[`ayto-trabajadores/sysConfigBackup.cfg`](../software/switch-tplink/ayto-trabajadores/sysConfigBackup.cfg)** y **[`casa-cultura/sysConfigBackup.cfg`](../software/switch-tplink/casa-cultura/sysConfigBackup.cfg)**.

```cfg
# Muestra de configuración Syslog en switches TP-Link SG2210MP:
logging host index 1 10.1.4.138 6
```

- **Depuración y Adaptación**: Jorge Cortés, Pau Roig y Jose Luis Oliver colaboraron en la depuración del tráfico entrante y en la adaptación de los registros de Wazuh para procesar las alertas del hardware de red.

---

## ⚙️ Arquitectura del SIEM: Wazuh Manager (`ossec.conf`)

El servidor Wazuh Manager se desplegó en Ubuntu Server. El fichero de configuración completo utilizado en producción se encuentra en **[ossec.conf](../software/wazuh/ossec.conf)**. A continuación se resumen los módulos activos más relevantes:

- **Monitorización de Integridad de Archivos (FIM / Syscheck)**: Auditoría de archivos del sistema (`/etc`, `/usr/bin`, `/sbin`, `/boot`) cada 12 horas, con supervisión en **tiempo real y reporte de cambios de contenido** en `/home/soc/Descargas`. Generación de alertas ante ficheros nuevos y exclusión de registros temporales (`.log`, `.swp`).

```xml
<!-- Muestra de ossec.conf (FIM en tiempo real) -->
<directories check_all="yes" report_changes="yes" realtime="yes">/home/soc/Descargas</directories>
```

- **Inventario del Sistema (Syscollector)**: Escaneo horario de componentes de hardware, sistema operativo, interfaces de red, programas instalados, puertos abiertos, procesos, usuarios y servicios activos.
- **Evaluación de Protección (SCA)**: Auditoría de seguridad contra el perfil **CIS Benchmark Ubuntu 24.04** cada 12 horas.
- **Detección de Vulnerabilidades**: Habilitada con actualización automática del registro de fallos conocidos (CVEs) cada 60 minutos.
- **Rootcheck**: Escaneo cada 12 horas para detectar programas maliciosos ocultos (rootkits) o configuraciones anómalas.
- **Respuesta Automática (Active Response)**: Comandos de bloqueo definidos (`disable-account`, `firewall-drop`, `host-deny`, `route-null`), manteniendo el disparo bajo supervisión del equipo.

---

## 🔬 Integración con VirusTotal (Análisis de Malware)

Jorge Cortés configuró la integración entre el motor de supervisión de archivos de Wazuh y la API de VirusTotal. Cada vez que un nuevo programa o archivo sospechoso se creaba o modificaba en las rutas monitorizadas, Wazuh comprobaba automáticamente su huella (MD5/SHA256) en VirusTotal para verificar si contenía código dañino.

---

## 🦈 Sistema de Detección de Intrusiones Suricata (NIDS)

Jorge Cortés, con el apoyo de Marcos en la corrección de normas, integró **Suricata** enviando eventos en formato `eve.json` a Wazuh.

Para evitar la acumulación de avisos no urgentes (saturación por exceso de alertas), el equipo realizó una calibración cuidadosa, ajustando los umbrales de detección y creando un conjunto de **21 reglas personalizadas** (SID 1200001 a 1200021). El fichero completo de reglas está disponible en **[local.rules](../software/suricata/rules/local.rules)**.

```
# Muestra de regla local.rules:
alert tcp $HOME_NET any -> $HOME_NET any (msg:"Escaneo Interno Movimiento Entre Equipos"; \
  flags:S; threshold: type threshold, track by_src, count 40, seconds 5; \
  sid:1200006; rev:1;)
```

Las reglas cubren las siguientes categorías de detección:

| Categoría | SIDs | Descripción |
|:---|:---:|:---|
| **Escaneo de Red Externo** | 1200001 - 1200005 | Detección de rastreos y escaneos de red según el número de peticiones por segundo |
| **Movimiento entre Equipos Internos** | 1200006 | Escaneo originado entre equipos de la red interna (40 paquetes / 5 segundos) |
| **Ataques a Páginas Web** | 1200007 - 1200012 | Intentos de acceso por fuerza bruta, búsqueda de carpetas privadas (`/admin`, `/backup`), acceso a archivos sensibles (`.env`, `.sql`, `.bak`) y rastreo automatizado de webs |
| **Conexiones Remotas No Autorizadas** | 1200013 - 1200016 | Detección de consolas remotas (*Reverse Shells*) y conexiones salientes sospechosas |
| **Consultas Anómalas de Nombres (DNS)** | 1200017 - 1200018 | Volumen inusual de consultas de nombres de dominio o datos excesivamente grandes |
| **Fuerza Bruta a Servicios de Red** | 1200019 - 1200021 | Intentos repetidos de acceso a **SSH** (puerto 22), **Escritorio Remoto RDP** (3389) y **Acceso a Archivos Compartidos SMB** (445) |

---

## 🤖 Alertas y Notificaciones Tempranas (Bot de Telegram)

Para garantizar un tiempo de respuesta inmediato ante caídas de servicio o alertas críticas de seguridad, el equipo desarrolló el bot de notificaciones **GuarromanBot**.

> 💡 **Código y Documentación del Bot**: La arquitectura completa y guía de despliegue del bot están documentados en **[telegram-bot/README.md](../software/telegram-bot/README.md)**.

* **Desarrollo e Iteraciones**:
  - **Enrique Cebrián (Kike)**: Desarrollo del prototipo inicial de alertas en Bash (15 de abril) como prueba de concepto para comprobar disponibilidad de red por ICMP/puertos y errores en logs de Apache (`access.log` / `error.log`).
  - **Pau Roig Varea**: Desarrollo de la solución definitiva del **Bot de Telegram en Python** (20 de abril), unificando en una sola aplicación la comprobación del estado de los servicios (la lógica probada en el prototipo de Kike) junto con el parseo en tiempo real del JSON de alertas de Wazuh (`/var/ossec/logs/alerts/alerts.json`) y el envío de notificaciones push en Markdown.
  - **Carlos Delgado**: Integración de hooks `curl` en los scripts de **JSBach** (`vpn_wg`, `tallafocs`, `dhcp`, `portal_captiu`) para notificar automáticamente a Telegram si caía el túnel **VPN WireGuard**, el firewall **iptables**, o los servicios de **DHCP** y el **Portal Cautivo (Apache)**.

---

## 🛠️ Troubleshooting e Incidentes del SOC

La puesta en marcha de un SOC en producción conllevó resolver incidencias técnicas complejas:

1. **Reinstalación del Manager por Corrupción de API**:
   - Durante las pruebas iniciales del Bot de Telegram (1 de abril), peticiones síncronas masivas enviadas a la API del Wazuh Manager provocaron el colapso de la base de datos interna y la pérdida de comunicación con los agentes.
   - **Solución**: Kike lideró la reinstalación completa del Wazuh Manager, reconfigurando los parámetros de timeouts y aislando el bot para consumir únicamente alertas mediante lecturas asíncronas no bloqueantes de ficheros JSON.

2. **Depuración de Reglas y Falsos Positivos**:
   - Marcos y Jorge ejecutaron backups periódicos de las reglas y corrigieron errores sintácticos en el motor de decodificadores de Wazuh, logrando aislar el ruido del tráfico legítimo del Ayuntamiento para centrar la atención defensiva exclusivamente en los eventos reales del Red Team.

---

## 🎓 Formación y Concienciación Defensiva

El 15 de mayo de 2026, **Luis Fuster** impartió una sesión de concienciación y formación técnica dirigida al equipo interno del Ayuntamiento de Guarromán. 

En esta sesión se enseñó a interpretar los dashboards de Wazuh, entender la severidad de las firmas de Suricata y actuar coordinadamente ante notificaciones del bot de Telegram, asegurando que la tecnología desplegada fuera respaldada por un factor humano capacitado.
