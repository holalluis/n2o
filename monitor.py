import lectura as Lec
import time
import sys

'''Mostra continuament les dades del sensor sense registrar-les'''

while True:

	Lec.lectura()

	print("Ctrl-C per parar...")

	time.sleep(2)

	#esborra linies
	for i in range(5): sys.stdout.write("\033[F\033[K")
