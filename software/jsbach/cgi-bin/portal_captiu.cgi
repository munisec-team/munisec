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

echo "<h2>Portal Captiu $comand</h2>"

case $comand in
    "iniciar" | "aturar")
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal_captiu $comand) </pre><br>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal_captiu estat) </pre><br>"
        ;;
    "configurar")
        accio=$(echo "$QUERY_STRING" | sed -n 's/.*accio=\([^&]*\).*/\1/p')
        case $accio in
            "guardar_configuracio")
                nom=$(echo "$QUERY_STRING" | sed -n 's/.*nom=\([^&]*\).*/\1/p')
                ip=$(echo "$QUERY_STRING" | sed -n 's/.*ip=\([^&]*\).*/\1/p')
                ip=$(printf '%b' "${ip//%/\\x}")
                estat=$(echo "$QUERY_STRING" | sed -n 's/.*estat=\([^&]*\).*/\1/p')
                echo "Guardant configuracio $nom $ip $estat"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal_captiu configurar guardar_configuracio $nom $ip $estat) </pre><br>"
                ;;
            "afegir_usuari")
                usuari=$(echo "$QUERY_STRING" | sed -n 's/.*usuari=\([^&]*\).*/\1/p')
                contrasenya=$(echo "$QUERY_STRING" | sed -n 's/.*contrasenya=\([^&]*\).*/\1/p')
                contrasenya=$(printf '%b' "${contrasenya//%/\\x}")
                echo "Guardant usuari $usuari"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal_captiu configurar afegir_usuari $usuari $contrasenya) </pre><br>"
                ;;
            "eliminar_usuari")
                usuari=$(echo "$QUERY_STRING" | sed -n 's/.*usuari=\([^&]*\).*/\1/p')
                contrasenya=$(echo "$QUERY_STRING" | sed -n 's/.*contrasenya=\([^&]*\).*/\1/p')
                contrasenya=$(printf '%b' "${contrasenya//%/\\x}")
                echo "Eliminant usuari $usuari"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal_captiu configurar eliminar_usuari $usuari $contrasenya) </pre><br>"
                ;;
        esac
        ;;
    "estat")
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal_captiu estat) </pre><br>"
        ;;
esac

/bin/cat << EOM
</body>
</html>
EOM
