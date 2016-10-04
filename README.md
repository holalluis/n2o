# N2O : Sistema de Sensors + Arduino + Raspberry + MySQL

Última modificació: 4 octubre 2016, Lluís Bosch (lbosch@icra.cat)

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


L'Arduino està CONTÍNUAMENT ENVIANT DADES AL PORT SERIAL del Raspberry Pi. El Raspberry Pi processa les dades cada X temps, 
i si l'usuari vol, les emmagatzema a la base de dades

Programes
=========

1. monitor.py  : mostra contínuament les dades sense registrar-les a la base de dades. Veure animació:
![](https://raw.githubusercontent.com/holalluis/n2o/master/gif/monitor.gif)
2. manual.py   : permet obrir/tancar les vàlvules. Pe exemple, "o1" obre la vàlvula 1

(falta gif animat)

3. sessio.py   : fa lectures contínuament (cada X temps) i les inserta a la base de dades

(falta gif animat)

Web
===

Per veure les dades i descarregar-les en format CSV s'ha d'accedir a la web dins el raspberry des d'un mòbil o ordinador 
que estigui a la mateixa xarxa wifi que el Raspberry. Escriure al navegador:

http://[ip-del-raspberry]/n2o/ (per exemple: http://192.168.102.200/n2o)

(falta imatge)

Per saber la ip ("inet addr"): executar la comanda ifconfig a la consola
Els fitxers de la web estan a la carpeta web/ i dins el Raspberry han de ser a la carpeta /var/www/n2o.
Per veure la web des d'un altre ordinador (o el mòbil): 

Back-end (arxius de desenvolupament)
====================================

1. processa.py : funció que tradueix una trama de bytes de l'Arduino a valors llegibles
2. registra.py : funció que registra una sola lectura a la base de dades 
3. virtual.py  : funció que simula un arduino enviant trames

## Codi Arduino (arxiu arduino/nodegasos.ino)

Es pot modificar el codi des del raspberry utilitzant ino (http://inotool.org). Algunes comandes:

```
ino init #crea l'arxiu sketch.ino
ino build #compila l'arxiu sketch.ino
ino upload #carrega a l'arduino l'arxiu compilat
ino serial #mostra per pantalla el monitor serial de l'arduino
          #per sortir: ctrl-a ctrl-x
```
Aquesta opció és ideal per treballar de forma remota. Important: per arduino mega 2560, cal fer build i upload amb la opcio -b mega2560 (veure documentacio a la web de ino)

```
ino build -b mega2560
```

## Base de dades MySQL

La base de dades Es diu "n2o" i conté una única taula anomenada "mesures" {id,id_campana,hora,temperatura,pressio,volum,oberta}
Per entrar al mysql:

```
$ mysql -u root --password=raspberry -D n2o
>>> SELECT * FROM mesures WHERE id_campana=3;
+-------+------------+---------------------+-------------+---------+-------+--------+
| id    | id_campana | hora                | temperatura | pressio | volum | oberta |
+-------+------------+---------------------+-------------+---------+-------+--------+
| 12079 | 1          | 2016-07-11 11:59:18 | 24          | 0       | 150   | 1      |
| 12080 | 2          | 2016-07-11 12:09:19 | 23          | -0.04   | 190   | 0      |
| 12081 | 3          | 2016-07-11 12:19:21 | 24          | 0       | 160   | 0      |
| 12082 | 4          | 2016-07-11 12:29:23 | 25          | -0.04   | 120   | 0      |
| 12083 | 1          | 2016-07-11 12:39:25 | 26          | -0.04   | 170   | 1      |
| ...   | ...        | ...                 | ...         | ...     | ...   | ...    |
```

## Com canviar la hora del Raspberry (exemple)

La hora està en UTC (així evitem problemes de canvi horari)
Per canvia la data al dia 28 de juliol de 2016 a les 18:40:00, fer:

```
sudo date --set="2016-07-28 18:40:00"
```

Per obtenir la hora d'internet, es pot fer amb la companda ntpd (network time protocol daemon):

```
sudo /etc/init.d/ntp stop
sudo ntpd -q-g
sudo /etc/init.d/ntp start
```

## Configuració Wifi Raspberry

Es configura a l'arxiu /etc/network/interfaces:

```
auto lo
iface lo inet loopback
iface eth0 inet dhcp
auto wlan0
allow-hotplug wlan0
iface wlan0 inet dhcp
  wpa-ssid "ICRA"
  wpa-psk "#1wifi09icr@"
```

## Com crear un fitxer csv fent servir la comanda "mysql"

```
echo "SELECT * FROM mesures WHERE id_campana=1;" | mysql -u root --password=raspberry -D n2o > campana1.csv;
```

vim:ts=2:sw=2:expandtab:ft=help:norl:
