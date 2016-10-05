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
print "Obrir i tancar les electrovàlvules de forma manual:"
print "Escriu comanda '[ot][1234]', '?' per ajuda, o 'q' per sortir\n"

while True:
    print "manual >>",
    comanda = raw_input()

    #help
    if comanda is '?': 
        print "Exemple: la comanda 'o1' obre la vàlvula 1"
        print "Exemple: la comanda 't2' tanca la vàlvula 2"
        continue

    #comprova errors
    if comanda is "": continue
    if comanda in ["q","exit","quit"]: break
    if (comanda[0] not in ['o','t']) or (comanda[1] not in ['1','2','3','4']): print "Comanda desconeguda";continue

    co=comanda[0] #comanda "o" o "t"
    ev=comanda[1] #nº electrovalvula

    #Env.envia('O1',ser)
    if co is 'o':
        print "Obrint vàlvula %s..." % ev
        Env.envia('O'+ev,ser)
    elif co is 't':
        print "Tancant vàlvula %s..." % ev
        Env.envia('T'+ev,ser)
