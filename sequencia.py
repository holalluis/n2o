#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Mode manual per obrir i tancar vàlvules
'''
import serial
import envia as Env

try:
    ser=serial.Serial('/dev/ttyACM0',9600)
except:
    print("CREANT SERIAL VIRTUAL")
    import virtual
    ser=virtual.Serial()

print("Port serial: "+ser.port+". open: "+str(ser.isOpen())+" --> Ctrl-C per parar\n")

while True:

    #llegir comandes seqüencialment. exemple:
    Env.envia('O1',ser)
    espera(100 segons)
    Env.envia('T1',ser)

    Env.envia('O2',ser)
    espera(100 segons)
    Env.envia('T2',ser)
