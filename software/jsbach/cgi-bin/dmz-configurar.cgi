#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
source $DIR/$DIR_PROJECTE/$DIR_CONF/$IFWAN_CONF
source $DIR/$DIR_PROJECTE/$DIR_SCRIPTS/funcions

echo "Content-type: text/html; charset=utf-8"
echo ""

VLAN_DATA="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge mostrar bridge)"

/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>Hola món CGI</title>
EOM

echo "</head><body>"

cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

echo "<h2>Configuració DMZ</h2>"

echo "<table>"
echo "<tr><th>Port</th><th>Protocol</th><th>ip</th><th></th></tr>"

for iface in $("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dmz mostrar); do
    PORT=$(echo "$iface" | cut -d';' -f1)
    PROTO=$(echo "$iface" | cut -d';' -f2)
    IP_DMZ=$(echo "$iface" | cut -d';' -f3)

    echo "<tr><td>$PORT</td><td>$PROTO</td><td>$IP_DMZ</td>"

    echo "<td><button onclick=\"location.href='/cgi-bin/dmz.cgi?comand=configurar&argument=eliminar&port=$PORT&proto=$PROTO&ipdmz=$IP_DMZ'\">Eliminar</button></td></tr>"
done
echo "</table>"

echo "<button onclick=\"location.href='/cgi-bin/dmz-nou-servei.cgi'\">Obrir nou servei</button>"

/bin/cat << EOM
</body>
</html>
EOM
