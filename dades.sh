#!/bin/bash
echo "Base de dades n2o (MySQL)"
read -p "Usuari: " user
read -p "Password: " pass
read -p "Nº campana {1,2,3,4}: " campana
echo "SELECT * FROM mesures WHERE id_campana=$campana;" | mysql -u $user --password=$pass -D n2o
