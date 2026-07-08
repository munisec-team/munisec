#!/bin/bash

############################################
# Configuració
############################################
source /usr/local/JSBach/conf/variables.conf

echo "Content-type: text/html; charset=utf-8"
echo ""

############################################
# Funció per llegir paràmetres GET (URL decode correcte)
############################################
get_param() {
    local PARAM
    PARAM="$(echo "$QUERY_STRING" | tr '&' '\n' | grep "^$1=" | cut -d= -f2-)"
    PARAM="${PARAM//+/ }"
    printf '%b' "${PARAM//%/\\x}"
}

############################################
# Llegir paràmetres
############################################
VNOM="$(get_param vnom)"
POSICIO="$(get_param posicio)"

PROTO="$(get_param proto)"

IP_ORIG="$(get_param ip_orig)"
IP_ORIG_NOT="$(get_param ip_orig_not)"

IP_DEST="$(get_param ip_dest)"
IP_DEST_NOT="$(get_param ip_dest_not)"

PORT_ORIG="$(get_param port_orig)"
PORT_ORIG_NOT="$(get_param port_orig_not)"

PORT_DEST="$(get_param port_dest)"
PORT_DEST_NOT="$(get_param port_dest_not)"

MAC_ORIG="$(get_param mac_orig)"
MAC_ORIG_NOT="$(get_param mac_orig_not)"

MODULS_EXTRA="$(get_param moduls_extra)"

JUMP="$(get_param jump)"
LOGTXT="$(get_param logtxt)"

############################################
# Construcció de la regla
############################################
REGLA="iptables -A Input-wan"

# Protocol
[ -n "$PROTO" ] && REGLA="$REGLA -p $PROTO"

# IP origen
if [ -n "$IP_ORIG" ]; then
    [ "$IP_ORIG_NOT" = "1" ] && REGLA="$REGLA !"
    REGLA="$REGLA -s $IP_ORIG"
fi

# IP destí
if [ -n "$IP_DEST" ]; then
    [ "$IP_DEST_NOT" = "1" ] && REGLA="$REGLA !"
    REGLA="$REGLA -d $IP_DEST"
fi

# Ports (només tcp / udp)
if [[ "$PROTO" == "tcp" || "$PROTO" == "udp" ]]; then
    if [ -n "$PORT_ORIG" ]; then
        [ "$PORT_ORIG_NOT" = "1" ] && REGLA="$REGLA !"
        REGLA="$REGLA --sport $PORT_ORIG"
    fi

    if [ -n "$PORT_DEST" ]; then
        [ "$PORT_DEST_NOT" = "1" ] && REGLA="$REGLA !"
        REGLA="$REGLA --dport $PORT_DEST"
    fi
fi

# MAC origen
if [ -n "$MAC_ORIG" ]; then
    REGLA="$REGLA -m mac"
    [ "$MAC_ORIG_NOT" = "1" ] && REGLA="$REGLA !"
    REGLA="$REGLA --mac-source $MAC_ORIG"
fi

# Mòduls extra (text lliure)
if [ -n "$MODULS_EXTRA" ]; then
    REGLA="$REGLA $MODULS_EXTRA"
fi

# Acció (-j)
if [ "$JUMP" = "LOG" ]; then
    REGLA="$REGLA -j LOG"
    [ -n "$LOGTXT" ] && REGLA="$REGLA --log-prefix \"$LOGTXT\""
else
    [ -n "$JUMP" ] && REGLA="$REGLA -j $JUMP"
fi

REGLA_COMPLETA="$REGLA"

############################################
# Executar backend
############################################
CMD="$DIR/$DIR_PROJECTE/$DIR_SCRIPTS/client_srv_cli"

resultat=$("$CMD" tallafocs configurar afegir_nova_regla_wan "$POSICIO" "$REGLA_COMPLETA" 2>&1)


############################################
# Sortida HTML
############################################
echo "<html>"
echo "<head>"
echo "<meta charset=\"UTF-8\">"
echo "<title>Afegir regla tallafocs</title>"
cat $DIR/$DIR_PROJECTE/$DIR_CGI/$CSS_CGI_BIN
echo "</head>"
echo "<body>"
echo "<h2>Regla enviada</h2>"
echo "<pre>$REGLA_COMPLETA</pre>"
echo "<pre>$resultat</pre>"
echo "<br>"
retorn="$(get_param retorn)"
if [ -n "$retorn" ]; then
echo "<a href=\"$retorn\"><button>Tornar</button></a>"
fi
echo "</body>"
echo "</html>"

