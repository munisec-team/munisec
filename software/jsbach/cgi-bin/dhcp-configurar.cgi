#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html><head><title>Gestió de VLANs</title>"
echo "<meta charset='utf-8'>"

cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

echo "</head><body>"

VLAN_DATA="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp mostrar conf)"

# Llegim totes les línies en un array
mapfile -t VLANS <<< "$VLAN_DATA"

# -------------------------------------------------------------------
# DHCP CONFIGURACIO VLANS
# -------------------------------------------------------------------
echo "<h2>DHCP CONFIGURACIO VLANS</h2>"
echo "<table>"
echo "<tr><th>vid</th><th>inici</th><th>final</th><th>gateway</th><th>dns1</th><th>activat</th><th>Accions</th></tr>"

for ((i = 0; i < ${#VLANS[@]}; i++)); do
    line="${VLANS[$i]}"
    [ -z "$line" ] && continue
    IFS=';' read -r vid inici final gateway dns1 activat <<< "$line"
    echo "<tr><td>$vid</td><td>$inici</td><td>$final</td><td>$gateway</td><td>$dns1</td><td>$activat</td>"
    echo "<td>"
    echo "<button onclick=\"location.href='/cgi-bin/dhcp-modificar.cgi?vid=$vid'\">Modificar</button>"
    echo "</td></tr>"
done

echo "</table>"

# -------------------------------------------------------------------
# DHCP CONFIGURACIO WIFI
# -------------------------------------------------------------------

WIFI_DATA="$($DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli dhcp mostrar wifi_conf)"

if [[ "$WIFI_DATA" != ERROR* ]]; then
    interface=$(echo "$WIFI_DATA" | cut -d';' -f1)
    ip=$(echo "$WIFI_DATA" | cut -d';' -f2)
    inici=$(echo "$WIFI_DATA" | cut -d';' -f3)
    final=$(echo "$WIFI_DATA" | cut -d';' -f4)
    gateway=$(echo "$WIFI_DATA" | cut -d';' -f5)
    dns1=$(echo "$WIFI_DATA" | cut -d';' -f6)
    activat=$(echo "$WIFI_DATA" | cut -d';' -f7)

    echo "<h2>DHCP CONFIGURACIO WIFI</h2>"
    echo "<table>"
    echo "<tr><th>interface</th><th>ip</th><th>inici</th><th>final</th><th>gateway</th><th>dns1</th><th>activat</th><th>Accions</th></tr>"

    echo "<tr><td>$interface</td><td>$ip</td><td>$inici</td><td>$final</td><td>$gateway</td><td>$dns1</td><td>$activat</td>"
    echo "<td>"
    echo "<button onclick=\"location.href='/cgi-bin/dhcp-modificar-wifi.cgi'\">Modificar</button>"
    echo "</td></tr>"
    echo "</table>"
fi

echo "</body></html>"
