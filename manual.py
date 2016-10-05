#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Mode manual per obrir i tancar vàlvules
'''
import serial
import sys
import time
import processa as Pro

try:
	ser=serial.Serial('/dev/ttyACM0',9600)
except:
	print("CREANT SERIAL VIRTUAL")
	import virtual
	ser=virtual.Serial()
print("Port serial: "+ser.port+". open: "+str(ser.isOpen())+" --> Ctrl-C per parar\n")

'''ENVIA UNA COMANDA (format: 2 caràcters: [ot][1234])'''
def envia(comanda):
	ser.flushOutput()
	ser.write(comanda+'\n')
	trama=""
	ser.flushInput()
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
		else: time.sleep(1); envia(comanda)
	elif comanda[0] is 'T':
		if d['E'+EV] is 0: print "FET!"; return
		else: time.sleep(1); envia(comanda)

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
	if comanda in ["q","exit","quit"]: sys.exit()
	if (comanda[0] not in ['o','t']) or (comanda[1] not in ['1','2','3','4']): print "Comanda desconeguda";continue
	co=comanda[0] #comanda
	ev=comanda[1] #electrovalvula

	#al codi .ino obrir i tancar estan girats!
	if co is 'o':
		print "Obrint vàlvula %s..." % ev
		envia('O'+ev)
	elif co is 't':
		print "Tancant vàlvula %s..." % ev
		envia('T'+ev)
