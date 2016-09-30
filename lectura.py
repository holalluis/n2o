#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    Funció "lectura": Connecta amb l'Arduino i processa les primeres dades que trobis
    exemple trama "IT1-450,T2-450,T3-450,T4-450,P1-200,P2-200,P3-200,P4-200F"
    retorna json del format {T1:25,...,T4:24,P1:0.5,...,P4:0.3,C1:0,...,C4:1}
'''
import serial
import processa as Pro

#connecta amb l'arduino
ser=serial.Serial('/dev/ttyACM0',9600)
print "Port serial: "+ser.port+". open: "+str(ser.isOpen())
print ""

'''Llegeix una sola trama crea un json'''
def lectura():

	trama=""
	while True:
		ser.flush()
		c=ser.read()
		trama+=c

		if c is "F":
			try:
				dades=Pro.processa(trama)
				break 
			except: 
				pass
			trama=""

	return dades
