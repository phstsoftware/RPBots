<?php

include __DIR__.'/../connection.php';

$sql = "UPDATE examen SET Titulo=\"".$_POST["Titulo"]."\", num_preguntas = ".$_POST["num_preguntas"]." WHERE examen=".$_POST["id"]."";
$link->query($sql);
if(isset($_POST["asignado_nuevo"])&&$_POST["asignado_nuevo"]!="null"){
    // hay que asignarlo a alguien
    $sql = "INSERT INTO examen_asigna(empleado, examen, entidad) VALUES (".$_POST["asignado_nuevo"].",".$_POST["id"].",".$_POST["entidad"].")";
    $link->query($sql);
}
echo "
<script>
window.location.href = \"https://rpbots.000webhostapp.com/admin_examen/main.php?e=".$_POST["entidad"]."\"; 
</script>
";
?>