# 03. Bastionado y Defensa en Profundidad (Hardening)

> 👉 Para consultar el desglose exacto de tareas técnicas realizadas por cada miembro, revisa el **[Registro de Contribuyentes](../CONTRIBUTORS.md)**.<br>
> **Periodo**: Mayo 2026

## Descripción General

Tras la evaluación de la postura de seguridad y el análisis de los ataques ejecutados por el Red Team, el equipo implementó una estrategia de defensa en profundidad. El objetivo fue reducir la superficie de ataque, restringir el movimiento lateral y proteger la integridad de los datos, siguiendo las directrices del Esquema Nacional de Seguridad (ENS).

## Medidas Implementadas

### 🛡️ Control de Acceso y Red

*   **Autenticación Fuerte (2FA)**: Se implementó un Doble Factor de Autenticación mediante tokens USB hardware para el acceso a sistemas críticos, previniendo ataques de fuerza bruta o robo de credenciales.
*   **Segmentación de Red y Firewalls Locales (iptables)**: Se configuraron reglas estrictas de `iptables` en el router JSBach y en los servidores.
    *   *Deny by default*: Bloqueo total del tráfico inter-VLAN, permitiendo solo puertos específicos (ej. 80/443 hacia la DMZ, 53 hacia el DNS del AD).
    *   *Restricción de Gestión*: Acceso SSH y HTTP(S) a los paneles de gestión (Switches, pfSense, JSBach) restringido exclusivamente a la IP del administrador en la VLAN 1.

### 🌐 Securización de Servicios Web

El servidor Apache que alojaba WordPress y phpMyAdmin en la DMZ fue objeto de un bastionado severo por parte de Alfonso tras detectar el uso del escenario vulnerable por parte del equipo rival:

*   **Ofuscación de Banners**: Modificación de las cabeceras HTTP (`ServerSignature Off`, `ServerTokens Prod`) para evitar la enumeración de versiones del servidor web y del sistema operativo.
*   **ModSecurity (WAF)**: Implementación del *Web Application Firewall* ModSecurity en Apache, con el conjunto de reglas OWASP Core Rule Set (CRS) para bloquear ataques de inyección SQL (SQLi), Cross-Site Scripting (XSS) e inclusiones de archivos locales (LFI/RFI).
*   **Cifrado en Tránsito**: Despliegue de certificados TLS/SSL forzando HTTPS en todas las comunicaciones web internas y externas.

### 💻 Endpoint, Datos y GPOs

*   **Cifrado de Datos en Reposo**: Implementación de **gocryptfs** en los servidores Ubuntu críticos para cifrar directorios sensibles, protegiendo la información en caso de acceso físico no autorizado al almacenamiento.
*   **Políticas de Active Directory**: Luis y Kike aplicaron políticas globales (GPOs) desde el AD para asegurar los endpoints del dominio. A continuación se detalla el checklist de políticas aplicadas:

#### 📜 Checklist de Directivas de Grupo (GPOs)

**Firewall y Protocolos Inseguros**
- [x] Firewall de Windows activo en todos los equipos del dominio.
- [ ] *Auditoría*: Verificar que los equipos de Benimerda no tengan el firewall desactivado (posible entrada de ataque).
- [x] **SMBv1 desactivado** en todos los equipos.
- [ ] *Auditoría*: Verificar que los equipos de Benimerda tengan SMBv1 desactivado.

**Política de Contraseñas**
- [x] Longitud mínima: **12 caracteres**.
- [x] Máximo de **5 intentos** de inicio de sesión antes de bloqueo.

**Ejecución de Scripts**
- [x] Activada ejecución de scripts en modo seguro.
- [x] Solo se permiten **scripts firmados** (no se pueden ejecutar scripts no cifrados/sin firmar).

**Control de Dispositivos Extraíbles (USB)**
- [x] Bloqueada escritura, lectura y ejecución desde pendrives en equipos del Ayuntamiento (previniendo exfiltración de datos o ataques *BadUSB*).
- [ ] **Pendiente**: aplicar en equipos de Casa de la Cultura y PCs restantes del dominio.
- [x] **Desactivada** reproducción automática (Autorun) de dispositivos.
- [x] En caso de conectar un dispositivo USB, no se podrá acceder sin activación manual.

**Control de Cuentas de Usuario (UAC)**
- [x] Opciones de seguridad configuradas para requerir permisos de administrador.
- [x] Control de cuentas de usuario activado y estricto.
