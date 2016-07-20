'''
	Exemple per rebre ordres d'un arduino via serial
	- Creat el 02/07/2015
'''
import serial
import urllib2
import time

# nova connexio serial
ser=serial.Serial('/dev/ttyAMA0',9600)
#print '\n',ser

# comprovem que s'hagi obert la connexio
print "Serial esta obert:",ser.isOpen()

while True:
	try:
		print("[+] Son les "+time.strftime("%H:%M:%S"))
		print "[+] Escoltant el port serial (arduino)... (ctrl+c per parar d'escoltar)"
		
		#llegeix la comanda que arriba
		line=ser.readline()

		#a vegades es generen espais que donen errors
		line=line.replace(' ','')

		print "[+] S'ha rebut la comanda:\n\t '"+line+"'"

		#urllib2.urlopen("http://localhost/n2o/novaMesura.php?campana=1&t=1&p=1&v=1");
		resposta = urllib2.urlopen("http://localhost/n2o/novaMesura.php?"+line);

		print resposta.read()
	except:
		break
