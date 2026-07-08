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

echo "<h2>IFWAN</h2>"
echo "<pre>"
echo "$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli ifwan estat) <br>"
echo "</pre>"

echo "<h2>ENRUTAR</h2>"
echo "<pre>"
echo "$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli enrutar estat) <br>"
echo "</pre>"

echo "<h2>BRIDGE & VLANS</h2>"
echo "<pre>"
echo "$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli bridge estat)"
echo "</pre>"

echo "<h2>WIFI</h2>"
echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli wifi estat) </pre><br>"

echo "<h2>VPN</h2>"
echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli vpn_wg estat) </pre><br>"

echo "<h2>DHCP</h2>"
echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dhcp estat) </pre><br>"

echo "<h2>TALLAFOCS</h2>"
echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli tallafocs estat) </pre><br>"

echo "<h2>DMZ</h2>"
echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli dmz estat) </pre><br>"

echo "<h2>PORTAL CAPTIU</h2>"
echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal_captiu estat) </pre><br>"

/bin/cat << EOM
</body>
</html>
EOM
