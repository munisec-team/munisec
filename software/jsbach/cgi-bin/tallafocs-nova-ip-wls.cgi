#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html><head><title>Crear VLAN</title>"
echo "<meta charset='utf-8'>"

cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

echo "</head><body>"

echo "<h2>Afegir ip sense restriccions a ip_wls</h2>"
echo "<form action='/cgi-bin/tallafocs.cgi' method='get'>"
echo "<input type='hidden' name='comand' value='configurar'>"
echo "<input type='hidden' name='accio' value='afegir_ip_wls'>"
echo "<input type='hidden' name='retorn' value='tallafocs-configuracio.cgi'>"
echo "<table>"
echo "<tr><th>vid, si es la WIFI posa 4095</th><th>ip</th><th>mac</th></tr>"
echo "<tr>"
echo "<td><input type='text' name='vid' value='' style='width: 250px;'></td>"
echo "<td><input type='text' name='ip' value='' ></td>"
echo "<td><input type='text' name='mac' value=''></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit'>Afegir</button>"
echo "</form>"

echo "</body></html>"
