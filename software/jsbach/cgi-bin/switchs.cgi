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
    "iniciar")
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli switchs iniciar) </pre><br>"
    ;;
    "aturar")
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli switchs aturar) </pre><br>"
    ;;
    "configurar")
        accio=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')
        case $accio in
            "eliminar_switch" | "afegir_switch")  
                nom=$(echo "$QUERY_STRING" | sed -n 's/^.*nom=\([^&]*\).*$/\1/p')
                ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
                user=$(echo "$QUERY_STRING" | sed -n 's/^.*user=\([^&]*\).*$/\1/p')
                pass=$(echo "$QUERY_STRING" | sed -n 's/^.*pass=\([^&]*\).*$/\1/p')
                protocol=$(echo "$QUERY_STRING" | sed -n 's/^.*protocol=\([^&]*\).*$/\1/p')

                echo "$accio el switch $nom $ip"

                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli switchs configurar $accio $nom $ip $user $pass $protocol) <br>"
            ;;
            "desactivar_acl_admin" | "desactivar_acl_macs" | "activar_acl_admin" | "activar_acl_macs")
                ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli switchs configurar $comand $ip) </pre><br>"
            ;;
            "blocar_mac")
                mac=$(echo "$QUERY_STRING" | sed -n 's/^.*mac=\([^&]*\).*$/\1/p' | sed 's/%3[aA]/:/g')
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli switchs configurar blocar_mac $mac) </pre><br>"
            ;;
            "desblocar_mac")
                mac=$(echo "$QUERY_STRING" | sed -n 's/^.*mac=\([^&]*\).*$/\1/p' | sed 's/%3[aA]/:/g')
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli switchs configurar desblocar_mac $mac) </pre><br>"
            ;;    
            "eliminar_mac_vlan_admin")
                echo "eliminar mac vlan admin"
                mac=$(echo "$QUERY_STRING" | sed -n 's/^.*mac=\([^&]*\).*$/\1/p' | sed 's/%3[aA]/:/g')
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli switchs configurar eliminar_mac_vlan_admin $mac)</pre><br>"
            ;;
            "afegir_mac_vlan_admin")
                echo "afegir mac vlan admin"
                mac=$(echo "$QUERY_STRING" | sed -n 's/^.*mac=\([^&]*\).*$/\1/p' | sed 's/%3[aA]/:/g')
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli switchs configurar afegir_mac_vlan_admin $mac)</pre><br>"
            ;;
        esac    
esac

/bin/cat << EOM
</body>
</html>
EOM
