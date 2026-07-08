#!/bin/bash

source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

echo "<html><head><title>Gestió de VLANs</title>"
echo "<meta charset='utf-8'>"

cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

echo "</head><body>"

LANS_DATA="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal_captiu configurar mostrar_configuracio)"

# Llegim totes les línies en un array
mapfile -t LANS <<< "$LANS_DATA"

# -------------------------------------------------------------------
# PORTAL CAPTIU CONFIGURACIO LANS
# -------------------------------------------------------------------
echo "<h2>PORTAL CAPTIU CONFIGURACIO LANS</h2>"
echo "<table>"
echo "<tr><th>nom</th><th>ip</th><th>estat</th><th></th></tr>"

for ((i = 0; i < ${#LANS[@]}; i++)); do
    line="${LANS[$i]}"
    [ -z "$line" ] && continue
    IFS=';' read -r nom ip estat <<< "$line"
    echo "<tr><td>$nom</td><td>$ip</td><td>$estat</td>"
    echo "<td><button onclick=\"location.href='/cgi-bin/portal_captiu-modificar.cgi?nom=$nom'\">Modificar</button></td>"
    echo "</tr>"
done

echo "</table>"

# -------------------------------------------------------------------
# PORTAL CAPTIU CONFIGURACIO USUARIS
# -------------------------------------------------------------------

USUARIS_DATA="$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli portal_captiu configurar mostrar_usuaris)"

# Llegim totes les línies en un array
mapfile -t USUARIS <<< "$USUARIS_DATA"

echo "<h2>PORTAL CAPTIU CONFIGURACIO USUARIS</h2>"
echo "<table>"
echo "<tr><th>usuari</th><th>contrasenya</th><th>ip</th><th>mac</th><th></th></tr>"

for ((i = 0; i < ${#USUARIS[@]}; i++)); do
    line="${USUARIS[$i]}"
    [ -z "$line" ] && continue
    IFS=';' read -r usuari password ip mac <<< "$line"
    echo "<tr><td>$usuari</td><td>$password</td><td>$ip</td><td>$mac</td>"
    echo "<td><button onclick=\"location.href='/cgi-bin/portal_captiu.cgi?accio=eliminar_usuari&comand=configurar&usuari=$usuari&contrasenya=$password'\">Eliminar</button></td>"
    echo "</tr>"
done

echo "</table>"

echo "<h2>PORTAL CAPTIU AFEGIR USUARI</h2>"
echo "<form action='/cgi-bin/portal_captiu.cgi' method='get'>"
echo "<input type='hidden' name='accio' value='afegir_usuari'>"
echo "<input type='hidden' name='comand' value='configurar'>"
echo "<table>"
echo "<tr><th>usuari</th><th>contrasenya</th><th></th></tr>"
echo "<tr><td><input type='text' name='usuari' placeholder='Usuari'></td><td><input type='password' name='contrasenya' placeholder='Contrasenya'></td><td><input type='submit' value='Afegir'></td></tr>"
echo "</table>"
echo "</form>"

echo "</body></html>"
