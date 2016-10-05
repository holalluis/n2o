#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Interpreta una trama i retorna json'''
def processa(trama):

	'''Les trames són strings que comencen per 'I' i acaben per 'F' '''
	if trama[0] is not "I": raise RuntimeError("Trama incorrecta");
	if trama[len(trama)-1] is not "F": raise RuntimeError("Trama incorrecta");
	'''troba el valor analògic de temperatura o pressió dins la trama'''
	def troba(TPC,n):
		'''
			exemple per T1 = 'troba("T",1)'
			Parametres
			* TPC: <string> "T","P","C","E" (temperatura, pressió, o pols cabal)
			* n:   <int>     1,2,3,4   (número de campana)

			exemple de trama
			IT1-473,T2-477,T3-472,T4-466,P1-180,P2-181,P3-181,P4-182,E1-0,E2-0,E3-0,E4-0,C1-1,C2-1,C3-1,C4-1F
		'''
		#busca posicions inici i final dins la trama
		inici=trama.find(TPC+str(n)+"-")+3

		#Si es T4 ò P4 ò C4, la posició final es busca de forma diferent
		if n==4:
			if TPC=="T":
				final=trama.find(",P1-") #després de T4 va ,P1-
			elif TPC=="P":
				final=trama.find(",E1-") #després de P4 va ,E1-
			elif TPC=="E":
				final=trama.find(",C1-") #després de E4 va ,C1-
			elif TPC=="C":
				final=trama.find("F")
		else:
			#manera normal (n=1,2,3)
			final=trama.find(","+TPC+str(n+1)+"-")

		#troba el valor analogic (0-1023) dins la trama
		valor=int(trama[inici:final])

		#si és pols cabal o estat electrovàlvula ja estem (valen <0,1>)
		if TPC in ["C","E"]: return valor

		#converteix el valor analogic a graus o bars segons TPC
		'''
			mail felix:
				T: Quan X val 180, estem a 0º,     quan X val 901 estem a 60º. 
				P: Quan X val 180, estem a 0 bars, quan X val 901 estem a 0,29 bars
			Calculem la recta amb dos punts (x0,y0) i (x1,y1)
				y=Mx+N 
			on:
				M=pendent, N=ordenada, x=valor analogic, y=pressio (bar) o temperatura (ºC)
			fórmules:
				M=(y1-y0)/(x1-x0)
				N=y1-M*x1
		'''
		if(TPC=="T"):
			'''punts (180,0) i (901,60)'''
			x0=180; y0=0.0; x1=901; y1=60.0;
		elif(TPC=="P"):
			'''punts (180,0) i (901,0.29)'''
			x0=180; y0=0.0; x1=901; y1=0.29;

		'''aplicar la fórmula general de la recta y=Mx+N'''
		M=(y1-y0)/(x1-x0)
		N=y1-M*x1
		conv=M*valor+N

		'''esborra pressió negativa (i.e. -0.0)'''
		if TPC is "P": conv=max(conv,0)

		'''fi'''
		return round(conv,2)

	'''Temperatura, Pressió i Cabal'''
	T1=troba("T",1); P1=troba("P",1); C1=troba("C",1); E1=troba("E",1)
	T2=troba("T",2); P2=troba("P",2); C2=troba("C",2); E2=troba("E",2)
	T3=troba("T",3); P3=troba("P",3); C3=troba("C",3); E3=troba("E",3)
	T4=troba("T",4); P4=troba("P",4); C4=troba("C",4); E4=troba("E",4)

	'''stdout'''
	#print("TRAMA "+trama)
	print("  Temperatura -> T1="+str(T1)+"ºC, T2="+str(T2)+"ºC, T3="+str(T3)+"ºC, T4="+str(T4)+"ºC")
	print("  Pressió     -> P1="+str(P1)+" bar, P2="+str(P2)+" bar, P3="+str(P3)+" bar, P4="+str(P4)+" bar")
	print("  Pols cabal  -> C1="+str(C1)+", C2="+str(C2)+", C3="+str(C3)+", C4="+str(C4))
	print("  E-vàlvula   -> E1="+str(E1)+", E2="+str(E2)+", E3="+str(E3)+", E4="+str(E4))

	'''return objecte json'''
	return {"T1":T1,"T2":T2,"T3":T3,"T4":T4,"P1":P1,"P2":P2,"P3":P3,"P4":P4,"C1":C1,"C2":C2,"C3":C3,"C4":C4,"E1":E1,"E2":E2,"E3":E3,"E4":E4}

'''TEST'''
#processa("IT1-300,T2-350,T3-375,T4-450,P1-180,P2-200,P3-400,P4-700,E1-1,E2-0,E3-0,E4-0,C1-0,C2-0,C3-0,C4-0F")
