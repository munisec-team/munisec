#!/bin/bash
#
# Este script tiene como propósito hacer BACKUPS de JSBach y RESTAURARLOS,
# así como configurar SSL en la web una vez instalado JSBach
#

if [ $EUID -ne 0 ]; then
	echo "Ejecuta como root"
	exit 1
fi

function setup_dir (){
	if [ ! -d $1 ]; then
		mkdir -p $1
	fi

}

actualTimestamp=$(date +%d-%m-%Y_%H-%M)
backupRoute="backups/JSBach_$actualTimestamp"

jsbachConfRoute="/usr/local/JSBach/conf/"
jsbachScriptsRoute="/usr/local/JSBach/scripts/"
jsbachLoggerRoute="/usr/local/bin/jsbach-logger.sh"
sslKeyRoute="/etc/ssl/private/jsbach.key"
sslCertRoute="/etc/ssl/certs/jsbach.crt"
apacheSiteConfRoute="/etc/apache2/sites-available/jsbach_site.conf"
rsyslogConfRoute="/etc/rsyslog.d/60-custom-log.conf"

case $1 in
	--backup)
		# Scripts JSBach (logging implementado)
		setup_dir $backupRoute/jsbach_scripts/
		if [ -d $jsbachScriptsRoute ]; then
			echo "Haciendo copia de los scripts de JSBach..."
			cp -R $jsbachScriptsRoute* $backupRoute/jsbach_scripts/
		else
			echo "No se han detectado SCRIPTS de JSBach"
		fi

		# Logger
		setup_dir $backupRoute/jsbach_logger/
		if [ -f $jsbachLoggerRoute ]; then
			echo "Haciendo copia del logger jsbach-logger.sh..."
			cp $jsbachLoggerRoute $backupRoute/jsbach_logger/
		else
			echo "No se ha detectado el logger jsbach-logger.sh"
		fi

		# Config Rsyslog
		setup_dir $backupRoute/jsbach_rsyslog/
		if [ -f $rsyslogConfRoute ]; then
			echo "Haciendo copia de la conf rsyslog 60-custom-log.conf..."
			cp $rsyslogConfRoute $backupRoute/jsbach_rsyslog/
		else
			echo "No se ha detectado conf de rsyslog en $rsyslogConfRoute"
		fi

		# Configuración JSBach
		setup_dir $backupRoute/jsbach_conf/
		if [ -d $jsbachConfRoute ]; then
			echo "Haciendo copia de la conf de JSBach..."
			cp -R $jsbachConfRoute* $backupRoute/jsbach_conf/
		else
			echo "No se ha detectado conf de JSBach (VLANs, switches, DMZ, etc.)"
		fi
		
		# Certificados
		sslFileMiss=0
		setup_dir $backupRoute/ssl/
		if [ -f $sslKeyRoute ]; then
			echo "Haciendo copia de jsbach.key..."
			cp $sslKeyRoute $backupRoute/ssl/
		else
			echo "No se ha detectado un jsbach.key"
			sslFileMiss=1
		fi
		if [ -f $sslCertRoute ]; then
			echo "Haciendo copia de jsbach.crt..."
			cp $sslCertRoute $backupRoute/ssl/
		else
			echo "No se ha detectado un jsbach.crt"
			sslFileMiss=1
		fi

		if [ $sslFileMiss -eq 1 ]; then
			echo "Proceda con precaución al RESTAURAR si el servidor estaba configurado por HTTPS"
			echo "El servidor puede llegar a ROMPERSE por AUSENCIA de certificados"
		else
			chmod 600 $backupRoute/ssl/*
		fi

		# Configuración sitio apache
		setup_dir $backupRoute/apache_conf/
		if [ -f $apacheSiteConfRoute ]; then
			echo "Haciendo copia de la conf del sitio JSBach en Apache..."
			cp $apacheSiteConfRoute $backupRoute/apache_conf/
		else
			echo "No se ha detectado una conf del sitio JSBach en Apache"
		fi
	;;

	--restore)

		if [ -z $2 ] || [ ! -d $2 ]; then
			echo "Uso: sudo bash backupJSBach.sh --restore /ruta/a/directorio/backup"
			exit 1
		fi
		if [ ! -d /usr/local/JSBach ]; then
			echo "JSBach tiene que estar instalado para poder proceder"
			exit 1
		fi

		# Cosas que son más delicadas de restaurar en masa por seguridad
		case $3 in
			--rsyslog)
				# Rsyslog
				if [ -f $rsyslogConfRoute ]; then
					echo "Se ha detectado un 60-custom-log.conf ya existente."
					echo "Haciendo backup a 60-custom-log.conf antes de restaurar"
					mv $rsyslogConfRoute $rsyslogConfRoute.bak
				fi
				cp $2/jsbach_rsyslog/60-custom-log.conf $rsyslogConfRoute
				sudo systemctl restart rsyslog
				;;
		esac

		# Scripts JSBach
		rm -r $jsbachScriptsRoute*
		cp -R $2/jsbach_scripts/* $jsbachScriptsRoute

		# Logger
		if [ -f $jsbachLoggerRoute ]; then
			echo "Se ha detectado un jsbach-logger.sh ya existente."
			echo "Haciendo backup a jsbach-logger.sh.bak antes de restaurar"
			mv $jsbachLoggerRoute $jsbachLoggerRoute.bak
		fi
		cp $2/jsbach_logger/jsbach-logger.sh /usr/local/bin/

		# Configuración JSBach
		rm -r $jsbachConfRoute*
		cp -R $2/jsbach_conf/* $jsbachConfRoute

		# Certficados
		if [ -f $sslKeyRoute ]; then
			echo "Se ha detectado un jsbach.key ya existente."
			echo "Haciendo backup a jsbach.key.bak antes de restaurar"
			mv $sslKeyRoute $sslKeyRoute.bak
		fi
		if [ -f $sslCertRoute ]; then
			echo "Se ha detectado un jsbach.crt ya existente."
			echo "Haciendo backup a jsbach.crt.bak antes de restaurar"
			mv $sslCertRoute $sslCertRoute.bak
		fi

		cp $2/ssl/jsbach.key $sslKeyRoute
		cp $2/ssl/jsbach.crt $sslCertRoute

		# Configuración sitio apache
		if [ -f $apacheSiteConf ]; then
			echo "Se ha detectado el sitio jsbach_site.conf en apache"
			echo "Haciendo backup a jsbach_site.conf.bak"
			mv $apacheSiteConfRoute $apacheSiteConfRoute.bak
		fi
		cp $2/apache_conf/jsbach_site.conf $apacheSiteConfRoute

		# Reinicio apache
		echo "Eliminando sites residuales..."
		if a2dissite jsbach-cgi &>/dev/null || a2dissite jsbach_site &>/dev/null; then
			echo "Sites residuales eliminados"
		fi
		if a2ensite jsbach_site.conf &>/dev/null; then
			echo "Sitio jsbach_site.conf habilitado correctamente"
		fi
		systemctl reload apache2 && systemctl restart apache2

		echo "[WARNING] NO SE HA RESTAURADO LA CONFIG RSYSLOG POR SEGURIDAD."
		echo "SI DESEA RESTAURARLO, EJECUTE sudo bash backupJSBach.sh --restore /ruta/a/directorio/backup --rsyslog"
	;;

	*)
		echo "Falta argumento \$1"
		echo "Uso: sudo bash backupJSBach.sh [--backup|--restore]"
		exit 1
	;;
esac

