#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html>"
echo "<head>"
echo "  <meta charset=\"utf-8\">"
echo "  <title>Hola món CGI</title>"
echo "</head>"

cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

echo "<body>"


ESTAT_PORTMIRROR=$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror estat)
if [[ "$ESTAT_PORTMIRROR" == $ACTIVAT* ]]; then
    echo "<h2>Port Mirror, per configurar ha d'estar desactivat</h2>"
    echo "<br>"
    INTERFACE_SENSOR=$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror mostrar interface_sensor)
    echo "Interfaç per on s'envien les captures: $INTERFACE_SENSOR"
    echo "<br><br>"
    LLISTA_INTEFACES=$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror mostrar interfaces_aptes_sensor)
    echo "Interfaces per on s'envien les captures: $LLISTA_INTEFACES"

    echo "<br>"
    echo "<pre>$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror estat)</pre>"
    
else

    echo "<h2>Port Mirror configurar</h2>"
    echo "<br>"
    INTERFACE_SENSOR=$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror mostrar interface_sensor)
    if [ -z "$INTERFACE_SENSOR" ]; then
        echo "Interfaç per on s'envien les captures: <font color='red'><h5>NO SELECCIONADA</font>"
    else
        echo "Interfaç per on s'envien les captures: <h5>$INTERFACE_SENSOR</h5>"
    fi
    
    echo "Canviar Interfaç per on s'envien les captures (no pot formar part del bridge ni estar activada)"
    LLISTA_INTEFACES=$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror mostrar interfaces_aptes_sensor)
    echo "<form method=\"get\" action=\"/cgi-bin/portmirror.cgi\">"
    echo "<input type='hidden' name='comand' value='configurar'>"
    echo "<input type='hidden' name='argument' value='canviar_interface_sensor'>"
    echo "<input type='hidden' name='retorn' value='portmirror-configurar.cgi'>"
    echo "<select name=\"interface_sensor\">"
    for interface in $LLISTA_INTEFACES
    do
        if [ "$interface" == "$INTERFACE_SENSOR" ]; then
            echo "<option value=\"$interface\" selected>$interface</option>"
        else
            echo "<option value=\"$interface\">$interface</option>"
        fi
    done
    echo "</select>"
    echo "<input type=\"submit\" value=\"Canviar\">"
    echo "</form>"
    echo "<br>"

    echo " Interfaces d'on es fan les captures:"
    INTERFACES_LAN=$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror mostrar interfaces_lan)

    echo "<form action='/cgi-bin/portmirror.cgi' method='get'>"
    echo "<input type='hidden' name='comand' value='configurar'>"
    echo "<input type='hidden' name='argument' value='modificar_interfaces_lan'>"
    echo "<input type='hidden' name='retorn' value='portmirror-configurar.cgi'>"
    echo "<table>"
    echo "<tr><th>Interface lan</th><th>capturar</th></tr>"
    LLISTA_INTEFACES=$(ip -o link show | awk -F': ' '{print $2}')
    mapfile -t LLISTA_INTEFACES <<< "$LLISTA_INTEFACES"

    for ((i = 0; i < ${#LLISTA_INTEFACES[@]}; i++)); do
        interface="${LLISTA_INTEFACES[$i]}"
        [ -z "$interface" ] && continue
        [ "$interface" == "$INTERFACE_SENSOR" ] && continue
        echo "<tr><td>$interface</td>"
        if [[ $(echo "$INTERFACES_LAN" | grep "$interface")   ]]; then
            echo "<td><input type="checkbox" name="$interface" value="$interface" checked></td></tr>"
        else
            echo "<td><input type="checkbox" name="$interface" value="$interface"></td></tr>"
        fi
    done
    echo "</table>"
    echo "<input type='submit' value='Guardar'>"
    echo "</form>"
fi

echo "</body>"
echo "</html>"
