# 04. Bastionado y Defensa en Profundidad (Hardening)

> **Participantes**: Kike, Alfonso, Jose Luis, Luis Fuster
> **Periodo**: Mayo 2026

## Descripción General

Tras la evaluación de la postura de seguridad y el análisis de los ataques ejecutados por el Red Team, el equipo implementó una estrategia de defensa en profundidad. El objetivo fue reducir la superficie de ataque, restringir el movimiento lateral y proteger la integridad de los datos, siguiendo las directrices del Esquema Nacional de Seguridad (ENS).

## Medidas Implementadas

### 🔒 Control de Acceso y Red

*   **Autenticación Fuerte (2FA)**: Se implementó un Doble Factor de Autenticación mediante tokens USB hardware para el acceso a sistemas críticos, previniendo ataques de fuerza bruta o robo de credenciales.
*   **Segmentación de Red y Firewalls Locales (iptables)**: Se configuraron reglas estrictas de `iptables` en el router JSBach y en los servidores.
    *   *Deny by default*: Bloqueo total del tráfico inter-VLAN, permitiendo solo puertos específicos (ej. 80/443 hacia la DMZ, 53 hacia el DNS del AD).
    *   *Restricción de Gestión*: Acceso SSH y HTTP(S) a los paneles de gestión (Switches, pfSense, JSBach) restringido exclusivamente a la IP del administrador en la VLAN 1.

### 🌐 Securización de Servicios Web

El servidor Apache que alojaba WordPress y phpMyAdmin en la DMZ fue objeto de un bastionado severo por parte de Alfonso:

*   **Ofuscación de Banners**: Modificación de las cabeceras HTTP (`ServerSignature Off`, `ServerTokens Prod`) para evitar la enumeración de versiones del servidor web y del sistema operativo.
*   **ModSecurity (WAF)**: Implementación del *Web Application Firewall* ModSecurity en Apache, con el conjunto de reglas OWASP Core Rule Set (CRS) para bloquear ataques de inyección SQL (SQLi), Cross-Site Scripting (XSS) e inclusiones de archivos locales (LFI/RFI).
*   **Cifrado en Tránsito**: Despliegue de certificados TLS/SSL forzando HTTPS en todas las comunicaciones web internas y externas.

### 🛡️ Endpoint y Datos

*   **Directivas de Grupo (GPOs)**: Luis y Kike aplicaron políticas desde el AD para deshabilitar puertos USB (previniendo exfiltración de datos o ataques *BadUSB*), forzar el bloqueo automático de pantallas, y restringir la ejecución de scripts de PowerShell no firmados.
*   **Cifrado de Datos en Reposo**: Implementación de **gocryptfs** en los servidores Ubuntu críticos para cifrar directorios sensibles, protegiendo la información en caso de acceso físico no autorizado al almacenamiento.

