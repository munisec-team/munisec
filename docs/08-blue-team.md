# 08. Blue Team y Respuesta a Incidentes (IR)

> **Participantes**: Kike, Jorge Cortés, Equipo Completo
> **Periodo**: Abril 2026 - Mayo 2026

## Descripción General

El equipo defensivo (Blue Team) se enfrentó no solo a las intrusiones lógicas simuladas por el Red Team, sino a un incidente físico real que puso a prueba la capacidad de resiliencia de la infraestructura: un desastre eléctrico.

## El Incidente Físico: Disaster Recovery (DR)

### Descripción del Evento
Durante las fases intermedias del proyecto, una tormenta eléctrica real provocó un corte de suministro y un pico de tensión en el laboratorio físico. Esto resultó en la pérdida de configuración de múltiples dispositivos de red (switches TP-Link y routers pfSense) que no contaban con sistemas de alimentación ininterrumpida (UPS).

### Acciones de Respuesta (Disaster Recovery)
1. **Evaluación de Daños**: Se constató la pérdida total de las tablas de enrutamiento y las reglas de firewall en los dispositivos de frontera (pfSense).
2. **Re-arquitectura Rápida**: Ante la imposibilidad de restaurar inmediatamente el hardware original, el equipo tomó la decisión técnica de descartar la capa de pfSense.
3. **Restauración de Servicios**: 
   - Se reasignaron las IPs públicas (172.29.230.160/161) directamente a las interfaces WAN de los routers internos Linux (JSBach).
   - Se re-estableció el túnel VPN directamente entre los dos JSBach.
   - Gracias a que el equipo había desarrollado previamente un script de backup de la configuración de JSBach (ackupJSBACH.sh), la restauración de iptables y tablas de enrutamiento de las VLANs internas fue casi inmediata.

### Documentación Legal Simulada
Para dar realismo al ejercicio, se generaron los documentos correspondientes que una Administración Pública debería emitir en un evento de este tipo:
- *Informe Ejecutivo del Incidente*.
- *Notificación de Brecha a la Agencia Española de Protección de Datos (AEPD)* (simulada).

*(Ver documentos en la carpeta ../reports/incident-response/)*

## Detección y Contención Lógica (Red Team vs Blue Team)

Durante el asalto del Red Team, el Blue Team utilizó las herramientas del SOC para monitorizar el progreso del ataque.

*   **Identificación Temprana**: Wazuh detectó los intentos iniciales de fuerza bruta contra el panel phpMyAdmin gracias a las reglas configuradas por el equipo.
*   **Análisis Forense en Caliente**: Una vez que el Red Team obtuvo la Reverse Shell, el Blue Team utilizó herramientas del sistema (Sysmon, 
etstat) para identificar el PID del proceso anómalo generado por el usuario www-data y rastrear la IP de destino de la shell (192.168.x.x - equipo del atacante).
*   **Contención Simulada**: Aunque se permitió al Red Team completar la cadena de ataque por motivos formativos, el Blue Team documentó los pasos exactos para la contención: *kill* del proceso anómalo, aislamiento de red de la VLAN 2 en JSBach, y limpieza de la plantilla PHP comprometida.
