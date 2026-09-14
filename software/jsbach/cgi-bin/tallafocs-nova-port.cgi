#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html><head><title>Crear VLAN</title>"
echo "<meta charset='utf-8'>"

cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN
accio=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')
llista=$(echo "$accio"| cut -d'_' -f3)

echo "</head><body>"

echo "<h2>Afegir port a mode ports $llista</h2>"
echo "<form action='/cgi-bin/tallafocs.cgi' method='get'>"
echo "<input type='hidden' name='comand' value='configurar'>"
echo "<input type='hidden' name='accio' value=$accio>"
echo "<input type='hidden' name='retorn' value='tallafocs-configuracio.cgi'>"
echo "<table>"
echo "<tr><th>protocol</th><th>port</th></tr>"
echo "<tr>"
echo "<td><input type='text' name='protocol' value='' style='width: 250px;'></td>"
echo "<td><input type='text' name='port' value='' ></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit'>Afegir</button>"
echo "</form>"

echo "</body></html>"