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

case "$comand" in
    "iniciar")
        echo "<h2>DHCP Iniciar</h2>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp iniciar) </pre> <br>"
        ;;
    "aturar")
        echo "<h2>DHCP Aturar</h2>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp aturar) </pre> <br>"
        ;;
    "configurar")
        accio=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')
        case "$accio" in
            "guardar_conf")

                vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p')
                inici=$(echo "$QUERY_STRING" | sed -n 's/^.*inici=\([^&]*\).*$/\1/p')
                final=$(echo "$QUERY_STRING" | sed -n 's/^.*final=\([^&]*\).*$/\1/p')
                gateway=$(echo "$QUERY_STRING" | sed -n 's/^.*gateway=\([^&]*\).*$/\1/p')
                dns1=$(echo "$QUERY_STRING" | sed -n 's/^.*dns1=\([^&]*\).*$/\1/p')
                activat=$(echo "$QUERY_STRING" | sed -n 's/^.*activat=\([^&]*\).*$/\1/p')
                echo "<h2>DHCP Guardar configuracio vlan $vid</h2>"
                echo "$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp configurar guardar_conf $vid $inici $final $gateway $dns1 $activat) <br>"
                ;;
            "guardar_wifi_conf")
                echo "<h2>DHCP Guardar configuracio wifi</h2>"
                ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
                ip=$(printf '%b' "${ip//%/\\x}")
                inici=$(echo "$QUERY_STRING" | sed -n 's/^.*inici=\([^&]*\).*$/\1/p')
                final=$(echo "$QUERY_STRING" | sed -n 's/^.*final=\([^&]*\).*$/\1/p')
                gateway=$(echo "$QUERY_STRING" | sed -n 's/^.*gateway=\([^&]*\).*$/\1/p')
                dns1=$(echo "$QUERY_STRING" | sed -n 's/^.*dns1=\([^&]*\).*$/\1/p')
                activat=$(echo "$QUERY_STRING" | sed -n 's/^.*activat=\([^&]*\).*$/\1/p')
                echo "$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp configurar guardar_wifi_conf $ip $inici $final $gateway $dns1 $activat) <br>"
                ;;
            *)
                echo "falta [guardar_conf, guardar_wifi_conf]"
                ;;
        esac
        ;;
    "estat")
        echo "<h2>DHCP Estat</h2>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp estat) </pre>"
        ;;
    *)
        echo "falta [iniciar, aturar, configurar, estat]"
        ;;
esac

/bin/cat << EOM
</body>
</html>
EOM
