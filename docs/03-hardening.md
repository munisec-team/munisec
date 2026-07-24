# 03. Bastionado y Defensa en Profundidad (Hardening)

> 👉 Para consultar el desglose exacto de tareas técnicas realizadas por cada miembro, revisa el **[Registro de Contribuyentes](../CONTRIBUTORS.md)**.<br>
> **Periodo**: Mayo 2026

## Descripción General

Tras evaluar la postura de seguridad inicial y analizar las técnicas empleadas durante las simulaciones de ciberataques, el equipo implementó una estrategia de defensa en profundidad. El objetivo principal consistió en reducir la superficie de exposición, erradicar vectores de movimiento lateral entre sedes y garantizar la integridad de las estaciones y servidores del Ayuntamiento de Guarromán.

---

## 🛡️ 1. Control de Acceso y Red Perimetral (JSBach)

* **Filtrado de Tráfico e iptables**: **Jose Luis Oliver (Joselu)** y **Alfonso Garrido (Alfon)** diseñaron e implementaron una política estricta de *Deny by Default* en el router de frontera JSBach.
  - **Aislamiento Inter-VLAN**: Bloqueo total del tráfico cruzado entre las subredes de la sede (VLAN 3 Servidores, VLAN 4 SOC, VLAN 5/6 Trabajadores), permitiendo únicamente tráfico explícito (ej. consulta `53/UDP` hacia el DNS del Active Directory).
  - **Control de Acceso a la DMZ**: El tráfico hacia los servicios públicos alojados en la interfaz física dedicada de la DMZ se restringió exclusivamente a los puertos web `80/TCP` y `443/TCP`.
  - **Restricción de Paneles de Gestión**: Los servicios de administración (SSH `22/TCP`, paneles HTTP/HTTPS de switches TP-Link SG2210MP) se configuraron para aceptar conexiones únicamente desde IPs autorizadas pertenecientes a la **VLAN 1 (Administración)**.
* **Autenticación Fuerte (2FA)**: **Enrique Cebrián (Kike)** integró un sistema de autenticación de doble factor mediante tokens hardware USB en los servidores críticos, protegiendo las cuentas privilegiadas ante ataques de fuerza bruta o suplantación de credenciales.

---

## 🌐 2. Securización de Servicios Web en DMZ

El servidor Apache que hospeda el portal institucional y phpMyAdmin en la DMZ fue objeto de un bastionado intensivo ejecutado por **Alfonso Garrido**, **Pau Roig** y **Jose Luis Oliver**:

* **Ofuscación de Banners y Cabeceras HTTP**: Desactivación de la firma del servidor (`ServerSignature Off`, `ServerTokens Prod`) para ocultar las versiones del servidor web y del sistema operativo ante escaneos de reconocimiento.
* **Web Application Firewall (ModSecurity)**: Despliegue del WAF **ModSecurity** en Apache integrado con la regla base *OWASP Core Rule Set (CRS)*, filtrando activamente intentos de inyección SQL (SQLi), Cross-Site Scripting (XSS) e inclusión de archivos locales/remotos (LFI/RFI).
* **Cifrado en Tránsito (HTTPS)**: Despliegue de certificados TLS/SSL forzando la redirección y comunicación cifrada en todas las sesiones HTTP.

---

## 💻 3. Hardening de Endpoints y Directivas de Dominio (GPOs)

**Luis Fuster**, **Enrique Cebrián (Kike)**, **Jorge Cortés** y **Marcos Bori** aplicaron un conjunto unificado de Directivas de Grupo (GPOs) desde el Active Directory (`guarroman.local`) para securizar las estaciones de trabajo y servidores del dominio.

### 📜 Checklist de Directivas de Grupo (GPOs)

#### 🔒 Firewall y Protocolos Inseguros
- [x] **Firewall de Windows**: Habilitado obligatoriamente en todos los perfiles de red (Dominio, Privado y Público).
- [ ] *Auditoría Pendiente*: Confirmar la ausencia de excepciones locales deshabilitadas en equipos cliente de sedes secundarias.
- [x] **Desactivación de SMBv1**: Deshabilitado globalmente en todas las estaciones para neutralizar vectores de ejecución remota de código (RCE) tipo WannaCry/EternalBlue.
- [ ] *Auditoría Pendiente*: Auditada la desinstalación completa de la característica SMBv1 en la totalidad del inventario.

#### 🔑 Políticas de Autenticación y Bloqueo
- [x] **Complejidad y Longitud**: Requisito de longitud mínima de **12 caracteres** con parámetros de complejidad activos (mayúsculas, minúsculas, números y símbolos).
- [x] **Umbral de Bloqueo de Cuenta**: Bloqueo automático de la cuenta tras **5 intentos fallidos** consecutivos de inicio de sesión.

#### ⚙️ Control de Ejecución de Scripts
- [x] **Ejecución Restringida de Scripts**: Configuración de `ExecutionPolicy` para permitir únicamente la ejecución de **scripts firmados digitalmente**, bloqueando la ejecución de scripts arbitrarios o sin validar en PowerShell y CMD.

#### 💾 Control de Dispositivos Extraíbles (USB)
- [x] **Bloqueo de Unidades de Almacenamiento**: Denegación de permisos de lectura, escritura y ejecución para dispositivos de almacenamiento masivo USB en los equipos del Ayuntamiento.
- [ ] *Despliegue Pendiente*: Extender la directiva de denegación USB a los terminales de la Casa de la Cultura.
- [x] **Desactivación de Autorun/Autoplay**: Deshabilitada la ejecución automática de medios extraíbles para neutralizar amenazas tipo *BadUSB*.

#### 🛡️ Control de Cuentas de Usuario (UAC)
- [x] **UAC Estricto**: Ajustado al nivel máximo de elevación de privilegios, solicitando credenciales administrativas explícitas ante cualquier modificación del sistema.

---

## 🔐 4. Protección y Cifrado de Datos en Reposo

* **Cifrado de Almacenamiento con gocryptfs**: **Enrique Cebrián (Kike)** implementó el cifrado a nivel de sistema de archivos mediante **gocryptfs** en los servidores Ubuntu críticos. Esta medida garantiza que los directorios sensibles permanezcan cifrados en disco, protegiendo la información confidencial frente a la extracción física de unidades o accesos no autorizados al almacenamiento.
