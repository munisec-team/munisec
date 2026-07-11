# 🏛️ munisec: Infraestructura Municipal Segura

![Wazuh](https://img.shields.io/badge/SIEM-Wazuh-blue)
![Suricata](https://img.shields.io/badge/IDS%2FIPS-Suricata-red)
![pfSense](https://img.shields.io/badge/Firewall-pfSense-orange)

**munisec** es un proyecto integral de ciberseguridad que simula la infraestructura IT completa de un ayuntamiento ficticio: **el ayuntamiento de Guarroman**.
Fue desarrollado por un equipo de especialistas durante tres meses, y el proyecto abarca desde el diseño y despliegue de redes hasta la implementación de un SOC, ejecución de operaciones de Red Team, bastionado profundo, análisis forense avanzado así como seguir la normativa establecida para organismos públicos (ayuntamientos).

<div align="center">
  <img src="assets/branding/00-portada.png" alt="Ayuntamiento de Guarroman" width="600"/>
</div>

## 📌 Resumen Ejecutivo

El proyecto se estructuró como un laboratorio realista donde se desplegaron dos sedes conectadas por VPN: el Ayuntamiento (Ayto) y la Casa de la Cultura (CC).
Posteriormente, la infraestructura fue sometida a pruebas de intrusión severas, tanto propias como de un equipo rival, además de enfrentarse a incidentes reales de desastre físico (tormenta eléctrica) que forzaron la ejecución de *planes de recuperación ante desastres*.

El objetivo final fue diseñar, comprometer, recuperar y securizar completamente una red institucional, aplicando normativas como el **Esquema Nacional de Seguridad (ENS)** y el **RGPD**.

## 🏗️ Arquitectura de Red

La topología de red se divide en dos sedes físicas conectadas mediante un túnel VPN:

- **Ayuntamiento**: Sede principal, compuesta por varias VLANs:
    - 10.1.1.0/24 (VLAN 1 - Administración)
    - 10.1.2.0/24 (VLAN 2 - DMZ)
    - 10.1.3.0/24 (VLAN 3 - AD/Odoo)
    - 10.1.4.0/24 (VLAN 4 - SOC)
    - 10.1.5.0/24 y 10.1.6.0/24 (VLAN 5 y 6 - Trabajadores)
    - 10.1.99.0/24 (WiFi - Trabajadores)
Todas las IPs internas de esta sede pertenecen a la subred `10.1.x.x`.

- **Casa de la Cultura (CC)**: Sede secundaria, compuesta por:
    - 10.2.1.0/24 (VLAN 1 - Administración)
    - 10.2.2.0/24 (VLAN 2 - DMZ)
    - 10.2.15.0/24 y 10.2.16.0/24 (VLAN 15 y 16 - Biblioteca)
    - 10.2.99.0/24 (WiFi - Pública)
Las IPs de esta otra sede pertenecen a la subred `10.2.x.x`.

Ambas sedes tienen salida a Internet independiente, cada una con su propio router pfSense dedicado.
Inicialmente las VPNs se establecían a través de los pfSense (IPs públicas `172.29.230.160` y `.161`), pero tras un fallo eléctrico la VPN se redesplegó a través de routers Linux (JSBach).

*Ver diagrama de topología en [01-network-architecture.md](docs/01-network-architecture.md).*

## 📂 Estructura del Repositorio

Toda la documentación técnica se encuentra en la carpeta `/docs`.

### 🛡️ Blue Team & Defensa
- [01. Arquitectura de Red](docs/01-network-architecture.md) - Topología, VLANs, y routers (JSBach, pfSense).
- [02. Infraestructura y Servicios](docs/02-infrastructure.md) - Active Directory, Odoo, DMZ.
- [03. SOC y SIEM](docs/03-soc-siem.md) - Wazuh, Suricata, integración de alertas.
- [04. Bastionado (Hardening)](docs/04-hardening.md) - Aseguramiento de servidores, 2FA, iptables.
- [08. Respuesta a Incidentes](docs/08-blue-team.md) - Gestión del desastre eléctrico y restauración.
- [09. Análisis Forense](docs/09-forensics.md) - Metodología forense, volcado de memoria, scripts de automatización.
- [10. Cumplimiento Legal (ENS/RGPD)](docs/10-compliance.md) - Adecuación al Esquema Nacional de Seguridad.

### ⚔️ Red Team & Ataque
- [05. Inteligencia de Fuentes Abiertas (OSINT)](docs/05-osint.md) - Metodología de reconocimiento de perfiles gubernamentales.
- [06. Operaciones Red Team](docs/06-red-team.md) - Informe completo de intrusión, desde el acceso inicial hasta la escalada a `root`.
- [07. Vulnerabilidades Identificadas](docs/07-findings.md) - Matriz de hallazgos críticos.

## 👥 El Equipo

Este proyecto fue desarrollado por un grupo de 8 técnicos de ciberseguridad. Para consultar la aportación detallada de cada integrante a la infraestructura, pentesting, desarrollo de scripts y documentación, consulta:

👉 **[Contribuyentes y Asignación de Roles](CONTRIBUTORS.md)**

## 📅 Timeline del Proyecto

- **Marzo 2026**: Despliegue de red base, AD y primeras conexiones (JSBach/pfSense).
- **Abril 2026**: Implementación del SOC, monitorización de logs, y gestión del incidente de DR por tormenta eléctrica.
- **Mayo 2026**: Fases OSINT, ejecución de ataques dirigidos (Red Team), bastionado intensivo, y desarrollo forense automatizado.

---
*Este proyecto fue desarrollado íntegramente en un entorno de laboratorio controlado para fines académicos y educativos.*
