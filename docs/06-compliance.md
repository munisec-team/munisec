# 06. Normativa, Cumplimiento y Gobierno de Seguridad

> 👉 Para consultar el desglose exacto de tareas técnicas realizadas por cada miembro, revisa el **[Registro de Contribuyentes](../CONTRIBUTORS.md)**.<br>
> **Periodo**: Abril 2026 - Mayo 2026

## Descripción General

Tratándose de una Administración Pública local, el diseño, despliegue y operación de la infraestructura tecnológica del Ayuntamiento de Guarromán debieron adaptarse a los marcos normativos vigentes en España y la Unión Europea: el **Esquema Nacional de Seguridad (ENS)** (Real Decreto 311/2022) y el **Reglamento General de Protección de Datos (RGPD)** (Reglamento UE 2016/679).

* **Responsables del Área**: **Carlos Delgado**, **Luis Fuster**, **Alfonso Garrido**, **Enrique Cebrián (Kike)** y **Jorge Cortés**.
* **Elaboración Legal e Incidentes**: **Enrique Cebrián** y **Jorge Cortés** lideraron la redacción de la documentación legal de brechas, incidentes y cadena de custodia.

---

## 🏛️ 1. Alineación Técnica y Expediente ENS

Para alcanzar la acreditación en categoría de seguridad *Media/Alta*, se elaboró el expediente de adecuación y se implementaron los siguientes controles técnicos y operativos exigidos por el ENS:

* 📄 **Documento Oficial del Expediente**: **[Expediente_Normativo_ENS_Guarroman.pdf](../reports/compliance/Expediente_Normativo_ENS_Guarroman.pdf)**

### 🛡️ Medidas Técnicas Implementadas (RD 311/2022)

| Medida ENS | Denominación | Implementación Técnica en Guarromán |
| :--- | :--- | :--- |
| **[op.acc.1]** | Identificación y Autenticación | Despliegue de segundo factor de autenticación (2FA) en servidores críticos y doble factor en acceso a VPNs. |
| **[op.exp.2]** | Registro de Actividad | Recolección centralizada e inalterable de registros de actividad mediante Wazuh SIEM, Sysmon y rsyslog remoto desde switches TP-Link. |
| **[mp.info.6]** | Confidencialidad de la Información | Obligatoriedad de TLS 1.3/HTTPS en servicios web y cifrado en reposo con `gocryptfs` en los volúmenes del ERP Odoo. |
| **[op.cont.1]** | Plan de Continuidad de Negocio | Automatización de procedimientos de backup (**[`backupJSBach.sh`](../scripts/backup/backupJSBach.sh)**) y plan de recuperación ante desastres (*Bare Metal recovery*). |

---

## 📜 2. Auditoría de Protecciones y Configuración Segura (Wazuh SCA)

A través del módulo **Security Configuration Assessment (SCA)** de Wazuh Manager, se auditó el nivel de protección de los equipos y servidores del Ayuntamiento respecto a los estándares **CIS Benchmark**:

* **Evaluaciones Automatizadas**: Monitoreo continuo de las configuraciones de seguridad del sistema base.
* **Métricas Obtenidas**: Identificación de configuraciones por defecto no seguras, eliminación de servicios innecesarios y verificación de permisos estrictos en archivos de sistema (`/etc/shadow`, `/etc/passwd`).

---

## ⚖️ 3. Cumplimiento del RGPD y Gestión de Brechas (AEPD)

Ante simulaciones de robo de información y brechas de seguridad provocadas por incidentes operativos y actividades del Red Team, se redactaron los expedientes legales correspondientes:

### 📄 Expedientes Legales y Documentación Adjunta

1. **Notificación Oficial a la AEPD**:
   * Documento formal de comunicación de brecha de datos a la **Agencia Española de Protección de Datos (AEPD)** en un plazo inferior a 72 horas.
   * 📎 **[04-RGPD-Notificacion-Brecha-AEPD.docx](../reports/incident-response/04-RGPD-Notificacion-Brecha-AEPD.docx)**
2. **Cadena de Custodia de Evidencias Digitales**:
   * Procedimiento formal para garantizar la integridad, trazabilidad y validez judicial de las evidencias recolectadas durante las investigaciones forenses.
   * 📎 **[03-Cadena-Custodia-Evidencias.docx](../reports/incident-response/03-Cadena-Custodia-Evidencias.docx)**
3. **Informes de Incidentes**:
   * Documentación técnica y ejecutiva redactada tras la gestión de incidentes graves (como la caída por tormenta eléctrica y fallo de infraestructura).
   * 📎 **[01-Informe-Incidente-Inicial_Guarroman.pdf](../reports/incident-response/01-Informe-Incidente-Inicial_Guarroman.pdf)**
   * 📎 **[02-Informe-Ejecutivo-Incidente.docx](../reports/incident-response/02-Informe-Ejecutivo-Incidente.docx)**

---

## 👥 4. Medidas Organizativas, Concienciación y Gobierno

* **Plan de Concienciación y Formación**: Impartición de sesiones de concienciación sobre SIEM/Suricata, correo corporativo y buenas prácticas de seguridad dirigidas por **Luis Fuster** y el equipo técnico.
* **Gobierno y Políticas Organizativas**: Establecimiento de plantillas de acuerdos de confidencialidad para el personal y definición de las bases operativas del **Canal de Denuncias** interno de la entidad.
