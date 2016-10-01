#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Comença a llegir i guardar dades
'''
import time
import sys
import lectura as Lec
import registra as Reg

#Volum inicial de les 4 campanes (L)
V1=0; V2=0; V3=0; V4=0;

#primera lectura per saber estat inicial pols cabal
d=Lec.lectura()
C1=d['C1']; C2=d['C2']; C3=d['C3']; C4=d['C4']

#esborra 4 linies
for i in range(4): sys.stdout.write("\033[F\033[K")

#registra lectures a la base de dades
while True:
    d=Lec.lectura() #llegeix Arduino

		#si el pols canvia, suma 10 L
    if(d['C1']!=C1): V1+=10
    if(d['C2']!=C2): V2+=10
    if(d['C3']!=C3): V3+=10
    if(d['C4']!=C4): V4+=10

		#afegeix el volum a l'objecte "d"
    d['V1']=V1; d['V2']=V2; d['V3']=V3; d['V4']=V4

		#update valor del pols
    C1=d['C1']; C2=d['C2']; C3=d['C3']; C4=d['C4'];

    try:
			print(d)
			#Reg.registra(d)
			#esborra línies
			for i in range(9): sys.stdout.write("\033[F\033[K")
			time.sleep(1)
    except: 
			pass
