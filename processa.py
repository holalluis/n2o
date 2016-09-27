#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''tradueix una trama a llenguatge huma'''
def processa(trama):

    '''exemple trama "IT1-450,T2-450,T3-450,T4-450,P1-200,P2-200,P3-200,P4-200F" '''
    print("<TRAMA: "+trama+">")

    '''troba el valor analogic de temperatura o pressio especificat dins la trama,'''
    def troba(ToP,n):
        '''
            per exemple per trobar T1, cal cridar 'troba("T",1)'

            Parametres
                * ToP: <string> "T" or "P" (temperatura o pressio)
                * n:   <int>     1,2,3,4   (numero de campana)
        '''
        #busca posicions inici i final dins la trama
        inici=trama.find(ToP+str(n)+"-")+3

        #Si es T4 o P4, la posicio final es busca de forma diferent
        if(n==4):
            if(ToP=="T"):
                final=trama.find(",P1-") #després de T4 va ,P1
            elif(ToP=="P"):
                final=trama.find(",C") #després de P4 podria venir C#-1
                if(final==-1):
                    final=trama.find("F") #si no hi ha C#-1, hi haurà F
        else:
            #manera normal (n!=4)
            final=trama.find(","+ToP+str(n+1)+"-")

        #troba el valor analogic (0-1023) de temperatura o pressio dins la trama
        valor=int(trama[inici:final])

        #converteix el valor analogic a graus o bars segons ToP
        '''
            mail felix:
                T: Quan X val 180, estem a 0º,     quan X val 901 estem a 60º. 
                P: Quan X val 180, estem a 0 bars, quan X val 901 estem a 0,29 bars

            Calculem la recta amb dos punts (x0,y0) i (x1,y1)
                y=Mx+N 
                    on:
                        M=pendent, 
                        N=ordenada, 
                        x=valor analogic, 
                        y=pressio (bar) o temperatura (ºC)
                M=(y1-y0)/(x1-x0)
                N=y1-M*x1
        '''
        if(ToP=="T"):
            ''' punts (180,0) i (901,60)'''
            x0=180
            y0=0.0
            x1=901
            y1=60.0
        elif(ToP=="P"):
            ''' punts (180,0) i (901,0.29)'''
            x0=180
            y0=0.0
            x1=901
            y1=0.29
        else:
            quit("ERROR")

        '''aplicar formula general de la recta y=Mx+N'''
        M=(y1-y0)/(x1-x0)
        N=y1-M*x1
        conv=M*valor+N

        '''fi'''
        return round(conv,2)

    '''temperatura campanes 1,2,3,4'''
    T1=troba("T",1)
    T2=troba("T",2)
    T3=troba("T",3)
    T4=troba("T",4)
    '''pressio campanes 1,2,3,4'''
    P1=troba("P",1)
    P2=troba("P",2)
    P3=troba("P",3)
    P4=troba("P",4)

    '''stdout'''
    print("     T1="+str(T1)+"ºC, T2="+str(T2)+"ºC, T3="+str(T3)+"ºC, T4="+str(T4)+"ºC")
    print("     P1="+str(P1)+" bar, P2="+str(P2)+" bar, P3="+str(P3)+" bar, P4="+str(P4)+" bar")
    print("")

    '''
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

'''TEST'''
#processa("IT1-449,T2-451,T3-448,T4-450,P1-180,P2-182,P3-180,P4-181F")
#processa("IT1-555,T2-666,T3-777,T4-444,P1-190,P2-200,P3-300,P4-400,C1-1,C3-1F")
