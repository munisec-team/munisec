# 00. Arquitectura de Red y Topología

> [**Participantes y Contribuciones**](#créditos-y-responsables-de-red)<br>
> **Periodo**: Marzo 2026 - Mayo 2026

## Descripción General

La arquitectura de red del proyecto está diseñada para simular una infraestructura gubernamental distribuida en dos edificios físicos. El diseño inicial sufrió modificaciones importantes debido a contingencias físicas (desastres eléctricos) y decisiones de seguridad derivadas de las pruebas de penetración.

## Topología de Red Lógica

![Arquitectura de Red](../assets/diagrams/network-topology-1.jpeg)
*(Basado en el plano físico de diseño)*

La red está segmentada físicamente en dos ubicaciones, conectadas de forma segura a través de Internet público.

### 🏢 Ayuntamiento (Sede Principal)

El tráfico de entrada desde Internet se gestiona a través de un firewall **pfSense** (IP pública: `172.29.230.160`), que a su vez enruta hacia el router de distribución interno basado en Linux, denominado **JSBach**. 

Es este enrutador JSBach el encargado de gestionar y distribuir la red interna (`10.1.0.0/16`) hacia las siguientes VLANs, utilizando switches TP-Link. Todas las IPs internas de esta sede pertenecen a la subred `10.1.x.x`.

Ambas sedes tienen salida a Internet independiente, cada una con su propio router pfSense dedicado (con IPs "públicas" `172.29.230.160` y `.161` respectivamente).<br>

A continuación, se conectaron ambos pfSense a través de una VPN **Wireguard** de tipo Site-to-Site en la subred `10.200.0.0/30`.<br>
También se abrió un túnel VPN adicional (`10.201.0.0/24`) para simular a los trabajadores que quisieran teletrabajar en remoto. Este túnel se implementó exclusivamente en el Ayuntamiento.<br><br>

La segmentación interna de las VLANs de esta sede es la siguiente:

| VLAN | Subred | Propósito | Servicios / Equipos Críticos |
|------|--------|-----------|-----------------------------|
| **VLAN 1** | `10.1.1.0/24` | **Administración** | Gestión de red, switches, acceso privilegiado |
| **VLAN 2** | `10.1.2.0/24` | **DMZ (Desmilitarizada)** | Web corporativa (WordPress), servicios expuestos |
| **VLAN 3** | `10.1.3.0/24` | **Servidores Internos** | Active Directory (AD), Servidor Odoo (ERP) |
| **VLAN 4** | `10.1.4.0/24` | **SOC / Seguridad** | Servidor Wazuh Manager, Suricata NIDS |
| **VLAN 5** | `10.1.5.0/24` | **Oficinas / Trabajo** | Endpoints de funcionarios (Trabajo interno) |
| **VLAN 6** | `10.1.6.0/24` | **Oficinas / Trabajo** | Endpoints de funcionarios (Trabajo interno) |
| **WiFi** | `10.1.99.0/24` | **Wi-Fi Trabajadores** | Red inalámbrica para empleados del Ayuntamiento |

### 🏛️ Casa de la Cultura (Sede Secundaria)

Similar a la sede principal, el tráfico entra por un pfSense (IP pública: `172.29.230.161`), enrutado hacia el JSBach local. 

La red interna (`10.2.0.0/16`) es distribuida por el JSBach local y se segmenta en:

| VLAN | Subred | Propósito | Servicios / Equipos Críticos |
|------|--------|-----------|-----------------------------|
| **VLAN 1** | `10.2.1.0/24` | **Administración** | Gestión de switches locales |
| **VLAN 2** | `10.2.2.0/24` | **DMZ / Sistemas** | Equipos de soporte, mantenimiento y servicios expuestos |
| **VLAN 15**| `10.2.15.0/24`| **Biblioteca (Pública)** | Ordenadores de consulta pública (incluso para equipo rival) |
| **VLAN 16**| `10.2.16.0/24`| **Biblioteca (Pública)** | Ordenadores de consulta pública (incluso para equipo rival) |
| **WiFi** | `10.2.99.0/24` | **Wi-Fi Cultura** | Acceso inalámbrico público simulando la red de la biblioteca |

> **Control de Acceso Inalámbrico**: Ambas redes Wi-Fi (Ayuntamiento y Casa de la Cultura) restringen el tráfico mediante la implementación de un **Portal Cautivo**, forzando la autenticación de los usuarios a través de un servidor web Apache antes de proporcionar conectividad hacia otras VLANs o Internet.

## 🔐 Enlace Seguro: Evolución de la VPN

### Fase 1: Arquitectura Inicial (VPN sobre pfSense)
![Arquitectura de Red Pre-incidente](../assets/diagrams/network-topology-0.jpeg)

Inicialmente, la red dependía de los firewalls pfSense como único punto de entrada, estableciendo dos túneles VPN estratégicos:
- **Túnel Site-to-Site (WireGuard):** Conectaba las redes `10.1.0.0/16` y `10.2.0.0/16`. El objetivo principal era permitir que el SOC auditase los equipos de la Casa de la Cultura y que dichos equipos pudieran unirse al dominio (Active Directory) gestionado desde el Ayuntamiento.
- **Túnel de Teletrabajo:** Se implementó exclusivamente en el Ayuntamiento. Gracias a las tablas de enrutamiento existentes entre sedes, no fue necesario configurar un tercer túnel; los teletrabajadores obtenían acceso transparente a ambas infraestructuras conectándose al conectarse por VPN a la sede.

### Fase 2: Contingencia y Rediseño (VPN sobre JSBach)
Tras un incidente de sobretensión ("tormenta eléctrica") que dejó los equipos pfSense inutilizables, el equipo de red tomó la decisión arquitectónica de ejecutar un rediseño de emergencia, eliminando la capa de pfSense y exponiendo directamente los routers Linux internos ([JSBach](../software/jsbach/)) a Internet. 

![Arquitectura de Red Post-incidente](../assets/diagrams/network-topology-1.jpeg)

Se procedió a configurar los túneles VPN directamente entre los dos JSBach.

```bash
# Ejemplo conceptual del enrutamiento de contingencia implementado
sudo ip r a 10.2.0.0/16 via [IP_Túnel_Ayto]
sudo ip r a 10.1.0.0/16 via [IP_Túnel_CC]
```

## Créditos y Responsables de Red

La implementación, despliegue y mantenimiento de la infraestructura de red fue un esfuerzo netamente colaborativo. A continuación se detallan las áreas de enfoque donde cada miembro lideró o aportó valor técnico, extraídas directamente de la bitácora del proyecto:

### 🏛️ Jose Luis Oliver (Arquitecto de Red y Enrutamiento Core)
- **Ingeniería de Enrutamiento:** Despliegue y configuración de los routers Linux (JSBach) y firewalls pfSense como nodos de frontera.
- **Comunicaciones Seguras:** Extensa investigación e implementación de los túneles VPN (WireGuard), trabajando codo con codo con Alfonso para resolver problemas de enrutamiento y conectar ambas sedes.
- **Rediseño y Contingencia:** Reestructuración de la topología tras desastres de hardware, coordinando la eliminación de la capa pfSense y migrando los servicios de frontera directamente a los enrutadores JSBach.
- **Automatización y Resiliencia:** Desarrollo de scripts de `--backup` y `--restore` para recuperación ante desastres y ejecución de pruebas de Alta Disponibilidad eléctrica.
- **Bastionado y Topología:** Diseño de los esquemas de red lógicos y físicos definitivos apoyado por Kike y Alfonso, además de desplegar logging auditado en módulos críticos.

### 🛡️ Enrique Cebrián (Kike) (Soporte en Red y DR)
- **Despliegue Core:** Instalación y montaje de la nueva red para la Casa de la Cultura, colaborando en la puesta en marcha del router local.
- **Disaster Recovery (DR):** Responsable de las copias de seguridad de switches y routers previo a cortes eléctricos. Lideró la restauración de red completa paso a paso junto al resto del equipo tras la caída por sobretensión.
- **Planimetría y VPN:** Desarrollo conjunto del plano definitivo de red y apoyo directo a Marcos en la configuración del túnel VPN en la Casa de la Cultura.

### ⚙️ Alfonso Garrido (Alfon) (Firewall y Troubleshooting)
- **Firewalling y Bastionado:** Planteamiento, diseño y aplicación de reglas de firewall (iptables) para securizar las VLANs. Trabajó junto a Jolu en el bastionado de los accesos a los switches (migraciones HTTPS) y Apache.
- **Comunicaciones Seguras (VPN):** Soporte fundamental en la investigación y configuración de la VPN, actuando como cliente de pruebas (WireGuard) y colaborando activamente en la implementación sobre pfSense.
- **Troubleshooting de Red:** Diagnóstico y resolución de fallos críticos conjuntos (ej. problemas de NAT en pfSense o fallos de capa física en la Casa de la Cultura).

### 🛠️ Jorge Cortés (Switches y Troubleshooting)
- **Switching:** Configuración inicial, despliegue de VLANs y asignación de puertos en los switches administrables.
- **Troubleshooting VPN:** Diagnóstico y corrección de errores de enrutamiento en la VPN en colaboración con Jolu, identificando rutas estáticas faltantes para levantar los túneles.
- **Disaster Recovery (DR):** Colaboración estrecha con Kike en la creación de copias de seguridad pre-tormenta y participación activa en la restauración del servicio.

### 🔌 Marcos (Configuración Nodos CC)
- **Despliegue Core:** Instalación, descarga y configuración del nuevo router JSBach en la Casa de la Cultura (Ubuntu 24.04).
- **VPN y DMZ:** Configuración de la conectividad de la DMZ y despliegue del extremo de la VPN en la Casa de la Cultura apoyándose en Kike y Jolu.
- **Contingencia:** Restauración activa del JSBach del Ayuntamiento tras formateos.

### 📐 Carlos Delgado, Pau Roig y Luis Fuster
- **Carlos Delgado:** Configuración de las VLANs 6 y 7, limpieza de interfaces de red, y apoyo general en la reestructuración del montaje de red.
- **Pau Roig:** Montaje inicial de la red, elaboración del plano físico post-modificaciones y etiquetado estructurado del hardware.
- **Luis Fuster:** Asesoramiento estratégico en la topología de red, proponiendo optimizaciones de subnetting (de `/24` a `/30`) para aislar los enlaces de red.
