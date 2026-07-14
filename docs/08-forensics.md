# 08. Análisis Forense (DFIR)

> **Participantes**: Carlos Delgado, Alfonso (Alfon), Jorge Cortés, Kike
> **Periodo**: Mayo 2026

## Descripción General

El análisis forense se implementó como una capa de auditoría reactiva y continua. Se buscó no solo investigar incidentes post-mortem (como el ataque del Red Team), sino establecer una línea base (baseline) diaria del estado de los equipos críticos para detectar anomalías sutiles (ej. persistencia de malware o rootkits).

## Adquisición Automatizada de Evidencias

Para evitar el error humano y asegurar una captura constante de datos, Alfon y Carlos desarrollaron un sistema de adquisición remota automatizado.

### Scripts Forenses
Se implementaron scripts en Bash/PowerShell que se ejecutaban de forma programada (cron/Task Scheduler) o bajo demanda en los endpoints:
1. **Script de Recolección**: Extrae información volátil del sistema (procesos activos, conexiones de red establecidas 
etstat, usuarios logueados, módulos del kernel cargados).
2. **Volcado de Memoria (Dump)**: Generación de volcados completos de la RAM (usando herramientas como LiME en Linux o DumpIt en Windows).
3. **Script de Reporte**: Consolida la información recolectada en un formato legible.

### Transferencia Segura
Los reportes generados eran transferidos automáticamente de forma remota al servidor del SOC, con un formato estandarizado: Reporte_[NombreEquipo]_[Fecha]_[Hora].

## Análisis con Volatility

Los *memory dumps* obtenidos eran transferidos a una estación de análisis forense aislada (Kali Linux), donde Jorge Cortés y Carlos Delgado utilizaban **Volatility Framework** para inspeccionar la memoria.

Las tareas comunes con Volatility incluían:
- linux_pslist / pslist: Comparar la lista de procesos en memoria con la obtenida por el sistema operativo (búsqueda de procesos ocultos/rootkits).
- linux_netstat / 
etscan: Identificar conexiones de red en memoria que pudieran pertenecer a *Command and Control* (C2) o *Reverse Shells*.

## Repositorio de Evidencias

El sistema automatizado generó **67 reportes forenses en formato HTML**, cubriendo la actividad de 8 equipos críticos (AD, Desktop, JSBach Ayto, JSBach CC, Odoo, SOC, WINCLI2, WordPress) durante 10 días continuos (13 al 22 de Mayo).

*(Los reportes HTML detallados se encuentran disponibles en la carpeta ../reports/forensics/ del repositorio).*
