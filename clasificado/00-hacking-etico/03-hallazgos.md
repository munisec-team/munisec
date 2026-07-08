# 🔐 INFORME DE HALLAZGOS - RED TEAM
## Vulnerabilidades Críticas Identificadas
**Fecha:** 21 de Mayo 2026  
**Operación:** Red Team Exercise - Ayuntamientos Benimerda y Guarroman  
**Clasificación:** INTERNO - CRÍTICO

---

## 📊 RESUMEN EJECUTIVO DE HALLAZGOS

Durante la operación de Red Team, se identificaron **7 vulnerabilidades críticas** que permitieron acceso completo a los sistemas de Guarroman con escalada a root en menos de 4 horas. La mayoría de vulnerabilidades son **fácilmente explotables** y resultan de **malas prácticas de configuración** en lugar de fallos de software complejos.

### 🎯 Impacto Global:
- **Confidencialidad:** 🔴 COMPROMETIDA (acceso a BD, archivos, credenciales)
- **Integridad:** 🔴 COMPROMETIDA (capacidad de modificar datos)
- **Disponibilidad:** 🔴 COMPROMETIDA (capacidad de afectar servicios)

---

## 🔴 HALLAZGOS CRÍTICOS (Severidad 9.9/10)

### H1: Credenciales por Defecto en Zabbix
**ID:** CVE-SYS-001  
**Ubicación:** `10.0.3.2:80` (VLAN SOC - Benimerda)  
**Severidad:** 🔴 CRÍTICA (9.9/10)

#### Descripción:
El sistema de monitorización empresarial **Zabbix** está configurado con credenciales por defecto de instalación:
- **Usuario:** `Admin`
- **Contraseña:** `zabbix`

#### Evidencia:
![Zabbix con credenciales por defecto](./04-evidencias/19-ZabbixDefaultCreds.png)
![Sesión autenticada en Zabbix](./04-evidencias/20-ZabbixLoggedIn.png)

#### Impacto:
- ✅ Acceso a interfaz de administración completa
- ✅ Visibilidad de dispositivos monitoreados (incluido JSBach de Benimerda)
- ✅ Información de infraestructura crítica
- ✅ Posible modificación de alertas y umbrales
- ⚠️ Punto de pivoting hacia otros sistemas

#### Recomendación Inmediata:
```bash
# ACCIÓN CRÍTICA - Ejecutar hoy mismo
# 1. Cambiar credenciales de administrador
# 2. Deshabilitar usuario "Admin" por defecto
# 3. Crear usuario administrativo con contraseña fuerte (20+ caracteres)
# 4. Forzar cambio de contraseña en próximo login
```

---

### H2: phpMyAdmin Expuesto Públicamente
**ID:** CVE-SYS-002  
**Ubicación:** `http://172.29.230.161/phpmyadmin/` (Guarroman)  
**Severidad:** 🔴 CRÍTICA (9.9/10)

#### Descripción:
La herramienta de administración MySQL **phpMyAdmin** es accesible sin restricciones de IP desde la red. Aunque requiere credenciales, es un punto de enumeración obvio para atacantes.

#### Evidencia:
![Panel de login phpMyAdmin expuesto](./04-evidencias/25-PhpMyAdminLogin.png)

#### Impacto:
- ✅ Exposición de información sobre base de datos
- ✅ Enumeración de usuarios y permisos
- ✅ Herramienta conocida con exploits documentados
- ✅ Punto de entrada para SQL injection
- ✅ Facilita ataques de fuerza bruta contra MySQL

#### Cadena de Explotación:
```
phpMyAdmin (enumeration) 
  ↓
Credenciales débiles (funcionario2guarroman:MiaNube98Trini)
  ↓
Acceso a tablas sensibles (wp_users, wp_pass)
  ↓
Reutilización de credenciales en WordPress
```

#### Recomendación Inmediata:
```bash
# OPCIÓN 1: Deshabilitar (preferido)
# - Desinstalar phpMyAdmin
# - Usar mysqldump para backups en lugar de interfaz web

# OPCIÓN 2: Restringir Acceso
# - Limitar por IP (solo administradores)
# - Cambiar URL por defecto (/admin-panel/ en lugar de /phpmyadmin/)
# - Requerir VPN para acceder
# - Implementar MFA

# OPCIÓN 3: Fortalecer
# - Cambiar puerto (no usar 80/443)
# - Renombrar directorio
# - Desabilitar listado de usuarios
```

---

### H3: Almacenamiento de Contraseñas en Texto Plano
**ID:** CVE-APP-001  
**Ubicación:** Base de datos WordPress - Tabla `wp_pass`  
**Severidad:** 🔴 CRÍTICA (9.9/10)

#### Descripción:
Las contraseñas de WordPress están almacenadas en una tabla separada (`wp_pass`) **en texto plano sin cifrado**. Esto contrasta con la tabla `wp_users` que usa bcrypt.

#### Evidencia:
![Tabla wp_pass con contraseñas visibles](./04-evidencias/27-WP_Pass_Table.png)

#### Impacto:
- 🎯 **CRÍTICO:** Acceso a credenciales válidas de múltiples usuarios
- ✅ Reutilización exitosa en otros servicios (funcionario1)
- ✅ Potencial para ataques de reutilización de credenciales en infraestructura completa
- ✅ Exposición de patrones de contraseñas de la organización
- ✅ Incumplimiento de regulaciones (GDPR, normativas bancarias)

#### Recomendación Inmediata:
```bash
# ACCIÓN CRÍTICA - Ejecutar inmediatamente
# 1. Eliminar tabla wp_pass
# 2. Resetear TODAS las contraseñas de WordPress
# 3. Notificar a usuarios que cambien contraseñas en otros servicios
# 4. Auditar logs de acceso a esta tabla

# SQL para eliminar tabla insegura
DROP TABLE IF EXISTS wp_pass;

# Verificar que WordPress usa solo wp_users con bcrypt
# Las contraseñas deben estar hasheadas con: $2y$ (bcrypt) o $argon2 (mejor)
```

---

### H4: Plugin File Manager Vulnerable
**ID:** CVE-WP-001  
**Ubicación:** Plugin "File Manager" - WordPress  
**Severidad:** 🔴 CRÍTICA (9.9/10)

#### Descripción:
Plugin de WordPress que permite navegación completa del sistema de archivos y subida de archivos. Usado comúnmente para **Remote Code Execution (RCE)**.

#### Evidencia:
![Instalación del plugin vulnerable](./04-evidencias/28-FileManagerPlugin.png)
![Subida de reverse shell](./04-evidencias/29-UploadRevshell.png)

#### Impacto:
- 🎯 **CRÍTICO:** Remote Code Execution directa
- ✅ Ejecución de comandos como usuario `www-data`
- ✅ Acceso a sistema de archivos completo
- ✅ Posibilidad de crear backups de datos
- ✅ Instalación de puertas traseras (backdoors)
- ✅ Modificación de código fuente

#### Cadena de Explotación:
```
Plugin File Manager instalado
  ↓
Acceso a interface de usuario
  ↓
Subida de archivo .php malicioso
  ↓
Navegación a URL del archivo
  ↓
Ejecución de código PHP
  ↓
Reverse shell obtenida
  ↓
Usuario: www-data (con acceso a archivos web)
```

#### Recomendación Inmediata:
```bash
# ACCIÓN CRÍTICA
# 1. Desactivar inmediatamente plugin File Manager
# 2. Eliminar plugin completamente
# 3. Escanear WordPress en busca de backdoors/shells
# 4. Revisar logs de acceso a la carpeta /uploads/

# Auditar en búsqueda de files maliciosos
find /var/www/wordpress -type f -name "*.php" -newermt '2026-05-19'
find /var/www/wordpress -type f -perm /111 2>/dev/null | grep php

# Verificar integridad de core WordPress
wp core verify-checksums --allow-root
```

---

### H5: Reutilización de Contraseñas entre Servicios
**ID:** CVE-ORG-001  
**Ubicación:** Múltiples sistemas (phpMyAdmin, WordPress, Local, AD/Odoo)  
**Severidad:** 🔴 CRÍTICA (9.9/10)

#### Descripción:
Las credenciales de un usuario OSINT (`funcionario1`) se reutilizan sin cambios en múltiples servicios:
1. phpMyAdmin (Guarroman)
2. WordPress (Guarroman)
3. WordPress (Benimerda)
4. Usuario local del sistema (Guarroman)
5. Potencialmente en AD/Odoo

#### Evidencia:
- Acceso phpMyAdmin: usuario `funcionario2guarroman`
- Tabla wp_pass: credenciales de `funcionario1guarroman`
- Cambio local: `su - funcionario1guarroman` (funciona)
- Acceso WordPress Benimerda: usuario `funcionario1` (funciona)

#### Impacto:
- 🎯 **CRÍTICO:** Compromiso en cascada de múltiples servicios
- ✅ Una contraseña rota = acceso a toda la infraestructura
- ✅ Escalada horizontal entre sistemas
- ✅ Falta de segmentación
- ✅ Movimiento lateral facilitado

#### Recomendación Inmediata:
```bash
# AUDITORÍA URGENTE - Ejecutar hoy
# 1. Generar lista de todas las cuentas de usuario `funcionario1*` en todos los sistemas
# 2. Resetear contraseñas únicas y complejas para cada servicio
# 3. Implementar política de contraseñas diferentes por servicio

# Script de auditoría
echo "=== WordPress Guarroman ==="
wp user list --allow-root

echo "=== WordPress Benimerda ==="
# (en servidor Benimerda)

echo "=== Usuarios locales ==="
getent passwd | grep funcionario

echo "=== Usuarios LDAP/AD ==="
# ldapsearch (si aplica)

echo "=== Usuarios MySQL ==="
mysql -u root -p -e "SELECT user, host FROM mysql.user;"
```

---

### H6: Permisos Sudo Incorrectos (ALL : ALL)
**ID:** CVE-SYS-003  
**Ubicación:** `/etc/sudoers` - Usuario `funcionario1guarroman`  
**Severidad:** 🔴 CRÍTICA (9.9/10)

#### Descripción:
El usuario `funcionario1guarroman` tiene permisos en sudoers configurados como:
```
funcionario1guarroman ALL=(ALL) : ALL
```

Esto permite ejecutar **CUALQUIER comando como root SIN necesidad de contraseña**.

#### Evidencia:
![Permisos sudoers del usuario](./04-evidencias/38-SwitchToFuncionario1.png)
![Acceso root obtenido](./04-evidencias/40-RootShell.png)

#### Impacto:
- 🎯 **CRÍTICO:** Escalada de privilegios trivial
- ✅ Una vez dentro como `funcionario1`, acceso root inmediato
- ✅ Control total del sistema
- ✅ Capacidad para:
  - Instalar puertas traseras
  - Modificar archivos de sistema
  - Acceder a datos sensibles
  - Afectar disponibilidad

#### Recomendación Inmediata:
```bash
# ACCIÓN CRÍTICA - Ejecutar ahora
# Revisar y corregir sudoers

sudo visudo

# ELIMINAR esta línea:
# funcionario1guarroman ALL=(ALL) NOPASSWD: ALL

# REEMPLAZAR con principio de menor privilegio:
# funcionario1guarroman ALL=(ALL) REQUIRE_PASS /usr/bin/supervisorctl
# funcionario1guarroman ALL=(ALL) REQUIRE_PASS /usr/sbin/service apache2 *

# Verificar cambios
sudo grep -r "NOPASSWD" /etc/sudoers*

# Ver logs de sudo
sudo journalctl -u sudo -n 20
```

---

### H7: Credenciales por Defecto en Router JSBach
**ID:** CVE-HW-001  
**Ubicación:** Router Benimerda `172.29.230.171`  
**Severidad:** 🔴 CRÍTICA (9.9/10)

#### Descripción:
El router JSBach (dispositivo crítico de frontera) está configurado con credenciales por defecto:
- **Usuario:** `admin`
- **Contraseña:** `admin`

#### Evidencia:
![Panel de login JSBach](./04-evidencias/03-CapturaLoginJSBach.png)
![Acceso exitoso - configuración VLANs](./04-evidencias/04-CapturaJSBachLosChichos.png)

#### Impacto:
- 🎯 **CRÍTICO:** Acceso a dispositivo de frontera
- ✅ Extracción de configuración de VLANs
- ✅ Modificación de rutas de red
- ✅ Man-in-the-Middle (MiTM) posible
- ✅ Acceso a redes internas (10.0.0.0/16, 10.1.0.0/16)
- ✅ Punto de pivoting hacia infraestructura completa

#### Cadena de Explotación:
```
Credenciales por defecto JSBach admin:admin
  ↓
Acceso a panel administrativo
  ↓
Extracción de configuración VLANs (10.0.x.x/24)
  ↓
Modificación de tabla de enrutamiento (sudo ip r a)
  ↓
Acceso lateral a VLANs (SOC, AD, Backups)
  ↓
Descubrimiento de sistemas adicionales
```

#### Recomendación Inmediata:
```bash
# ACCIÓN CRÍTICA - Prioritario
# 1. Cambiar credenciales de admin del JSBach
# 2. Crear usuarios administrativos separados
# 3. Habilitar cifrado de acceso administrativo (HTTPS)
# 4. Implementar control de acceso por IP

# Desde panel JSBach:
# - Administración > Usuarios > Cambiar contraseña admin
# - Crear usuario nuevo con permisos limitados
# - Deshabilitar puerto HTTP (usar HTTPS obligatorio)
# - Restringir acceso administrativo a IPs de management
# - Habilitar logging de acceso administrativo
```

---

## 🟠 HALLAZGOS ALTOS (Severidad 7.0-8.9)

### H8: Falta de Segmentación de Red
**ID:** CVE-NET-001  
**Severidad:** 🟠 ALTA (8.5/10)

#### Descripción:
Las VLANs están configuradas pero sin firewall entre ellas. Un atacante en la VLAN 10.0.1.0 (Guarroman) puede acceder a:
- VLAN 10.0.2.0 (AD)
- VLAN 10.0.3.0 (SOC/Wazuh)
- VLAN 10.0.99.0 (Backups)

#### Impacto:
- ✅ Movimiento lateral sin restricciones
- ✅ Acceso a sistemas críticos (AD, Backups)
- ✅ Robo de datos sin detección

#### Recomendación:
```
1. Implementar firewall entre VLANs (pfSense, Checkpoint)
2. Crear políticas de segmentación estrictas
3. Permitir solo tráfico necesario entre VLANs
4. Monitorizar flujos inter-VLAN
5. Implementar micro-segmentación en aplicaciones críticas
```

---

### H9: Versión de Apache Conocida como Vulnerable
**ID:** CVE-2024-XXX (Apache 2.4.58)  
**Ubicación:** `172.29.230.161:443` y SOC  
**Severidad:** 🟠 ALTA (7.5/10)

#### Descripción:
Apache httpd 2.4.58 tiene vulnerabilidades públicas documentadas. Aunque no se explotó en esta operación, es un vector conocido.

#### Recomendación:
```
1. Actualizar Apache a versión más reciente
2. Configurar WAF (ModSecurity)
3. Implementar rate limiting
4. Monitorizar logs de acceso en búsqueda de exploits
```

---

## 🟡 HALLAZGOS MEDIOS (Severidad 4.0-6.9)

### H10: Tabla wp_users con Hashes Bcrypt Débiles
**ID:** CVE-APP-002  
**Severidad:** 🟡 MEDIA (6.0/10)

#### Descripción:
La tabla `wp_users` contiene hashes bcrypt de contraseñas. Aunque están hasheados (mejor que texto plano), los patrones de contraseñas organizacionales pueden permitir ataques offline.

#### Recomendación:
- Implementar política de contraseñas complejas (20+ caracteres, mixtas)
- Auditoría de contraseñas débiles
- Uso de Argon2 en lugar de bcrypt (más seguro)

---

## 📈 MATRIZ DE IMPACTO

| Hallazgo | Confidencialidad | Integridad | Disponibilidad | CVSS | Explotabilidad |
|----------|-----------------|-----------|----------------|------|-----------------|
| H1: Zabbix Default | ALTA | ALTA | MEDIA | 9.9 | ✅ Trivial |
| H2: phpMyAdmin | CRÍTICA | CRÍTICA | MEDIA | 9.9 | ✅ Trivial |
| H3: wp_pass Plaintext | CRÍTICA | CRÍTICA | BAJA | 9.9 | ✅ Trivial |
| H4: File Manager Plugin | CRÍTICA | CRÍTICA | CRÍTICA | 9.9 | ✅ Trivial |
| H5: Reutilización Creds | CRÍTICA | CRÍTICA | MEDIA | 9.9 | ✅ Fácil |
| H6: Sudoers NOPASSWD | CRÍTICA | CRÍTICA | CRÍTICA | 9.9 | ✅ Trivial |
| H7: Router Default | CRÍTICA | CRÍTICA | CRÍTICA | 9.9 | ✅ Trivial |
| H8: Sin Segmentación | ALTA | ALTA | MEDIA | 8.5 | ✅ Media |
| H9: Apache Viejo | MEDIA | MEDIA | MEDIA | 7.5 | ⚠️ Conocida |
| H10: wp_users Débil | MEDIA | MEDIA | BAJA | 6.0 | ⚠️ Offline |

---

## 🎯 CADENA DE ATAQUE COMPLETA (Attack Chain)

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMPROMISO TOTAL DEL SISTEMA                  │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                    ┌─────────┴─────────┐
                    │  Root Access ✅   │ (4 horas total)
                    └─────────┬─────────┘
                              △
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
    ┌───┴───┐          ┌──────┴──────┐         ┌────┴────┐
    │ H6:   │          │ Escalada a: │         │ H5:     │
    │Sudoers│          │ funcionario1│         │Reutili- │
    │       │          │ (sin passwd)│         │ zación  │
    └───┬───┘          └──────┬──────┘         └────┬────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                    ┌─────────┴──────────┐
                    │ Shell Remota ✅    │
                    │ (usuario www-data) │
                    └─────────┬──────────┘
                              △
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
    ┌───┴───┐          ┌──────┴──────┐         ┌────┴────┐
    │ H4:   │          │ Reverse     │         │ H3:     │
    │File   │          │ Shell       │         │wp_pass  │
    │Manager│          │ uploaded    │         │obteni-  │
    │plugin │          │ en /uploads │         │das      │
    └───┬───┘          └──────┬──────┘         └────┬────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                    ┌─────────┴──────────┐
                    │ WordPress Pirated  │
                    │ (funcionario1)     │
                    └─────────┬──────────┘
                              △
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
    ┌───┴───┐          ┌──────┴──────┐         ┌────┴────┐
    │ H2:   │          │ Credenciales│         │ H5:     │
    │phpMy- │          │ de wp_pass  │         │OSINT    │
    │Admin  │          │ en BD       │         │de       │
    │acceso │          │             │         │usuario1 │
    └───┬───┘          └──────┬──────┘         └────┬────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                    ┌─────────┴──────────┐
                    │ Enumeración BD ✅  │
                    │ (phpMyAdmin)       │
                    └─────────┬──────────┘
                              △
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
    ┌───┴───┐          ┌──────┴──────┐         ┌────┴────┐
    │ H2:   │          │ Gobuster    │         │ H1:     │
    │Direc- │          │ --->        │         │Zabbix   │
    │torio  │          │ /phpmyadmin │         │(info)   │
    │Exposado          │             │         │         │
    └───┬───┘          └──────┬──────┘         └────┬────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                    ┌─────────┴──────────┐
                    │ Reconocimiento ✅  │
                    │ (NMAP, Gobuster)   │
                    └─────────┬──────────┘
                              △
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
    ┌───┴───┐          ┌──────┴──────┐         ┌────┴────┐
    │ H7:   │          │Pivoting     │         │Enumera- │
    │Router │          │de VLANs     │         │ción de  │
    │JSBach │          │(admin:admin)│         │subredes │
    │       │          │             │         │         │
    └───────┘          └─────────────┘         └─────────┘

```

**Tiempo total de ataque:** ~4 horas  
**Puntos de quiebre:** 7/7 vulnerabilidades críticas explotadas

---

## 💡 LECCIONES APRENDIDAS

### 1. Las Credenciales por Defecto son Críticas
Todas las credenciales por defecto encontradas (Zabbix, JSBach, potencialmente MySQL) permitieron acceso inicial a sistemas críticos.

### 2. La Reutilización de Contraseñas es Mortal
Una única contraseña OSINT (`funcionario1`) abrió puertas en múltiples sistemas de ambas organizaciones.

### 3. El Almacenamiento de Contraseñas en Texto Plano es Inaceptable
La tabla `wp_pass` convirtió el acceso a phpMyAdmin en acceso a WordPress directo.

### 4. Los Plugins sin Revisar son Puertas Traseras
El plugin File Manager es un conocido vector de RCE que debería haberse bloqueado o revisado antes de la instalación.

### 5. Los Permisos de Sudo Incorrectos Garantizan Root
Un usuario con `NOPASSWD: ALL` en sudoers es equivalente a tener acceso root automático.

### 6. La Segmentación de Red es Esencial
Sin firewall entre VLANs, un compromiso en un segmento significa compromiso de toda la red.

---

## 🛡️ ROADMAP DE REMEDIATION

### FASE 1: EMERGENCIA (HOY - 24 horas)
- [ ] Cambiar credenciales de Zabbix (admin -> credencial fuerte)
- [ ] Cambiar credenciales de JSBach
- [ ] Resetear tabla `wp_pass` o eliminarla
- [ ] Desactivar plugin File Manager
- [ ] Resetear contraseña de `funcionario1` en todos los servicios
- [ ] Revisar y corregir sudoers (eliminar NOPASSWD)

### FASE 2: CRÍTICA (Semana 1)
- [ ] Auditoría de permisos sudoers en todos los servidores
- [ ] Auditoría de plugins WordPress instalados
- [ ] Cambio de credenciales para TODOS los usuarios administrativos
- [ ] Desactivar/desinstalar phpMyAdmin o restringir por IP
- [ ] Implementar firewalls entre VLANs

### FASE 3: IMPORTANTE (Mes 1)
- [ ] Actualizar Apache, MySQL, WordPress a versiones recientes
- [ ] Implementar WAF (ModSecurity)
- [ ] Configurar logging centralizado
- [ ] Implementar MFA en accesos críticos
- [ ] Programa de concienciación sobre credenciales
- [ ] Auditoría de seguridad de WordPress

### FASE 4: ESTRATÉGICA (Trimestral)
- [ ] Implementar Zero Trust Architecture
- [ ] Segmentación de red avanzada (Microsegmentación)
- [ ] Programa de Penetration Testing trimestral
- [ ] Monitorización de seguridad 24/7 (SOC)
- [ ] Plan de respuesta a incidentes
- [ ] Auditoría de cumplimiento regulatorio

---

## 📞 CONTACTO Y PRÓXIMOS PASOS

**Responsable de Remediation:** Equipo de Seguridad de Benimerda/Guarroman  
**Fecha de Seguimiento:** 28 de Mayo 2026 (1 semana)  
**Segunda Auditoría:** 30 de Junio 2026 (1 mes)

---

**Informe compilado por:** Red Team - Guarroman  
**Fecha:** 21 de Mayo 2026  
**Clasificación:** CONFIDENCIAL - INTERNO
