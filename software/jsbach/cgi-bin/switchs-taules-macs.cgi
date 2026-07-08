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

echo "<h2>Taules macs</h2>"
echo "<br>"

RESULTAT=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli switchs totes_les_taula_mac)
in_table=0

while IFS= read -r linia; do
    # Si la línia comença amb "Switch ", és un nou switch
    if [[ $linia =~ ^Switch ]]; then
        if [[ $in_table -eq 1 ]]; then
            echo "</tbody></table>"
            echo "<br>"
        fi
        echo "<h3>$linia</h3>"
        echo "<table>"
        echo "<thead><tr><th>MAC</th><th>IP</th><th>VLAN</th><th>Port</th><th>Type</th><th></th></tr></thead>"
        echo "<tbody>"
        in_table=1
    # Si la línia té format de MAC (xx:xx:xx:xx:xx:xx)
    elif [[ $linia =~ ^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2} ]]; then
        read -r mac vlan port type aging <<< "$linia"
        INFO_MAC=$(fnc_ip_de_mac $mac)
        if [ -z "$INFO_MAC" ]; then
            INFO_MAC=$(fnc_mac_propia $mac)
        fi
        echo "<tr><td>$mac</td><td>$INFO_MAC</td><td>$vlan</td><td>$port</td><td>$type</td><td><a href='/cgi-bin/switchs.cgi?comand=configurar&accio=blocar_mac&mac=$mac'><button type=\"button\">Blocar</button></a></td></tr>"
    # Si la línia és el resum final d'un switch
    elif [[ $linia =~ ^Total\ MAC\ Addresses ]]; then
        if [[ $in_table -eq 1 ]]; then
            echo "</tbody></table>"
            in_table=0
        fi
        echo "<p><strong>$linia</strong></p>"
        echo "<br>"
    fi
done <<< "$RESULTAT"

if [[ $in_table -eq 1 ]]; then
    echo "</tbody></table>"
fi

echo "<br>"

/bin/cat << EOM
</body>
</html>
EOM
