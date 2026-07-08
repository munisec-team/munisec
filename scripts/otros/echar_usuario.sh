#!/bin/bash

USUARIO="concejalguarroman"

while true; do
    if who | awk '{print $1}' | grep -qx "$USUARIO"; then
        echo "$(date): expulsando a $USUARIO"

        # Mata todos los procesos del usuario
        pkill -KILL -u "$USUARIO"

        # Cierra sesiones activas
        loginctl terminate-user "$USUARIO" 2>/dev/null
    fi

    sleep 5
done
