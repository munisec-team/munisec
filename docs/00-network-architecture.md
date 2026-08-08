# 00. Arquitectura de Red y Topología

> 👉 Para consultar el desglose exacto de tareas técnicas realizadas por cada miembro, revisa el **[Registro de Contribuyentes](../CONTRIBUTORS.md)**.<br>
> **Periodo**: Marzo 2026 - Mayo 2026

## Descripción General

La arquitectura de red del proyecto está diseñada para simular una infraestructura gubernamental distribuida en dos edificios físicos. El diseño inicial sufrió modificaciones importantes debido a contingencias físicas (desastres eléctricos) y decisiones de seguridad derivadas de las pruebas de penetración.

## Topología de Red Lógica

### 📐 Topología Inicial (Pre-Incidente)

![Arquitectura de Red Pre-Incidente](../assets/diagrams/network-topology-1.jpeg)
*(Plano de diseño inicial de la red)*

La red está segmentada físicamente en dos ubicaciones, conectadas de forma segura a través de Internet público.

### 🏢 Ayuntamiento (Sede Principal)

El tráfico de entrada desde Internet se gestiona a través de un firewall **pfSense** (IP pública: `172.29.230.160`), que a su vez enruta hacia el router de distribución interno, una solución a medida basada en Linux denominada **[JSBach](../software/jsbach/)**. 

> 💡 **Nota Técnica**: Este software propio se diseñó desde el inicio del proyecto como el orquestador principal de la red, encargándose de la creación de las VLANs, la asignación DHCP, el portal cautivo y el filtrado del cortafuegos interno. Para consultar su código y automatizaciones, visita la **[Documentación de JSBach](../software/jsbach/README.md)**.

Es este enrutador JSBach el encargado de gestionar y distribuir la red interna (`10.1.0.0/16`) hacia las siguientes VLANs, utilizando switches TP-Link. Todas las IPs internas de esta sede pertenecen a la subred `10.1.x.x`.

Ambas sedes tienen salida a Internet independiente, cada una con su propio router pfSense dedicado (con IPs "públicas" `172.29.230.160` y `.161` respectivamente).<br>

A continuación, se conectaron ambos pfSense a través de una VPN **WireGuard** de tipo Site-to-Site en la subred `10.200.0.0/30`.<br>
También se abrió un túnel VPN adicional (`10.201.0.0/24`) para simular a los trabajadores que quisieran teletrabajar en remoto. Este túnel se implementó exclusivamente en el Ayuntamiento.<br><br>

#### Distribución de VLANs (Ayuntamiento)

| VLAN | Subred | Propósito | Servicios / Equipos Críticos |
|------|--------|-----------|-----------------------------|
| **VLAN 1** | `10.1.1.0/24` | **Administración** | Gestión de red, switches, acceso privileged |
| **VLAN 3** | `10.1.3.0/24` | **Servidores Internos** | Active Directory (AD), Servidor Odoo (ERP) |
| **VLAN 4** | `10.1.4.0/24` | **SOC / Seguridad** | Servidor Wazuh Manager (`10.1.4.138`), Suricata NIDS |
| **VLAN 5** | `10.1.5.0/24` | **Oficinas / Trabajo** | Endpoints de funcionarios (Trabajo interno) |
| **VLAN 6** | `10.1.6.0/24` | **Oficinas / Trabajo** | Endpoints de funcionarios (Trabajo interno) |
| **WiFi** | `10.1.99.0/24` | **Wi-Fi Trabajadores** | Red inalámbrica para empleados del Ayuntamiento |

### 📚 Casa de la Cultura (Sede Secundaria)

Similar a la sede principal, el tráfico entra por un pfSense (IP pública: `172.29.230.161`), enrutado hacia el JSBach local. 

La red interna (`10.2.0.0/16`) es distribuida por el JSBach local y se segmenta en:

#### Distribución de VLANs (Casa de la Cultura)

| VLAN | Subred | Propósito | Servicios / Equipos Críticos |
|------|--------|-----------|-----------------------------|
| **VLAN 1** | `10.2.1.0/24` | **Administración** | Gestión de switches locales |
| **VLAN 2** | `10.2.2.0/24` | **DMZ / Sistemas** | Equipos de soporte, mantenimiento y servicios expuestos |
| **VLAN 15**| `10.2.15.0/24`| **Biblioteca (Pública)** | Ordenadores de consulta pública |
| **VLAN 16**| `10.2.16.0/24`| **Biblioteca (Pública)** | Ordenadores de consulta pública |
| **WiFi** | `10.2.99.0/24` | **Wi-Fi Cultura** | Acceso inalámbrico público simulando la red de la biblioteca |

> **Control de Acceso Inalámbrico**: Ambas redes Wi-Fi (Ayuntamiento y Casa de la Cultura) restringen el tráfico mediante la implementación de un **Portal Cautivo**, forzando la autenticación de los usuarios a través de un servidor web Apache antes de proporcionar conectividad hacia otras VLANs o Internet.

## 🔐 Enlace Seguro: Evolución de la VPN y Contingencia

### Fase 1: VPN sobre pfSense
Inicialmente, se estableció un túnel VPN IPSec/WireGuard entre los dos dispositivos pfSense de frontera para conectar las redes `10.1.0.0/16` y `10.2.0.0/16`.

### Fase 2: Contingencia y Rediseño (VPN sobre JSBach)

![Arquitectura de Red Definitiva (Post-Incidente)](../assets/diagrams/network-topology-2.jpeg)
*(Topología definitiva tras la caída de pfSense)*

Tras un incidente de sobretensión ("tormenta eléctrica") que dañó los equipos pfSense, el equipo de red tomó la decisión arquitectónica de eliminar la capa de pfSense y exponer directamente los routers Linux (JSBach) a Internet. 

Se procedió a configurar el nuevo túnel VPN directamente entre los dos JSBach.

```bash
# Ejemplo conceptual del enrutamiento de contingencia implementado
sudo ip r a 10.2.0.0/16 via [IP_Túnel_Ayto]
sudo ip r a 10.1.0.0/16 via [IP_Túnel_CC]
```
