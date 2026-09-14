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

echo "<h2>Tallafocs  $comand</h2>"

case "$comand" in
    "iniciar" | "aturar")
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs $comand) </pre><br>"
        ;;
    "estat")
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs $comand) </pre><br>"
        ;;
    "configurar")
        accio=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')
        case "$accio" in
            "aillar" | "connectar" | "desconnectar" | "connectar_port_wls" | "connectar_regles_propies" | "connectar_regles_propies_input" | "connectar_input" | "desconnectar_input")
                id=$(echo "$QUERY_STRING" | sed -n 's/^.*id=\([^&]*\).*$/\1/p')
                echo "$accio vlan $id"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar $accio $id) </pre><br>"
                ;;
            "eliminar_port_wls")
                protocol=$(echo "$QUERY_STRING" | sed -n 's/^.*protocol=\([^&]*\).*$/\1/p')
                port=$(echo "$QUERY_STRING" | sed -n 's/^.*port=\([^&]*\).*$/\1/p')
                echo "Eliminar protocol $protocol  port $port"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar $accio $protocol $port)  </pre><br>"
                ;;
            "eliminar_ip_wls")
                vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p')
                ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
                mac=$(echo "$QUERY_STRING" | sed -n 's/^.*mac=\([^&]*\).*$/\1/p')
                mac=$(printf '%b' "${mac//%/\\x}")
                echo "Eliminar ip $ip mac $mac de la vlan $vid"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar $accio $vid $ip $mac)  </pre><br>"
                ;;
            "afegir_port_wls")
                protocol=$(echo "$QUERY_STRING" | sed -n 's/^.*protocol=\([^&]*\).*$/\1/p')
                port=$(echo "$QUERY_STRING" | sed -n 's/^.*port=\([^&]*\).*$/\1/p')
                echo "Afegir protocol $protocol  port $port"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar $accio $protocol $port)  </pre><br>"
                ;;
            "afegir_ip_wls")
                vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p')
                ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
                mac=$(echo "$QUERY_STRING" | sed -n 's/^.*mac=\([^&]*\).*$/\1/p')
                mac=$(printf '%b' "${mac//%/\\x}")
                echo "Afegir ip $ip mac $mac de la vlan $vid"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar $accio $vid $ip $mac)  </pre><br>"
                ;;
            "afegir_dominis_wls")
                domini=$(echo "$QUERY_STRING" | sed -n 's/^.*domini=\([^&]*\).*$/\1/p')
                echo "Afegir domini $domini"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar $accio $domini)  </pre><br>"
                ;;
            "eliminar_dominis_wls")
                domini=$(echo "$QUERY_STRING" | sed -n 's/^.*domini=\([^&]*\).*$/\1/p')
                echo "Eliminar domini $domini"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar $accio $domini)  </pre><br>"
                ;;
            "afegir_dominis_bls")
                domini=$(echo "$QUERY_STRING" | sed -n 's/^.*domini=\([^&]*\).*$/\1/p')
                echo "Afegir domini $domini"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar $accio $domini)  </pre><br>"
                ;;
            "eliminar_dominis_bls")
                domini=$(echo "$QUERY_STRING" | sed -n 's/^.*domini=\([^&]*\).*$/\1/p')
                echo "Eliminar domini $domini"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar $accio $domini)  </pre><br>"
                ;;
            "afegir_port_bls")
                protocol=$(echo "$QUERY_STRING" | sed -n 's/^.*protocol=\([^&]*\).*$/\1/p')
                port=$(echo "$QUERY_STRING" | sed -n 's/^.*port=\([^&]*\).*$/\1/p')
                echo "Afegir protocol $protocol  port $port"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar $accio $protocol $port)  </pre><br>"
                ;;
            "eliminar_port_bls")
                protocol=$(echo "$QUERY_STRING" | sed -n 's/^.*protocol=\([^&]*\).*$/\1/p')
                port=$(echo "$QUERY_STRING" | sed -n 's/^.*port=\([^&]*\).*$/\1/p')
                echo "Eliminar protocol $protocol  port $port"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar $accio $protocol $port)  </pre><br>"
                ;;
            "afegir_port_wls")
                protocol=$(echo "$QUERY_STRING" | sed -n 's/^.*protocol=\([^&]*\).*$/\1/p')
                port=$(echo "$QUERY_STRING" | sed -n 's/^.*port=\([^&]*\).*$/\1/p')
                echo "Afegir protocol $protocol  port $port"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar $accio $protocol $port)  </pre><br>"
                ;;
            "eliminar_port_wls")
                protocol=$(echo "$QUERY_STRING" | sed -n 's/^.*protocol=\([^&]*\).*$/\1/p')
                port=$(echo "$QUERY_STRING" | sed -n 's/^.*port=\([^&]*\).*$/\1/p')
                echo "Eliminar protocol $protocol  port $port"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar $accio $protocol $port)  </pre><br>"
                ;;
            "eliminar_regla")
                vnom=$(echo "$QUERY_STRING" | sed -n 's/^.*vnom=\([^&]*\).*$/\1/p')
                posicio=$(echo "$QUERY_STRING" | sed -n 's/^.*posicio=\([^&]*\).*$/\1/p')
                resultat=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar eliminar_regla $vnom $posicio)
                echo "<pre>$resultat</pre><br>"
                echo "Eliminant regla $posicio de la vlan $vnom"
                ;;
            "eliminar_regla_input")
                vnom=$(echo "$QUERY_STRING" | sed -n 's/^.*vnom=\([^&]*\).*$/\1/p')
                posicio=$(echo "$QUERY_STRING" | sed -n 's/^.*posicio=\([^&]*\).*$/\1/p')
                resultat=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar eliminar_regla_input $vnom $posicio)
                echo "<pre>$resultat</pre><br>"
                echo "Eliminant regla $posicio de la vlan $vnom"
                ;;
            "eliminar_regla_wan")
                posicio=$(echo "$QUERY_STRING" | sed -n 's/^.*posicio=\([^&]*\).*$/\1/p')
                resultat=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar eliminar_regla_wan $posicio)
                echo "<pre>$resultat</pre><br>"
                echo "Eliminant regla $posicio de la vlan WAN"
                ;;
            "eliminar_regla_dns_dhcp_pc")
                posicio=$(echo "$QUERY_STRING" | sed -n 's/^.*posicio=\([^&]*\).*$/\1/p')
                resultat=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs configurar eliminar_regla_dns_dhcp_pc $posicio)
                echo "<pre>$resultat</pre><br>"
                echo "Eliminant regla $posicio de la vlan dns_dhcp_pc"
                ;; 
        esac
        retorn=$(echo "$QUERY_STRING" | sed -n 's/^.*retorn=\([^&]*\).*$/\1/p')
        id=$(echo "$QUERY_STRING" | sed -n 's/^.*id=\([^&]*\).*$/\1/p')
        vnom=$(echo "$QUERY_STRING" | sed -n 's/^.*vnom=\([^&]*\).*$/\1/p')
        if [ "$retorn" != "" ]; then
            echo "<a href='/cgi-bin/$retorn?id=$id&vnom=$vnom'><button>Tornar</button></a>"
        fi 
        ;;
esac

/bin/cat << EOM
</body>
</html>
EOM
