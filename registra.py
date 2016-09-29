'''
	Insertar lectures a la base de dades
'''

import urllib2
import sys

url="http://localhost/n2o/novaMesura.php?"

def registra(dades):

	#desempaqueta les dades (Temperatura, Pressio, Volum)
	T1=dades['T1'];P1=dades['P1'];V1=dades['V1']
	T2=dades['T2'];P2=dades['P2'];V2=dades['V2']
	T3=dades['T3'];P3=dades['P3'];V3=dades['V3']
	T4=dades['T4'];P4=dades['P4'];V4=dades['V4']

	sys.stdout.write("\033[F\033[F")

	#campana 1
	res=urllib2.urlopen(url+"campana=1&t="+str(T1)+"&p="+str(P1)+"&v="+str(V1));print res.read()
	sys.stdout.write("\033[F\033[F")

	#campana 2
	res=urllib2.urlopen(url+"campana=2&t="+str(T2)+"&p="+str(P2)+"&v="+str(V2));print res.read()
	sys.stdout.write("\033[F\033[F")

	#campana 3
	res=urllib2.urlopen(url+"campana=3&t="+str(T3)+"&p="+str(P3)+"&v="+str(V3));print res.read()
	sys.stdout.write("\033[F\033[F")

	#campana 4
	res=urllib2.urlopen(url+"campana=4&t="+str(T4)+"&p="+str(P4)+"&v="+str(V4));print res.read()

	print("")
