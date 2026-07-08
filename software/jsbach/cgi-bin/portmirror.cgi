#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>Hola món CGI</title>
EOM
cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN
/bin/cat << EOM
</head>
<body>
EOM

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

case $comand in
    iniciar)
        echo "<h2>Port Mirror iniciar</h2>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portmirror iniciar) </pre><br>"
        ;;
    aturar)
        echo "<h2>Port Mirror aturar</h2>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portmirror aturar) </pre><br>"
        ;;
    configurar)        
        argument=$(echo "$QUERY_STRING" | sed -n 's/^.*argument=\([^&]*\).*$/\1/p')
        case $argument in
            canviar_interface_sensor)
                interface_sensor=$(echo "$QUERY_STRING" | sed -n 's/^.*interface_sensor=\([^&]*\).*$/\1/p')
                echo "<h2>Port Mirror configurar canviar_interface_sensor $interface_sensor</h2>"
                echo "<pre>$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror configurar canviar_interface_sensor $interface_sensor) </pre><br>"
                ;;
            modificar_interfaces_lan)
                echo "<h2>Port Mirror configurar modificar_interfaces_lan</h2>"
                LLISTA_INTEFACES=$(ip link show | grep "^[0-9]:" | cut -d ":" -f 2 | cut -d "@" -f 1)
                INTERFACES_LAN=""
                for interface in $LLISTA_INTEFACES
                do
                    if echo "$QUERY_STRING" | grep -q "$interface"; then
                        INTERFACES_LAN+="$interface,"
                    fi
                done
                echo "<pre>$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror configurar modificar_interfaces_lan $INTERFACES_LAN) </pre><br>"
                ;;
        esac
        ;;
    mostrar)
        argument=$(echo "$QUERY_STRING" | sed -n 's/^.*argument=\([^&]*\).*$/\1/p')
        case $argument in       
            interface_sensor)
                echo "<h2>Port Mirror mostrar interface_sensor</h2>"
                echo "<pre>$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror mostrar interface_sensor) </pre><br>"
                ;;
            interfaces_lan)
                echo "<h2>Port Mirror mostrar interfaces_lan</h2>"
                echo "<pre>$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror mostrar interfaces_lan) </pre><br>"
                ;;
            tot)
                echo "<h2>Port Mirror mostrar</h2>"
                echo "<pre>$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror mostrar tot) </pre><br>"
                ;;
        esac
        ;;
    estat | *)
        echo "<h2>Port Mirror estat</h2>"
        echo "<pre>$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli portmirror estat) </pre><br>"
        echo "<br>"
        ;;

esac
retorn=$(echo "$QUERY_STRING" | sed -n 's/^.*retorn=\([^&]*\).*$/\1/p')
if [ "$retorn" != "" ]; then
    echo "<br><br><a href='/cgi-bin/$retorn'><button>Tornar</button></a>"
fi 
/bin/cat << EOM
</body>
</html>
EOM
