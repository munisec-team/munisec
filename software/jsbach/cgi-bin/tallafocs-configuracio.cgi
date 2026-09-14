#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
source $DIR/$DIR_PROJECTE/$DIR_SCRIPTS/$FUNCIONS

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>Hola món CGI</title>

EOM
cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN
/bin/cat << EOM
</head>
<body>
EOM

estat_tallafocs=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs estat)
if [[ "$estat_tallafocs" == $ACTIVAT* ]]; then
    echo "<h2> FORWARD CONFIGURACIÓ LANS </h2>"
    echo "<br>"

    for linia in $(fnc_buscar_Lans | grep -v '#'); do
        nom=$(echo "$linia" | cut -d';' -f1)
        id=$(echo "$linia" | cut -d';' -f2)
        ip=$(echo "$linia" | cut -d';' -f3)
        estat_vlan=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs estat forward $id)
        echo "<h3 style='display: flex; justify-content: space-between;'>"
        echo "<span>  $nom $ip </span>"
        echo "<span> $estat_vlan</span>"
        echo "</h3>"
        case "$estat_vlan" in
            "CONNECTADA")
                echo "<a href='tallafocs.cgi?comand=configurar&id=$id&accio=desconnectar&retorn=tallafocs-configuracio.cgi'><button type='button'>DESCONECTAR FORWARD</button></a>"
                echo "<a href='tallafocs-crear-regla.cgi?vnom=$nom&id=$id'><button type='button'>REGLES FORWARD PROPIES</button></a>"
                ;;
            "DESCONNECTADA")
                if [[ "$id" == "1" || "$id" == "2" ]]; then
                    echo "<a href='tallafocs.cgi?comand=configurar&id=$id&accio=aillar&retorn=tallafocs-configuracio.cgi'><button type='button'>AÏLLAR FORWARD</button></a>"
                else
                    echo "<a href='tallafocs.cgi?comand=configurar&id=$id&accio=connectar&retorn=tallafocs-configuracio.cgi'><button type='button'>CONNECTAR FORWARD</button></a>"
                    echo "<a href='tallafocs-crear-regla.cgi?vnom=$nom&id=$id'><button type='button'>REGLES FORWARD PROPIES</button></a>"
                fi
                ;;
            "REGLES PROPIES")
                echo "<a href='tallafocs.cgi?comand=configurar&id=$id&accio=desconnectar&retorn=tallafocs-configuracio.cgi'><button type='button'>DESCONECTAR FORWARD</button></a>"
                echo "<a href='tallafocs.cgi?comand=configurar&id=$id&accio=connectar&retorn=tallafocs-configuracio.cgi'><button type='button'>CONNECTAR FORWARD</button></a>"
                echo "<a href='tallafocs-crear-regla.cgi?vnom=$nom&id=$id'><button type='button'>REGLES FORWARD PROPIES</button></a>"
                ;;
            "AÏLLADA")
                echo "<a href='tallafocs.cgi?comand=configurar&id=$id&accio=desconnectar&retorn=tallafocs-configuracio.cgi'><button type='button'>DESCONECTAR FORWARD</button></a>"
                ;;
        esac

    done

    echo "<br>"
    echo "<br>"
    echo "<br>"
    echo "<h2> FORWARD CONFIGURACIO MODES (s'apliquen en les regles propies de cada vlan)</h2>"

    echo "<br>"
    echo "<h3> mode ports_wls forward (ports acceptats)</h3>"
    /bin/cat << EOM
	<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
	  <thead>
	    <tr>
	      <th>Protocol</th>
	      <th>Port</th>
	      <th></th>
	    </tr>
	  </thead>
	  <tbody>
EOM

    for linia in $(grep -v '#' "$DIR/$DIR_PROJECTE/$DIR_CONF/$IPTABLES_PORTS_WLS"); do
        PROTOCOL=$(echo "$linia" | cut -d';' -f1)
        PORT=$(echo "$linia" | cut -d';' -f2)
        echo "<tr>"
        echo "<td>$PROTOCOL</td>"
        echo "<td>$PORT</td>"
        echo "<td>"
        echo "<a href='tallafocs.cgi?comand=configurar&accio=eliminar_port_wls&protocol=$PROTOCOL&port=$PORT&retorn=tallafocs-configuracio.cgi'><button type='button'>Eliminar</button></a>"
        echo "</td>"
        echo "</tr>"
    done
    echo "</tbody>"
    echo "</table>"
    echo "<a href='tallafocs-nova-port.cgi?accio=afegir_port_wls'><button type='button'>Afegir port</button></a>"

    echo "<br>"
    echo "<br>"

    echo "<br>"
    echo "<h3> mode dominis_wls forward (dominis o ips acceptades)</h3>"
    /bin/cat << EOM
	<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
	  <thead>
	    <tr>
	      <th>Domini</th>
	      <th></th>
	    </tr>
	  </thead>
	  <tbody>
EOM

    for linia in $(grep -v '#' "$DIR/$DIR_PROJECTE/$DIR_CONF/$IPTABLES_DOMINIS_WLS"); do
        DOMINI=$(echo "$linia" | cut -d';' -f1)
        echo "<tr>"
        echo "<td>$DOMINI</td>"
        echo "<td>"
        echo "<a href='tallafocs.cgi?comand=configurar&accio=eliminar_dominis_wls&domini=$DOMINI&retorn=tallafocs-configuracio.cgi'><button type='button'>Eliminar</button></a>"
        echo "</td>"
        echo "</tr>"
    done
    echo "</tbody>"
    echo "</table>"
    echo "<a href='tallafocs-nova-domini.cgi?accio=afegir_dominis_wls'><button type='button'>Afegir domini</button></a>"

    echo "<br>"
    echo "<br>"

 echo "<br>"
    echo "<h3> mode ports_bls forward (ports bloquejats)</h3>"
    /bin/cat << EOM
	<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
	  <thead>
	    <tr>
	      <th>Protocol</th>
	      <th>Port</th>
	      <th></th>
	    </tr>
	  </thead>
	  <tbody>
EOM

    for linia in $(grep -v '#' "$DIR/$DIR_PROJECTE/$DIR_CONF/$IPTABLES_PORTS_BLS"); do
        PROTOCOL=$(echo "$linia" | cut -d';' -f1)
        PORT=$(echo "$linia" | cut -d';' -f2)
        echo "<tr>"
        echo "<td>$PROTOCOL</td>"
        echo "<td>$PORT</td>"
        echo "<td>"
        echo "<a href='tallafocs.cgi?comand=configurar&accio=eliminar_port_bls&protocol=$PROTOCOL&port=$PORT&retorn=tallafocs-configuracio.cgi'><button type='button'>Eliminar</button></a>"
        echo "</td>"
        echo "</tr>"
    done
    echo "</tbody>"
    echo "</table>"
    echo "<a href='tallafocs-nova-port.cgi?accio=afegir_port_bls'><button type='button'>Afegir port</button></a>"

    echo "<br>"
    echo "<br>"

    echo "<br>"
    echo "<h3> mode dominis_bls forward (dominis o ips bloquejades)</h3>"
    /bin/cat << EOM
	<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
	  <thead>
	    <tr>
	      <th>Domini</th>
	      <th></th>
	    </tr>
	  </thead>
	  <tbody>
EOM

    for linia in $(grep -v '#' "$DIR/$DIR_PROJECTE/$DIR_CONF/$IPTABLES_DOMINIS_BLS"); do
        DOMINI=$(echo "$linia" | cut -d';' -f1)
        echo "<tr>"
        echo "<td>$DOMINI</td>"
        echo "<td>"
        echo "<a href='tallafocs.cgi?comand=configurar&accio=eliminar_dominis_bls&domini=$DOMINI&retorn=tallafocs-configuracio.cgi'><button type='button'>Eliminar</button></a>"
        echo "</td>"
        echo "</tr>"
    done
    echo "</tbody>"
    echo "</table>"
    echo "<a href='tallafocs-nova-domini.cgi?accio=afegir_dominis_bls'><button type='button'>Afegir domini</button></a>"

    echo "<br>"
    echo "<br>"

else
    echo "<h2> </h2>"
    echo "<h3>TALLAFOCS NO INICIAT</h3>"
fi
/bin/cat << EOM
	</body>
	</html>
EOM
