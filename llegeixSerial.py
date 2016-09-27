'''
    Rebre dades d'un arduino via serial
    - Creat  02/07/2016
    - Modif  27/09/2016
'''
import serial
import time

'''classes propies'''
import Processa

#nova connexio serial
ser=serial.Serial('/dev/ttyACM0',115200)

#comprovem que s'hagi obert la connexio
print "Serial "+ser.port+" obert: ",ser.isOpen()
print("[+] Son les "+time.strftime("%H:%M:%S"))
print "[+] Escoltant el port serial (arduino: "+ser.port+")... (ctrl+c per parar)"

'''bucle infint de lectura'''
while True:
    trama=""
    c=ser.read() # read 1 byte (1 char)

    #busquem inici de trama
    if(c!="I"): 
        continue

    #significa que c=="I"
    trama=c
    while True:
        c=ser.read()
        trama+=c
        if(c=="F"): 
            break
    Processa.processa(trama)
