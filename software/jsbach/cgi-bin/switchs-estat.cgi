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

echo "<h2> </h2>"
echo "<br>"
echo "<h2> LLISTA SWITCHS</h2>"

/bin/cat << EOM

<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
  <thead>
    <tr>
      <th>nom</th>
      <th>ip</th>
      <th>estat</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
EOM

while IFS=' ' read -r nom ip estat; do
    echo "<tr>"
    echo "<td>$nom</td>"
    if [[ "$estat" == "FUNCIONA" ]]; then
        echo "<td><a href='http://$ip'>$ip</a></td>"
    else
        echo "<td>$ip</td>"
    fi
    echo "<td>$estat</td>"
    echo "<td>"
    echo "<a href='switchs.cgi?comand=configurar&accio=eliminar_switch&nom=$nom&ip=$ip'><button type='button'>Eliminar</button></a>"
    echo "</td>"
    echo "</tr>"
done < <("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli switchs estat)

echo "</tbody>"
echo "</table>"
echo "<button onclick=\"location.href='/cgi-bin/switchs-nou.cgi'\">Afegir nou switch</button>"
echo "</body></html>"
