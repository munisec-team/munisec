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
    "estat")
        echo "<h2>Bridge Estat </h2>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge $comand)  </pre><br>"
        ;;
    "iniciar")
        echo "<h2>Bridge Iniciar </h2>"
        echo "$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge $comand)<br>"
        ;;
    "aturar")
        echo "<h2>Bridge Aturar </h2>"
        echo "$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge $comand)<br>"
        ;;
    "configurar")
        argument=$(echo "$QUERY_STRING" | sed -n 's/^.*argument=\([^&]*\).*$/\1/p')
        case $argument in
            "aillar")
                echo "<h2>Bridge aillar </h2>"
                vlan=$(echo "$QUERY_STRING" | sed -n 's/^.*vlan=\([^&]*\).*$/\1/p')
                echo "<pre>"
                echo "$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli bridge $comand $argument $vlan)"
                echo "</pre>"
                ;;
            "desaillar")
                echo "<h2>Bridge desaillar </h2>"
                vlan=$(echo "$QUERY_STRING" | sed -n 's/^.*vlan=\([^&]*\).*$/\1/p')
                echo "<pre>"
                echo "$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli bridge $comand $argument $vlan)"
                echo "</pre>"
                ;;
            "aplicar_macs_admin")
                echo "<h2>Bridge aplicar macs admin </h2>"
                echo "<pre>"
                echo "$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli bridge $comand $argument)"
                echo "</pre>"
                ;;
            "no_aplicar_macs_admin")
                echo "<h2>Bridge no aplicar macs admin </h2>"
                echo "<pre>"
                echo "$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli bridge $comand $argument)"
                echo "</pre>"
                ;;
            "guardar")
                accio=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')
                case $accio in
                    "vlan_nova")
                        echo "<h2>Bridge Guardar vlan </h2>"
                        nom=$(echo "$QUERY_STRING" | sed -n 's/^.*nom=\([^&]*\).*$/\1/p')
                        vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p')
                        ipmasc=$(echo "$QUERY_STRING" | sed -n 's/^.*ipmasc=\([^&]*\).*$/\1/p')
                        ippe=$(echo "$QUERY_STRING" | sed -n 's/^.*ippe=\([^&]*\).*$/\1/p')
                        nom=$(printf '%b' "${nom//%/\\x}")
                        ipmasc=$(printf '%b' "${ipmasc//%/\\x}")
                        ippe=$(printf '%b' "${ippe//%/\\x}")
                        echo "<h2>Bridge Guardar vlan $nom $vid $ipmasc $ippe</h2>"
                        echo "<pre>"
                        echo "$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge $comand $argument $accio $nom $vid $ipmasc $ippe)"
                        echo "</pre>"
                        ;;
                    "bridge")
                        # Extreiem els valors del QUERY_STRING
                        int=$(echo "$QUERY_STRING" | sed -n 's/^.*int=\([^&]*\).*$/\1/p')
                        tag=$(echo "$QUERY_STRING" | sed -n 's/^.*tag=\([^&]*\).*$/\1/p')
                        untag=$(echo "$QUERY_STRING" | sed -n 's/^.*untag=\([^&]*\).*$/\1/p')

                        tag=$(printf '%b' "${tag//%/\\x}")
                        echo "<h2>Bridge Guardar bridge $int $untag $tag</h2>"
                        echo "<pre>"
                        echo "$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli bridge $comand $argument $accio $int $untag $tag)"
                        echo "</pre>"
                        ;;
                    "mac")
                        mac=$(echo "$QUERY_STRING" | sed -n 's/^.*mac=\([^&]*\).*$/\1/p' | sed 's/%3[aA]/:/g')
                        echo "<h2>Bridge Guardar mac $mac</h2>"
                        echo "<pre>"
                        echo "$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli bridge $comand $argument $accio $mac)"
                        echo "</pre>"
                        ;;
                esac
                ;;
            "esborrar")
                accio=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')
                case $accio in
                    "vlan")
                        vid=$(echo "$QUERY_STRING" | sed -n 's/^.*vid=\([^&]*\).*$/\1/p')
                        echo "<h2>Bridge Esborrar vlan $vid</h2>"
                        echo "<pre>"
                        echo "$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli bridge $comand $argument $accio $vid)"
                        echo "</pre>"
                        ;;
                    "bridge")
                        # Extreiem els valors del QUERY_STRING
                        int=$(echo "$QUERY_STRING" | sed -n 's/^.*int=\([^&]*\).*$/\1/p')
                        echo "<h2>Bridge Esborrar interfaç $int del bridge</h2>"
                        echo "<pre>"
                        echo "$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli bridge $comand $argument $accio $int)"
                        echo "</pre>"
                        ;;
                    "mac")
                        mac=$(echo "$QUERY_STRING" | sed -n 's/^.*mac=\([^&]*\).*$/\1/p' | sed 's/%3[aA]/:/g')
                        echo "<h2>Bridge Esborrar mac $mac</h2>"
                        echo "<pre>"
                        echo "$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli bridge $comand $argument $accio $mac)"
                        echo "</pre>"
                        ;;
                esac
                ;;
        esac
        retorn=$(echo "$QUERY_STRING" | sed -n 's/^.*retorn=\([^&]*\).*$/\1/p')
        if [ "$retorn" != "" ]; then
            echo "<br><br><a href='/cgi-bin/$retorn'><button>Tornar</button></a>"
        fi 
        ;;
    *)
        echo "$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge $comand)<br>"
        ;;
esac

/bin/cat << EOM
</body>
</html>
EOM
