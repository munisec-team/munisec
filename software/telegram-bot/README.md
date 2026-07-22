# 🤖 Telegram Alert Bot & Health Monitor (`GuarromanBot`)

**GuarromanBot** es el sistema de notificaciones push en tiempo real desarrollado para el Centro de Operaciones de Seguridad (SOC) y el equipo de administración del Ayuntamiento de Guarromán. 

Su función principal es reducir el tiempo de detección (TTD) y respuesta (TTR) enviando alertas instantáneas a un canal privado de Telegram ante caídas de servicios críticos o eventos de alta severidad registrados por el SIEM (Wazuh).

---

## 🏗️ Modos de Operación y Arquitectura

El bot opera integrando tres mecanismos complementarios:

### 1. Daemon Python para Alertas SIEM (Wazuh)
- **Función**: Proceso en segundo plano que realiza un seguimiento (*tailing*) en tiempo real del archivo de alertas JSON de Wazuh (`/var/ossec/logs/alerts/alerts.json`).
- **Lógica**: Filtra eventos con severidad `rule.level >= 7`, extrae la información del incidente (ID de regla, nivel, agente afectado, IP de origen y descripción) y emite un mensaje estructurado en Markdown al canal de Telegram.

### 2. Prototipo Bash de Disponibilidad de Servicios (Health Checks)
- **Función**: Script en Bash ejecutado mediante cron para sondear el estado de la infraestructura.
- **Lógica**: Realiza pings ICMP a las pasarelas y sondeos TCP a los puertos web (80/443). Además, parsea los registros de Apache (`access.log` y `error.log`) para notificar picos anormales de errores HTTP 40x/50x o accesos no autorizados.

### 3. Hooks Directos en Módulos de JSBach (`curl`)
- **Función**: Integración directa en los scripts de administración del router JSBach.
- **Lógica**: Hooks basados en `curl` insertados en los módulos `vpn_wg`, `tallafocs`, `dhcp` y `portal_captiu` que invocan el API de Telegram (`https://api.telegram.org/bot<TOKEN>/sendMessage`) para notificar caídas del túnel VPN WireGuard, cambios no autorizados en iptables o reinicios de servicios localmente.

---

## 📲 Formato de los Mensajes en Telegram

Los mensajes enviados al canal privado están formateados en Markdown para facilitar su lectura inmediata desde dispositivos móviles:

```markdown
🚨 [ALERTA SOC] Amenaza Detectada
• Regla: 87105 - VirusTotal: Archivo malicioso detectado
• Nivel: 12 (Crítico)
• Agente: servidor-odoo (10.1.3.10)
• IP Origen: 192.168.1.105
• Detalles: Coincidencia de hash SHA256 con firmas de malware en /home/soc/Descargas/
```

---

## ⚙️ Configuración y Variables de Entorno

Para habilitar la comunicación con la API de Telegram, se requieren las siguientes variables de configuración (sanitizadas):

```bash
# Credenciales del Bot de Telegram
TELEGRAM_BOT_TOKEN="<BOT_TOKEN_TELEGRAM>"
TELEGRAM_CHAT_ID="<CHAT_ID_CANAL_PRIVADO>"

# Endpoint API
TELEGRAM_API_URL="https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage"
```

---

## 👥 Créditos y Autores

- **Enrique Cebrián (Kike)**: Desarrolló el prototipo inicial en Bash (15 de abril) como prueba de concepto para comprobar disponibilidad de red (pings ICMP, puertos) y registros de Apache (`access.log` / `error.log`).
- **Pau Roig Varea**: Desarrolló la solución definitiva del **Bot de Telegram en Python** (20 de abril), unificando en una sola aplicación el motor de notificaciones push, la comprobación de estado de servicios que había probado Kike y el parseo en tiempo real de las alertas JSON de Wazuh (`alerts.json`).
- **Carlos Delgado**: Inyección de hooks `curl` en los módulos de JSBach (`vpn_wg`, `tallafocs`, `dhcp`, `portal_captiu`) para emitir alertas directas desde el router.
- **Jorge Cortés**: Pruebas de integración en laboratorio con el prototipo inicial y calibración de umbrales para evitar la fatiga de alertas (*Alert Fatigue*).
