<div align="center">

# 🏛️ munisec: Infraestructura Municipal Segura

![Wazuh](https://img.shields.io/badge/SIEM-Wazuh-blue)
![Suricata](https://img.shields.io/badge/IDS%2FIPS-Suricata-red)
![pfSense](https://img.shields.io/badge/Firewall-pfSense-orange)

</div>

<br>

**munisec** es un proyecto integral de ciberseguridad que simula la infraestructura IT completa de un ayuntamiento ficticio: **el ayuntamiento de Guarroman**.

Fue desarrollado por un equipo de especialistas durante tres meses, y el proyecto abarca desde el diseño y despliegue de redes hasta la implementación de un SOC, ejecución de operaciones de Red Team, bastionado profundo, análisis forense y la aplicación de la normativa correspondiente como el ENS, RGPD, AEPD, etc.

<div align="center">
  <img src="assets/branding/00-portada.png" alt="Ayuntamiento de Guarroman" width="600"/>
</div>

## 📌 Origen del proyecto
El objetivo del proyecto era el siguiente: nos dividimos en 2 grupos ficticios, el equipo de **[Guarroman](https://github.com/joliher/munisec)** y el equipo de **[Benimerda](https://pablogonzalez-personalweb.lovable.app/proyectos/benimerda)**.

El proyecto se estructuró como un laboratorio realista donde en cada equipo se desplegarían dos sedes conectadas por VPN: el Ayuntamiento (Ayto) y la Casa de la Cultura (CC).

Se planificaron e implementaron las infraestructuras de red correspondiente a cada equipo y, una vez nos aseguramos de que ambos equipos estábamos preparados, procedimos a someter la infraestructura del equipo rival a pruebas de intrusión severas para poder practicar y aprender sobre habilidades de Red Team en un entorno lo más cercano a la realidad posible.

Además, ambos equipos tuvimos que enfrentarnos a incidentes reales de desastre físico (como una tormenta eléctrica) que forzaron la ejecución de *planes de recuperación ante desastres*.

El objetivo final fue diseñar, comprometer, recuperar y securizar completamente una red institucional, aplicando la normativa correspondiente.

## 🏗️ Arquitectura de Red

![Arquitectura de Red Pre-incidente](./assets/diagrams/network-topology-0.jpeg)

La topología de red del equipo de Guarroman se dividía en dos sedes físicas conectadas mediante un túnel VPN:

- **Ayuntamiento**: Sede principal que estaba compuesta por una DMZ, un Domain Controller (AD), un ERP (Odoo), un SIEM (Wazuh), varios equipos cliente para poder hacer pruebas contra el AD y el SIEM, y una red WiFi para uso exclusivo de los trabajadores.

- **Casa de la Cultura (CC)**: Sede secundaria, compuesta por una DMZ, varios equipos clientes que eran de uso público (simulando algo parecido al funcionamiento de una biblioteca) y una red WiFi también pública para cualquiera.

Ambas sedes tenían su propia salida a Internet de forma independiente, cada una con su propio router pfSense.

Posteriormente, se configuraron 2 túneles VPN:
- El primero sirvió para conectar ambos routers (pfSense) a través de una VPN **Wireguard**, lo que permitiría al **SOC** acceder a los equipos cliente de la **Casa de la Cultura**, así como permitiría a estos mismos equipos cliente unirse al AD para poder ser administrados desde ahí.

- El segundo se abrió para simular la necesidad de una empresa por querer ofrecer una modalidad de teletrabajo a sus trabajadores, permitiéndoles conectarse a la red empresarial sin necesidad de estar físicamente en el lugar.

Este segundo túnel se implementó **exclusivamente** en el Ayto dado que el router (pfSense del Ayto) ya se encontraba comunicado con la CC a través de VPN, por lo que no era necesario configurar un tercer túnel para este mismo propósito. Los teletrabajadores tendrían acceso a ambas sedes sin necesidad de configuración adicional.

**Incidente de Recuperación ante Desastres:**
Las VPNs se configuraron inicialmente en los pfSense, pero tras un fallo eléctrico (simulado) que dejó a los dispositivos inutilizables, se ejecutó un rediseño de emergencia y se redesplegaron ambos túneles directamente en los routers Linux internos mediante [JSBach](./software/jsbach/).

Después de eliminar los pfSense, la distribución final de la red quedó de la siguiente manera:

![Arquitectura de Red Post-incidente](./assets/diagrams/network-topology-1.jpeg)

## 📂 Estructura del Repositorio
Toda la documentación técnica se encuentra en la carpeta [`/docs`](./docs/).

### 🌐 Infraestructura y Redes
- [00. Arquitectura de Red](./docs/00-network-architecture.md) - Topología en detalle, VLANs, y routers (JSBach, pfSense).
- [01. Infraestructura y Servicios](./docs/01-infrastructure.md) - Active Directory, Odoo, DMZ.
- [02. SOC y SIEM](./docs/02-soc-siem.md) - Wazuh, Suricata, integración de alertas y VirusTotal.

### 🛡️ Blue Team & Defensa
- [03. Bastionado (Hardening)](./docs/03-hardening.md) - Aseguramiento de servidores, 2FA, iptables.
- [07. Respuesta a Incidentes](./docs/07-blue-team.md) - Gestión del desastre eléctrico y restauración.
- [08. Análisis Forense](./docs/08-forensics.md) - Metodología forense, volcado de memoria, scripts de automatización.
- [09. Cumplimiento Legal (ENS/RGPD)](./docs/09-compliance.md) - Adecuación al Esquema Nacional de Seguridad.

### ⚔️ Red Team & Ataque
- [04. Inteligencia de Fuentes Abiertas (OSINT)](./docs/04-osint.md) - Metodología de reconocimiento de perfiles gubernamentales del equipo de **Benimerda**.
- [05. Operaciones Red Team](./docs/05-red-team.md) - Informe completo de intrusión, desde el acceso inicial hasta la escalada a `root`.
- [06. Vulnerabilidades Identificadas](./docs/06-findings.md) - Matriz de hallazgos críticos.

## 👥 El Equipo
Este proyecto fue desarrollado por un grupo de 8 técnicos de ciberseguridad. Para consultar la aportación detallada de cada integrante a la infraestructura, pentesting, desarrollo de scripts y documentación, consulta:

👉 **[Contribuyentes y Asignación de Roles](./CONTRIBUTORS.md)**

## 📅 Timeline del Proyecto
- **Marzo 2026**: Planificación y despliegue de red, instalación de servidores Windows Server 2016 y Ubuntu 22.04 (JSBach), creación del AD y configuración inicial de OUs y endpoints.
- **Abril 2026**: Despliegue inicial de firewalls de frontera (pfSense) y túneles VPN. Instalación del SOC (Wazuh, Suricata y VirusTotal) y aplicación de GPOs en el AD. Se aplicó bastionado de tráfico inter-VLAN, 2FA en los servidores críticos e implementación de monitorización de logs. Gestión del incidente de DR por tormenta eléctrica e inicio de la recopilación OSINT.
- **Mayo 2026**: Finalización fase OSINT, ejecución de ataques dirigidos (Red Team), bastionado intensivo, desarrollo forense automatizado y generación de documentación legal simulada.

---
*Este proyecto fue desarrollado íntegramente en un entorno de laboratorio controlado para fines académicos y educativos.*
