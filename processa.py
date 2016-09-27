
'''tradueix una trama a llenguatge huma'''
'''exemple de trama = "IT1-XXX,T2-XXX,T3-XXX,T4-XXX,P1-XXX,P2-XXX,P3-XXX,P4-XXXF" '''
def llegeix(trama):
    print(trama)
    inici=trama.find("T1")+3
    final=trama.find(",T2")
    T1 = int(trama[inici:final])
    print(T1)

    #import urllib2
    #urllib2.urlopen("http://localhost/n2o/novaMesura.php?campana=1&t=1&p=1&v=1");
    #resposta = urllib2.urlopen("http://localhost/n2o/novaMesura.php?"+line);
    #print resposta.read()
