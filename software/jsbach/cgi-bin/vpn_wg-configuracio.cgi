#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
source $DIR/$DIR_PROJECTE/$DIR_CONF/$VPN_WG_CONF

echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html><head><title>Gestió de VPN WireGuard</title>"
echo "<meta charset='utf-8'>"

cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

echo "</head><body>"

MODE="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg mostrar mode)"
if [[ $MODE == "PRINCIPAL" ]]; then  

    # -------------------------------------------------------------------
    # VPN WireGuard CONFIGURACIO ROUTERS
    # -------------------------------------------------------------------
    echo "<h2>VPN $vpn_wg_int_router $vpn_wg_ip_router/$vpn_wg_ip_routers_mascara </h2>"

    echo "<h4>Els routers connectats accediran a les xarxes:</h4>"
    echo "<form action='/cgi-bin/vpn_wg.cgi' method='get'>"
    echo "<input type='hidden' name='comand' value='configurar'>"
    echo "<input type='hidden' name='accio' value='modificar_lans_router'>"
    echo "<table>"
    echo "<tr><th>Nom lan IP lan</th><th>Accés</th></tr>"

    LLISTA_LANS="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg mostrar llista_lans)"
    mapfile -t LLISTA_LANS <<< "$LLISTA_LANS"

    for ((i = 0; i < ${#LLISTA_LANS[@]}; i++)); do
        linia="${LLISTA_LANS[$i]}"
        [ -z "$linia" ] && continue
        lan_nom=$(echo "$linia" | cut -d ";" -f 1)
        lan_ip=$(echo "$linia" | cut -d ";" -f 3)
        echo "<tr><td>$lan_nom $lan_ip</td>"
        if [[ "$vpn_wg_routers_allowed_ips" == *"$lan_ip"* ]]; then
            echo "<td><input type="checkbox" name="$lan_nom" value="$lan_ip" checked></td></tr>"
        else
            echo "<td><input type="checkbox" name="$lan_nom" value="$lan_ip"></td></tr>"
        fi
    done
    echo "</table>"
    echo "<input type='submit' value='Guardar rutes'>"
    echo "</form>"


    ROUTERS_DATA="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg mostrar llista_routers)"

    # Llegim totes les línies en un array
    mapfile -t ROUTERS <<< "$ROUTERS_DATA"

    echo "<h3>ROUTERS connectats a $vpn_wg_int_router:</h3>"
    echo "<table>"
    echo "<tr><th>IP PÚBLICA</th><th>IP PRIVADA</th><th>Rutes</th><th></th></tr>"

    for ((i = 0; i < ${#ROUTERS[@]}; i++)); do
        line="${ROUTERS[$i]}"
        [ -z "$line" ] && continue
        IFS=';' read -r ip_publica ip_privada clau_publica clau_privada rutes <<< "$line"
        echo "<tr><td>$ip_publica</td><td>$ip_privada</td><td>$rutes</td>"
        echo "<td><button onclick=\"location.href='/cgi-bin/vpn_wg.cgi?comand=configurar&accio=eliminar_router&ip_publica=$ip_publica'\">Eliminar</button>"
        echo "<button onclick=\"location.href='/cgi-bin/vpn_wg.cgi?comand=mostrar&accio=config_router&argument=$ip_publica'\">Mostrar configuració</button></td>"
        echo "</tr>"
    done

    echo "</table>"

    echo "<h4>AFEGIR ROUTER</h4>"
    echo "<form action='/cgi-bin/vpn_wg.cgi' method='get'>"
    echo "<input type='hidden' name='accio' value='afegir_router'>"
    echo "<input type='hidden' name='comand' value='configurar'>"
    echo "<table>"
    echo "<tr><th>ip publica</th><th>rutes</th><th></th></tr>"
    echo "<tr><td><input type='text' name='ip_publica' placeholder='IP Publica'></td><td><input type='text' name='rutes' placeholder='Rutes'></td><td><input type='submit' value='Afegir'></td></tr>"
    echo "</table>"
    echo "</form>"

    echo "<br><br>"
    # -------------------------------------------------------------------
    # VPN WireGuard CONFIGURACIO USUARIS
    # -------------------------------------------------------------------

    USUARIS_DATA="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg mostrar llista_usuaris)"

    # Llegim totes les línies en un array
    mapfile -t USUARIS <<< "$USUARIS_DATA"

    echo "<h2>VPN $vpn_wg_int_users $vpn_wg_ip_users/$vpn_wg_ip_users_mascara </h2>" 


    echo "<h4>Els usuaris connectats accediran a les xarxes:</h4>"
    echo "<form action='/cgi-bin/vpn_wg.cgi' method='get'>"
    echo "<input type='hidden' name='comand' value='configurar'>"
    echo "<input type='hidden' name='accio' value='modificar_lans_usuari'>"
    echo "<table>"
    echo "<tr><th>Nom lan IP lan</th><th>Accés</th></tr>"

    LLISTA_LANS="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg mostrar llista_lans)"
    mapfile -t LLISTA_LANS <<< "$LLISTA_LANS"

    for ((i = 0; i < ${#LLISTA_LANS[@]}; i++)); do
        linia="${LLISTA_LANS[$i]}"
        [ -z "$linia" ] && continue
        lan_nom=$(echo "$linia" | cut -d ";" -f 1)
        lan_ip=$(echo "$linia" | cut -d ";" -f 3)
        echo "<tr><td>$lan_nom $lan_ip</td>"
        if [[ "$vpn_wg_users_allowed_ips" == *"$lan_ip"* ]]; then
            echo "<td><input type="checkbox" name="$lan_nom" value="$lan_ip" checked></td></tr>"
        else
            echo "<td><input type="checkbox" name="$lan_nom" value="$lan_ip"></td></tr>"
        fi
    done
    echo "</table>"
    echo "<input type='submit' value='Guardar rutes'>"
    echo "</form>"

    echo "<h3>USUARIS connectats a $vpn_wg_int_users:</h3>"
    echo "<table>"
    echo "<tr><th>nom d'usuari</th><th>ip privada</th><th></th></tr>"

    for ((i = 0; i < ${#USUARIS[@]}; i++)); do
        line="${USUARIS[$i]}"
        [ -z "$line" ] && continue
        IFS=';' read -r usuari ip clau_publica clau_privada rutes <<< "$line"
        echo "<tr><td>$usuari</td><td>$ip</td>"
        echo "<td><button onclick=\"location.href='/cgi-bin/vpn_wg.cgi?accio=eliminar_usuari&comand=configurar&argument=$usuari'\">Eliminar</button>"
        echo "<button onclick=\"location.href='/cgi-bin/vpn_wg.cgi?comand=mostrar&accio=config_usuari&argument=$usuari'\">Mostrar configuració</button></td>"
        echo "</tr>"
    done

    echo "</table>"

    echo "<h4>AFEGIR USUARI</h4>"
    echo "<form action='/cgi-bin/vpn_wg.cgi' method='get'>"
    echo "<input type='hidden' name='accio' value='afegir_usuari'>"
    echo "<input type='hidden' name='comand' value='configurar'>"
    echo "<table>"
    echo "<tr><th>nom d'usuari</th><th></th></tr>"
    echo "<tr><td><input type='text' name='argument' placeholder='Usuari'></td><td><input type='submit' value='Afegir'></td></tr>"
    echo "</table>"
    echo "</form>"

else
    echo "<h2>VPN Secundari</h2>"
    echo ""
    echo "<form action='/cgi-bin/vpn_wg.cgi' method='get'>"
    echo "<input type='hidden' name='comand' value='configurar'>"
    echo "<input type='hidden' name='accio' value='guardar_conf_secundari'>"
    echo "Ruta del fitxer de configuracio:"
    echo "<input type='text' name='fitxer' placeholder='Fitxer'>"
    echo "<input type='submit' value='Aplicar'>"
    echo "</form>"
   
fi

echo "</body></html>"
