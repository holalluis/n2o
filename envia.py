#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Funció per enviar comandes al arduino
		ENVIA UNA COMANDA (format: 2 caràcters: [OT][1234])
		La funció necessita la variable "ser", que és un objecte serial.Serial()
'''
import sys
import time
import processa as Pro

def envia(comanda,ser):
    if comanda[0] not in ["O","T"]: raise RuntimeError("Comanda desconeguda"); return
    if comanda[1] not in ["1","2","3","4"]: raise RuntimeError("Comanda desconeguda"); return

    ser.flushOutput()
    ser.write(comanda+'\n')
    trama=""
    ser.flushInput()
    #mira l'estat de la valvula
    while True:
        c=ser.read()
        trama+=c
        if c is "F":
            try: 
                d=Pro.processa(trama)
                for i in range(4): sys.stdout.write("\033[F\033[K")
                break
            except: pass
            trama=""
            ser.flushInput()

    EV=comanda[1] #nº electrovàlvula
    #processa les comandes i fes crides recursives per forçar estat desitjat
    if comanda[0] is 'O':
        if d['E'+EV] is 1: print "FET!"; return
        else: time.sleep(1); envia(comanda,ser)
    elif comanda[0] is 'T':
        if d['E'+EV] is 0: print "FET!"; return
        else: time.sleep(1); envia(comanda,ser)
