#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Comença a llegir i guardar dades
    és com un monitor amb la diferència que guarda els valors a la base de dades
'''
import serial
import registra as Reg
import processa as Pro
import sys
import time
import os

#Arguments
if len(sys.argv)!=2:
	print "Introdueix interval de temps (segons): ",
	tempsEspera=raw_input()
else:
	tempsEspera=sys.argv[1]

#transforma a enter
tempsEspera=int(tempsEspera)

#comprova tempsEspera
if(tempsEspera<0): raise RuntimeError("temps espera negatiu")

os.system('clear')
print("Adquirint dades cada %s segons" %tempsEspera)

#connecta amb l'arduino via serial
try:
	ser=serial.Serial('/dev/ttyACM0',9600)
except:
	print("CREANT SERIAL VIRTUAL")
	import virtual
	ser=virtual.Serial()

print("Port serial: "+ser.port+". open: "+str(ser.isOpen())+" --> Ctrl-C per parar\n\n")

'''
    Volum inicial de les 4 campanes (L) = 0
    Poso -10 pq el 1r cop que comprovem el pols sumarem 10 i quedarà igual a zero
'''
V1=-10;V2=-10;V3=-10;V4=-10
'''
    Estat del pols inicial: posem un valor diferent a 0 ò 1
    Com funciona el pols: varia el bit Cn quan s'envia el pols (on n={1,2,3,4})
    0000000011111111111111111111000000000000000000111111111...
            ^pols 1             ^pols2            ^pols3
'''
C1=2;C2=2;C3=2;C4=2

#comença bucle de lectura
trama=""
lectures=0 #nombre de lectures fetes mentre esperes (1 segon)
while True:

    #ves comptant el volum mentre esperes
    while True:
        c=ser.read()
        trama+=c
        if c is "F":
            try: 
                d=Pro.processa(trama) #saltarà si la trama és incorrecta
                for i in range(4): sys.stdout.write("\033[F\033[K")
                trama=""
            except: 
                print trama
                trama=""
                ser.flushInput()
                continue
        else:
            continue #continua afegint caracters a la trama

        #si som aquí vol dir que la trama és correcta
        #si l'estat del pols ha canviat, suma 10 L
        if(d['C1']!=C1): V1+=10
        if(d['C2']!=C2): V2+=10
        if(d['C3']!=C3): V3+=10
        if(d['C4']!=C4): V4+=10
        #update estat del pols
        C1=d['C1'];C2=d['C2'];C3=d['C3'];C4=d['C4'];
        #afegeix el volum a l'objecte "d"
        d['V1']=V1;d['V2']=V2;d['V3']=V3;d['V4']=V4

        sys.stdout.write("\033[F\033[K")
        print "Volum (L): "+str([V1,V2,V3,V4])

        #registra a la base de dades si el comptador està a zero
        if lectures is 0:
            try: Reg.registra(d)
            except: print("Error: Dades no registrades")

        lectures+=1
        time.sleep(1)
        if lectures > tempsEspera: break
        ser.flushInput()
    #final del temps d'espera

    #reset comptador de lectures
    lectures=0
    #neteja pantalla
    os.system('clear')
    print("Adquirint dades cada %s segons" %tempsEspera)
    #flush input! IMPORTANTISSIM
    ser.flushInput()

