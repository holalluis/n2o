Última modificació: 20 de juliol 2016, Lluís Bosch (lbosch@icra.cat)
Arxiu per apuntar on són totes les coses importants

+============================+
| INDEX						 |
+============================+
|	* FITXERS WEB			 |
|	* ARXIU llegeixSerial.py |
|	* ARXIU guardarDades.sh  |
|	* COM CANVIAR LA HORA	 |
|	* CONFIGURACIÓ WIFI		 |
+============================+

* CODI ARDUINO
	** esta a la carpeta ~/codi_arduino
	** es pot modificar el codi de dues maneres:
		1. Obrint la interfície gràfica (startx) i executant la comanda arduino
		2. Des de la línia de comanda, utilitzant ino:
			ino init (crea l'arxiu sketch.ino)
			ino build (compila l'arxiu sketch.ino)
			ino upload (carrega a l'arduino l'arxiu compilat)
			ino serial (mostra per pantalla el monitor serial de l'arduino)
				per sortir: ctrl-a ctrl-x
			més info: inotool.org
			aquesta opció és ideal per treballar de forma remota
			important: per arduino mega 2560, cal fer build i upload amb la opcio -b mega2560 (veure documentacio a la web de ino)

* FITXERS WEB
	** estan a la carpeta:
		/var/www/n2o
	** per veure la web des d'un altre ordinador: 
		http://[ip del raspberry]/n2o/
		per exemple: http://192.168.102.193/n2o
	** per saber la ip:
		ifconfig
	** es veurà una cosa semblant a:
		wlan0   Link encap:Ethernet  HWaddr 00:b3:13:d1:25:ff
				inet addr: 192.168.102.193  Bcast:192.168.103.255  Mask:255.255.254.0

* BASE DE DADES
	es diu "n2o" i la taula es diu "mesures"
	per entrar al mysql:
		mysql -u root --password=raspberry -D n2o
	llavors un cop dins de mysql per llegir les dades (exemple: campana 3)
		SELECT * FROM mesures WHERE id_campana=3;
	i es veurà una taula com la següent
			id		id_campana	hora				temperatura	pressio	volum
			12079	3			2016-07-11 11:59:18	30			0		150
			12080	3			2016-07-11 12:09:19	30			-0.04	190
			12081	3			2016-07-11 12:19:21	30			0		160
			12082	3			2016-07-11 12:29:23	30			-0.04	120
			12083	3			2016-07-11 12:39:25	30			-0.04	170

* ARXIU llegeixSerial.py
	** arxiu que va escolta el que diu l'arduino i inserta les dades a la base de dades
	** per executar: 
		python llegeixSerial.py
	** per parar d'escoltar: 
		Ctrl+c

* ARXIU guardarDades.sh
	** Arxiu que anirà creant arxius CSV cada 8 hores
	** Els fitxers es guarden a la carpeta ~/Desktop/dades
	** Fitxers: campana1.csv, campana2.csv, campana3.csv i campana4.csv
	** per executar: 
		bash guardarDades.sh
	** per parar: 
		Ctrl+c

* Com canviar la hora (exemple)
	** Canviar la data al dia 28 de juliol de 2016 a les 18:40:00, fer:
		sudo date --set="2016-07-28 18:40:00"
	** Per obtenir la hora d'internet, es pot fer amb la companda ntpd (network time protocol daemon):
		sudo /etc/init.d/ntp stop
		sudo ntpd -q-g
		sudo /etc/init.d/ntp start

* CONFIGURACIÓ WIFI
	** Arxiu /etc/network/interfaces. Exemple:
		auto lo
		iface lo inet loopback
		iface eth0 inet dhcp
		auto wlan0
		allow-hotplug wlan0
		iface wlan0 inet dhcp
			wpa-ssid "ICRA"
			wpa-psk "#1wifi09icr@"
