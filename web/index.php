<?php include 'mysql.php' ?>
<!doctype html><html><head>
	<meta charset=utf-8>
	<title>N2O</title>
	<style>
		*{margin:1px}
		body{
			font-family:Helvetica;
			font-size:14px;
			overflow-y:scroll;
		}
		h1{cursor:pointer}
		table{ 
			display:inline-block; 
			border-collapse:collapse;
			vertical-align:top;
		}
		td,th{
			border:1px solid #666;
			padding:5px;
		}
		th{
			background:lightblue;
			font-weight:normal;
		}
		#seleccionaCampana{
			padding:1em;
			background:#fafafa;
		}
	</style>
	<script>
		function exporta(campana)
		{
			//Agafa la taula id=taula
			var taula=document.querySelector('table[campana="'+campana+'"]');

			//string on escriurem l'arxiu csv
			var str="";

			//recorre la taula en loop (comença per la fila 2)
			for(var i=2; i<taula.rows.length; i++)
			{
				str += taula.rows[i].cells[0].textContent+'\t';
				str += taula.rows[i].cells[1].textContent+'\t';
				str += taula.rows[i].cells[2].textContent+'\t';
				str += taula.rows[i].cells[3].textContent+'\t';
				str += taula.rows[i].cells[4].textContent+'\t';
				str += '\r\n'
			}
			//genera link clickable
			var a         = document.createElement('a');
			a.href        = 'data:text/csv;charset=utf-8,'+encodeURI(str);
			a.target      = '_blank';
			a.download    = 'Campana'+campana+'.csv';
			//clica el link
			document.body.appendChild(a);
			a.click();
		}
	</script>
</head><body><center><!--titol--><h1 onclick=window.location='index.php'>Historial N<sub>2</sub>O</h1>

<h4>Nota: el sistema esborra automàticament dades més antigues de 10 mesos</h4>

<!--tria campana-->
<div id=seleccionaCampana>
Veure:
	<a href=index.php?campana=1>Campana 1</a> |
	<a href=index.php?campana=2>Campana 2</a> |
	<a href=index.php?campana=3>Campana 3</a> |
	<a href=index.php?campana=4>Campana 4</a> |
	<button onclick="window.location='reset.php'">Esborrar totes les dades de totes les campanes</button>
</div>

<!--DB SIZE-->
<table cellpadding=3 style="display:inline-block;vertical-align:top">
	<tr><th colspan=3>Base de dades
	<tr><th>Taula<th>Files<th>Tamany (MB)
	<?php
		$sql="	
				SELECT table_name,round(((data_length + index_length)/1024/1024),3) as 'size'
				FROM INFORMATION_SCHEMA.TABLES 
				WHERE table_schema='n2o' 
				ORDER BY TABLE_ROWS DESC
			";
		$res=mysql_query($sql) or die(mysql_error());
		$totalMB=0;
		$totalRows=0;
		while($row=mysql_fetch_array($res))
		{
			$table_name=$row['table_name'];
			$size=$row['size'];
			$rows=current(mysql_fetch_array(mysql_query("SELECT COUNT(*) FROM $table_name")));
			$totalMB+=$size;
			$totalRows+=$rows;
			echo "<tr>
				<td>$table_name
				<td align=right>$rows
				<td align=right>$size";
		}
		echo "<tr align=right><td><b>Total</b><td><b>$totalRows</b><td><b>$totalMB</b>";
	?>
</table>

<?php
	function campana($campana,$limit)
	{
		//dades mostrades
		$limit = isset($limit) ? $limit : 30;

		//dades totals campana
		$total=current(mysql_fetch_assoc(mysql_query("SELECT COUNT(1) FROM mesures WHERE id_campana=$campana")));

		//sobreescriu limit en cas que sigui més gran al total
		if($limit>$total)$limit=$total;

		echo "<table campana=$campana>";
		echo "<tr><th colspan=5>CAMPANA $campana";
		echo "
			<button onclick=exporta($campana) style=float:right>&rarr; CSV</button>
			";
		//menu per veure més dades i exportar
		echo "
			<tr><td colspan=5>
				<form method=GET action=index.php>
					<input name=campana type=hidden value=$campana>
					Veient últimes 
					<input name=limit value='$limit' style='width:30px' autocomplete=off>
					dades de $total
					<button type=submit>Veure</button>
				</form>
		";
		echo "<tr><th>Data<th>Temp (C)<th>Press (Pa)<th>Vol (L)<th>EV oberta";
		$sql="SELECT * FROM (
				SELECT * FROM mesures WHERE id_campana=$campana ORDER BY hora DESC LIMIT $limit
				) sub
				ORDER BY hora ASC
			";	
		$res=mysql_query($sql);
		while($row=mysql_fetch_array($res))
		{
			$hora		= $row['hora'];
			//
			// Si temperatura pressio o volum valen -1 vol dir que no hi ha dada disponible
			//
			$temperatura	= $row['temperatura']==-1 ? "<span style=color:red>N/A</span>" : $row['temperatura'];
			$pressio	= $row['pressio']==-1 	  ? "<span style=color:red>N/A</span>" : $row['pressio'];
			$volum		= $row['volum']==-1 	  ? "<span style=color:red>N/A</span>" : $row['volum'];
			$oberta		= $row['oberta'];
			echo "<tr>";
			echo "<td>$hora";
			echo "<td>$temperatura";
			echo "<td>$pressio";
			echo "<td>$volum";
			echo "<td>$oberta";
		}
		if(mysql_num_rows($res)==0)
			echo "<tr><td colspan=5 style='color:#666'>No hi ha dades";
		echo "</table><br>";
	}
?>

<?php
	if(isset($_GET['campana']))
	{
		$limit = isset($_GET['limit']) ? $_GET['limit'] : 10;
		campana($_GET['campana'],$limit);
	}
	else
		echo "<div style=padding:1em>Tria una campana</a>";
?>
