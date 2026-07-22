# 02. SOC, SIEM y Monitorización

> 👉 Para consultar el desglose exacto de tareas técnicas realizadas por cada miembro, revisa el **[Registro de Contribuyentes](../CONTRIBUTORS.md)**.<br>
> **Periodo**: Abril 2026 - Mayo 2026

## Descripción General

El Centro de Operaciones de Seguridad (SOC) se estableció como el núcleo de visibilidad y defensa del Ayuntamiento de Guarromán. Alojado de forma aislada en la **VLAN 4 (SOC / Seguridad)** (subred `10.1.4.0/24`), su función principal fue ingestar, correlacionar y analizar en tiempo real la telemetría generada por servidores, dispositivos de red y endpoints de ambas sedes (Ayuntamiento y Casa de la Cultura).

El *stack* tecnológico defensivo combinó herramientas de código abierto líderes en el sector: **Wazuh** como SIEM/XDR central, **Suricata** como NIDS/IPS perimetral e inter-VLAN, **Sysmon** para telemetría profunda en endpoints Windows, la **API de VirusTotal** para análisis automático de archivos y un **Bot de Telegram** propio para notificaciones instantáneas.

---

## 🛰️ Ingesta de Telemetría y Fuentes de Datos

La eficacia del SIEM dependió directamente del alcance y la granularidad de las fuentes de datos integradas en el Wazuh Manager (`10.1.4.138`):

### 1. Wazuh Agents (Servidores y Endpoints)
- **Instalación y Provisión**: Carlos Delgado ejecutó el despliegue del paquete `wazuh-agent` en los endpoints de trabajo Windows y servidores Ubuntu de la red corporativa, configurando el parámetro `WAZUH_MANAGER="10.1.4.138"` para establecer la conexión cifrada por el puerto `1514/TCP`.
- **Recolección de Logs de Autenticación**: A través del agente se auditaron de forma nativa los registros de autenticación del sistema (como los intentos de acceso SSH en `/var/log/auth.log` en Linux y los Event Logs en Windows).
- **Gestión de Agentes y Grupos**: Jorge Cortés centralizó el alta y la vinculación de claves (`manage_agents`) en el manager, organizando los nodos en grupos lógicos (`servidores-core`, `dmz-web`, `endpoints-funcionarios`) para aplicar políticas de monitorización diferenciadas.

### 2. Sysmon (EDR en Windows)
- Luis Fuster desplegó el ejecutable `Sysmon64.exe` (System Monitor de Sysinternals) junto a la plantilla de reglas `sysmonconfig.xml` en los sistemas Windows 10/Server del dominio.
- La telemetría de Sysmon se reenvió a Wazuh a través del canal de eventos de Windows (`Microsoft-Windows-Sysmon/Operational`), permitiendo auditar:
  - **Event ID 1**: Creación de procesos sospechosos (ej. `cmd.exe` o `powershell.exe` ejecutados por procesos no habituales).
  - **Event ID 3**: Conexiones de red originadas por binarios locales.
  - **Event ID 13**: Modificaciones en claves críticas del Registro de Windows (`HKLM\Software\Microsoft\Windows\CurrentVersion\Run`).

### 3. Log Forwarding Centralizado desde JSBach
- **Script Global de Log**: Alfonso Garrido diseñó e implementó el script **[`jsbach-logger.sh`](../software/jsbach/jsbach-logger.sh)** para estandarizar el registro de eventos del router Linux. Jose Luis Oliver colaboró en la integración del logging en los módulos de VPN WireGuard (`vpn_wg`) y scripts de backup.

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

- **Reenvío Syslog (`rsyslog`)**: Se desplegó el fichero de configuración **[`60-custom-log.conf`](../software/rsyslog/60-custom-log.conf)** en rsyslog para monitorizar `/var/log/jsbach/user-actions.log` mediante el módulo `imfile` y reenviar las alertas al Wazuh Manager (`10.1.4.138:514/UDP`).

```conf
# Muestra de 60-custom-log.conf:
input(type="imfile"
      File="/var/log/jsbach/user-actions.log"
      Tag="jsbach-actions:"
      Facility="local7")

local7.* @10.1.4.138:514
```

### 4. Syslog Remoto desde Switches TP-Link (Infraestructura Física)
- **Configuración de Hardware**: Carlos Delgado habilitó la transmisión de logs en los switches gestionables TP-Link hacia la IP del Wazuh Manager (`10.1.4.138:514/UDP`). Las configuraciones de respaldo de los switches se encuentran estructuradas por sede y función en **[`ayto-principal/sysConfigBackup.cfg`](../software/switch-tplink/ayto-principal/sysConfigBackup.cfg)**, **[`ayto-servidores/sysConfigBackup.cfg`](../software/switch-tplink/ayto-servidores/sysConfigBackup.cfg)** y **[`casa-cultura/sysConfigBackup.cfg`](../software/switch-tplink/casa-cultura/sysConfigBackup.cfg)**.

```cfg
# Muestra de configuración Syslog en switches TP-Link SG2210MP:
logging host index 1 10.1.4.138 6
```

- **Depuración y Decodificación**: Jorge Cortés, Pau Roig y Jose Luis Oliver colaboraron en la depuración del tráfico entrante y en la adaptación de los decodificadores de Wazuh para procesar las alertas del hardware de conmutación.

---

## ⚙️ Arquitectura del SIEM: Wazuh Manager (`ossec.conf`)

El servidor Wazuh Manager se desplegó en Ubuntu Server. El fichero de configuración completo utilizado en producción se encuentra en **[`ossec.conf`](../software/wazuh/ossec.conf)**. A continuación se resumen los módulos activos más relevantes:

- **File Integrity Monitoring (FIM / Syscheck)**: Auditoría de binarios del sistema (`/etc`, `/usr/bin`, `/sbin`, `/boot`) cada 12 horas, con monitorización en **tiempo real y reporte de cambios de contenido** en `/home/soc/Descargas`. Generación de alertas ante ficheros nuevos y exclusión de logs rotativos (`.log`, `.swp`).

```xml
<!-- Muestra de ossec.conf (FIM en tiempo real) -->
<directories check_all="yes" report_changes="yes" realtime="yes">/home/soc/Descargas</directories>
```

- **Inventario de Sistema (Syscollector)**: Escaneo horario de hardware, sistema operativo, interfaces de red, paquetes instalados, puertos abiertos, procesos, usuarios y servicios activos.
- **SCA (Security Configuration Assessment)**: Auditoría de bastionado contra el perfil **CIS Benchmark Ubuntu 24.04** cada 12 horas.
- **Detección de Vulnerabilidades**: Habilitada con actualización del feed de CVEs cada 60 minutos.
- **Rootcheck**: Escaneo cada 12 horas contra bases de datos de rootkits, troyanos y procesos/puertos anómalos.
- **Active Response**: Comandos definidos (`disable-account`, `firewall-drop`, `host-deny`, `route-null`) aunque sin reglas de disparo automático configuradas en producción.

---

## 🔬 Integración con VirusTotal (Escaneo de Malware)

Jorge Cortés configuró la integración nativa entre el motor FIM de Wazuh y la API de VirusTotal. Cada vez que un nuevo ejecutable o archivo sospechoso se creaba o modificaba en las rutas monitorizadas, Wazuh enviaba el hash (MD5/SHA256) a VirusTotal para comprobar su reputación.

### Configuración

La integración se habilitó insertando un bloque `<integration>` en **[`ossec.conf`](../software/wazuh/ossec.conf)**:

```xml
<!-- Muestra de integración con VirusTotal -->
<integration>
  <name>virustotal</name>
  <api_key><TU_API_KEY_VIRUSTOTAL></api_key>
  <group>syscheck</group>
  <alert_format>json</alert_format>
</integration>
```

### Reglas de Categorización

Las respuestas del API se procesaban mediante 7 reglas XML (IDs 87100 a 87106), disponibles en **[`0490-virustotal_rules.xml`](../software/wazuh/rules/0490-virustotal_rules.xml)**. El desglose de severidades es:

| Rule ID | Nivel | Descripción | Mapeo |
|:---:|:---:|:---|:---|
| 87100 | 0 | Mensaje base de integración VirusTotal | — |
| 87101 | 3 | Rate limit alcanzado (HTTP 204) | — |
| 87102 | 3 | Error de credenciales (HTTP 403) | GDPR IV 35.7.d |
| 87103 | 3 | Hash no encontrado en la base de datos de VT | — |
| 87104 | 3 | Hash encontrado, 0 positivos (fichero limpio) | — |
| **87105** | **12** | **Archivo detectado como malicioso por N motores** | **MITRE ATT&CK T1203**, PCI DSS 10.6.1 / 11.4 |
| 87106 | 3 | Timeout en la petición al API (HTTP 408) | GDPR IV 35.7.d |

---

## 🦈 NIDS Suricata & Ajuste de Reglas (Tuning)

Jorge Cortés, con el apoyo de Marcos en la corrección estructural de normas, integró **Suricata** enviando eventos en formato `eve.json` a Wazuh.

Para evitar la "fatiga de alertas" (*Alert Fatigue*), el equipo realizó un trabajo intensivo de *tuning*, ajustando umbrales de detección (*thresholds*) y creando un conjunto de **21 reglas personalizadas** (SID 1200001 a 1200021). El fichero completo de reglas está disponible en **[`local.rules`](../software/suricata/rules/local.rules)**.

```
# Muestra de regla local.rules:
alert tcp $HOME_NET any -> $HOME_NET any (msg:"Escaneo Interno Movimiento Lateral"; \
  flags:S; threshold: type threshold, track by_src, count 40, seconds 5; \
  sid:1200006; rev:1;)
```

Las reglas cubren las siguientes categorías de detección:

| Categoría | SIDs | Descripción |
|:---|:---:|:---|
| **Escaneo de Red Externo** | 1200001 - 1200005 | Detección de barridos SYN, FIN, NULL/XMAS, UDP e ICMP Sweep por umbral de paquetes/segundo |
| **Movimiento Lateral Interno** | 1200006 | Escaneo SYN originado desde `$HOME_NET` hacia `$HOME_NET` (40 paquetes / 5 segundos) |
| **Ataques Web** | 1200007 - 1200012 | Fuerza bruta HTTP POST, rastreo de `/admin` y `/backup`, exposición de ficheros sensibles (`.env`, `.sql`, `.bak`), User-Agents maliciosos (`curl`/`wget`) y fuzzing de directorios (`gobuster`/`ffuf`/`dirbuster`) |
| **Reverse Shells y C2** | 1200013 - 1200016 | Detección de `/dev/tcp`, `nc -e`, ejecución de `/bin/sh` y tráfico de tipo *beaconing* C2 |
| **Exfiltración DNS** | 1200017 - 1200018 | Volumen anómalo de consultas DNS (60/10s) y payloads DNS superiores a 180 bytes |
| **Fuerza Bruta por Servicio** | 1200019 - 1200021 | Ataques por umbral contra **SSH** (puerto 22), **RDP** (3389) y **SMB** (445) |

---

## 🤖 Alertas y Notificaciones Tempranas (Bot de Telegram)

Para garantizar un tiempo de respuesta inmediato ante caídas de servicio o alertas críticas de seguridad, el equipo desarrolló el bot de notificaciones **GuarromanBot**.

> 💡 **Código y Documentación del Bot**: La arquitectura completa y guía de despliegue del bot están documentados en **[`telegram-bot/README.md`](../software/telegram-bot/README.md)**.

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
