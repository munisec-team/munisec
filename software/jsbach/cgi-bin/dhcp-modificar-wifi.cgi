#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

QUERY_STRING=${QUERY_STRING:-$1}
VID=$(echo "$QUERY_STRING" | sed -n 's/.*vid=\([0-9]*\).*/\1/p')

echo "<html><head><title>Modificar DHCP VLAN</title>"
echo "<meta charset='utf-8'>"
cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN
echo "</head><body>"

WIFI_DATA="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp mostrar wifi_conf)"

if [ -z "$WIFI_DATA" ]; then
    echo "<p><b>Error:</b> No s'ha trobat cap WIFI</p>"
    echo "</body></html>"
    exit 0
fi

IFS=';' read -r interface ip inici final gateway dns1 activat <<< "$WIFI_DATA"

echo "<h2>Modificar WIFI</h2>"
echo "<form action='/cgi-bin/dhcp.cgi' method='get'>"
echo "<input type='hidden' name='comand' value='configurar'>"
echo "<input type='hidden' name='accio' value='guardar_wifi_conf'>"
echo "<table>"
echo "<tr><th>interface</th><th>ip</th><th>inici</th><th>final</th><th>gateway</th><th>dns1</th><th>activat</th></tr>"
echo "<tr>"
echo "<td><input type='text' name='interface' value='$interface' size='10' readonly></td>"
echo "<td><input type='text' class='ip' name='ip' value='$ip' size='10'readonly></td>"
echo "<td><input type='text' class='ip' name='inici' value='$inici' size='10'></td>"
echo "<td><input type='text' class='ip' name='final' value='$final' size='10'></td>"
echo "<td><input type='text' class='ip' name='gateway' value='$gateway' size='10'></td>"
echo "<td><input type='text' class='ip' name='dns1' value='$dns1' size='10'></td>"
echo "<td><select name='activat'>"
if [ "$activat" == "$ACTIVAT" ]; then
    echo "<option value='$ACTIVAT' selected>$ACTIVAT</option>"
    echo "<option value='$DESACTIVAT'>$DESACTIVAT</option>"
else
    echo "<option value='$ACTIVAT'>$ACTIVAT</option>"
    echo "<option value='$DESACTIVAT' selected>$DESACTIVAT</option>"
fi
echo "</select></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit'>Guardar</button>"
echo "</form>"

echo "</body></html>"
