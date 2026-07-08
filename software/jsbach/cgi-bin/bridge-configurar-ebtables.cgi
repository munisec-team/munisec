#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

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

estat_ebtables=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge estat_ebtables)
while read -r NOM VLAN ESTAT; do
    echo "<h2 style='display: flex; justify-content: space-between;'>"
    echo "<span>  ports de $NOM amb vid $VLAN </span>"
    echo "<span> $ESTAT</span>"
    echo "</h2>"
    case "$ESTAT" in
        "aïllada")
            echo "<a href='bridge.cgi?comand=configurar&argument=desaillar&vlan=$VLAN'><button type='button'>DESAILLAR</button></a>"
            if [[ "$VLAN" == "1" ]]; then
                echo "<a href='bridge.cgi?comand=configurar&argument=aplicar_macs_admin&vlan=$VLAN'><button type='button'>APLICAR MACS ADMIN</button></a>"
                echo "<a href='bridge-configurar-macs-admin.cgi'><button type='button'>CONFIGURAR MACS ADMIN</button></a>"
            fi
            ;;
        "desaïllada")
            echo "<a href='bridge.cgi?comand=configurar&argument=aillar&vlan=$VLAN'><button type='button'>AILLAR</button></a>"
            if [[ "$VLAN" == "1" ]]; then
                echo "<a href='bridge.cgi?comand=configurar&argument=aplicar_macs_admin&vlan=$VLAN'><button type='button'>APLICAR MACS ADMIN</button></a>"
                echo "<a href='bridge-configurar-macs-admin.cgi'><button type='button'>CONFIGURAR MACS ADMIN</button></a>"
            fi
            ;;
        "MACS ADMIN aplicades")
            echo "<a href='bridge.cgi?comand=configurar&argument=aillar&vlan=$VLAN'><button type='button'>AILLAR</button></a>"
            echo "<a href='bridge.cgi?comand=configurar&argument=no_aplicar_macs_admin&vlan=$VLAN'><button type='button'>NO APLICAR MACS ADMIN</button></a>"
            echo "<a href='bridge-configurar-macs-admin.cgi'><button type='button'>CONFIGURAR MACS ADMIN</button></a>"
            ;;
    esac
done <<< "$estat_ebtables"

/bin/cat << EOM
	</body>
	</html>
EOM
