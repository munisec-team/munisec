#!/bin/bash

read POST_DATA

RESULTAT=$(echo "$POST_DATA" | sed -n 's/^.*resultat=\([^&]*\).*$/\1/p' | sed 's/+/ /g')
FITXER=$(echo "$POST_DATA" | sed -n 's/^.*fitxer=\([^&]*\).*$/\1/p')

RESULTAT=$(printf '%b' "${RESULTAT//%/\\x}")

echo "Content-Type: text/plain"
echo "Content-Disposition: attachment; filename=\"$FITXER\""
echo ""

echo "$RESULTAT"
