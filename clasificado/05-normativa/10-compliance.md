# 10. Normativa y Cumplimiento Legal

> **Participantes**: Carlos Delgado, Luis Fuster, Alfonso, Kike
> **Periodo**: Abril 2026 - Mayo 2026

## Descripción General

Tratándose de una Administración Pública simulada, el diseño y operación de la infraestructura del Ayuntamiento de Guarromán debían alinearse con los marcos normativos españoles y europeos.

El equipo trabajó en la adaptación organizativa y técnica para cumplir con:
1. **Esquema Nacional de Seguridad (ENS)** (Real Decreto 311/2022).
2. **Reglamento General de Protección de Datos (RGPD)**.

## Adaptación Técnica (ENS)

Gran parte del esfuerzo defensivo del proyecto estuvo dictado por las medidas de seguridad exigidas por el ENS para sistemas de categoría *Media/Alta*:

*   **[op.acc.1] Identificación y Autenticación**: Implementación obligatoria de doble factor (2FA) en todos los accesos administrativos y VPNs.
*   **[op.exp.2] Protección de Registros de Actividad**: Despliegue del SIEM (Wazuh) para recolección centralizada e inalterabilidad de logs.
*   **[mp.info.6] Protección de la Confidencialidad**: Cifrado en tránsito (TLS obligatorio en DMZ e Intranet) y cifrado en reposo (gocryptfs) de la información sensible del ERP.
*   **[op.cont.1] Plan de Continuidad**: Creación de rutinas de backup automatizadas (ackupJSBACH.sh) para asegurar la recuperación rápida de la conectividad en caso de desastre (RTO minimizado).

## Medidas Organizativas (RGPD)

Desde el punto de vista procedimental, se elaboró documentación obligatoria para una entidad pública:

*   **Plan de Concienciación**: Material didáctico y sesiones impartidas a los perfiles de "funcionarios" simulados para prevenir ataques de *phishing* y el uso seguro del correo corporativo.
*   **Gestión de Brechas de Seguridad**: Redacción formal de la notificación de brecha de datos a la Agencia Española de Protección de Datos (AEPD), simulando el procedimiento legal a seguir tras la exfiltración de la base de datos perpetrada por el Red Team.
*   **Canal de Denuncias**: *(Información pendiente de adjuntar).*

*(Ver el documento de Notificación a la AEPD en la carpeta ../reports/incident-response/).*
