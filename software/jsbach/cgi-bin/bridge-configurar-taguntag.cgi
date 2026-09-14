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
 cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN
echo "</head><body>"
 

ESTAT=$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli bridge estat)

if echo "$ESTAT" | grep -q "^ACTIVAT"; then
    echo "<h2>Per configurar el bridge primer ha d'estar desactivat</h2>"

    echo "<table>"
    echo "<tr><th>Interfaç</th><th>UNTAG</th><th>TAG</th></tr>"
    for iface in $VLAN_DATA; do
        VLAN_IF=$(echo "$iface" | cut -d';' -f1)
        VLAN_UNTAG=$(echo "$iface" | cut -d';' -f2)
        VLAN_TAG=$(echo "$iface" | cut -d';' -f3)
        echo "<tr><td>$VLAN_IF</td>"
        echo "<td>$VLAN_UNTAG</td>"
        echo "<td>$VLAN_TAG</td>"
    done
    echo "</table>"
    echo "<br>"
    echo "<br>"



    echo "<h3>Interfaces fora del bridge</h3>"
    echo "<table>"
    echo "<tr><th>Interfaç</th></tr>"
    for iface in $(fnc_interfaces_ethernet | grep -vF "$IFW_IFWAN"); do
        linia_int=$(echo "$VLAN_DATA" | grep -E "^${iface};")
        VLAN_UNTAG=$(echo "$linia_int" | cut -d';' -f2)
        if [[ -z "$VLAN_UNTAG" ]]; then
            echo "<tr><td>$iface</td></tr>"
        fi
    done
    echo "</table>"

else
    echo "<h2>Configuració Interfaces i Tag-Untag</h2>"
    echo "<table>"
    echo "<tr><th>Interfaç</th><th>UNTAG</th><th>TAG</th><th></th></tr>"
    for iface in $VLAN_DATA; do
        VLAN_IF=$(echo "$iface" | cut -d';' -f1)
        VLAN_UNTAG=$(echo "$iface" | cut -d';' -f2)
        VLAN_TAG=$(echo "$iface" | cut -d';' -f3)
        echo "<tr><td>$VLAN_IF</td>"
        echo "<td>$VLAN_UNTAG</td>"
        echo "<td>$VLAN_TAG</td>"
        echo "<td><button onclick=\"location.href='/cgi-bin/bridge-modificar-taguntag.cgi?int=$VLAN_IF'\">Modificar</button><button onclick=\"location.href='/cgi-bin/bridge.cgi?comand=configurar&argument=esborrar&accio=bridge&int=$VLAN_IF&retorn=bridge-configurar-taguntag.cgi'\">Esborrar interfaç del bridge</button></td></td></tr>"
    done
    echo "</table>"
    echo "<br>"
    echo "<br>"



    echo "<h3>Afegir interfaces al bridge</h3>"
    echo "<table>"
    echo "<tr><th>Interfaç</th><th></th></tr>"
    for iface in $(fnc_interfaces_ethernet | grep -vF "$IFW_IFWAN"); do
        linia_int=$(echo "$VLAN_DATA" | grep -E "^${iface};")
        VLAN_UNTAG=$(echo "$linia_int" | cut -d';' -f2)
        if [[ -z "$VLAN_UNTAG" ]]; then
            echo "<tr><td>$iface</td><td><button onclick=\"location.href='/cgi-bin/bridge.cgi?comand=configurar&argument=guardar&accio=bridge&int=$iface&untag=0&tag=0&retorn=bridge-configurar-taguntag.cgi'\">Afegir al bridge</button></td></tr>"
        fi
    done
    echo "</table>"
fi
/bin/cat << EOM


</body>
</html>
EOM
