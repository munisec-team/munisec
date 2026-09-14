#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-Type:text/html;charset=utf-8"
/bin/cat << EOM

<html>
<head>
<title>Administrant el Router</title>
<meta http-equiv=Content-Type content="text/html; charset=windows-1252">
<meta content="MSHTML 6.00.2900.3660" name=GENERATOR>
EOM
cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN
/bin/cat << EOM
</head>
<body link="#E9AB17" vlink="#E9AB17" alink="#E9AB17">


EOM

echo "<h2 align="center">Administrant el Router "$HOSTNAME" amb "$DIR_PROJECTE"</h2>"

/bin/cat << EOM

<script>
function wan(){
window.top.frames['menu'].location.href='/cgi-bin/ifwan-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/ifwan.cgi?comand=estat&';
}
function enrutar(){
window.top.frames['menu'].location.href='/cgi-bin/enrutar-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/enrutar.cgi?comand=estat&';
}
function bridge(){
window.top.frames['menu'].location.href='/cgi-bin/bridge-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/bridge.cgi?comand=estat&';
}
function portmirror(){
window.top.frames['menu'].location.href='/cgi-bin/portmirror-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/portmirror.cgi?comand=estat&';
}
function switchs(){
window.top.frames['menu'].location.href='/cgi-bin/switchs-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/switchs-estat.cgi';
}
function wifi(){
window.top.frames['menu'].location.href='/cgi-bin/wifi-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/wifi.cgi?comand=estat&';
}
function vpn_wg(){
window.top.frames['menu'].location.href='/cgi-bin/vpn_wg-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/vpn_wg.cgi?comand=estat&';
}
function dhcp(){
window.top.frames['menu'].location.href='/cgi-bin/dhcp-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/dhcp.cgi?comand=estat&';
}
function tallafocs(){
window.top.frames['menu'].location.href='/cgi-bin/tallafocs-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/tallafocs.cgi?comand=estat&';
}
function dmz(){
window.top.frames['menu'].location.href='/cgi-bin/dmz-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/dmz.cgi?comand=estat&';
}
function portal_captiu(){
window.top.frames['menu'].location.href='/cgi-bin/portal_captiu-menu.cgi';
window.top.frames['body'].location.href='/cgi-bin/portal_captiu.cgi?comand=estat&';
}

</script>

<table width="100%">
  <tr>
    <td>
      <!-- Botons esquerra -->
      <button onclick="wan()">WAN</button>
      <button onclick="enrutar()">ENRUTAR</button> 
      <button onclick="bridge()">BRIDGE</button> 
      <button onclick="portmirror()">PORTMIRROR</button> 
      <button onclick="switchs()">SWITCHS</button> 
      <button onclick="wifi()">WIFI</button> 
      <button onclick="vpn_wg()">VPN</button> 
      <button onclick="dhcp()">DHCP</button> 
      <button onclick="tallafocs()">TALLAFOCS</button>
      <button onclick="dmz()">DMZ</button> 
      <button onclick="portal_captiu()">PORTAL CAPTIU</button>    

  </tr>
</table>

</body>
</html>

EOM
