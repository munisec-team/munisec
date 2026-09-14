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

case "$comand" in
    "iniciar")
        echo "<h2>WIFI $comand</h2>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi iniciar) </pre>"
        ;;
    "aturar")
        echo "<h2>WIFI $comand</h2>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi aturar) </pre>"
        ;;
    "guardar")
        echo "<h2>WIFI $comand configuracio</h2>"
        interface=$(echo "$QUERY_STRING" | sed -n 's/^.*interface=\([^&]*\).*$/\1/p')
        ip=$(echo "$QUERY_STRING" | sed -n 's/^.*ip=\([^&]*\).*$/\1/p')
        ip=$(printf '%b' "${ip//%/\\x}")
        driver=$(echo "$QUERY_STRING" | sed -n 's/^.*driver=\([^&]*\).*$/\1/p')
        ssid=$(echo "$QUERY_STRING" | sed -n 's/^.*wifi_ssid=\([^&]*\).*$/\1/p')
        hw_mode=$(echo "$QUERY_STRING" | sed -n 's/^.*hw_mode=\([^&]*\).*$/\1/p')
        channel=$(echo "$QUERY_STRING" | sed -n 's/^.*channel=\([^&]*\).*$/\1/p')
        auth_algs=$(echo "$QUERY_STRING" | sed -n 's/^.*auth_algs=\([^&]*\).*$/\1/p')
        ignore_broadcast_ssid=$(echo "$QUERY_STRING" | sed -n 's/^.*ignore_broadcast_ssid=\([^&]*\).*$/\1/p')
        ap_isolate=$(echo "$QUERY_STRING" | sed -n 's/^.*ap_isolate=\([^&]*\).*$/\1/p')
        wpa=$(echo "$QUERY_STRING" | sed -n 's/^.*wpa=\([^&]*\).*$/\1/p')
        wpa_passphrase=$(echo "$QUERY_STRING" | sed -n 's/^.*wpa_passphrase=\([^&]*\).*$/\1/p')
        wpa_key_mgmt=$(echo "$QUERY_STRING" | sed -n 's/^.*wpa_key_mgmt=\([^&]*\).*$/\1/p')
        rsn_pairwise=$(echo "$QUERY_STRING" | sed -n 's/^.*rsn_pairwise=\([^&]*\).*$/\1/p')
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi configurar guardar_wifi_ip $ip) </pre>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi configurar guardar_wifi_hostapd_conf $interface $driver $ssid $hw_mode $channel $auth_algs $ignore_broadcast_ssid $ap_isolate $wpa $wpa_passphrase $wpa_key_mgmt $rsn_pairwise) </pre>"
        ;;
    "estat")
        echo "<h2>WIFI $comand</h2>"
        echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi estat) </pre>"
        ;;
esac

/bin/cat << EOM
</body>
</html>
EOM
