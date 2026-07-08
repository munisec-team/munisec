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

VLAN_DATA="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp mostrar conf)"
mapfile -t VLANS <<< "$VLAN_DATA"

FOUND_LINE=""
for line in "${VLANS[@]}"; do
    IFS=';' read -r vid inici final gateway dns1 dns2 activat <<< "$line"
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

vid=$(echo $FOUND_LINE | cut -d';' -f1)
inici=$(echo $FOUND_LINE | cut -d';' -f2)
final=$(echo $FOUND_LINE | cut -d';' -f3)
gateway=$(echo $FOUND_LINE | cut -d';' -f4)
dns1=$(echo $FOUND_LINE | cut -d';' -f5)
activat=$(echo $FOUND_LINE | cut -d';' -f6)

echo "<h2>Modificar VLAN</h2>"
echo "<form action='/cgi-bin/dhcp.cgi' method='get'>"
echo "<input type='hidden' name='comand' value='configurar'>"
echo "<input type='hidden' name='accio' value='guardar_conf'>"
echo "<table>"
echo "<tr><th>VID</th><th>inici</th><th>final</th><th>gateway</th><th>dns1</th><th>activat</th></tr>"
echo "<tr>"
echo "<td><input type='text' name='vid' value='$vid' size='3' readonly></td>"
echo "<td><input type='text' class='ip' name='inici' value='$inici' size='15'></td>"
echo "<td><input type='text' class='ip' name='final' value='$final' size='15'></td>"
echo "<td><input type='text' class='ip' name='gateway' value='$gateway' size='15'></td>"
echo "<td><input type='text' class='ip' name='dns1' value='$dns1' size='15'></td>"
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
