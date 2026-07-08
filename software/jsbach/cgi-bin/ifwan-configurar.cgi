#!/bin/bash

source /usr/local/JSBach/conf/variables.conf
source "$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/funcions

#Vull una pagina cgi amb bash per apache2 per linux que... primera seccio dos radius option, la #primera opcio "dhcp" i la segona "manual" cas de polsar algun dels dos, que per metode get es pase #mode=[dhcp o manual] Segona secció "Interfaç" Amb la funció: Interfaces_Ethernet() { for iface in #$(ip -o link show | awk -F': ' '{print $2}'); do if [[ "$iface" != "lo" ]]; then if ! iw dev 2>/#dev/null | grep -q "$iface"; then echo "$iface" fi fi done } amb la llista que me torne, crea una #llista de radius option i la que siga seleccionada torne per GET int="el nome de la targeta" I #tercera seccio: Estarà oculta i cas de seleccionar mode manual en la primera seccio, mostrar #quatre inptus de text, el primer de no ip i torna per metode get ip="la ip introduida", el segon #de nom mascara tornarà per get masc="la mascara introduida", el tercer de nom porta d'enllaç i #torna per GET pe="la ip introduida" i el darrer de nom dns i torna per get dns=" la ip introduida" #Acabarem amb un boto guardar que al polsar enllace amb la paguina guardar-ifwan.cgi

echo "Content-type: text/html"
echo ""

# --- Funció per obtenir interfícies Ethernet (sense lo ni wifi) ---
# Ara utilitzem la funció centralitzada fnc_interfaces_ethernet de funcions

CONFIGURACIO=$("$DIR"/"$DIR_PROJECTE"/"$DIR_SCRIPTS"/client_srv_cli ifwan mostrar)
conf_mode=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' ' -f1)
conf_int=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' ' -f2)
if [[ "$conf_mode" == "manual" ]]; then
    conf_ip=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' ' -f3)
    conf_masc=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' ' -f4)
    conf_pe=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' ' -f5)
    conf_dns=$(echo "$CONFIGURACIO" | tr -s ' ' | cut -d' ' -f6)
fi

# --- Inici HTML ---
cat << 'EOF'
<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<title>Configuració de la WAN</title>
EOF

cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN

cat << 'EOF'
<script>
function toggleManual() {
  const modeManual = document.getElementById("manual").checked;
  const manualSection = document.getElementById("manual-section");
  manualSection.style.display = modeManual ? "block" : "none";
}

  // Quan la pàgina es carrega, comprova l'estat i actualitza la visibilitat
  window.addEventListener("DOMContentLoaded", toggleManual);
  
</script>
</head>
<body>
<h2>Configuració de la interfície WAN</h2>

<form action="/cgi-bin/ifwan.cgi" method="get">
<input type="hidden" name="comand" value="configurar">
<input type="hidden" name="argument" value="guardar">

EOF

# --- SECCIÓ 1: MODE (DHCP o MANUAL) ---
cat << 'EOF'
<fieldset>
  <legend>Mode de configuració</legend>
EOF
dhcp_check=""
manual_check=""
if [[ "$conf_mode" == "dhcp" ]]; then
    dhcp_check="checked"
else
    manual_check="checked"
fi

echo '<input type="radio" id="dhcp" name="mode" value="dhcp" onclick="toggleManual()" '$dhcp_check'>'
cat << 'EOF'
  <label for="dhcp">DHCP</label><br>
EOF
echo '<input type="radio" id="manual" name="mode" value="manual" onclick="toggleManual()" '$manual_check'>'
cat << 'EOF'

  <label for="manual">Manual</label>
</fieldset>
EOF

# --- SECCIÓ 2: INTERFÍCIES ---
echo '<fieldset>'
echo '  <legend>Interfície</legend>'

for iface in $(fnc_interfaces_ethernet); do
    if [[ "$iface" == "$conf_int" ]]; then
        echo "  <input type='radio' name='int' id='$iface' value='$iface' checked>"
    else
        echo "  <input type='radio' name='int' id='$iface' value='$iface' >"
    fi
    echo "  <label for='$iface'>$iface</label><br>"
done

echo '</fieldset>'

# --- SECCIÓ 3: CONFIGURACIÓ MANUAL (OCULTA PER DEFECTE) ---
cat << 'EOF'
<fieldset id="manual-section" class="hidden">
  <legend>Configuració manual</legend>
  <label>IP:</label><br>
EOF
echo '<input type="text" name="ip" value='$conf_ip'><br><br>'
cat << 'EOF'

  <label>Màscara:</label><br>
EOF
echo ' <input type="text" name="masc" value='$conf_masc'><br><br>'
cat << 'EOF'

  <label>Porta d'enllaç:</label><br>
EOF
echo ' <input type="text" name="pe" value='$conf_pe'><br><br>'
cat << 'EOF'

  <label>DNS:</label><br>
EOF
echo ' <input type="text" name="dns" value='$conf_dns'><br><br>'
cat << 'EOF'

</fieldset>
<br>
<input type="submit" value="Guardar">
</form>
</body>
</html>
EOF
