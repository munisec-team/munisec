# 07. Hallazgos y Vulnerabilidades (Findings)

> **Participantes**: Red Team (Carlos Delgado, Pau Roig, Jose Luis Oliver)
> **Periodo**: Mayo 2026

## Resumen Ejecutivo de Hallazgos

Como resultado de las pruebas de penetración (Red Team), se identificaron un total de **7 vulnerabilidades críticas/altas** en la infraestructura. Estas fallas abarcan desde configuraciones por defecto hasta credenciales en texto plano, permitiendo el compromiso total de la red.

A continuación se detalla la matriz de hallazgos.

---

### [CRÍTICO] 1. Exposición de Zabbix sin control de acceso
**Descripción**: El panel de monitorización Zabbix es accesible directamente desde el exterior (172.29.230.160/zabbix) sin restricción de IP de origen.
**Impacto**: Un atacante podría intentar ataques de fuerza bruta contra el panel de control o aprovechar vulnerabilidades conocidas (CVEs) en la versión instalada de Zabbix.
**Remediación**: Configurar el WAF o reglas en pfSense para bloquear el acceso a este panel desde Internet, limitándolo únicamente a las IPs de gestión de la VLAN 1 o VPN de administradores.

### [CRÍTICO] 2. Credenciales por defecto en Zabbix
**Descripción**: Zabbix mantiene las credenciales de instalación por defecto (Admin/zabbix).
**Impacto**: Compromiso total del panel de monitorización. Zabbix tiene capacidades de ejecución remota de comandos en los agentes instalados, lo que permite a un atacante ejecutar código malicioso como root/SYSTEM en todas las máquinas monitorizadas.
**Remediación**: Cambiar inmediatamente la contraseña por defecto del usuario Admin y deshabilitar cuentas no utilizadas.

### [CRÍTICO] 3. Exposición de phpMyAdmin en DMZ
**Descripción**: El gestor de bases de datos phpMyAdmin está expuesto al exterior (/phpmyadmin) en el servidor web.
**Impacto**: Permite intentos de acceso directo a la base de datos MySQL subyacente.
**Remediación**: Bloquear el acceso a la URI /phpmyadmin desde el exterior mediante la configuración de Apache o .htaccess, permitiendo acceso solo desde localhost o IPs de gestión.

### [ALTA] 4. Credenciales débiles en MySQL (phpMyAdmin)
**Descripción**: El usuario root de MySQL posee una contraseña extremadamente débil y predecible.
**Impacto**: Acceso administrativo total a todas las bases de datos alojadas (incluyendo WordPress).
**Remediación**: Aplicar políticas de contraseñas robustas para bases de datos, con una longitud mínima de 16 caracteres generados aleatoriamente.

### [CRÍTICO] 5. Contraseñas de WordPress en texto plano
**Descripción**: Se encontró un usuario de base de datos con la contraseña almacenada en texto plano dentro de la tabla de usuarios, evadiendo la función de hash estándar de WordPress.
**Impacto**: Permite a cualquier persona con acceso de lectura a la base de datos (incluso mediante una inyección SQL ciega) obtener credenciales válidas para el panel de administración web sin necesidad de crackear hashes.
**Remediación**: Forzar el reseteo de la contraseña del usuario afectado para que WordPress la almacene utilizando su algoritmo de cifrado.

### [ALTA] 6. Ejecución de Código a través del Editor de Temas
**Descripción**: La cuenta comprometida tenía permisos de Administrador en WordPress, lo que permite editar los archivos PHP del tema activo.
**Impacto**: El Red Team inyectó una Reverse Shell modificando la plantilla 404 del tema, logrando Ejecución de Código Remoto (RCE) en el servidor.
**Remediación**: Deshabilitar la edición de archivos desde el panel de control de WordPress añadiendo define('DISALLOW_FILE_EDIT', true); en wp-config.php.

### [MEDIA] 7. Archivos de sistema expuestos o sin proteger
**Descripción**: Varios archivos críticos de configuración o logs antiguos eran accesibles públicamente debido a falta de permisos en el sistema de archivos Linux.
**Impacto**: Fuga de información sensible que facilita posteriores vectores de ataque.
**Remediación**: Configurar los permisos correctos para archivos de configuración, asegurando que el propietario sea el usuario del servidor web.
