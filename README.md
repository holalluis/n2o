# N2O : Sistema de Sensors + Arduino + Raspberry + MySQL

Última modificació: 6 octubre 2016, Lluís Bosch (lbosch@icra.cat)

Introducció
===========

Aquest paquet de software conté tot el codi necessari per fer funcionar un sistema de sensors i electrovàlvules connectats a un Arduino, 
i controlats per un Raspberry Pi. L'Arduino està contínuament llegint els sensors i enviant les dades al port serial (USB) del Raspberry Pi. 
L'usuari controla cada quan vol registrar les dades, i en quin ordre s'obren les 4 electrovàlvules.
A més, hi ha una web que permet visualitzar les dades i descarregar-les per un posterior anàlisi.

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

- __inici.sh__    : menú principal on es poden executar la resta de programes.
![](https://raw.githubusercontent.com/holalluis/n2o/master/gif/inici.gif)
- __info.py__     : Mostra breus instruccions per obrir la web i els crèdits del projecte.
- __manual.py__   : Permet obrir/tancar manualment les vàlvules utilizant comandes. Per exemple, la comanda "o1" obre la vàlvula 1.
- __monitor.py__  : Mostra de forma contínua l'estat del sistema (temperatura i pressió), sense registrar les dades:
![](https://raw.githubusercontent.com/holalluis/n2o/master/gif/monitor.gif)
- __sequencia.py__: Permet programar l'ordre d'obertura i tancament de vàlvules i registrar les dades a la base de dades.
Exemple d'arxiu "sequencia.txt":

```
# Seqüència de comandes 
# Sintaxi:
#    O{N}: Obre vàlvula N
#    T{N}: Tanca vàlvula N
#    E{N}: Espera N segons
O1
E5
T1
O2
E5
T2
```

- __sessio.py__     : Fa lectures cada X temps i les inserta a la base de dades, sense obrir ni tancar vàlvules.
- __veureDades.sh__ : mostra les 30 últimes dades insertades de les 4 campanes.

Web
===

Per veure i descarregar les dades en format CSV (excel) s'ha d'accedir a la web des d'un mòbil o un ordinador 
que estigui a la mateixa xarxa wifi que el Raspberry. La URL és:

  http://[ip-del-raspberry]/n2o/ (per exemple: http://192.168.102.200/n2o)

![](https://raw.githubusercontent.com/holalluis/n2o/master/gif/web.png)

Per saber la ip del Raspberry cal escriure la comanda `ifconfig` a la consola.
Els fitxers web s'han de colocar a la carpeta `/var/www/n2o`.
El fitxer `desplegaWeb.sh` serveix per copiar els fitxers a la carpeta /var/www/n2o (necessita permisos d'administrador).

Back-end (arxius de desenvolupament)
====================================

- __processa.py__ : funció que tradueix una trama de bytes de l'Arduino a valors llegibles.
- __registra.py__ : funció que registra una sola lectura a la base de dades.
- __virtual.py__  : funció que simula un arduino enviant trames.
- __envia.py__    : funció que envia una comanda (obrir/tancar vàlvula) a l'arduino.

## Codi Arduino (arduino/codi/src/sketch.ino)

Es pot modificar el fitxer `sketch.ino` des del mateix Raspberry utilitzant la comanda `ino` (http://inotool.org). Algunes comandes:

```
ino init #crea un nou projecte, i l'arxiu sketch.ino
ino build #compila l'arxiu sketch.ino
ino upload #carrega a l'arduino l'arxiu sketch.ino compilat
ino serial #mostra per pantalla el monitor serial de l'arduino. Per sortir: ctrl-a ctrl-x
```

Ino és ideal per treballar de forma remota (per exemple, a través de `ssh`)
Important: per Arduino Mega cal executar les comandes `build` i `upload` amb l'opció `-m mega2560` (veure documentacio a la web de ino):

```
ino build -m mega2560
```

Tambés es pot crear un fitxer `ino.ini`:

```
[build]
board-model = mega2560

[upload]
board-model = mega2560
```

## Base de dades MySQL

La base de dades es diu "n2o" i conté una única taula anomenada "mesures". 
Per veure les dades registrades sense fer servir la web (ús avançat):

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

Per obtenir la hora d'internet, es pot fer amb la comanda `ntpd` (network time protocol daemon):

```
sudo /etc/init.d/ntp stop
sudo ntpd -q-g
sudo /etc/init.d/ntp start
```

## Configuració Wifi Raspberry

El wifi del Raspberry es configura a l'arxiu `/etc/network/interfaces`:

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

## Com crear un fitxer csv fent servir la comanda `mysql`

```
echo "SELECT * FROM mesures WHERE id_campana=1;" | mysql -u root --password=raspberry -D n2o > campana1.csv;
```
