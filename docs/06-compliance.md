# 06. Normativa, Cumplimiento y Gobierno de Seguridad

> 👉 Para consultar el desglose exacto de tareas técnicas realizadas por cada miembro, revisa el **[Registro de Contribuyentes](../CONTRIBUTORS.md)**.<br>
> **Periodo**: Abril 2026 - Mayo 2026

## Descripción General

Tratándose de una Administración Pública local, el diseño, despliegue y operación de la infraestructura tecnológica del Ayuntamiento de Guarromán debieron adaptarse a los marcos normativos vigentes en España y la Unión Europea: el **Esquema Nacional de Seguridad (ENS)** (Real Decreto 311/2022) y el **Reglamento General de Protección de Datos (RGPD)** (Reglamento UE 2016/679).

* **Responsables del Área**: **Carlos Delgado**, **Luis Fuster**, **Alfonso Garrido** y **Enrique Cebrián**.

---

## 🏛️ 1. Alineación Técnica con el Esquema Nacional de Seguridad (ENS)

Para alcanzar una categoría de seguridad *Media/Alta*, se implementaron los siguientes controles técnicos y operativos exigidos por el ENS:

| Medida ENS | Denominación | Implementación Técnica en Guarromán |
| :--- | :--- | :--- |
| **[op.acc.1]** | Identificación y Autenticación | Despliegue de segundo factor de autenticación (2FA) por USB hardware en servidores críticos y doble factor en acceso a VPNs. |
| **[op.exp.2]** | Registro de Actividad | Recolección centralizada e inalterable de logs mediante Wazuh SIEM, Sysmon y rsyslog remoto desde switches TP-Link. |
| **[mp.info.6]** | Confidencialidad de la Información | Obligatoriedad de TLS 1.3/HTTPS en servicios web y cifrado en reposo con `gocryptfs` en los volúmenes del ERP Odoo. |
| **[op.cont.1]** | Plan de Continuidad de Negocio | Automatización de procedimientos de backup (`backupJSBACH.sh`) y plan de recuperación ante desastres (*Bare Metal recovery*). |

---

## 📜 2. Auditoría del Perfil CIS Benchmark en Wazuh (SCA)

A través del módulo **Security Configuration Assessment (SCA)** de Wazuh Manager, se auditó periódicamente el nivel de bastionado del servidor principal JSBach respecto al perfil oficial **CIS Benchmark para Ubuntu 24.04 LTS**:

* **Evaluaciones Automatizadas**: Frecuencia de escaneo cada 12 horas.
* **Métricas Obtenidas**: Identificación de configuraciones por defecto no seguras, eliminación de servicios innecesarios y verificación de permisos en archivos de sistema (`/etc/shadow`, `/etc/passwd`).

---

## ⚖️ 3. Cumplimiento del RGPD y Gestión de Brechas (AEPD)

En el ámbito organizativo y procedimental, se estructuraron las medidas obligatorias para la protección de datos de carácter personal:

* **Plan de Concienciación y Formación**: Impartición de sesiones de concienciación dirigidas por **Luis Fuster** al personal técnico y administrativo simulado para prevenir vectores de ingeniería social (*phishing*) y promover el uso seguro del correo corporativo.
* **Notificación Oficial de Brecha de Seguridad**: Tras la simulación de exfiltración de la base de datos por parte del equipo ofensivo, se redactó formalmente el documento de notificación de brecha de seguridad para su comunicación a la **Agencia Española de Protección de Datos (AEPD)** en un plazo inferior a 72 horas, detallando el alcance de los datos afectados y las medidas correctoras inmediatas.
