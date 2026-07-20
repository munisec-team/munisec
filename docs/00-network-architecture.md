# 00. Arquitectura de Red y Topología

> 👉 Para consultar el desglose exacto de tareas técnicas realizadas por cada miembro, revisa el **[Registro de Contribuyentes](../CONTRIBUTORS.md)**.<br>
> **Periodo**: Marzo 2026 - Mayo 2026

## Descripción General

La arquitectura de red del proyecto está diseñada para simular una infraestructura gubernamental distribuida en dos edificios físicos. El diseño inicial sufrió modificaciones importantes debido a contingencias físicas (desastres eléctricos) y decisiones de seguridad derivadas de las pruebas de penetración.

## Topología de Red Lógica

![Arquitectura de Red](../assets/diagrams/network-topology-1.jpeg)
*(Basado en el plano físico de diseño)*

La red está segmentada físicamente en dos ubicaciones, conectadas de forma segura a través de Internet público.

### 🏢 Ayuntamiento (Sede Principal)

El tráfico de entrada desde Internet se gestiona a través de un firewall **pfSense** (IP pública: `172.29.230.160`), que a su vez enruta hacia el router de distribución interno, una solución a medida basada en Linux denominada **[JSBach](../software/jsbach/)**. 

> 💡 **Nota Técnica**: Este software propio se diseñó desde el inicio del proyecto como el orquestador principal de la red, encargándose de la creación de las VLANs, la asignación DHCP, el portal cautivo y el filtrado del cortafuegos interno. Para consultar su código y automatizaciones, visita la **[Documentación de JSBach](../software/jsbach/README.md)**.

Es este enrutador JSBach el encargado de gestionar y distribuir la red interna (`10.1.0.0/16`) hacia las siguientes VLANs, utilizando switches TP-Link. Todas las IPs internas de esta sede pertenecen a la subred `10.1.x.x`.

Ambas sedes tienen salida a Internet independiente, cada una con su propio router pfSense dedicado (con IPs "públicas" `172.29.230.160` y `.161` respectivamente).<br>

A continuación, se conectaron ambos pfSense a través de una VPN **Wireguard** de tipo Site-to-Site en la subred `10.200.0.0/30`.<br>

#### Distribución de VLANs (Ayuntamiento)

| VLAN ID | Nombre | Rango IP | Propósito |
| :---: | :--- | :--- | :--- |
| **1** | Gestión | `10.1.10.0/24` | Acceso a las interfaces de administración (Switches, pfSense, JSBach). Solo accesible por la IP de gestión `10.1.10.10`. |
| **2** | DMZ | `10.1.20.0/24` | Servicios expuestos al exterior (Portal Web institucional en WordPress y phpMyAdmin). Aislada de la red corporativa. |
| **3** | Servidores Internos | `10.1.30.0/24` | Servicios Core: Active Directory/DNS (Windows Server) y ERP Odoo. |
| **5** | Red Interna Corporativa | `10.1.50.0/24` | Equipos de trabajo de los empleados municipales (PC-13, PC-25, etc.) unidos al dominio. |
| **6** | Red Ocio (WIFI) | `10.1.60.0/24` | Red WiFi aislada, sin acceso a servidores internos. |

### 📚 Casa de la Cultura (Sede Secundaria)

Actúa como delegación. Su conexión a la red corporativa depende del túnel VPN principal hacia el Ayuntamiento. 
IP Pública: `172.29.230.161` (gestionada por su pfSense local).

#### Distribución de VLANs (Casa de la Cultura)

| VLAN ID | Nombre | Rango IP | Propósito |
| :---: | :--- | :--- | :--- |
| **11** | Gestión | `10.2.10.0/24` | Administración local de esta sede. |
| **14** | Biblioteca | `10.2.40.0/24` | Equipos públicos de consulta de la biblioteca. |
| **15** | Administración | `10.2.50.0/24` | Equipos corporativos de los empleados de la sede. |
| **16** | WIFI Biblioteca | `10.2.60.0/24` | Red inalámbrica para visitantes (protegida por el portal cautivo de JSBach). |
| **17** | SOC (Seguridad) | `10.2.70.0/24` | Infraestructura de monitorización defensiva (Wazuh SIEM y Suricata). Segmentada para evitar compromisos en cascada. |

## ⚠️ Rediseño de Contingencia (Disaster Recovery)

Durante la fase de simulación, la infraestructura sufrió un desastre eléctrico ("Tormenta en Guarromán") que destruyó ambos firewalls pfSense, cortando el acceso a Internet y destruyendo los túneles VPN que unían las sedes.

Debido a que el router Linux interno (**JSBach**) poseía un sistema modular de copias de seguridad de sus reglas de iptables y tablas de enrutamiento (ejecutado previamente por el equipo de forma preventiva), se procedió a un rediseño de emergencia:

1. Se eliminó la capa pfSense.
2. JSBach (Ayuntamiento) y JSBach (Casa de la Cultura) asumieron el rol de firewalls de frontera.
3. Se levantaron nuevos túneles **WireGuard** directamente entre los routers JSBach.
4. Se modificaron las tablas de enrutamiento para asegurar la continuidad del servicio (`10.1.0.0/16` ↔ `10.2.0.0/16`).

```bash
# Ejemplo conceptual del enrutamiento de contingencia implementado
sudo ip r a 10.2.0.0/16 via [IP_Túnel_Ayto]
sudo ip r a 10.1.0.0/16 via [IP_Túnel_CC]
```
