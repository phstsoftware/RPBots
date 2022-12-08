<?php

include __DIR__.'/../connection.php';
$id_examen = $_POST["id_examen"];
$nota = 0;
$sql = "SELECT * FROM respuestas WHERE empleado_entidad = ".$_POST["entidad"]." AND empleado_discord = ".$_POST["discord"]." AND examen = $id_examen";
$result_resp = $link->query($sql);
    if (!empty($result_resp) AND mysqli_num_rows($result_resp) > 0) {
       // output data of each row
       while($row_res=$result_resp->fetch_assoc()) {
        $update = "UPDATE respuestas SET puntuacion = ".$_POST["nota_".$row_res["pregunta"].""]." WHERE pregunta = ".$row_res["pregunta"]." AND empleado_entidad = ".$_POST["entidad"]." AND empleado_discord = ".$_POST["discord"]." AND examen = $id_examen";
        $link->query($update);
        $nota += $_POST["nota_".$row_res["pregunta"].""];
       }
    }
    $sql = "UPDATE examen_asigna SET nota=".$nota." WHERE entidad = ".$_POST["entidad"]." AND empleado = ".$_POST["discord"]." AND examen = $id_examen";
    $link->query($sql);
    echo "
<script>
window.location.href = \"https://rpbots.000webhostapp.com/admin_examen/main.php?e=".$_POST["entidad"]."\"; 
</script>
";