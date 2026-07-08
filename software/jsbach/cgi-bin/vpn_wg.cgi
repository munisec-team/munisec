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
        RESULTAT=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg mostrar mode)
        if [ $RESULTAT == "PRINCIPAL" ]; then
            echo "<h2>VPN $comand PRINCIPAL</h2>"
            echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg $comand) </pre><br>"
            echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg estat) </pre><br>"
        else
            echo "<h2>VPN $comand SECUNDARI</h2>"
            echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg_client $comand) </pre><br>"
            echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg_client estat) </pre><br>"
        fi
        ;;
    "mostrar")
        accio=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')
        
        case $accio in
            "mode")            
                RESULTAT=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg mostrar mode)
                echo "<h2>VPN mode $RESULTAT</h2>"
                echo ""
                echo "<form method='get' action='/cgi-bin/vpn_wg.cgi?'>"
                echo "<input type='hidden' name='comand' value='configurar'>"
                echo "<input type='hidden' name='accio' value='canviar_mode'>"
                echo "<p>Tria un mode:</p>"
                echo "<label>"
                if [ "$RESULTAT" = "PRINCIPAL" ]; then
                    echo "  <input type=\"radio\" name=\"mode\" value=\"PRINCIPAL\" checked>"
                else
                    echo "  <input type=\"radio\" name=\"mode\" value=\"PRINCIPAL\">"
                fi
                echo "  PRINCIPAL"
                echo "</label>"
                echo "<label>"
                if [ "$RESULTAT" = "SECUNDARI" ]; then
                    echo "  <input type=\"radio\" name=\"mode\" value=\"SECUNDARI\" checked>"
                else
                    echo "  <input type=\"radio\" name=\"mode\" value=\"SECUNDARI\">"
                fi
                echo "  SECUNDARI"
                echo "</label>"
                echo "<input type='submit' value='Canviar mode'>"
                echo "</form>"
                ;;
            *)
                echo "<h2>VPN $comand $accio</h2>"
                argument=$(echo "$QUERY_STRING" | sed -n 's/^.*argument=\([^&]*\).*$/\1/p')
                RESULTAT=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg mostrar $accio $argument)
                echo "<pre>$RESULTAT</pre><br>"
                echo "<form method='post' action='/cgi-bin/descarrega_resultat.cgi'>"
                echo "<textarea name='resultat' style='display:none;'>$RESULTAT</textarea>"
                echo "<textarea name='fitxer' style='display:none;'>wg-$argument.conf</textarea>"
                echo "<input type='submit' value='Descarregar wg-$argument.conf'>"
                echo "</form>"
                ;;  
        esac
        ;;
    "configurar")
        accio=$(echo "$QUERY_STRING" | sed -n 's/^.*accio=\([^&]*\).*$/\1/p')
        case $accio in
            "afegir_router")
                ip_publica=$(echo "$QUERY_STRING" | sed -n 's/^.*ip_publica=\([^&]*\).*$/\1/p')
                rutes=$(echo "$QUERY_STRING" | sed -n 's/^.*rutes=\([^&]*\).*$/\1/p')
                rutes=$(printf '%b' "${rutes//%/\\x}")
                echo "<h2>VPN $comand afegir router $ip_publica</h2>"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg configurar $accio $ip_publica \\ $rutes) </pre><br>"
                echo "Router $ip_publica afegit correctament"
                ;;
            "eliminar_router")
                ip_publica=$(echo "$QUERY_STRING" | sed -n 's/^.*ip_publica=\([^&]*\).*$/\1/p')
                echo "<h2>VPN $comand afegir router $ip_publica</h2>"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg configurar $accio $ip_publica) </pre><br>"
                echo "Router $ip_publica eliminat correctament"
                ;;
            "afegir_usuari")
                argument=$(echo "$QUERY_STRING" | sed -n 's/^.*argument=\([^&]*\).*$/\1/p')
                echo "<h2>VPN $comand afegir usuari $argument</h2>"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg configurar $accio $argument) </pre><br>"
                echo "Usuari $argument afegit correctament"
                ;;
            "eliminar_usuari")
                argument=$(echo "$QUERY_STRING" | sed -n 's/^.*argument=\([^&]*\).*$/\1/p')
                echo "<h2>VPN $comand afegir usuari $argument</h2>"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg configurar $accio $argument) </pre><br>"
                echo "Usuari $argument eliminat correctament"
                ;;
            "modificar_lans_router")
                echo "<h2>VPN $comand modificar lans router</h2>"
                noves_lans_router=""
                LLISTA_LANS="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg mostrar llista_lans)"
                mapfile -t LLISTA_LANS <<< "$LLISTA_LANS"

                for ((i = 0; i < ${#LLISTA_LANS[@]}; i++)); do
                    linia="${LLISTA_LANS[$i]}"
                    lan_nom=$(echo "$linia" | cut -d ";" -f 1)
                    lan_ip=$(echo "$linia" | cut -d ";" -f 3)
                    if [ $(echo "$QUERY_STRING" | sed -n 's/^.*'$lan_nom'=\([^&]*\).*$/\1/p') ]
                    then
                        noves_lans_router+="$lan_ip,"
                    fi
                done
                echo "noves lans router: $noves_lans_router<br>"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg configurar $accio $noves_lans_router) </pre><br>"
                echo "Lans router modificats correctament<br>"
                ;;
            "modificar_lans_usuari")
                echo "<h2>VPN $comand modificar lans usuari</h2>"
                noves_lans_usuari=""
                LLISTA_LANS="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg mostrar llista_lans)"
                mapfile -t LLISTA_LANS <<< "$LLISTA_LANS"

                for ((i = 0; i < ${#LLISTA_LANS[@]}; i++)); do
                    linia="${LLISTA_LANS[$i]}"
                    lan_nom=$(echo "$linia" | cut -d ";" -f 1)
                    lan_ip=$(echo "$linia" | cut -d ";" -f 3)                    
                    if [ $(echo "$QUERY_STRING" | sed -n 's/^.*'$lan_nom'=\([^&]*\).*$/\1/p') ]
                    then
                        noves_lans_usuari+="$lan_ip,"
                    fi
                done
                echo "noves lans usuari: $noves_lans_usuari<br>"
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg configurar $accio $noves_lans_usuari) </pre><br>"
                echo "Lans usuari modificats correctament<br>"
                ;;
            "canviar_mode")
                echo "<h2>VPN $comand canviar mode</h2>"
                mode=$(echo "$QUERY_STRING" | sed -n 's/^.*mode=\([^&]*\).*$/\1/p')
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg configurar $accio $mode) </pre><br>"
                echo "Mode canviat correctament a $mode<br>"
                ;;
            "guardar_conf_secundari")
                echo "<h2>VPN $comand guardar configuracio secundari</h2>"
                fitxer=$(echo "$QUERY_STRING" | sed -n 's/^.*fitxer=\([^&]*\).*$/\1/p')
                echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg_client configurar guardar $fitxer) </pre><br>"
                echo "Configuracio secundari guardada correctament<br>"
                ;;
        esac
        ;;
    "estat")
        echo "<h2>VPN Estat</h2>"
        RESULTAT=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg estat router)
        echo "<pre>$RESULTAT</pre>"
        if [[ $RESULTAT =~ ^$ACTIVAT ]]; then
            echo ""
            echo "<h4><a href=\"/cgi-bin/vpn_wg.cgi?comand=mostrar&argument=config_int_router\" target=\"body\">veure configuracio wg-routers</a></h4>"
        fi

        echo "<h3>  </h3>"

        RESULTAT=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg estat users)
        echo "<pre>$RESULTAT</pre>"
        if [[ $RESULTAT =~ ^$ACTIVAT ]]; then
            echo ""
            echo "<h4><a href=\"/cgi-bin/vpn_wg.cgi?comand=mostrar&argument=config_int_usuari\" target=\"body\">veure configuracio wg-users</a></h4>"
        fi
        ;;   
esac

/bin/cat << EOM
</body>
</html>
EOM
