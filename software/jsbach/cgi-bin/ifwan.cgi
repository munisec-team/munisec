#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
PAGINA="IFWAN"

echo "Content-type: text/html; charset=utf-8"
echo ""

/bin/cat << EOM
<html>
<head>
  <meta charset="utf-8">
  <title>Hola món </title>
EOM
cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN
/bin/cat << EOM
</head>
<body>
EOM

comand=$(echo "$QUERY_STRING" | sed -n 's/^.*comand=\([^&]*\).*$/\1/p')

case $comand in
    "iniciar" | "aturar")
        echo "<h2>$PAGINA $comand</h2>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli ifwan $comand) </pre><br>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli ifwan estat) </pre><br>"
        ;;
    "configurar")
        argument=$(echo "$QUERY_STRING" | sed -n 's/^.*argument=\([^&]*\).*$/\1/p')
        echo "<h2>$PAGINA $argument</h2>"

        case $argument in
            "guardar")
                mode=$(echo "$QUERY_STRING" | sed -n 's/^.*mode=\([^&]*\).*$/\1/p')
                int=$(echo "$QUERY_STRING" | sed -n 's/^.*int=\([^&]*\).*$/\1/p')
                if [[ "$mode" == "manual" ]]; then
                    ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
                    masc=$(echo "$QUERY_STRING" | sed -n 's/^.*masc=\([^&]*\).*$/\1/p')
                    pe=$(echo "$QUERY_STRING" | sed -n 's/^.*pe=\([^&]*\).*$/\1/p')
                    dns=$(echo "$QUERY_STRING" | sed -n 's/^.*dns=\([^&]*\).*$/\1/p')
                fi

                if [[ ! -z $ip ]]; then
                    ipmas=$ip/$masc
                fi

                ordre="ifwan configurar guardar $mode $int $ipmas $pe $dns"

                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli $ordre)</pre> <br>"
                ;;
        esac
        ;;
    "estat")
        echo "<h2>$PAGINA $comand</h2>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli ifwan estat) </pre><br>"
        ;;
esac

/bin/cat << EOM
</body>
</html>
EOM
