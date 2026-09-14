#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

############################################
# Llegir únic paràmetre GET: vnom
############################################

FITXER="$DIR/$DIR_PROJECTE/$DIR_CONF/$IPTABLES_INPUT_WAN"

############################################
# Comptar línies reals del fitxer
############################################
if [ -f "$FITXER" ]; then
    NUM_LINIES=$(grep -v '^\s*$' "$FITXER" | grep -v '^#' | wc -l)
else
    NUM_LINIES=0
fi

POSICIO_DEF=$((NUM_LINIES + 1))

############################################
# HTML capçalera
############################################
cat << EOF
<html>
<head>
<meta charset="UTF-8">
<title>Tallafocs INPUT WAN</title>

EOF
cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

/bin/cat << EOF
<script>
function mostrarLog(select) {
    var logRow = document.getElementById("logrow");
    if (select.value === "LOG") {
        logRow.style.display = "";
    } else {
        logRow.style.display = "none";
    }
}
</script>
</head>
<body>

<h1>Tallafocs INPUT WAN</h1>
EOF

############################################
# SECCIÓ REGLES
############################################
echo "<h2>REGLES</h2>"
echo "<table>"
echo "<tr><th>#</th><th>Regla</th><th>Acció</th></tr>"

if [ -f "$FITXER" ]; then
    N=0
    while IFS= read -r LINIA; do
        case "$LINIA" in "" | \#*) continue ;; esac
        N=$((N + 1))
        echo "<tr>"
        echo "<td>$N</td>"
        echo "<td>$LINIA</td>"
        echo "<td>
	<form method=\"get\" action=\"tallafocs.cgi\" style=\"margin:0\">
	<input type=\"hidden\" name=\"comand\" value=\"configurar\">
	<input type=\"hidden\" name=\"accio\" value=\"eliminar_regla_wan\">
	<input type=\"hidden\" name=\"posicio\" value=\"$N\">
    <input type="hidden" name="retorn" value="tallafocs-crear-regla-wan.cgi">
	<input type=\"submit\" value=\"Eliminar\">
	</form>
	</td>"
        echo "</tr>"
    done < "$FITXER"
else
    echo "<tr><td colspan='3'>No hi han regles</td></tr>"
fi

echo "</table>"

############################################
# SECCIÓ NOVA REGLA
############################################
cat << EOF
<h2>NOVA REGLA</h2>

<form method="get" action="tallafocs-afegir-regla-wan.cgi">
<input type="hidden" name="retorn" value="tallafocs-crear-regla-wan.cgi">
<table>

<tr>
<td>Posició</td>
<td>
<input type="text" name="posicio" value="$POSICIO_DEF">
</td>
</tr>

<tr>
<td>Protocol</td>
<td>
<select name="proto">
<option value="">--</option>
<option value="tcp">tcp</option>
<option value="udp">udp</option>
<option value="icmp">icmp</option>
</select>
</td>
</tr>

<tr>
<td>IP origen</td>
<td>
<input type="checkbox" name="ip_orig_not" value="1"> !
<input type="text" name="ip_orig">
</td>
</tr>

<tr>
<td>Port origen</td>
<td>
<input type="checkbox" name="port_orig_not" value="1"> !
<input type="text" name="port_orig">
</td>
</tr>

<tr>
<td>Port destí</td>
<td>
<input type="checkbox" name="port_dest_not" value="1"> !
<input type="text" name="port_dest">
</td>
</tr>

<tr>
<td>MAC origen</td>
<td>
<input type="checkbox" name="mac_orig_not" value="1"> !
<input type="text" name="mac_orig" placeholder="AA:BB:CC:DD:EE:FF">
</td>
</tr>

<tr>
<td>Mòduls extra</td>
<td>
<input type="text" name="moduls_extra"
       style="width: 100%"
       placeholder="-m iprange --src-range 192.168.0.1-192.168.0.100">
</td>
</tr>

<tr>
<td>Acció (-j)</td>
<td>
<select name="jump" onchange="mostrarLog(this)">
<option value="ACCEPT">ACCEPT</option>
<option value="DROP">DROP</option>
<option value="REJECT">REJECT</option>
<option value="LOG">LOG</option>
</select>
</td>
</tr>

<tr id="logrow" style="display:none">
<td>Log prefix</td>
<td><input type="text" name="logtxt"></td>
</tr>

<tr>
<td colspan="2" align="center">
<input type="submit" value="AFEGIR">
</td>
</tr>

</table>
</form>

</body>
</html>
EOF
