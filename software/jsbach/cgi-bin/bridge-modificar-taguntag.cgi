#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

int=$(echo "$QUERY_STRING" | sed -n 's/^.*int=\([^&]*\).*$/\1/p')

echo "<html><head><title>Modificar VLAN</title>"
echo "<meta charset='utf-8'>"

cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

echo "</head><body>"

VLAN_DATA="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge mostrar bridge)"
linia_int=$(echo "$VLAN_DATA" | grep -E "^${int};")
VLAN_UNTAG=$(echo "$linia_int" | cut -d';' -f2)
if [[ -z "$VLAN_UNTAG" ]]; then
    VLAN_UNTAG=0
fi
VLAN_TAG=$(echo "$linia_int" | cut -d';' -f3)
if [[ -z "$VLAN_TAG" ]]; then
    VLAN_TAG=0
fi

echo "<h2>Modificar Tag-Untag</h2>"
echo "<form action='/cgi-bin/bridge.cgi' method='get'>"
echo "<input type='hidden' name='comand' value='configurar'>"
echo "<input type='hidden' name='argument' value='guardar'>"
echo "<input type='hidden' name='accio' value='bridge'>"
echo "<input type='hidden' name='retorn' value='bridge-configurar-taguntag.cgi'>"
echo "<table>"
echo "<tr><th>Interfaç</th><th>Untag</th><th>Tag</th></tr>"
echo "<tr>"

echo "<td><input type='text' name='int' value='$int' style='width: 250px;' readonly></td>"
echo "<td><input type='text' class='untag' name='untag' value='$VLAN_UNTAG'></td>"
echo "<td><input type='text' class='tag' name='tag' value='$VLAN_TAG'></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit'>Guardar</button>"
echo "</form>"

echo "</body></html>"
