# Restaurar conexión a Internet

✅ Tarea realizada: Realizada
👤 Persona: Jose Luis Oliver Herranz
📅 Fecha: 30 de marzo de 2026
📝 Descripción / Bitácora: Debido a que el día anterior se configuraron los pfSense en ambos lados de la red para habilitar la configuración de la VPN, se perdió la conectividad con la WAN y el resto de la red no tenía acceso a Internet.
Pasadas unas horas, después de probar muchas cosas, se terminó solucionando.
🚧 Bloqueos / Problemas: El problema venía principalmente de una configuración que estábamos pasando por alto en el pfSense.
El último día se desactivó el firewall para poder hacer pruebas de VPN correctamente, pero al hacerlo también deshabilitamos las funciones NAT, lo que hacía que los paquetes no se les devolviesen a su respectivo origen y se perdieran en el limbo.

Se volvió a activar el firewall y se solucionó el problema.