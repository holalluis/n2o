#!/bin/bash

read -p "Nº campana {1,2,3,4}: " campana

echo "SELECT * FROM mesures WHERE id_campana=$campana;" | mysql -u root --password=raspberry -D n2o

