+=====+==================================================+
| N2O | Sistema de Sensors + Arduino + Raspberry + MySQL |
+=====+==================================================+

Última modificació: 30 de setembre 2016, Lluís Bosch (lbosch@icra.cat)

Idea General:

 Tª +---------+    +---------+
 P  | Sensors |--->|         |
 V  +---------+    |         |       +-----------+
                   | Arduino |<----->| Raspberry |<-----USUARI
                   | Mega    |       | Pi        |
   +----------+    |         |       +-----------+
   | Vàlvules |<---|         |
   +----------+    |         |
                   +---------+


L'Arduino està CONTÍNUAMENT ENVIANT DADES AL PORT SERIAL del Raspberry Pi

El Raspberry Pi processa les dades cada X temps, i si l'usuari vol, les emmagatzema a una base de dades MySQL

 Arxius Python: "Mòduls" (controlables per l'usuari)
===============

1. monitor.py  : mostra contínuament les dades sense registrar-les a la base de dades
2. sessio.py   : fa lectures contínuament i les inserta a la base de dades
3. lectura.py  : funció que llegeix la primera trama disponible i ho mostra
4. registra.py : funció que registra una sola lectura a la bbdd 
5. processa.py : tradueix una trama de bytes de l'Arduino a JSON


 Altres arxius
===============

+=============================+
| INDEX                       |
+=============================+
| * CODI ARDUINO              |
| * FITXERS WEB               |
| * BASE DE DADES MYSQL       |
| * COM CANVIAR LA HORA       |
| * CONFIGURACIÓ WIFI         |
| * COM CREAR UN CSV DE MYSQL |
+=============================+

* CODI ARDUINO (nodeGasos.ino)
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

* BASE DE DADES MYSQL
	es diu "n2o" i la taula es diu "mesures"
	per entrar al mysql:
		mysql -u root --password=raspberry -D n2o
	llavors un cop dins de mysql per llegir les dades (exemple: campana 3)
		SELECT * FROM mesures WHERE id_campana=3;
	i es veurà una taula com la següent:
	
	id	id_campana	hora			temperatura	pressio	volum
	12079	3		2016-07-11 11:59:18	30		0	150
	12080	3		2016-07-11 12:09:19	30		-0.04	190
	12081	3		2016-07-11 12:19:21	30		0	160
	12082	3		2016-07-11 12:29:23	30		-0.04	120
	12083	3		2016-07-11 12:39:25	30		-0.04	170

* COM CANVIAR LA HORA (EXEMPLE)
	** LA HORA ESTÀ EN UTC (així evitem problemes de canvi horari)
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

* COM CREAR UN FITXER CSV DES DE MYSQL
	echo "SELECT * FROM mesures WHERE id_campana=1;" | mysql -u root --password=raspberry -D n2o > campana1.csv;
