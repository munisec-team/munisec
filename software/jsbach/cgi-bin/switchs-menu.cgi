#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

/bin/cat << EOM

<html>
<head>
<meta http-equiv=Content-Type content="text/html; charset=windows-1252">
<meta content="MSHTML 6.00.2900.3660" name=GENERATOR> 

EOM
cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN
/bin/cat << EOM

</head>
<body>
<h2>Switchs</h2>

<h4><a href="/cgi-bin/switchs-estat.cgi" target="body">estat switchs</a></h4>
<h4><a href="/cgi-bin/switchs-estat-acls.cgi" target="body">estat acls</a></h4>
<h4><a href="/cgi-bin/switchs.cgi?comand=iniciar" target="body">iniciar totes les acls</a></h4>
<h4><a href="/cgi-bin/switchs.cgi?comand=aturar" target="body">aturar totes les acls</a></h4>
<h4><a href="/cgi-bin/switchs-taules-macs.cgi" target="body">mostrar taules macs</a></h4>
<h4><a href="/cgi-bin/switchs-macs-vlans.cgi" target="body">macs bloquejades en tots els ports</a></h4>
<h4><a href="/cgi-bin/switchs-macs-admin.cgi" target="body">macs admeses en vlan admin</a></h4>
</body>
</html>

EOM
