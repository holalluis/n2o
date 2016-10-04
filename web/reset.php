
<?php
	include 'mysql.php';
	mysql_query("DELETE FROM mesures WHERE 1") or exit("error");
	header("Location: index.php");
?>

