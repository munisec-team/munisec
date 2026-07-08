# 02. Infraestructura Central y Servicios

> **Participantes**: Pau Roig, Luis Fuster, Marcos, Equipo Completo
> **Periodo**: Marzo 2026 - Abril 2026

## Descripción General

La infraestructura de servidores base provee los servicios críticos del ayuntamiento: gestión de identidades, servicios web públicos e internos, y el sistema de planificación de recursos empresariales (ERP). Estos sistemas fueron desplegados mayoritariamente sobre sistemas operativos Windows Server 2016 y distribuciones de Linux (Ubuntu).

## Componentes Críticos

### 🔑 Active Directory (AD)

El Active Directory es el núcleo de la gestión de identidades del Ayuntamiento, alojado en la VLAN 3 (Servidores Internos).

* **Sistema Operativo**: Windows Server 2016.
* **Diseño Organizativo**: Se crearon Unidades Organizativas (OUs) lógicas para separar a los distintos departamentos, usuarios ficticios y perfiles de gestión (Alcaldía, Biblioteca, Funcionarios Base).
* **Políticas (GPOs)**: Se configuraron Directivas de Grupo para restringir el acceso a unidades de disco, forzar políticas de contraseñas robustas (posteriormente evadidas por ataques de diccionario), e instalar software predeterminado.
* **Integración**: Los endpoints de trabajo (Windows 10) de la VLAN 5 fueron unidos al dominio, permitiendo *Single Sign-On* (SSO) para los funcionarios simulados.

### 🌐 Infraestructura Web (DMZ)

La Zona Desmilitarizada (VLAN 2) aloja los servicios web accesibles desde el exterior, con el fin de aislarlos de la red corporativa en caso de compromiso.

* **Servidor Web Principal**: Apache HTTP Server sobre Linux.
* **CMS Público**: Despliegue de **WordPress** para la página institucional del Ayuntamiento, conectado a una base de datos MySQL gestionada vía phpMyAdmin.
* **Problemas de Seguridad Detectados**: Durante las fases iniciales, la DMZ presentaba configuraciones por defecto (como el panel phpMyAdmin expuesto sin restricciones de IP y contraseñas débiles en WordPress), lo que permitió la entrada inicial del Red Team.

### 💼 ERP / Gestión Interna

* **Plataforma**: Odoo (Open Source ERP).
* **Ubicación**: VLAN 3.
* **Propósito**: Simular la gestión interna municipal (inventario, nóminas, gestión de ciudadanos).

## Rutamiento Avanzado (JSBach)

El componente "JSBach" actuó como router dinámico inter-VLAN. Este servidor Linux, provisto inicialmente como una "caja negra" educativa, fue integrado y reconfigurado por el equipo.

Se crearon scripts de *backup* y restauración automática (`backupJSBACH.sh`) para mitigar la pérdida de configuraciones (tablas de enrutamiento y reglas iptables) en caso de reinicios abruptos, algo que demostró ser crucial durante el desastre eléctrico.

## Evidencias
*(Capturas de despliegue de AD y Odoo pendientes de adjuntar)*

