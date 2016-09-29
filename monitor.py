#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Mostra continuament les dades del sensor sense registrar-les'''
import lectura as Lec
import time
import sys

while True:

	Lec.lectura() #mostra les dades instantànies

	print("Ctrl-C per parar...")

	time.sleep(2)

	#esborra linies
	for i in range(5): sys.stdout.write("\033[F\033[K")
