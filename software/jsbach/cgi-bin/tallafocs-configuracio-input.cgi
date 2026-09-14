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
    echo "<h2> INPUT CONFIGURACIÓ LANS</h2>"
    echo "<br>"

    for linia in $(fnc_buscar_Lans | grep -v '#'); do
        nom=$(echo "$linia" | cut -d';' -f1)
        id=$(echo "$linia" | cut -d';' -f2)
        ip=$(echo "$linia" | cut -d';' -f3)
        estat_vlan=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs estat input $id)
        echo "<h3 style='display: flex; justify-content: space-between;'>"
        echo "<span>  Input-$nom $ip </span>"
        echo "<span> $estat_vlan</span>"
        echo "</h3>"
        case "$estat_vlan" in
            "CONNECTADA")
                echo "<a href='tallafocs.cgi?comand=configurar&id=$id&accio=desconnectar_input'><button type='button'>DESCONECTAR INPUT</button></a>"
                echo "<a href='tallafocs-crear-regla-input.cgi?vnom=$nom&id=$id'><button type='button'>REGLES INPUT PROPIES</button></a>"
                ;;
            "DESCONNECTADA")
                echo "<a href='tallafocs.cgi?comand=configurar&id=$id&accio=connectar_input'><button type='button'>CONNECTAR INPUT</button></a>"
                echo "<a href='tallafocs-crear-regla-input.cgi?vnom=$nom&id=$id'><button type='button'>REGLES INPUT PROPIES</button></a>"
                ;;
            "REGLES PROPIES")
                echo "<a href='tallafocs.cgi?comand=configurar&id=$id&accio=desconnectar_input'><button type='button'>DESCONECTAR INPUT</button></a>"
                echo "<a href='tallafocs.cgi?comand=configurar&id=$id&accio=connectar_input'><button type='button'>CONNECTAR INPUT</button></a>"
                echo "<a href='tallafocs-crear-regla-input.cgi?vnom=$nom&id=$id'><button type='button'>REGLES INPUT PROPIES</button></a>"
                ;;
        esac

        echo "<br>"
    done

    echo "<br>"
    echo "<h2> INPUT CONFIGURACIÓ WAN </h2>"
    echo "<br>"
    echo "<h3 style='display: flex; justify-content: space-between;'>"
    echo "<span>  Input-WAN </span>"
    echo "</h3>"
    echo "<a href='tallafocs-crear-regla-wan.cgi?'><button type='button'>EDITAR REGLES INPUT WAN</button></a>"

    echo "<br>"
    echo "<br>"
    echo "<br>"
    echo "<h2> INPUT CONFIGURACIO MODES (s'apliquen en les regles propies de cada vlan)</h2>"

    echo "<br>"
    echo "<h3> mode serveis dns dhcp i portal captiu </h3>"
    /bin/cat << EOM
	<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
	  <thead>
	    <tr>
	      <th>Regles</th>
	    </tr>
	  </thead>
	  <tbody>
EOM
    while IFS= read -r linia; do
        # Saltar línies buides i comentaris
        [ -z "$linia" || "$linia" =~ ^# ]] && continue
        echo "<tr>"
        echo "<td>$linia</td>"
        echo "</tr>"
    done < "$DIR/$DIR_PROJECTE/$DIR_CONF/$IPTABLES_INPUT_DNS_DHCP_PC"
    echo "</tbody>"
    echo "</table>"
    echo "<a href='tallafocs-crear-regla-dns_dhcp_pc.cgi?'><button type='button'>EDITAR REGLES INPUT DNS DHCP PC</button></a>"

else
    echo "<h3> </h3>"
    echo "<h2>TALLAFOCS NO INICIAT</h2>"
fi
/bin/cat << EOM
	</body>
	</html>
EOM
