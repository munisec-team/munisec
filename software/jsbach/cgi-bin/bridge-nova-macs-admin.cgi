#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html><head><title>Crear VLAN</title>"
echo "<meta charset='utf-8'>"

cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

echo "</head><body>"

echo "<h2>Agregar nova MAC per vlan admin</h2>"
echo "<form action='/cgi-bin/bridge.cgi' method='get'>"
echo "<input type='hidden' name='comand' value='configurar'>"
echo "<input type='hidden' name='argument' value='guardar'>"
echo "<input type='hidden' name='accio' value='mac'>"
echo "<table>"
echo "<tr><th>MACS</th></tr>"
echo "<tr>"
# Nom ara també més ample
echo "<td><input type='text' name='mac' value='' style='width: 250px;'></td>"
echo "</tr>"
echo "</table>"
echo "<button type='submit'>Agregar</button>"
echo "</form>"

echo "</body></html>"
