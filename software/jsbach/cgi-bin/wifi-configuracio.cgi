#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
source "$DIR/$DIR_PROJECTE/$DIR_CONF/$WIFI_HOSTAPD_CONF"
source "$DIR/$DIR_PROJECTE/$DIR_CONF/$WIFI_DHCP_CONF"

echo "Content-type: text/html; charset=utf-8"
echo ""

############################################
# HTML capçalera
############################################
cat << EOF
<html>
<head>
<meta charset="UTF-8">
<title>WIFI Configuracio</title>

EOF
cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN
/bin/cat << EOF
</head>
<body>
<h1>WIFI Configuracio</h1>
<form method="get" action="wifi.cgi">
<input type="hidden" name="comand" value="guardar">
<table>
<tr>
<td>Interface</td>
<td>
<select name="interface">
EOF
for interface in $("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi configurar mostrar_wifi_int); do
    if [[ "$interface" == "$interface" ]]; then
        echo "<option value='$interface' selected>$interface</option>"
    else
        echo "<option value='$interface'>$interface</option>"
    fi
done
/bin/cat << EOF
</select>
</td>
</tr>
<tr>
<td>IP</td>
<td>
<input type="text" name="ip" value="$wifi_ip">
</td>
</tr>
<tr>
<td>driver</td>
<td>
<input type="text" name="driver" value="$driver" readonly>
</td>
</tr>
<tr>
<td>ssid</td>
<td>
<input type="text" name="wifi_ssid" value="$ssid">
</td>
</tr>
<tr>
<td>hw_mode</td>
<td>
<select name="hw_mode">
EOF
for mode in "a:802.11a (5 GHz)" "b:802.11b (2.4 GHz, lent)" "g:802.11g (2.4 GHz, ràpid)"; do
    key="${mode%%:*}"  # Obtenim la primera part (abans dels dos punts)
    value="${mode#*:}" # Obtenim la segona part (després dels dos punts)
    if [[ "$key" == "$hw_mode" ]]; then
        echo "<option value='$key' selected>$value</option>"
    else
        echo "<option value='$key'>$value</option>"
    fi
done
/bin/cat << EOF
</select>
</td>
</tr>
<tr>
<td>channel</td>
<td>
<select name="channel">
EOF
for i in {1..13}; do
    if [[ "$i" == "$channel" ]]; then
        echo "<option value='$i' selected>$i</option>"
    else
        echo "<option value='$i'>$i</option>"
    fi
done
/bin/cat << EOF
</select>
</td>
</tr>
<tr>
<td>auth_algs</td>
<td>
<select name="auth_algs">
EOF
for i in {1..3}; do
    if [[ "$i" == "$auth_algs" ]]; then
        echo "<option value='$i' selected>$i</option>"
    else
        echo "<option value='$i'>$i</option>"
    fi
done
/bin/cat << EOF
</select>
</td>
</tr>
<tr>
<td>ignore_broadcast_ssid</td>
<td>
<select name="ignore_broadcast_ssid">
EOF
for i in {0..1}; do
    if [[ "$i" == "$ignore_broadcast_ssid" ]]; then
        echo "<option value='$i' selected>$i</option>"
    else
        echo "<option value='$i'>$i</option>"
    fi
done
/bin/cat << EOF
</select>
</td>
</tr>
<tr>
<td>ap_isolate</td>
<td>
<select name="ap_isolate">
EOF
for i in {0..1}; do
    if [[ "$i" == "$ap_isolate" ]]; then
        echo "<option value='$i' selected>$i</option>"
    else
        echo "<option value='$i'>$i</option>"
    fi
done
/bin/cat << EOF
</select>
</td>
</tr>
<tr>
<td>wpa</td>
<td>
<select id="wpa" name="wpa" required onchange="updateEncryptionFields()">
EOF
for crypt in "1:NO" "2:WPA-PSK" "3:WPA-EAP"; do
    key="${crypt%%:*}"  # Obtenim la primera part (abans dels dos punts)
    value="${crypt#*:}" # Obtenim la segona part (després dels dos punts)
    if [[ "$key" == "$wpa" ]]; then
        echo "<option value='$key' selected>$value</option>"
    else
        echo "<option value='$key'>$value</option>"
    fi
done
/bin/cat << EOF
</select>
</td>
</tr>
<tr>
<td>wpa_passphrase</td>
<td>
<input type="text" name="wpa_passphrase" value="$wpa_passphrase">
</td>
</tr>
<tr>
<td>wpa_key_mgmt</td>
<td>
<select name="wpa_key_mgmt">
EOF
for i in "WPA-PSK" "WPA-PSK-SHA256" "WPA-PSK-SHA256 WPA-PSK"; do
    if [[ "$i" == "$wpa_key_mgmt" ]]; then
        echo "<option value='$i' selected>$i</option>"
    else
        echo "<option value='$i'>$i</option>"
    fi
done
/bin/cat << EOF
</select>
</td>
</tr>
<tr>
<td>rsn_pairwise</td>
<td>
<select name="rsn_pairwise">
EOF
for i in "CCMP" "TKIP" "TKIP CCMP"; do
    if [[ "$i" == "$rsn_pairwise" ]]; then
        echo "<option value='$i' selected>$i</option>"
    else
        echo "<option value='$i'>$i</option>"
    fi
done
/bin/cat << EOF
</select>
</td>
</tr>
<tr>
<td colspan="2" align="center">
<input type="submit" value="GUARDAR">
</td>
</tr>
</table>
</form>

</body>
</html>
EOF
