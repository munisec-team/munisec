# 🏛️ munisec: Infraestructura Municipal Segura

![Estado](https://img.shields.io/badge/Estado-Completado-success)
![Wazuh](https://img.shields.io/badge/SIEM-Wazuh-blue)
![Suricata](https://img.shields.io/badge/IDS%2FIPS-Suricata-red)
![pfSense](https://img.shields.io/badge/Firewall-pfSense-orange)

**munisec** es un proyecto integral de ciberseguridad que simula la infraestructura IT completa de un ayuntamiento (Guarromán). Desarrollado por un equipo de especialistas durante dos meses, el proyecto abarca desde el diseño y despliegue de redes corporativas hasta la implementación de un SOC, ejecución de operaciones de Red Team, bastionado profundo y análisis forense avanzado.

<div align="center">
  <img src="assets/branding/00-portada.png" alt="Ayuntamiento de Guarromán" width="600"/>
</div>

## 📌 Resumen Ejecutivo

El proyecto se estructuró como un laboratorio realista donde se desplegaron dos sedes conectadas por VPN (Ayuntamiento y Casa de la Cultura). Posteriormente, la infraestructura fue sometida a pruebas de intrusión severas, tanto propias como de un equipo rival, además de enfrentarse a incidentes reales de desastre físico (tormenta eléctrica) que forzaron la ejecución de planes de *Disaster Recovery*.

El objetivo final fue diseñar, comprometer, recuperar y securizar completamente una red institucional, aplicando normativas como el **Esquema Nacional de Seguridad (ENS)** y el **RGPD**.

## 🏗️ Arquitectura de Red

La topología de red se divide en dos sedes físicas conectadas mediante un túnel VPN:

- **Ayuntamiento**: Sede principal, con VLANs dedicadas para Administración (VLAN 1), DMZ (VLAN 2), AD/Odoo (VLAN 3), SOC (VLAN 4), y usuarios/clientes (VLAN 5, 6). Las IPs internas pertenecen a la subred `10.1.x.x`.
- **Casa de la Cultura (CC)**: Sede secundaria, con VLANs de Administración (VLAN 1, 2) y clientes (VLAN 15, 16). Las IPs internas pertenecen a la subred `10.2.x.x`.

Ambas sedes tienen salida a Internet independiente. Inicialmente las VPNs se establecían a través de dos pfSense (IPs públicas `172.29.230.160` y `.161`), pero tras un fallo eléctrico la VPN se redesplegó a través de routers Linux (JSBach).

*Ver diagrama de topología en [docs/01-network-architecture.md](docs/01-network-architecture.md).*

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
*Este proyecto fue desarrollado íntegramente en un entorno de laboratorio controlado para fines académicos y de entrenamiento avanzado.*
