#!/bin/bash

if (($#<1)); then echo "Ús: $0 campana"; exit; fi

echo "SELECT * FROM mesures WHERE id_campana=$1;" | mysql -u root --password=raspberry -D n2o
