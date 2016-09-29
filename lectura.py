#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import processa as Pro #classe propia
'''
    Llegeix una trama d'un arduino via serial
'''

#serial connect
ser=serial.Serial('/dev/ttyACM0',9600)
ser.flush()
print "Port serial: "+ser.port+". open: "+str(ser.isOpen())
print("")

'''Llegeix una trama'''
def lectura():
	while True:
		c=ser.read() #read 1 byte
		if(c!="I"): continue #si no és inici de trama torna a llegir

		#significa que c=="I"==inici de trama
		trama=c
		while True:
			c=ser.read()
			trama+=c
			if(c=="F"): break

		#intentar processar una sola trama fins que funcioni
		try:
			dades=Pro.processa(trama); #format json
			break 
		except: 
			pass
	return dades

'''test'''
#lectura()
