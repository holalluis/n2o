#!/bin/bash

clear

echo -e "S I S T E M A   N 2 O\n"

echo "[+] Tria un programa (ctrl-c per sortir):"

select op in $(ls|grep -E '.py|veureDades'|grep -Ev 'processa|registra|virtual|envia')
do
	echo -e "\n[+] Iniciant programa $op...\n"
	./$op
done
