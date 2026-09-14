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
    "iniciar" | "aturar")
        echo "<h2>DMZ $comand</h2>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dmz $comand) </pre><br>"
        ;;
    "estat")
        echo "<h2>DMZ Estat</h2>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dmz estat) </pre><br>"
        ;;
    "configurar")
        argument=$(echo "$QUERY_STRING" | sed -n 's/^.*argument=\([^&]*\).*$/\1/p')
        case $argument in
            "afegir")
                PORT=$(echo "$QUERY_STRING" | sed -n 's/^.*port=\([^&]*\).*$/\1/p')
                PROTO=$(echo "$QUERY_STRING" | sed -n 's/^.*proto=\([^&]*\).*$/\1/p')
                IP_DMZ=$(echo "$QUERY_STRING" | sed -n 's/^.*ipdmz=\([^&]*\).*$/\1/p')

                echo "<h2>AFEGIR $PORT $PROTO $IP_DMZ</h2>"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dmz configurar afegir $PORT $PROTO $IP_DMZ) </pre><br>"
                ;;
            "eliminar")
                PORT=$(echo "$QUERY_STRING" | sed -n 's/^.*port=\([^&]*\).*$/\1/p')
                PROTO=$(echo "$QUERY_STRING" | sed -n 's/^.*proto=\([^&]*\).*$/\1/p')
                IP_DMZ=$(echo "$QUERY_STRING" | sed -n 's/^.*ipdmz=\([^&]*\).*$/\1/p')

                echo "<h2>ELIMINAR $PORT $PROTO $IP_DMZ</h2>"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dmz configurar eliminar $PORT $PROTO $IP_DMZ) </pre><br>"
                ;;
        esac
        ;;
esac

/bin/cat << EOM
</body>
</html>
EOM
