#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

QUERY_STRING=${QUERY_STRING:-$1}
nom=$(echo "$QUERY_STRING" | sed -n 's/.*nom=\([^&]*\).*/\1/p')

echo "<html><head><title>Modificar DHCP VLAN</title>"
echo "<meta charset='utf-8'>"
cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN
echo "</head><body>"

LAN_DATA="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal_captiu configurar mostrar_configuracio)"
mapfile -t LAN <<< "$LAN_DATA"

FOUND_LINE=""
for line in "${LAN[@]}"; do
    IFS=';' read -r nom_lan ip estat <<< "$line"
    if [ "$nom_lan" == "$nom" ]; then
        FOUND_LINE="$line"
        break
    fi
done

if [ -z "$FOUND_LINE" ]; then
    echo "<p><b>Error:</b> No s'ha trobat cap LAN amb nom = $nom</p>"
    echo "</body></html>"
    exit 0
fi

IFS=';' read -r nom_lan ip_lan estat_lan <<< "$FOUND_LINE"

echo "<h2>Modificar LAN</h2>"
echo "<form action='/cgi-bin/portal_captiu.cgi' method='get'>"
echo "<input type='hidden' name='comand' value='configurar'>"
echo "<input type='hidden' name='accio' value='guardar_configuracio'>"
echo "<table>"
echo "<tr><th>nom</th><th>ip</th><th>estat</th></tr>"
echo "<tr>"
echo "<td><input type='text' name='nom' value='$nom_lan' size='15' readonly></td>"
echo "<td><input type='text' class='ip' name='ip' value='$ip_lan' size='15' readonly></td>"
echo "<td><select name='estat'>"
if [ "$estat_lan" == "$ACTIVAT" ]; then
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
