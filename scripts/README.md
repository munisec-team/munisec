# Scripts del Proyecto

Este directorio contiene los scripts y herramientas de automatización desarrollados a lo largo del proyecto para asistir en las labores operativas y de seguridad.

> [!WARNING]
> Algunos scripts pueden estar pendientes de subida (*Placeholders*) mientras se sanitizan credenciales o se extraen de los entornos de producción simulada.

## Estructura

- /forensics/: Scripts de Bash y PowerShell utilizados para la adquisición automatizada de datos volátiles y volcados de memoria (RAM).
- /backup/: Scripts de mantenimiento, destacando ackupJSBACH.sh para la preservación de configuraciones críticas (iptables, routing).
- /telegram-bot/: Código fuente del bot de Python utilizado para lanzar notificaciones *Push* desde Wazuh y monitorizar el estado de la DMZ (health checks).
