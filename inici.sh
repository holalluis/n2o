#!/bin/bash

clear;echo -e "S I S T E M A    N 2 O \n"

echo "[+] Tria una opció ('ctrl-c' per sortir):"

select op in $(ls|grep -e ".py" -e "dades"|grep -Ev 'processa|registra|virtual')

	do echo -e "\n[+] Iniciant programa $op...\n"

	./$op

done
