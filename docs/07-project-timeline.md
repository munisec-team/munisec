# 07. Cronología de Operaciones y Bitácora (Timeline)

> 👉 Para consultar el desglose exacto de tareas técnicas realizadas por cada miembro, revisa el **[Registro de Contribuyentes](../CONTRIBUTORS.md)**.<br>
> **Periodo**: Marzo 2026 - Mayo 2026

## Descripción General

Este documento consolida la cronología operativa del proyecto de ciberseguridad del Ayuntamiento de Guarromán. Resume más de 260 entradas registradas en la bitácora técnica de operaciones, abarcando desde el diseño inicial hasta la fase defensiva y de recuperación.

---

## 🗓️ Hitos Operativos

### 1. Marzo 2026: Despliegue de Infraestructura Base
* **23 Mar - 31 Mar**:
  - Despliegue de nodos Ubuntu Server y estaciones de trabajo Windows (`WinCLI1`, `WinCLI2`).
  - Creación del direccionamiento IP corporativo (`10.x.x.x`) y configuración base del router Linux JSBach.
  - Instalación de Windows Server 2016 y levantamiento del bosque inicial de Active Directory (`guarroman.local`).

### 2. Abril 2026: Servicios, SOC y Operaciones OSINT
* **01 Abr - 15 Abr**:
  - Provisión e instalación del ERP Odoo en la **VLAN 3 (Servidores)** y despliegue del portal web en Apache en la **DMZ**.
  - Primeras reglas de filtrado `iptables` en JSBach y prueba inicial del WAF ModSecurity.
  - Incidente por fallo eléctrico: Reinstalación y reconfiguración de GPOs en el Active Directory.
* **16 Abr - 30 Abr**:
  - Despliegue del servidor central **Wazuh Manager** (`10.1.4.138`) e instalación masiva de `wazuh-agent`.
  - Fase de reconocimiento OSINT: Recopilación de huella digital y perfiles ficticios del Ayuntamiento objetivo.
  - Pruebas de interconexión VPN IPSec entre sedes.

### 3. Mayo 2026: Ataque, Bastionado, DFIR y Recuperación
* **01 May - 10 May**:
  - Desarrollo de scripts de adquisición forense de memoria RAM por **Alfonso Garrido** y **Carlos Delgado**.
  - **Desastre Físico (DRP)**: Fallo eléctrico masivo destruye los firewalls pfSense. Transición de emergencia de los túneles VPN WireGuard al router Linux JSBach mediante `backupJSBACH.sh`.
  - Despliegue de **Sysmon** en endpoints Windows y vinculación de eventos con Wazuh SIEM.
* **11 May - 18 May (Fase Ofensiva / Red Team)**:
  - Ejecución de la auditoría Red Team. Explotación de phpMyAdmin en DMZ, RCE en WordPress y obtención de acceso `root` en JSBach por sudoers permisivos.
  - Puesta en producción del **Bot de Telegram** (GuarromanBot) para notificaciones de alertas en tiempo real.
* **19 May - 26 May (Fase de Bastionado y Cierre)**:
  - Implementación de 2FA por USB hardware y cifrado de volúmenes con `gocryptfs`.
  - Auditoría forense continua sobre 8 activos mediante Volatility.
  - Redacción de informes ejecutivos, notificación de brecha a la AEPD y consolidación de documentación normativo-técnica (ENS).
