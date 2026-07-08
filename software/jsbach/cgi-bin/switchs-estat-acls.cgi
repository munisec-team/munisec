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
echo "<h2> LLISTA ACLS EN WITCHS</h2>"

/bin/cat << EOM

<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
  <thead>
    <tr>
      <th>nom</th>
      <th>ip</th>
      <th>ACL Vlan Admin</th>
      <th>ACL Macs</th>
    </tr>
  </thead>
  <tbody>
EOM

while IFS=' ' read -r nom ip acl1 acl2; do
    echo "<tr>"
    echo "<td>$nom</td>"
    if [[ "$acl1" == "NO_RESPON" ]]; then
        echo "<td>NO_RESPON</td>"
    else
        echo "<td><a href='http://$ip'>$ip</a></td>"
    fi
    if [[ "$acl1" == "ACL_ADMIN" ]]; then
        echo "<td>Activa <a href='switchs.cgi?comand=configurar&accio=desactivar_acl_admin&ip=$ip'><button type='button'>Desactivar</button></a></td>"
    elif [[ "$acl1" == "NO_ACL_ADMIN" ]]; then
        echo "<td>Desactivada <a href='switchs.cgi?comand=configurar&accio=activar_acl_admin&ip=$ip'><button type='button'>Activar</button></a></td>"
    else
        echo "<td>""</td>"
    fi
    if [[ "$acl2" == "ACL_MACS" ]]; then
        echo "<td>Activa <a href='switchs.cgi?comand=configurar&accio=desactivar_acl_macs&ip=$ip'><button type='button'>Desactivar</button></a></td>"
    elif [[ "$acl2" == "NO_ACL_MACS" ]]; then
        echo "<td>Desactivada <a href='switchs.cgi?comand=configurar&accio=activar_acl_macs&ip=$ip'><button type='button'>Activar</button></a></td>"
    else
        echo "<td>""</td>"
    fi
    echo "</tr>"
done < <("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli switchs estat_acls)

echo "</tbody>"
echo "</table>"

echo "</body></html>"
