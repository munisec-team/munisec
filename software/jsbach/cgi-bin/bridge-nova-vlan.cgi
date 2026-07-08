#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html><head><title>Crear VLAN</title>"
echo "<meta charset='utf-8'>"

cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

echo "</head><body>"

echo "<h2>Crear VLAN</h2>"
echo "<form action='/cgi-bin/bridge.cgi' method='get'>"
echo "<input type='hidden' name='comand' value='configurar'>"
echo "<input type='hidden' name='argument' value='guardar'>"
echo "<input type='hidden' name='accio' value='vlan_nova'>"
echo "<table>"
echo "<tr><th>Nom</th><th>VID</th><th>IP-Subxarxa/Mascara</th><th>IP-Porta d'Enllaç/Mascara</th></tr>"
echo "<tr>"
# Nom ara també més ample
echo "<td><input type='text' name='nom' value='' style='width: 250px;'></td>"
# VID només lectura
echo "<td><input type='text' name='vid' value='' ></td>"
# Camps IP més amplis
echo "<td><input type='text' class='ip' name='ipmasc' value=''></td>"
echo "<td><input type='text' class='ip' name='ippe' value=''></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit'>Crear</button>"
echo "</form>"

echo "</body></html>"
