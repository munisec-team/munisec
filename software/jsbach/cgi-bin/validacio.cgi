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

usuari=$(echo "$QUERY_STRING" | sed -n 's/.*usuari=\([^&]*\).*/\1/p')
contrasenya=$(echo "$QUERY_STRING" | sed -n 's/.*contrasenya=\([^&]*\).*/\1/p')
contrasenya=$(printf '%b' "${contrasenya//%/\\x}")
echo "<pre>$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal_captiu configurar comprovar_usuari $usuari $contrasenya $REMOTE_ADDR)</pre>"

/bin/cat << EOM
</body>
</html>
EOM
