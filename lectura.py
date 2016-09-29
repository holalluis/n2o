#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	N2O:
    Llegeix una trama d'un arduino via serial

    - Creat  02/07/2016

	NEXT STEP: insertar a la base de dades
	import urllib2
	urllib2.urlopen("http://localhost/n2o/novaMesura.php?campana=1&t="+str(T1)+"&p="+str(P1)+"&v=1");
	urllib2.urlopen("http://localhost/n2o/novaMesura.php?campana=2&t="+str(T2)+"&p="+str(P2)+"&v=1");
	urllib2.urlopen("http://localhost/n2o/novaMesura.php?campana=3&t="+str(T3)+"&p="+str(P3)+"&v=1");
	urllib2.urlopen("http://localhost/n2o/novaMesura.php?campana=4&t="+str(T4)+"&p="+str(P4)+"&v=1");
	urllib2.urlopen("http://localhost/n2o/novaMesura.php?campana=1&t=1&p=1&v=1");
	resposta = urllib2.urlopen("http://localhost/n2o/novaMesura.php?"+line);
	print resposta.read()
'''
import serial
import time
import processa as Pro #classe propia

#serial connect
ser=serial.Serial('/dev/ttyACM0',9600)
ser.flush()
print "Port serial: "+ser.port+". open: "+str(ser.isOpen())

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
	ser.close()
	return dades

'''test'''
lectura()
