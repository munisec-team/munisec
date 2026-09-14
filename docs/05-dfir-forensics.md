# 05. Forense Digital y Respuesta a Incidentes (DFIR)

> 👉 Para consultar el desglose exacto de tareas técnicas realizadas por cada miembro, revisa el **[Registro de Contribuyentes](../CONTRIBUTORS.md)**.<br>
> **Periodo**: Mayo 2026

## Descripción General

La disciplina de Forense Digital y Respuesta a Incidentes (DFIR) permitió al equipo mantener una capacidad de análisis *post-mortem* y en tiempo real ante eventos anómalos o compromisos de red. La estrategia combinó la automatización de capturas de memoria RAM en los ordenadores de los usuarios con el análisis profundo en entornos aislados y planes de recuperación ante desastres (*Disaster Recovery*).

---

## 🛠️ 1. Automatización con Forensic Suite Dashboard

* **Desarrollo**: Herramienta de software propio desarrollada por **Alfonso Garrido**.
* **Ubicación**: Disponible en el repositorio en la carpeta **[`software/forensic-suite-dashboard/`](../software/forensic-suite-dashboard/)** y publicada en su repositorio oficial de GitHub: **[alfgarpen/Forensic-Suite-dashboard](https://github.com/alfgarpen/Forensic-Suite-dashboard)**.
* **Arquitectura**: Se desplegó una **Forensic Suite** integral con arquitectura cliente-servidor (Backend Flask + Frontend Web). Esta herramienta permitió centralizar y automatizar todo el ciclo de vida forense a través de una interfaz web moderna (puerto `5001`).
* **Despliegue**: El software incluye scripts instaladores de un solo clic (`install.sh` y `install.ps1`) que configuran servicios en segundo plano (`systemd` en Linux y servicios en Windows), descargan Volatility 3 de forma transparente y preparan el entorno de Python, manteniendo la capacidad forense siempre activa.

### 📋 Módulos del Sistema
1. **Adquisición Rápida**: Interfaz para capturar y subir volcados de memoria directamente desde el dashboard.
2. **Análisis Automático**: Integración directa con **Volatility 3** para procesar los volcados usando reglas preconfiguradas (detección de procesos ocultos, conexiones de red anómalas y búsqueda de programas o scripts maliciosos).
3. **Reportes Profesionales**: Motor de generación de reportes automáticos en HTML (se generaron 67 reportes durante el ejercicio para los distintos equipos del laboratorio).

---

## 🔬 2. Análisis de Memoria con Volatility Framework

* **Analistas Forenses**: **Jorge Cortés** y **Alfonso Garrido** (con apoyo en la recolección de evidencias).
* **Metodología**: Los volcados de memoria se inspeccionaron en una estación de trabajo forense dedicada (Kali Linux) mediante **Volatility Framework**:

```bash
# Muestra de comandos de inspección en Volatility:
volatility -f RAM_JSBach_20260515.raw --profile=LinuxUbuntu2404x64 linux_pslist
volatility -f RAM_JSBach_20260515.raw --profile=LinuxUbuntu2404x64 linux_netstat
```

### 🎯 Tareas de Análisis Forense
* **Detección de Procesos Ocultos (`pslist` vs `psscan`)**: Comparación entre las estructuras de tareas del sistema operativo y los bloques de memoria escaneados para identificar *rootkits* o procesos inyectados.
* **Inspección de Conexiones de Red (`netstat` / `netscan`)**: Rastreo de conexiones activas o sospechosas dirigidas hacia afuera (*Reverse Shells*).
* **Auditoría de Inyecciones de Código (`malfind`)**: Identificación de regiones de memoria sospechosas de albergar código malicioso inyectado.

### 📊 Repositorio de Evidencias Forenses
El sistema automatizado generó **67 reportes forenses en formato HTML**, auditando de forma continua 8 servidores y sistemas críticos (`Active Directory`, `JSBach Ayuntamiento`, `JSBach Casa Cultura`, `ERP Odoo`, `Wazuh SOC`, `WordPress DMZ`, `WinCLI1`, `WinCLI2`).

---

## 🚑 3. Respuesta a Incidentes y Recuperación Bare Metal (DRP)

Durante el periodo operativo ocurrieron dos incidentes críticos principales que requirieron una respuesta de emergencia inmediata:

1. **Recuperación tras Corrupción de Base de Datos en Wazuh**:
   - **Incidente**: Durante las pruebas de notificaciones masivas, peticiones síncronas masivas colapsaron la API del Wazuh Manager.
   - **Respuesta**: **Enrique Cebrián (Kike)** ejecutó la reinstalación completa del motor de gestión y aisló el Bot de Telegram para consumir exclusivamente alertas JSON no bloqueantes.
2. **Reconstrucción Bare Metal por Fallo Eléctrico Masivo**:
   - **Incidente**: Una caída generalizada de alimentación destruyó la configuración de los firewalls primarios pfSense.
   - **Respuesta**: **Jose Luis Oliver** y **Enrique Cebrián** ejecutaron los procedimientos de contingencia mediante el script **[`backupJSBach.sh`](../scripts/backup/backupJSBach.sh)**, rediseñando dinámicamente la topología para trasladar las terminaciones VPN WireGuard a los routers Linux JSBach, minimizando el tiempo de parada (RTO).
