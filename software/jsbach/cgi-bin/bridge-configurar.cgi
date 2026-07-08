#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html><head><title>Gestió de VLANs</title>"
echo "<meta charset='utf-8'>"

cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

echo "</head><body>"



ESTAT=$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli bridge estat)

if echo "$ESTAT" | grep -q "^ACTIVAT"; then
    echo "<h2>Per configurar el bridge, primer ha d'estar desactivat</h2>"

     # -------------------------------------------------------------------
    # Aquí posem la comanda o fitxer que genera les VLANs
    # -------------------------------------------------------------------
    VLAN_DATA="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge mostrar vlan)"

    # Llegim totes les línies en un array
    mapfile -t VLANS <<< "$VLAN_DATA"

    # Comprovem que tinguem almenys dues línies
    if [ "${#VLANS[@]}" -lt 2 ]; then
        echo "<p><b>Error:</b> no hi ha prou VLANs definides.</p>"
        echo "</body></html>"
        exit 0
    fi

    # -------------------------------------------------------------------
    # VLAN ADMINISTRACIÓ (primera línia)
    # -------------------------------------------------------------------
    echo "<h2>VLAN ADMINISTRACIÓ</h2>"
    echo "<table>"
    echo "<tr><th>Nom</th><th>VID</th><th>Subxarxa</th><th>Gateway</th></tr>"
    IFS=';' read -r nom vid subnet gw _ <<< "${VLANS[0]}"
    echo "<tr><td>$nom</td><td>$vid</td><td>$subnet</td><td>$gw</td></tr>"
    echo "</table>"

    # -------------------------------------------------------------------
    # VLAN DMZ (segona línia)
    # -------------------------------------------------------------------
    echo "<h2>VLAN DMZ</h2>"
    echo "<table>"
    echo "<tr><th>Nom</th><th>VID</th><th>Subxarxa</th><th>Gateway</th></tr>"
    IFS=';' read -r nom vid subnet gw _ <<< "${VLANS[1]}"
    echo "<tr><td>$nom</td><td>$vid</td><td>$subnet</td><td>$gw</td></tr>"
    echo "</table>"

    # -------------------------------------------------------------------
    # Altres VLANS (de la tercera en avant)
    # -------------------------------------------------------------------
    echo "<h2>VLANS</h2>"
    echo "<table>"
    echo "<tr><th>Nom</th><th>VID</th><th>Subxarxa</th><th>Gateway</th></tr>"

    for ((i = 2; i < ${#VLANS[@]}; i++)); do
        line="${VLANS[$i]}"
        [ -z "$line" ] && continue
        IFS=';' read -r nom vid subnet gw _ <<< "$line"
        echo "<tr><td>$nom</td><td>$vid</td><td>$subnet</td><td>$gw</td></tr>"
    done

    echo "</table>"

  
else

    # -------------------------------------------------------------------
    # Aquí posem la comanda o fitxer que genera les VLANs
    # -------------------------------------------------------------------
    VLAN_DATA="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge mostrar vlan)"

    # Llegim totes les línies en un array
    mapfile -t VLANS <<< "$VLAN_DATA"

    # Comprovem que tinguem almenys dues línies
    if [ "${#VLANS[@]}" -lt 2 ]; then
        echo "<p><b>Error:</b> no hi ha prou VLANs definides.</p>"
        echo "</body></html>"
        exit 0
    fi

    # -------------------------------------------------------------------
    # VLAN ADMINISTRACIÓ (primera línia)
    # -------------------------------------------------------------------
    echo "<h2>VLAN ADMINISTRACIÓ</h2>"
    echo "<table>"
    echo "<tr><th>Nom</th><th>VID</th><th>Subxarxa</th><th>Gateway</th><th>Accions</th></tr>"
    IFS=';' read -r nom vid subnet gw _ <<< "${VLANS[0]}"
    echo "<tr><td>$nom</td><td>$vid</td><td>$subnet</td><td>$gw</td>"
    echo "<td><button onclick=\"location.href='/cgi-bin/bridge-modificar.cgi?vid=$vid&retorn=bridge-configurar.cgi'\">Modificar</button></td></tr>"
    echo "</table>"

    # -------------------------------------------------------------------
    # VLAN DMZ (segona línia)
    # -------------------------------------------------------------------
    echo "<h2>VLAN DMZ</h2>"
    echo "<table>"
    echo "<tr><th>Nom</th><th>VID</th><th>Subxarxa</th><th>Gateway</th><th>Accions</th></tr>"
    IFS=';' read -r nom vid subnet gw _ <<< "${VLANS[1]}"
    echo "<tr><td>$nom</td><td>$vid</td><td>$subnet</td><td>$gw</td>"
    echo "<td><button onclick=\"location.href='/cgi-bin/bridge-modificar.cgi?vid=$vid&retorn=bridge-configurar.cgi'\">Modificar</button></td></tr>"
    echo "</table>"

    # -------------------------------------------------------------------
    # Altres VLANS (de la tercera en avant)
    # -------------------------------------------------------------------
    echo "<h2>VLANS</h2>"
    echo "<table>"
    echo "<tr><th>Nom</th><th>VID</th><th>Subxarxa</th><th>Gateway</th><th>Accions</th></tr>"

    for ((i = 2; i < ${#VLANS[@]}; i++)); do
        line="${VLANS[$i]}"
        [ -z "$line" ] && continue
        IFS=';' read -r nom vid subnet gw _ <<< "$line"
        echo "<tr><td>$nom</td><td>$vid</td><td>$subnet</td><td>$gw</td>"
        echo "<td>"
        echo "<button onclick=\"location.href='/cgi-bin/bridge-modificar.cgi?vid=$vid&retorn=bridge-configurar.cgi'\">Modificar</button>"
        echo "<button onclick=\"location.href='/cgi-bin/bridge-esborrar.cgi?vid=$vid&retorn=bridge-configurar.cgi'\">Esborrar</button>"
        echo "</td></tr>"
    done

    echo "</table>"

    # -------------------------------------------------------------------
    # Botó final
    # -------------------------------------------------------------------
    echo "<button onclick=\"location.href='/cgi-bin/bridge-nova-vlan.cgi'\">Crear nova VLAN</button>"

fi

echo "</body></html>"
