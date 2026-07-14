# 06. Hallazgos y Vulnerabilidades (Findings)

> **Participantes**: Red Team (Carlos Delgado, Pau Roig, Jose Luis Oliver)
> **Periodo**: Mayo 2026

## Resumen Ejecutivo de Hallazgos

Como resultado de las pruebas de penetración (Red Team), se identificaron un total de **10 vulnerabilidades** en la infraestructura, de las cuales 7 son críticas (CVSS 9.9), 2 altas (CVSS 7.5-8.5) y 1 media (CVSS 6.0). Estas fallas abarcan desde configuraciones por defecto hasta credenciales en texto plano, permitiendo el compromiso total de la red en menos de 4 horas.

### Impacto Global:
- **Confidencialidad:** COMPROMETIDA (acceso a BD, archivos, credenciales)
- **Integridad:** COMPROMETIDA (capacidad de modificar datos)
- **Disponibilidad:** COMPROMETIDA (capacidad de afectar servicios)

---

## Hallazgos Críticos (Severidad 9.9/10)

### H1: Credenciales por Defecto en Zabbix
**Severidad:** CRÍTICA (9.9/10)

**Descripción:** El sistema de monitorización Zabbix está configurado con credenciales por defecto de instalación: `Admin`/`zabbix`.

**Evidencia:**
![Zabbix con credenciales por defecto](../reports/pentesting/19-ZabbixDefaultCreds.png)
![Sesión autenticada en Zabbix](../reports/pentesting/20-ZabbixLoggedIn.png)

**Impacto:**
- Acceso a interfaz de administración completa
- Visibilidad de dispositivos monitorizados
- Información de infraestructura crítica
- Posible modificación de alertas y umbrales
- Punto de pivoting hacia otros sistemas

**Remediación:** Cambiar inmediatamente la contraseña por defecto del usuario Admin y deshabilitar cuentas no utilizadas.

---

### H2: phpMyAdmin Expuesto Públicamente
**Severidad:** CRÍTICA (9.9/10)

**Descripción:** La herramienta de administración MySQL phpMyAdmin es accesible sin restricciones de IP desde Internet en `http://172.29.230.161/phpmyadmin/`.

**Evidencia:**
![Panel de login phpMyAdmin expuesto](../reports/pentesting/25-PhpMyAdminLogin.png)

**Impacto:**
- Exposición de información sobre base de datos
- Enumeración de usuarios y permisos
- Herramienta conocida con exploits documentados
- Punto de entrada para ataques de fuerza bruta contra MySQL

**Cadena de Explotación:**
```
phpMyAdmin (enumeración) → Credenciales débiles → Acceso a tablas sensibles → Reutilización de credenciales en WordPress
```

**Remediación:** Bloquear el acceso a `/phpmyadmin` desde el exterior mediante configuración de Apache o `.htaccess`, permitiendo acceso solo desde localhost o IPs de gestión.

---

### H3: Almacenamiento de Contraseñas en Texto Plano
**Severidad:** CRÍTICA (9.9/10)

**Descripción:** Las contraseñas de WordPress están almacenadas en una tabla separada (`wp_pass`) en texto plano sin cifrado, mientras que la tabla `wp_users` usa bcrypt correctamente.

**Evidencia:**
![Tabla wp_pass con contraseñas visibles](../reports/pentesting/27-WP_Pass_Table.png)

**Impacto:**
- Acceso a credenciales válidas de múltiples usuarios
- Reutilización exitosa en otros servicios
- Exposición de patrones de contraseñas de la organización
- Incumplimiento de regulaciones (GDPR)

**Remediación:** Eliminar la tabla `wp_pass`, resetear todas las contraseñas de WordPress y forzar el uso del algoritmo de hash bcrypt de WordPress.

---

### H4: Plugin File Manager Vulnerable
**Severidad:** CRÍTICA (9.9/10)

**Descripción:** El plugin "File Manager" de WordPress permite navegación completa del sistema de archivos y subida de archivos, usado comúnmente para Remote Code Execution (RCE).

**Evidencia:**
![Instalación del plugin vulnerable](../reports/pentesting/28-FileManagerPlugin.png)
![Subida de reverse shell](../reports/pentesting/29-UploadRevshell.png)

**Impacto:**
- Remote Code Execution directa
- Ejecución de comandos como usuario `www-data`
- Acceso a sistema de archivos completo
- Instalación de puertas traseras (backdoors)

**Cadena de Explotación:**
```
Plugin File Manager instalado → Subida de archivo .php malicioso → Ejecución de código PHP → Reverse shell obtenida
```

**Remediación:** Deshabilitar la edición de archivos desde el panel de WordPress añadiendo `define('DISALLOW_FILE_EDIT', true);` en `wp-config.php` y eliminar el plugin File Manager.

---

### H5: Reutilización de Contraseñas entre Servicios
**Severidad:** CRÍTICA (9.9/10)

**Descripción:** Las credenciales del usuario `funcionario1` se reutilizan sin cambios en múltiples servicios: phpMyAdmin, WordPress (Guarroman y Benimerda), y usuario local del sistema.

**Impacto:**
- Compromiso en cascada de múltiples servicios
- Una contraseña comprometida = acceso a toda la infraestructura
- Escalada horizontal entre sistemas
- Movimiento lateral facilitado

**Remediación:** Generar contraseñas únicas y complejas para cada servicio. Implementar política de contraseñas diferentes por servicio.

---

### H6: Permisos Sudo Incorrectos (ALL:ALL)
**Severidad:** CRÍTICA (9.9/10)

**Descripción:** El usuario `funcionario1guarroman` tiene permisos en sudoers configurados como `ALL=(ALL) NOPASSWD: ALL`, permitiendo ejecutar cualquier comando como root sin contraseña.

**Evidencia:**
![Permisos sudoers del usuario](../reports/pentesting/38-SwitchToFuncionario1.png)
![Acceso root obtenido](../reports/pentesting/40-RootShell.png)

**Impacto:**
- Escalada de privilegios trivial
- Control total del sistema
- Capacidad para instalar puertas traseras, modificar archivos, acceder a datos sensibles

**Remediación:** Revisar y corregir sudoers aplicando el principio de menor privilegio. Eliminar cualquier regla `NOPASSWD: ALL`.

---

### H7: Credenciales por Defecto en Router JSBach
**Severidad:** CRÍTICA (9.9/10)

**Descripción:** El router JSBach (dispositivo crítico de frontera) está configurado con credenciales por defecto: `admin`/`admin`.

**Evidencia:**
![Panel de login JSBach](../reports/pentesting/03-CapturaLoginJSBach.png)
![Acceso exitoso - configuración VLANs](../reports/pentesting/04-CapturaJSBachLosChichos.png)

**Impacto:**
- Acceso a dispositivo de frontera
- Extracción de configuración de VLANs
- Modificación de rutas de red
- Man-in-the-Middle (MiTM) posible
- Punto de pivoting hacia infraestructura completa

**Cadena de Explotación:**
```
Credenciales por defecto JSBach → Acceso a panel administrativo → Extracción de configuración VLANs → Modificación de enrutamiento → Acceso lateral a VLANs
```

**Remediación:** Cambiar credenciales de admin del JSBach, crear usuarios administrativos separados, habilitar cifrado HTTPS y restringir acceso administrativo por IP.

---

## Hallazgos Altos (Severidad 7.0-8.9)

### H8: Falta de Segmentación de Red
**Severidad:** ALTA (8.5/10)

**Descripción:** Las VLANs están configuradas pero sin firewall entre ellas. Un atacante en una VLAN puede acceder a todas las demás sin restricciones.

**Impacto:**
- Movimiento lateral sin restricciones
- Acceso a sistemas críticos (AD, Backups)
- Robo de datos sin detección

**Remediación:**
1. Implementar firewall entre VLANs
2. Crear políticas de segmentación estrictas
3. Permitir solo tráfico necesario entre VLANs
4. Monitorizar flujos inter-VLAN
5. Implementar micro-segmentación en aplicaciones críticas

---

### H9: Versión de Apache Conocida como Vulnerable
**Severidad:** ALTA (7.5/10)

**Descripción:** Apache httpd 2.4.58 tiene vulnerabilidades públicas documentadas. Aunque no se explotó directamente en esta operación, es un vector conocido.

**Remediación:**
1. Actualizar Apache a versión más reciente
2. Configurar WAF (ModSecurity) con OWASP Core Rule Set
3. Implementar rate limiting
4. Monitorizar logs de acceso en búsqueda de exploits

---

## Hallazgos Medios (Severidad 4.0-6.9)

### H10: Hashes Bcrypt Débiles en wp_users
**Severidad:** MEDIA (6.0/10)

**Descripción:** La tabla `wp_users` contiene hashes bcrypt de contraseñas. Aunque están hasheados, los patrones de contraseñas organizacionales pueden permitir ataques offline.

**Remediación:**
- Implementar política de contraseñas complejas (20+ caracteres)
- Auditoría de contraseñas débiles
- Uso de Argon2 en lugar de bcrypt

---

## Matriz de Impacto

| Hallazgo | Confidencialidad | Integridad | Disponibilidad | CVSS | Explotabilidad |
|----------|-----------------|-----------|----------------|------|-----------------|
| H1: Zabbix Default | ALTA | ALTA | MEDIA | 9.9 | Trivial |
| H2: phpMyAdmin | CRÍTICA | CRÍTICA | MEDIA | 9.9 | Trivial |
| H3: wp_pass Plaintext | CRÍTICA | CRÍTICA | BAJA | 9.9 | Trivial |
| H4: File Manager Plugin | CRÍTICA | CRÍTICA | CRÍTICA | 9.9 | Trivial |
| H5: Reutilización Creds | CRÍTICA | CRÍTICA | MEDIA | 9.9 | Fácil |
| H6: Sudoers NOPASSWD | CRÍTICA | CRÍTICA | CRÍTICA | 9.9 | Trivial |
| H7: Router Default | CRÍTICA | CRÍTICA | CRÍTICA | 9.9 | Trivial |
| H8: Sin Segmentación | ALTA | ALTA | MEDIA | 8.5 | Media |
| H9: Apache Viejo | MEDIA | MEDIA | MEDIA | 7.5 | Conocida |
| H10: wp_users Débil | MEDIA | MEDIA | BAJA | 6.0 | Offline |

---

## Cadena de Ataque Completa (Attack Chain)

**Tiempo total de ataque:** ~4 horas
**Puntos de quiebre:** 7/7 vulnerabilidades críticas explotadas

```
Credenciales por defecto JSBach (admin:admin)
    ↓
Configuración de VLANs y rutas (pivoting)
    ↓
Descubrimiento de phpMyAdmin (Gobuster)
    ↓
Extracción de contraseñas (wp_pass texto plano)
    ↓
Acceso WordPress como administrador
    ↓
Plugin vulnerable File Manager
    ↓
Subida de Reverse Shell
    ↓
Shell remota como www-data
    ↓
Reutilización de credenciales (funcionario1)
    ↓
Escalada a root (sudoers NOPASSWD: ALL)
    ↓
ROOT ACCESS - Control total del sistema
```

---

## Roadmap de Remediación

### Fase 1: Emergencia (24 horas)
- [ ] Cambiar credenciales de Zabbix, JSBach y MySQL
- [ ] Eliminar tabla `wp_pass`
- [ ] Desactivar plugin File Manager
- [ ] Resetear contraseña de `funcionario1` en todos los servicios
- [ ] Revisar y corregir sudoers

### Fase 2: Crítica (Semana 1)
- [ ] Auditoría de permisos sudoers en todos los servidores
- [ ] Auditoría de plugins WordPress instalados
- [ ] Cambio de credenciales para todos los usuarios administrativos
- [ ] Desactivar/desinstalar phpMyAdmin o restringir por IP
- [ ] Implementar firewalls entre VLANs

### Fase 3: Importante (Mes 1)
- [ ] Actualizar Apache, MySQL, WordPress a versiones recientes
- [ ] Implementar WAF (ModSecurity) con OWASP CRS
- [ ] Configurar logging centralizado
- [ ] Implementar MFA en accesos críticos
- [ ] Programa de concienciación sobre credenciales

### Fase 4: Estratégica (Trimestral)
- [ ] Implementar Zero Trust Architecture
- [ ] Micro-segmentación de red
- [ ] Programa de Penetration Testing trimestral
- [ ] Monitorización de seguridad 24/7 (SOC)
- [ ] Plan de respuesta a incidentes
- [ ] Auditoría de cumplimiento regulatorio
