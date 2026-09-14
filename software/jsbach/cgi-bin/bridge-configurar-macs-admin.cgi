#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
source $DIR/$DIR_PROJECTE/$DIR_CONF/$IFWAN_CONF
source $DIR/$DIR_PROJECTE/$DIR_SCRIPTS/funcions

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>Hola món CGI</title>
EOM

echo "</head><body>"

cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

echo "<h2>Configuració Macs de vlan admin</h2>"

echo "<table>"
echo "<tr><th>MACs</th><th></th></tr>"
for mac in $(cat "$DIR/$DIR_PROJECTE/$DIR_CONF/$BRIDGE_MAC_ADMIN" | grep -v '^#'); do
    echo "<tr><td>$mac</td>"
    echo "<td><button onclick=\"location.href='/cgi-bin/bridge.cgi?comand=configurar&argument=esborrar&accio=mac&mac=$mac'\">Eliminar</button></td></tr>"
done
echo "</table>"

echo "<a href='bridge-nova-macs-admin.cgi'><button type='button'>Afegir MAC</button></a>"

/bin/cat << EOM
</body>
</html>
EOM
