<?php

include __DIR__.'/../connection.php';
$sql = "INSERT INTO bancos_preguntas (entidad) VALUES (".$_GET["e"].")";
$link->query($sql);
$sql = "INSERT INTO examen (entidad, Titulo, num_preguntas, banco_preguntas) VALUES (".$_GET["e"].",\"Nuevo examen\",5,".$link->insert_id.")";

$link->query($sql);

echo "
<script>
window.location.href = \"https://rpbots.000webhostapp.com/admin_examen/main.php?e=".$_GET["e"]."\"; 
</script>
";
?>