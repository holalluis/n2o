#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Instruccions per accedir a la web'''
import os
comanda="ifconfig wlan0 | grep 'inet addr'| awk '{print $2}'|cut -d\: -f2"
ip=os.popen(comanda).read().replace('\n','')
print "---Instruccions per accedir a la web per veure les dades---"
print "1. Connectat a la mateixa xarxa que el Raspberry Pi."
print "2. Entra a: http://%s/n2o" % ip
print "3. Dins la web et podràs descarregar les dades en format csv\n"
