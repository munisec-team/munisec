# 01. Infraestructura Central y Servicios

> **Participantes**: [Equipo de Infraestructura y Despliegue](#créditos-y-responsables-de-infraestructura)<br>
> **Periodo**: Marzo 2026 - Abril 2026

## Descripción General

La infraestructura de servidores base provee los servicios críticos del ayuntamiento: gestión de identidades centralizada (Active Directory), servicios web públicos (DMZ) e internos, y el sistema de planificación de recursos empresariales (ERP). Estos sistemas fueron desplegados mayoritariamente sobre ecosistemas híbridos (Windows Server 2016 y distribuciones GNU/Linux Ubuntu).

## Componentes Críticos

### 🔑 Active Directory (AD)

El Active Directory es el núcleo de la gestión de identidades del Ayuntamiento, alojado en la VLAN 3 (Servidores Internos). El dominio principal configurado fue `guarroman.local`.

* **Sistema Operativo**: Windows Server 2016.
* **Roles Implementados (Enfoque Híbrido)**: Aunque el servidor Windows centralizó el Active Directory y el DNS para la gestión del dominio, la asignación principal de red (DHCP) y la resolución de tráfico hacia Internet de los equipos cliente se gestionó apoyándose en el enrutador Linux principal. Esta decisión arquitectónica garantizaba que una caída temporal del Controlador de Dominio no dejase a la sede entera sin salida a Internet.
* **Diseño Organizativo**: Se crearon Unidades Organizativas (OUs) lógicas para separar a los distintos departamentos y perfiles de gestión, destacando los grupos `FUNCIONARIOS` y `ADMINISTRACION`, cada uno con permisos dedicados y carpetas compartidas aisladas.
* **Políticas (GPOs)**: Se configuraron Directivas de Grupo críticas basadas en nuestra guía de bastionado interna. Entre las más destacadas:
  - Desactivación forzada del protocolo inseguro **SMBv1** en todos los equipos.
  - Bloqueo de lectura, escritura y ejecución desde **dispositivos extraíbles (USB)**.
  - **Políticas de contraseñas robustas** (mínimo 12 caracteres y bloqueo tras 5 intentos fallidos), aunque posteriormente evadidas mediante ataques por el equipo rival.
  - Restricciones de Control de Cuentas de Usuario (UAC) y desactivación del AutoRun.
* **Integración**: Los endpoints de trabajo (Windows) de la VLAN 5 fueron unidos exitosamente al dominio `guarroman.local`, permitiendo el control centralizado de los trabajadores simulados.

> 💡 **Nota sobre el SOC (SIEM/IDS)**: Aunque la monitorización de toda esta infraestructura se realizó de forma constante, los detalles técnicos del despliegue de **Wazuh** y **Suricata** tienen su propio espacio detallado en el documento **[02. SOC y SIEM](02-soc-siem.md)**.

### 🌐 Infraestructura Web (DMZ)

La Zona Desmilitarizada (VLAN 2) aloja los servicios web accesibles desde el exterior, con el fin de aislarlos de la red corporativa interna en caso de compromiso.

* **Servidor Web Principal**: Servidor Ubuntu Linux corriendo Apache HTTP Server.
* **CMS Público (WordPress)**: Despliegue de un portal institucional para el Ayuntamiento. 
* **Seguridad y Hardening**: Inicialmente se detectaron problemas de seguridad (como paneles phpMyAdmin expuestos), lo cual fue remediado instalando y configurando plugins de seguridad específicos dentro del entorno de WordPress para blindar el acceso.

### 🏢 ERP / Gestión Interna

* **Plataforma**: Odoo (Open Source ERP).
* **Ubicación**: Servidor Linux en la VLAN 3 (Servidores Internos).
* **Propósito**: Simular la gestión interna municipal y servir como servicio corporativo de alto valor. Especialmente relevante fue la implementación del **módulo de Empleados**, el cual se nutrió con las identidades ficticias de los personajes asignados a la simulación (tales como el Alcalde o los bibliotecarios, cuyas fichas y roles se detallan en el documento de **[Inteligencia y OSINT](04-osint.md)**).

## Créditos y Responsables de Infraestructura

Basado en los registros extraídos de la bitácora técnica del proyecto, a continuación se detallan las responsabilidades específicas de cada miembro en la construcción de estos servicios:

### ⚙️ Marcos (Implementación AD Core)
- Instalación base de Windows Server 2016 y levantamiento del bosque inicial de Active Directory.
- Creación de los grupos principales (`FUNCIONARIOS`, `ADMINISTRACION`) y sus recursos compartidos.
- Ejecución de las tareas de limpieza y reestructuración del AD, eliminando configuraciones innecesarias y ordenando los permisos departamentales de la Casa de la Cultura y el Ayuntamiento.

### 🛡️ Enrique Cebrián (Kike) (Organización y Servicios)
- Liderazgo en la instalación y puesta en marcha del ERP **Odoo** en la red interna.
- Co-diseño estratégico de la estructura organizativa (OUs) del dominio para adaptarse a las necesidades de la simulación.
- Aplicación y configuración de las Directivas de Grupo (GPOs) junto a Luis y Jorge.

### 🌐 Pau Roig (Despliegue Web)
- Provisión e instalación de la máquina Ubuntu destinada a la DMZ.
- Despliegue del portal institucional en **WordPress**.
- Implementación de plugins de seguridad en WordPress para mitigar las vulnerabilidades de configuración iniciales.

### 🛠️ Carlos Delgado y Jorge Cortés (Endpoints y GPOs)
- **Carlos Delgado:** Responsable de integrar y añadir múltiples equipos cliente (ej. PC-13, PC-25, PC-29) al dominio `guarroman.local`, asegurando la conectividad DNS hacia el AD.
- **Jorge Cortés:** Colaboración directa en la adición de equipos al dominio y en la toma de decisiones para aplicar las directivas de seguridad (GPOs) del fichero de bastionado recomendado.

### 💻 Luis Fuster (Sistemas Cliente y GPOs)
- Despliegue e instalación masiva de los sistemas operativos de los equipos cliente (Windows) utilizando herramientas automatizadas (Ventoy).
- Participación activa en el diseño, debate y aplicación de las políticas de seguridad (GPOs) de Active Directory en el dominio, junto al equipo.
