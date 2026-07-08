# Restablecimiento Red tras tormenta eléctrica

✅ Tarea realizada: Restablecimiento de red en los Switchs y Routers JSBach
👤 Persona: kike
📅 Fecha: 28 de abril de 2026
📝 Descripción / Bitácora: Gracias a la copia de seguridad de la configuración de los distintos switches y de los backups de los routers, tras la tormenta sufrida la noche anterior fue “relativamente rápida” la restauracion de la red.
El orden en que realizamos dicha restauración fue el siguiente:
1)Nos conectamos al switch, una vez accedido a la interfaz de configuración de este system→systemtools→RestoreConfig→browser(buscamos donde tenemos la copia)→export, cargara el fichero y añadimos reinicio automatico.
2) Cambiamos IP para poder comprobar que el switch se ha configurado según lo esperado.
3)Realizamos misma operación en los otros 2 switches.
4)Instalamos en los dos routers afectados por los rayos la versión de ubuntu 24.04 desktop.(Gracias a la copia de seguridad de dicho S.O)
5)Procedemos a la instalación y restauración de nuestros Routers, el orden fue el siguiente:
Copiamos la carpeta de JSBAch a la la ruta correspondiente (/usr/local/JSBach) .
Accedemos a la carpeta de install y una vez en está lanzamos el sript de instalación.
Realizada la instalación, accedemos a nuestro router y comprobamos que la instalación se habia realizado correctamente.
En último lugar, comprobamos el correcto funcionamiento de la red conectandose un equipo a la biblioteca y otro al Ayuntamiento  y efectivamente tenian acceso a internet, con lo que verificamos que el incidente habia sido subsanado.

🚧 Bloqueos / Problemas: Lecciones aprendidas:
No tener sólo una copia de seguridad, que cada responsable tenga una copia e incluso una tercera copia en otro dispositivo guardada en el Ayto.