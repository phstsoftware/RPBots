<?php

include __DIR__.'/../connection.php';

$sql = "INSERT INTO pregunta (Pregunta,Tipo,puntuacion_max,banco) VALUES (\"".$_POST["Pregunta"]."\",".$_POST["Tipo"].",".$_POST["puntuacion_max"].",".$_POST["banco"].")";
$link->query($sql);
echo "
<script>
window.location.href = \"https://rpbots.000webhostapp.com/admin_examen/banco_preguntas.php?id=".$_POST["banco"]."\"; 
</script>
";
?>