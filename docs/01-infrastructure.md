# 01. Infraestructura Central y Servicios

> 👉 Para consultar el desglose exacto de tareas técnicas realizadas por cada miembro, revisa el **[Registro de Contribuyentes](../CONTRIBUTORS.md)**.<br>
> **Periodo**: Marzo 2026 - Abril 2026

## Descripción General

La infraestructura de servidores base provee los servicios críticos del ayuntamiento: gestión de identidades centralizada, servicios web públicos e internos, y el sistema de planificación de recursos empresariales (ERP). Estos sistemas fueron desplegados mayoritariamente sobre ecosistemas híbridos (Windows Server 2016 y distribuciones GNU/Linux Ubuntu).

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
* **Diseño de Escenario (Vulnerable by Design)**: Con el objetivo de simular un entorno realista para las pruebas del Red Team, **se expuso intencionadamente un panel de phpMyAdmin**. Adicionalmente, se plantó una tabla señuelo (`wp_pass`) que contenía las contraseñas de los usuarios en texto plano. Esta "negligencia simulada" sirvió como vector de entrada clave para que el equipo rival lograse comprometer la infraestructura inicial y simular una exfiltración de credenciales. *(La explotación y el impacto de este vector se detallan en el documento **[04. Operaciones Red Team y Pentesting](04-red-team-pentesting.md)**).*
* **Seguridad y Hardening posterior**: Tras el compromiso, los fallos intencionados fueron remediados mediante el bastionado de los accesos y la instalación de plugins de seguridad específicos en el entorno de WordPress.

### 🏢 ERP / Gestión Interna

* **Plataforma**: Odoo (Open Source ERP).
* **Ubicación**: Servidor Linux en la VLAN 3 (Servidores Internos).
* **Propósito**: Simular la gestión interna municipal y servir como servicio corporativo de alto valor. Especialmente relevante fue la implementación del **módulo de Empleados**, el cual se nutrió con las identidades ficticias de los personajes asignados a la simulación (tales como el Alcalde o los bibliotecarios, cuyas fichas y roles se detallan en la sección de OSINT del documento **[04. Operaciones Red Team y Pentesting](04-red-team-pentesting.md#1-inteligencia-de-fuentes-abiertas-osint)**).
