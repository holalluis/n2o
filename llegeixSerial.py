'''
Exemple per rebre ordres d'un arduino via serial
- Creat  02/07/2016
- Modif  27/09/2016
'''
import serial
import urllib2
import time

# nova connexio serial
ser=serial.Serial('/dev/ttyACM0',115200)
#print '\n',ser

# comprovem que s'hagi obert la connexio
print "Serial "+ser.port+" obert: ",ser.isOpen()
print("[+] Son les "+time.strftime("%H:%M:%S"))
print "[+] Escoltant el port serial (arduino: "+ser.port+")... (ctrl+c per parar)"

'''tradueix una trama a llenguatge huma'''
def llegeix(trama):
	print(trama)
	#urllib2.urlopen("http://localhost/n2o/novaMesura.php?campana=1&t=1&p=1&v=1");
	#resposta = urllib2.urlopen("http://localhost/n2o/novaMesura.php?"+line);
	#print resposta.read()

while True:
	'''bucle infint de lectura'''
	trama=""
	#read(n) reads n bytes
	#read()  reads 1 bytes
	c=ser.read() 

	if(c=="I"):
		trama=c
		while(1):
			c=ser.read()
			trama+=c
			if(c=="F"): break
		llegeix(trama)
	else:
		pass

