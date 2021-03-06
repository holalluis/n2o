#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Inserta una lectura a la base de dades
	"dades" és un objecte json creat a "lectura.py" amb els camps:
	T1,T2,T3,T4,P1,P2,P3,P4,C1,C2,C3,C4,V1,V2,V3,V4
	|---temp---|--pressio--|---cabal---|---volum--|
'''
import urllib2
import sys
import threading
import time

def registra(dades):
    t=threading.Thread(target=worker,args=[dades])
    t.start()

def worker(dades):
    #mostra la hora
    print "\n", time.ctime(), "UTC\n"

    #desempaqueta dades (Temperatura, Pressio, Volum, estat electrovalvula)
    T1=dades['T1']; P1=dades['P1']; V1=dades['V1']; E1=dades['E1']
    T2=dades['T2']; P2=dades['P2']; V2=dades['V2']; E2=dades['E2']
    T3=dades['T3']; P3=dades['P3']; V3=dades['V3']; E3=dades['E3']
    T4=dades['T4']; P4=dades['P4']; V4=dades['V4']; E4=dades['E4']

    #esborra una línia
    sys.stdout.write("\033[F\033[F")

    #script php que afegeix mesures
    url="http://localhost/n2o/novaMesura.php"

    #campanes
    res=urllib2.urlopen(url+"?campana=1&t="+str(T1)+"&p="+str(P1)+"&v="+str(V1)+"&e="+str(E1))
    print res.read()
    sys.stdout.write("\033[F\033[F")
    res=urllib2.urlopen(url+"?campana=2&t="+str(T2)+"&p="+str(P2)+"&v="+str(V2)+"&e="+str(E2))
    print res.read()
    sys.stdout.write("\033[F\033[F")
    res=urllib2.urlopen(url+"?campana=3&t="+str(T3)+"&p="+str(P3)+"&v="+str(V3)+"&e="+str(E3))
    print res.read()
    sys.stdout.write("\033[F\033[F")
    res=urllib2.urlopen(url+"?campana=4&t="+str(T4)+"&p="+str(P4)+"&v="+str(V4)+"&e="+str(E4))
    print res.read()

    print("")

'''TEST
dades={'P2':0.0,'P3':0.0,'P1':0.0,'P4':0.0,'T4':22.64,'T2':23.22,'T3':23.05,'T1':23.05,'V1':0,'V2':0,'V3':0,'V4':0,'E4':0,'C3':1,'C2':1,'C1':1,'E2':0,'E1':1,'E3':0,'C4':1}
registra(dades)
'''
