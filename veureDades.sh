#!/bin/bash
echo "Base de dades n2o (MySQL)"
read -p "Usuari: " user
read -p "Password: " pass
read -p "Nº campana {1,2,3,4}: " campana

limit=30
echo "Estàs veient les $limit últimes dades"
echo "
	SELECT * FROM (
		SELECT * FROM mesures WHERE id_campana=$campana ORDER BY hora DESC LIMIT $limit 
	) sub
	ORDER BY hora ASC
	" | mysql -u $user --password=$pass -D n2o
