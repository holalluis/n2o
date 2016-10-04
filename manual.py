#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Mode manual per obrir i tancar vàlvules
'''
import serial
import sys
import time
try:
	ser=serial.Serial('/dev/ttyACM0',9600)
	ser.timeout=1
	ser.flushOutput()
except:
	print("CREANT SERIAL VIRTUAL")
	import virtual
	ser=virtual.Serial()
print("Port serial: "+ser.port+". open: "+str(ser.isOpen())+" --> Ctrl-C per parar\n")

def envia(comanda):
	print "Enviant '"+comanda+"'...",
	ser.write(comanda+'\n\r\n')
	time.sleep(1)
	ser.flushOutput()
	print "Fet"

envia('T1'); 
sys.exit()

'''
print("Escriu comanda '[o,t][1,2,3,4,a]', o 'q' per sortir")
while True:
	#print "n2o >>",
	comanda = raw_input()

	if comanda in ["q","exit","quit"]:
		sys.exit()

	if (comanda[0] not in ['o','t']) or (comanda[1] not in ['1','2','3','4','a']):
	#	print "Comanda desconeguda";continue

	if comanda[1] is 'a':
		if comanda[0] is 'o':
	#		print "Obrint TOTES les vàlvules"
			ser.write('O1'); ser.write('O2'); ser.write('O2'); ser.write('O4')
		elif comanda[0] is 't':
	#		print "Tancant TOTES les vàlvules"
			ser.write('T1'); ser.write('T2'); ser.write('T2'); ser.write('T4')
	else:
		if comanda[0] is 'o':
	#		print "Obrint vàlvula %s" % comanda[1]
			ser.write('O'+str(comanda[1]))
		elif comanda[0] is 't':
	#		print "Tancant vàlvula %s" % comanda[1]
			ser.write('T'+str(comanda[1]))

'''
