# 12. Checklist de Seguridad - GPOs (Directivas de Grupo)

> **Participantes**: Luis Fuster, Kike
> **Periodo**: Mayo 2026

Políticas de grupo aplicadas sobre el Active Directory del Ayuntamiento de Guarromán para el bastionado de los endpoints Windows del dominio.

## Directivas Aplicadas

### Firewall
- [x] Firewall de Windows activo en todos los equipos del dominio
- [ ] Verificar que los equipos de Benimerda no tengan el firewall desactivado (posible entrada de ataque)

### Protocolos Inseguros
- [x] **SMBv1 desactivado** en todos los equipos
- [ ] Verificar que los equipos de Benimerda tengan SMBv1 desactivado

### Política de Contraseñas
- [x] Longitud mínima: **12 caracteres**
- [x] Máximo de **5 intentos** de inicio de sesión antes de bloqueo

### Ejecución de Scripts
- [x] Activada ejecución de scripts
- [x] Solo se permiten **scripts firmados** (no se pueden ejecutar scripts no cifrados/sin firmar)

### Control de Dispositivos Extraíbles (USB)
- [x] Bloqueada escritura, lectura y ejecución desde pendrives en equipos del Ayuntamiento
- [ ] **Pendiente** aplicar en equipos de Casa de la Cultura y PCs restantes del dominio

### Control de Cuentas de Usuario (UAC)
- [x] Opciones de seguridad configuradas para ejecutar solo administradores
- [x] Control de cuentas de usuario activado

### Reproducción Automática (Autorun)
- [x] **Desactivada** reproducción automática de dispositivos
- [x] En caso de conectar un dispositivo USB, no se podrá acceder sin activación manual
