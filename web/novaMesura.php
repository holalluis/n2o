<?php
/* CREA UNA NOVA MESURA */

include 'mysql.php';

//entrada
$campana=$_GET['campana'];

if(isset($_GET['t'])) $t=$_GET['t']; else $t=-1; //temperatura
if(isset($_GET['p'])) $p=$_GET['p']; else $p=-1; //pressio
if(isset($_GET['v'])) $v=$_GET['v']; else $v=-1; //volum
if(isset($_GET['e'])) $e=$_GET['e']; else $e=0;  //electrovalvula oberta

//executa
echo "Registrant lectura (c=$campana,t=$t,p=$p,v=$v,e=$e)... ";
$sql ="INSERT INTO mesures (id_campana,hora,temperatura,pressio,volum,oberta) ";
$sql.="VALUES ($campana,CURRENT_TIMESTAMP,$t,$p,$v,$e)";
mysql_query($sql) or exit('error');
echo "Ok!";
?>
