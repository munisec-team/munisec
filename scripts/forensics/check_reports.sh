#!/bin/bash

if [ $EUID -ne 0 ]; then
	echo "Ejecute como root"
	exit 1
fi

RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[93m"
BLUE="\e[96m"
RESET="\e[0m"

info()    { echo -e "${BLUE}$1${RESET}"; }
success() { echo -e "${GREEN}$1${RESET}"; }
warning() { echo -e "${YELLOW}$1${RESET}"; }

reportsPath="/home/bibliotecaguarroman/reports/"
actualDirs=("AD" "DESKTOP-FIM7UF9" "JSBachAyto" "JSBachCC" "Odoo" "soc" "WINCLI2" "wordpress")
let invalidInput=0

case $1 in
	--today)
		fecha=$(date +%d-%m-%Y)
		IFS="-" read -r day month year <<< "$fecha"
		;;

	--date)
		if [ -z $2 ]; then
			echo "Uso: sudo bash check_reports.sh --date dd-mm-yyyy"
			exit 1
		fi

		IFS="-" read -r day month year <<< "$2"

		if [ -z "$day" ]; then
			echo "[ERROR] Falta día dd"
			invalidInput=1
		fi

		if [ -z "$month" ]; then
			echo "[ERROR] Falta mes mm"
			invalidInput=1
		fi

		if [ -z "$year" ]; then
			echo "[ERROR] Falta año yyyy"
			invalidInput=1
		fi

		if (( invalidInput == 1 )); then
		    echo "Se espera:"
		    echo "sudo bash check_reports.sh dd-mm-yyyy"
		    exit 1
		fi

		invalidInput=0

		# DIA
		if [[ $day =~ ^[0-9]+$ ]]; then
			if (( day < 1 || day > 31 )); then
		        echo "[ERROR] día '$day' fuera de rango (1-31)"
		        invalidInput=1
		    else
		        if (( ${#day} == 1 )); then
		            day="0$day"
		        fi
		    fi
		else
		    echo "[ERROR] día '$day' debe ser un número entero"
		    invalidInput=1
		fi

		# MES
		if [[ $month =~ ^[0-9]+$ ]]; then
		    if (( month < 1 || month > 12 )); then
		        echo "[ERROR] mes '$month' fuera de rango (1-12)"
		        invalidInput=1
		    else
		        if (( ${#month} == 1 )); then
		            month="0$month"
		        fi
		    fi
		else
		    echo "[ERROR] mes '$month' debe ser un número entero"
		    invalidInput=1
		fi

		# AÑO
		if [[ $year =~ ^[0-9]+$ ]]; then
		    if (( ${#year} != 4 )); then
		        echo "[ERROR] año '$year' debe tener 4 dígitos"
		        invalidInput=1
		    fi
		else
		    echo "[ERROR] año '$year' debe ser un número entero"
		    invalidInput=1
		fi
	;;

	*)
		echo "Uso: sudo bash check_reports.sh [--today|--date dd-mm-yyyy]"
		exit 1
	;;
esac

# COMPROBACIÓN FINAL
if (( invalidInput == 0 )); then
    for dir in "${actualDirs[@]}"; do
	matches=$(ls -A "$reportsPath$dir" 2>/dev/null | grep "$year-$month-$day")

	info "Reportes $dir a fecha $day-$month-$year"
	info "------------------------------------------"
	if [ -z "$matches" ]; then
		warning "\t[WARNING] No se han encontrado reportes."
	else
		while IFS= read -r file; do
			success "\t- $file"
		done <<< "$matches"
	fi
	echo ""
    done
else
    echo "Fecha inválida"
    exit 1
fi

