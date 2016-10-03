+========================================================+
| N2O : Sistema de Sensors + Arduino + Raspberry + MySQL |
+========================================================+

Última modificació: 1 octubre 2016, Lluís Bosch (lbosch@icra.cat)

Idea General (esquema)
======================

     +---------+   +---------+
     | Sensors |-->|         |
     +---------+   |         |     +-----------+
                   | Arduino |<--->| Raspberry |<---USUARI
    +----------+   | Mega    |     | Pi        |
    | Vàlvules |<--|         |     +-----------+
    +----------+   |         |
                   +---------+


L'Arduino està CONTÍNUAMENT ENVIANT DADES AL PORT SERIAL del Raspberry Pi

El Raspberry pot donar la ordre de obrir i tancar les Vàlvules amb les ordres "O" i "T" (exemple: 'O1' obre la vàlvula 1)

El Raspberry Pi processa les dades cada X temps, i si l'usuari vol, les emmagatzema a una base de dades MySQL

Programes
=========

1. monitor.py  : mostra contínuament les dades sense registrar-les a la base de dades
2. manual.py   : permet obrir i tancar les vàlvules. Per exemple, la comanda "o1" obre la vàlvula 1
3. sessio.py   : fa lectures contínuament (cada X temps) i les inserta a la base de dades

Back-end
========
1. processa.py : funció que tradueix una trama de bytes de l'Arduino a JSON
2. registra.py : funció que registra una sola lectura a la base de dades 
3. virtual.py  : funció que simula un arduino enviant trames

+-----------------------------+
| Altres arxius               |
+-----------------------------+
| * CODI ARDUINO              |
| * FITXERS WEB               |
| * BASE DE DADES MYSQL       |
| * COM CANVIAR LA HORA       |
| * CONFIGURACIÓ WIFI         |
| * COM CREAR UN CSV DE MYSQL |
+-----------------------------+

* CODI ARDUINO (arduino/nodeGasos.ino)
	** es pot modificar el codi des del raspberry:
		*** Utilitzant ino (http://inotool.org):
      Algunes comandes:
        ino init (crea l'arxiu sketch.ino)
        ino build (compila l'arxiu sketch.ino)
        ino upload (carrega a l'arduino l'arxiu compilat)
        ino serial (mostra per pantalla el monitor serial de l'arduino)
          per sortir: ctrl-a ctrl-x
			més info: inotool.org
			aquesta opció és ideal per treballar de forma remota
			important: per arduino mega 2560, cal fer build i upload amb la opcio -b mega2560 (veure documentacio a la web de ino)

* FITXERS WEB
	** estan a la carpeta /var/www/n2o
	** per veure la web des d'un altre ordinador: 
		http://ip-del-raspberry/n2o/
		per exemple: http://192.168.102.200/n2o
	** per saber la ip ("inet addr"):
		ifconfig

* BASE DE DADES MYSQL
	Es diu "n2o" i dins hi ha una sola taula anomenada 
  "mesures" {id,id_campana,hora,temperatura,pressio,volum}
	per entrar al mysql:
		mysql -u root --password=raspberry -D n2o
	llavors un cop dins de mysql, podem enviar comandes MySQL, per exemple:
		SELECT * FROM mesures WHERE id_campana=3;
	i es veurà una taula com la següent:
	
  MESURES:
  +-------+------------+----------------------+-------------+---------+-------+
  | id    | id_campana | hora                 | temperatura | pressio | volum |
  +-------+------------+----------------------+-------------+---------+-------+
  | 12079 | 1          | 2016-07-11 11:59:18  | 24          | 0       | 150   |
  | 12080 | 2          | 2016-07-11 12:09:19  | 23          | -0.04   | 190   |
  | 12081 | 3          | 2016-07-11 12:19:21  | 24          | 0       | 160   |
  | 12082 | 4          | 2016-07-11 12:29:23  | 25          | -0.04   | 120   |
  | 12083 | 1          | 2016-07-11 12:39:25  | 26          | -0.04   | 170   |
  | ...   | ...        | ...                  | ...         | ...     | ...   |

* COM CANVIAR LA HORA (EXEMPLE)
	** LA HORA ESTÀ EN UTC (així evitem problemes de canvi horari)
	** Canviar la data al dia 28 de juliol de 2016 a les 18:40:00, fer:
		sudo date --set="2016-07-28 18:40:00"
	** Per obtenir la hora d'internet, es pot fer amb la companda ntpd (network time protocol daemon):
		sudo /etc/init.d/ntp stop
		sudo ntpd -q-g
		sudo /etc/init.d/ntp start

* CONFIGURACIÓ WIFI
	** Arxiu /etc/network/interfaces:
      auto lo
      iface lo inet loopback
      iface eth0 inet dhcp
      auto wlan0
      allow-hotplug wlan0
      iface wlan0 inet dhcp
        wpa-ssid "ICRA"
        wpa-psk "#1wifi09icr@"

* COM CREAR UN FITXER CSV DES DE MYSQL (des de bash)
	echo "SELECT * FROM mesures WHERE id_campana=1;" | mysql -u root --password=raspberry -D n2o > campana1.csv;

*No modificar aquesta línia
vim:ts=2:sw=2:expandtab:ft=help:norl:
