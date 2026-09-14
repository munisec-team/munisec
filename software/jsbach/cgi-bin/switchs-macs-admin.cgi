#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html>"
echo "<head>"
echo "  <meta charset=\"utf-8\">"
echo "  <title>Hola món CGI</title>"

cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

echo "</head>"
echo "<body>"

RESULTAT=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli switchs configurar veure_macs_vlan_admin)

echo "</tbody></table>"
echo "<br>"
echo "<h2>Taula de macs admeses en vlan admin</h2>"
echo "<table>"
echo "<thead><tr><th>MAC</th><th></th></tr></thead>"
echo "<tbody>"
while IFS= read -r linia; do
    if [ -z "$linia" ]; then
        continue
    fi
    echo "<tr><td>$linia</td><td><a href='/cgi-bin/switchs.cgi?comand=configurar&accio=eliminar_mac_vlan_admin&mac=$linia'><button type="button">Eliminar</button></a></td></tr>"
done <<< "$RESULTAT"
echo "</tbody></table>"

echo "<br>"
echo "<h2>Afegir mac</h2>"
echo "<table>"
echo "<thead><tr><th>MAC</th><th></th></tr></thead>"
echo "<tbody>"
echo "<form action='/cgi-bin/switchs.cgi' method='get'>"
echo "<input type='hidden' value='configurar' name='comand'>"
echo "<input type='hidden' value='afegir_mac_vlan_admin' name='accio'>"
echo "<tr><td><input type='text' name='mac'></td>"
echo "<td><input type='submit' value='Afegir i aplicar'></td></tr>"
echo "</form>"
echo "</tbody></table>"

echo "</body>"
echo "</html>"
