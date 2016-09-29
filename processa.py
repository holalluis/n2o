#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Processa trames enviades per Arduino a llenguatge humà
	exemple trama "IT1-450,T2-450,T3-450,T4-450,P1-200,P2-200,P3-200,P4-200F"
	retorna json del format {T1:25,...,T4:24,P1:0.5,...,P4:0.3,C1:0,...,C4:1}
'''
def processa(trama):

    '''troba el valor analogic de temperatura o pressio especificat dins la trama,'''
    def troba(TPC,n):
        '''
            per exemple per trobar T1, cal cridar 'troba("T",1)'

            Parametres
                * TPC: <string> "T","P" or "C" (temperatura, pressio, o cabal)
                * n:   <int>     1,2,3,4   (numero de campana)
        '''
        #busca posicions inici i final dins la trama
        inici=trama.find(TPC+str(n)+"-")+3

        #Si es T4 o P4, la posicio final es busca de forma diferent
        if n==4:
            if TPC=="T":
                final=trama.find(",P1-") #després de T4 va ,P1-
            elif TPC=="P":
                final=trama.find(",C1-") #després de P4 va ,C1-
            elif TPC=="C":
				final=trama.find("F") #després de C4 va F
        else:
            #manera normal (n!=4)
            final=trama.find(","+TPC+str(n+1)+"-")

        #troba el valor analogic (0-1023) de temperatura o pressio dins la trama
        valor=int(trama[inici:final])

        #si és cabal ja estem
        if TPC=="C": 
        	return valor

        #converteix el valor analogic a graus o bars segons TPC
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
        if(TPC=="T"):
            ''' punts (180,0) i (901,60)'''
            x0=180
            y0=0.0
            x1=901
            y1=60.0
        elif(TPC=="P"):
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

        '''elimina pressió negativa (a vegades surt -0.0)'''
        if TPC=="P":
        	conv=max(0,conv)

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
    '''cabal campanes 1,2,3,4'''
    C1=troba("C",1)
    C2=troba("C",2)
    C3=troba("C",3)
    C4=troba("C",4)

    '''stdout'''
    print("<TRAMA REBUDA: "+trama+">")
    print("     T1="+str(T1)+"ºC, T2="+str(T2)+"ºC, T3="+str(T3)+"ºC, T4="+str(T4)+"ºC")
    print("     P1="+str(P1)+" bar, P2="+str(P2)+" bar, P3="+str(P3)+" bar, P4="+str(P4)+" bar")
    print("     C1="+str(C1)+", C2="+str(C2)+", C3="+str(C3)+", C4="+str(C4))
    print("")
    '''return objecte json'''
    return {"T1":T1,"T2":T2,"T3":T3,"T4":T4,"P1":P1,"P2":P2,"P3":P3,"P4":P4,"C1":C1,"C2":C2,"C3":C3,"C4":C4}


'''TEST'''
#processa("IT1-458,T2-462,T3-458,T4-466,P1-180,P2-182,P3-182,P4-184,C1-0,C2-0,C3-0,C4-0F")
#processa("IT1-458,T2-462,T3-458,T4-466,P1-180,P2-182,P3-182,P4-184,C1-0,C2-0,C3-0,C4-1F")
