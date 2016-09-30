#!/usr/bin/env python
# -*- coding: utf-8 -*-
import processa as Pro
import serial
import sys

#connecta amb l'arduino
ser=serial.Serial('/dev/ttyACM0',9600)
print "Port serial: "+ser.port+". open: "+str(ser.isOpen()),

print(" --> Ctrl-C per parar")

print "\n\n\n\n"

#linies a esborrar per pantallazo
linies=4 

trama=""
while True:
	ser.flush()
	c=ser.read()
	trama+=c

	if c is "F":
		try: 
			for i in range(linies): sys.stdout.write("\033[F\033[K")
			Pro.processa(trama)
		except: 
			for i in range(linies): sys.stdout.write("\033[B")
		trama=""
