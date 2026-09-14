# 🚀 JSBach Router & Firewall Manager

**JSBach** es una solución de enrutamiento, gestión de redes y seguridad desarrollada a medida para la infraestructura del proyecto municipal. Actúa como el núcleo de comunicaciones de la red, gestionando desde el tráfico inter-VLAN hasta la seguridad perimetral.

Diseñado sobre una base Linux (Ubuntu), este software modular se planteó desde el inicio del proyecto como el principal orquestador de red para separar lógicamente los departamentos, aplicar portales cautivos y gestionar las políticas de acceso de cortafuegos.

## 🏗️ Módulos Principales (`/scripts`)

La arquitectura de JSBach se divide en múltiples scripts bash modulares, cada uno encargado de una función crítica de red:

- `tallafocs` / `tallafocs-old`: El núcleo del firewall. Gestiona las reglas de `iptables`, el filtrado de paquetes, la ofuscación de puertos y el NAT (Network Address Translation).
- `vpn_wg` / `vpn_wg_client`: Gestor automatizado de túneles VPN basados en WireGuard. Este módulo fue vital durante la simulación de contingencia eléctrica para levantar túneles Site-to-Site y Client-to-Site directamente desde el router.
- `portal_captiu`: Orquestador del Portal Cautivo basado en Apache. Controla el acceso a la red WiFi de invitados, especialmente en la sede de la Casa de la Cultura, restringiendo el tráfico hasta que el usuario se autentica.
- `dhcp`: Gestión dinámica de direcciones IP (DHCP) para los equipos cliente de las distintas VLANs.
- `dmz` / `wifi` / `bridge`: Módulos de configuración de interfaces y segmentación para aislar los servicios públicos y las redes inalámbricas del tráfico corporativo interno.

## 📝 Sistema de Logging

Para asegurar la trazabilidad y la auditoría de seguridad (esencial para el equipo SOC), el sistema incluye `jsbach-logger.sh`. 
Este script actúa como una función de logging global que captura eventos de todos los módulos (errores, levantamiento de túneles, bloqueos de firewall) y los inyecta tanto en el archivo local `/var/log/jsbach/user-actions.log` como en el demonio `syslog` para su posterior ingestión y alerta en SIEMs como Wazuh.

## 🔄 Integración con Backup y Disaster Recovery (Contingencia)

Aunque JSBach funcionaba como el enrutador principal, el equipo desarrolló de forma paralela e independiente scripts de *backup* y *restore* de estado. La capacidad de ejecutar estas copias (incluso si el servicio de JSBach estaba parado) para exportar las tablas de enrutamiento y las reglas de `iptables`, permitió al equipo restaurar las comunicaciones en tiempo récord tras el desastre eléctrico simulado que destruyó la capa de pfSense.
