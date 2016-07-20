#!/bin/bash
# crea un fitxer CSV des de la base de dades cada x temps

#carpeta on es guardaran els fitxers CSV
carpeta="Desktop/dades"

#bucle infinit (fins que s'apreti ctrl-c)
while :;
do
	echo "[$(date)]: Guardant dades...";

	echo "	Guardant $carpeta/campana1.csv";
	echo "SELECT * FROM mesures WHERE id_campana=1;" | mysql -u root --password=raspberry -D n2o > $carpeta/campana1.csv;
	echo "	Guardant $carpeta/campana2.csv";
	echo "SELECT * FROM mesures WHERE id_campana=2;" | mysql -u root --password=raspberry -D n2o > $carpeta/campana2.csv;
	echo "	Guardant $carpeta/campana3.csv";
	echo "SELECT * FROM mesures WHERE id_campana=3;" | mysql -u root --password=raspberry -D n2o > $carpeta/campana3.csv;
	echo "	Guardant $carpeta/campana4.csv";
	echo "SELECT * FROM mesures WHERE id_campana=4;" | mysql -u root --password=raspberry -D n2o > $carpeta/campana4.csv;

	#espera x temps
	echo "Esperant 8 hores... ";
	sleep 28800 #seconds: 8 hores
done
