# 01. Arquitectura de Red y Topología

> **Participantes**: Equipo de Infraestructura (Kike, Carlos, Jorge, Jose Luis, Alfonso)
> **Periodo**: Marzo 2026 - Mayo 2026

## Descripción General

La arquitectura de red del proyecto está diseñada para simular una infraestructura gubernamental distribuida en dos edificios físicos. El diseño inicial sufrió modificaciones importantes debido a contingencias físicas (desastres eléctricos) y decisiones de seguridad derivadas de las pruebas de penetración.

## Topología de Red Lógica

![Arquitectura de Red](../assets/diagrams/network_architecture.png)
*(Basado en el plano físico de diseño)*

La red está segmentada físicamente en dos ubicaciones, conectadas de forma segura a través de Internet público.

### 🏢 Ayuntamiento (Sede Principal)

El tráfico de entrada desde Internet se gestiona a través de un firewall **pfSense** (IP pública: `172.29.230.160`), que a su vez enruta hacia el router de distribución interno basado en Linux, denominado **JSBach**.

La red interna (`10.1.0.0/16`) se divide en las siguientes VLANs gestionadas por switches TP-Link:

| VLAN | Subred | Propósito | Servicios / Equipos Críticos |
|------|--------|-----------|-----------------------------|
| **VLAN 1** | `10.1.1.0/24` | **Administración** | Gestión de red, switches, acceso privilegiado |
| **VLAN 2** | `10.1.2.0/24` | **DMZ (Desmilitarizada)** | Web corporativa (WordPress), servicios expuestos |
| **VLAN 3** | `10.1.3.0/24` | **Servidores Internos** | Active Directory (AD), Servidor Odoo (ERP) |
| **VLAN 4** | `10.1.4.0/24` | **SOC / Seguridad** | Servidor Wazuh Manager, Suricata NIDS |
| **VLAN 5** | `10.1.5.0/24` | **Oficinas / Trabajo** | Endpoints de funcionarios |
| **VLAN 6** | `10.1.6.0/24` | **Wi-Fi Público** | Portal captivo para visitantes |

### 🏛️ Casa de la Cultura (Sede Secundaria)

Similar a la sede principal, el tráfico entra por un pfSense (IP pública: `172.29.230.161`), enrutado hacia el JSBach local. 

La red interna (`10.2.0.0/16`) se segmenta en:

| VLAN | Subred | Propósito | Servicios / Equipos Críticos |
|------|--------|-----------|-----------------------------|
| **VLAN 1** | `10.2.1.0/24` | **Administración** | Gestión de switches locales |
| **VLAN 2** | `10.2.2.0/24` | **Sistemas** | Equipos de soporte y mantenimiento |
| **VLAN 15**| `10.2.15.0/24`| **Biblioteca** | Ordenadores de consulta pública |
| **VLAN 16**| `10.2.16.0/24`| **Wi-Fi Cultura** | Acceso inalámbrico para estudiantes/usuarios |

## 🔗 Enlace Seguro: Evolución de la VPN

### Fase 1: VPN sobre pfSense
Inicialmente, se estableció un túnel VPN IPSec/WireGuard entre los dos dispositivos pfSense de frontera para conectar las redes `10.1.0.0/16` y `10.2.0.0/16`.

### Fase 2: Contingencia y Rediseño (VPN sobre JSBach)
Tras un incidente de sobretensión ("tormenta eléctrica") que dañó los equipos pfSense, el equipo de red tomó la decisión arquitectónica de eliminar la capa de pfSense y exponer directamente los routers Linux (JSBach) a Internet. 

Se procedió a configurar un nuevo túnel VPN directamente entre los dos JSBach.

```bash
# Ejemplo conceptual del enrutamiento de contingencia implementado
sudo ip r a 10.2.0.0/16 via [IP_Túnel_Ayto]
sudo ip r a 10.1.0.0/16 via [IP_Túnel_CC]
```

## Lecciones Aprendidas

1. **La segmentación de red es vital pero insuficiente si no hay filtrado**: Las pruebas del Red Team demostraron que la existencia de VLANs no previene el movimiento lateral si el firewall (iptables/pfSense) no bloquea explícitamente el tráfico inter-VLAN no autorizado.
2. **Alta disponibilidad**: La dependencia de un único dispositivo de frontera provocó la caída completa de la VPN tras un desastre físico. Un entorno de producción requeriría configuraciones CARP/VRRP para redundancia.

