#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html><head><title>Crear VLAN</title>"
echo "<meta charset='utf-8'>"

cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

echo "</head><body>"

echo "<h2>Afegir nou switch</h2>"
echo "<form action='/cgi-bin/switchs.cgi' method='get'>"
echo "<input type='hidden' name='comand' value='configurar' >"
echo "<input type='hidden' name='accio' value='afegir_switch' >"
echo "<table>"
echo "<tr><th>Nom</th><th>IP</th><th>Usuari</th><th>Contrasenya</th><th>Telnet|SSH</th></tr>"
echo "<tr>"
# Nom ara també més ample
echo "<td><input type='text' name='nom' value='' style='width: 250px;'></td>"
echo "<td><input type='text' name='ip' value='' ></td>"
echo "<td><input type='text' name='user' value=''></td>"
echo "<td><input type='text' name='pass' value=''></td>"
echo "<td><input type='text' name='protocol' value=''></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit'>Afegir switch</button>"
echo "</form>"

echo "</body></html>"
