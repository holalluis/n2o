#!/usr/bin/env python
'''
	Crea un serial virtual per quan no hi ha l'arduino (per testejar)
'''

class Serial:
	Trama = "IT1-300,T2-350,T3-375,T4-450,P1-180,P2-200,P3-400,P4-700,C1-0,C2-0,C3-0,C4-0F" #no canvia mai
	trama = Trama
	port ="VIRTUAL"
	def flushInput(self):
		pass
	def isOpen(self):
		return True
	def write(self,ordre):
		print "Has enviat %s" % ordre
	def read(self):
		n=len(self.trama)
		if n is 0: 
			self.trama=self.Trama
			n=len(self.trama)
		c=self.trama[0]
		self.trama=self.trama[1:n]
		return c
#test
'''
ser = Serial()    
trama=""
while True:
	c=ser.read()
	trama+=c
	if c is "F":
		print trama
		break
		'''
