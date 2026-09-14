#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

QUERY_STRING=${QUERY_STRING:-$1}
VID=$(echo "$QUERY_STRING" | sed -n 's/.*vid=\([0-9]*\).*/\1/p')

echo "<html><head><title>Esborrar  VLAN</title>"
echo "<meta charset='utf-8'>"

cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

echo "</head><body>"

VLAN_DATA="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge mostrar vlan)"
mapfile -t VLANS <<< "$VLAN_DATA"

FOUND_LINE=""
for line in "${VLANS[@]}"; do
    IFS=';' read -r nom vid subnet gw _ <<< "$line"
    if [ "$vid" == "$VID" ]; then
        FOUND_LINE="$line"
        break
    fi
done

if [ -z "$FOUND_LINE" ]; then
    echo "<p><b>Error:</b> No s'ha trobat cap VLAN amb VID = $VID</p>"
    echo "</body></html>"
    exit 0
fi

IFS=';' read -r nom vid subnet gw _ <<< "$FOUND_LINE"

echo "<h2>Esborrar VLAN</h2>"
echo "<form action='/cgi-bin/bridge.cgi' method='get'>"
echo "<input type='hidden' name='comand' value='configurar'>"
echo "<input type='hidden' name='argument' value='esborrar'>"
echo "<input type='hidden' name='accio' value='vlan'>"
echo "<table>"
echo "<tr><th>Nom</th><th>VID</th><th>IP/Subxarxa</th><th>IP/PE</th></tr>"
echo "<tr>"
# Nom ara també més ample
echo "<td><input type='text' name='nom' value='$nom' style='width: 250px;' readonly></td>"
# VID només lectura
echo "<td><input type='text' name='vid' value='$vid' readonly></td>"
# Camps IP més amplis
echo "<td><input type='text' class='ip' name='ipmasc' value='$subnet' readonly></td>"
echo "<td><input type='text' class='ip' name='ippe' value='$gw' readonly></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit'>Esborrar</button>"
echo "</form>"

echo "</body></html>"
