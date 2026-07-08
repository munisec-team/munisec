# 00. Visión General del Proyecto

> **Participantes**: Equipo Completo (8 personas)
> **Periodo**: 23 de Marzo 2026 – 26 de Mayo 2026

## 🎯 Objetivo Principal

El proyecto **munisec** simula el ciclo de vida completo de la infraestructura de ciberseguridad de una entidad gubernamental ficticia, el Ayuntamiento de Guarromán. 

El entorno de laboratorio se diseñó no solo para crear una infraestructura funcional (redes, servidores, dominios, web corporativa), sino para prepararla ante ciberataques reales, auditar su nivel de seguridad mediante ejercicios de Red Team, y testear su resiliencia mediante planes de recuperación de desastres (Disaster Recovery).

## 🏢 Sedes y Despliegue Físico

El proyecto se distribuye lógicamente en dos ubicaciones interconectadas:

1. **El Ayuntamiento (Sede Principal)**: Contiene los servicios críticos como el Active Directory, el ERP corporativo (Odoo), la zona desmilitarizada (DMZ) con la web pública, y el centro de operaciones de seguridad (SOC).
2. **La Casa de la Cultura (Sede Secundaria)**: Una sede más pequeña con zonas dedicadas a oficinas, biblioteca pública, y redes Wi-Fi abiertas para visitantes.

Ambas sedes están unidas mediante un túnel VPN que permite la comunicación segura de datos internos a través de Internet.

## 🛠️ Disciplinas de Ciberseguridad Aplicadas

A lo largo del proyecto se cubrieron las siguientes disciplinas:

* **Ingeniería de Sistemas y Redes**: Despliegue bare-metal de servidores Ubuntu y Windows Server, configuración de switches gestionables, y administración de routers firewall (pfSense y JSBach).
* **Blue Team (Defensa)**: Bastionado (hardening) de servicios, configuración de GPOs restrictivas, implementación de doble factor de autenticación (2FA) por hardware (USB), y encriptación de sistemas de archivos.
* **Security Operations Center (SOC)**: Despliegue de un SIEM (Wazuh) junto con un NIDS (Suricata) y EDRs (Sysmon), además de la integración de alertas automatizadas por Telegram.
* **Inteligencia (OSINT)**: Búsqueda activa de información sobre objetivos corporativos, creando vectores de ataque basados en ingeniería social pasiva.
* **Red Team (Ataque)**: Intrusión completa desde el exterior hasta la obtención de privilegios de administrador (`root`) en sistemas críticos, explotando vulnerabilidades de software y fallos de configuración.
* **DFIR (Digital Forensics & Incident Response)**: Recuperación ante caídas masivas de hardware, adquisición de evidencias de memoria RAM (volcados), y análisis de malware/shells tras los ataques.

## 👥 Personajes Ficticios y OSINT

Parte del realismo del proyecto involucraba la asignación de personajes y perfiles ficticios a correos corporativos reales. Estos perfiles debían ser investigados por el equipo rival.

| Cargo | Personaje |
|-------|-----------|
| **Alcalde** | Baltasar Cañete Huertas |
| **Concejala** | Rocío Mesa Jiménez |
| **Biblioteca** | Dolores Expósito |
| **Casa Cultura** | Fermín Valverde |
| **Funcionarios** | Isidoro Quesada, Trinidad Molina, Cristóbal Lorite, Valvanera Pinilla, Braulio |

