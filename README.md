# N2O : Sistema de Sensors + Arduino + Raspberry + MySQL

Última modificació: 5 octubre 2016, Lluís Bosch (lbosch@icra.cat)

Idea General (esquema)
======================

L'Arduino està contínuament llegint les dades dels sensors i enviant-les al port serial (USB) del Raspberry Pi. Aquest, processa les dades cada X temps, 
i si l'usuari vol, les emmagatzema a una base de dades.


     +---------+   +---------+
     | Sensors |-->|         |
     +---------+   |         |     +-----------+
                   | Arduino |<--->| Raspberry |<---USUARI
    +----------+   | Mega    |     | Pi        |
    | Vàlvules |<--|         |     +-----------+
    +----------+   |         |
                   +---------+


Programes
=========

- monitor.py  : mostra contínuament les dades sense registrar-les a la base de dades. Veure animació:
![](https://raw.githubusercontent.com/holalluis/n2o/master/gif/monitor.gif)

- manual.py   : permet obrir/tancar les vàlvules. Per exemple, la comanda "o1" obre la vàlvula 1.

(falta gif animat)

- sessio.py   : fa lectures contínuament (cada X temps) i les inserta a la base de dades.

(falta gif animat)

Web
===

Per veure les dades i poder descarregar-les en format CSV (excel) s'ha d'accedir a la web creada dins el Raspberry des d'un mòbil o un ordinador 
que estigui a la mateixa xarxa wifi que el Raspberry. La URL serà:

  http://[ip-del-raspberry]/n2o/ (per exemple: http://192.168.102.200/n2o)

(falta imatge)

Per saber la ip del Raspberry ("inet addr"), cal executar la comanda ifconfig a la consola.
Els fitxers de la web estan a la carpeta web/ però dins el Raspberry han de ser a la carpeta /var/www/n2o.
Si es fa una modificació a la web, el fitxer "web/desplegaWeb.sh" serveix per copiar 
els fitxers a la carpeta correcta (necessita permisos d'administrador).

Back-end (arxius de desenvolupament)
====================================

## Altres arxius Python

- processa.py : funció que tradueix una trama de bytes de l'Arduino a valors llegibles
- registra.py : funció que registra una sola lectura a la base de dades 
- virtual.py  : funció que simula un arduino enviant trames

## Codi Arduino (arxiu arduino/nodegasos.ino)

Es pot modificar el codi Arduino des del mateix Raspberry utilitzant la comanda ino (http://inotool.org). Algunes comandes:

```
ino init #crea un nou projecte, i l'arxiu sketch.ino
ino build #compila l'arxiu sketch.ino
ino upload #carrega a l'arduino l'arxiu sketch.ino compilat
ino serial #mostra per pantalla el monitor serial de l'arduino. Per sortir: ctrl-a ctrl-x
```

Aquesta opció és ideal per treballar de forma remota. 
Important: per arduino mega 2560, cal fer build i upload amb la opcio -m mega2560 (veure documentacio a la web de ino):

```
ino build -m mega2560
```

## Base de dades MySQL

La base de dades es diu "n2o" i conté una única taula anomenada "mesures" {id,id_campana,hora,temperatura,pressio,volum,oberta}
Per entrar al mysql sense fer servir la web (ús avançat):

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

La hora del Raspberry (i per tant, de la base de dades) està en UTC (així evitem problemes de canvi horari)
Per canviar la data al dia 28 de juliol de 2016 a les 18:40:00, cal executar:

```
sudo date --set="2016-07-28 18:40:00"
```

Per obtenir la hora d'internet, es pot fer amb la comanda ntpd (network time protocol daemon):

```
sudo /etc/init.d/ntp stop
sudo ntpd -q-g
sudo /etc/init.d/ntp start
```

## Configuració Wifi Raspberry

El wifi del Raspberry es configura a l'arxiu /etc/network/interfaces:

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
