<?php

include __DIR__.'/../connection.php';
if($_POST["submit"]=="Guardar"){
if(isset($_POST["opcion_ok"])){
    $opciones = "";
    for ($i = 0; $i < ($_POST["opcion_ko_num"]+1); $i++) {
        if($i == 0){
            $opciones .= " opcion_ok = \"".$_POST["opcion_ok"]."\",";
        }else{
            $opciones .= "opcion_ko_$i = \"".$_POST["opcion_ko_$i"]."\",";
        }
    }
    
}else{
    $opciones = "opcion_ko_num = 3,";
}

    $sql = "UPDATE pregunta SET Pregunta = \"".$_POST["Pregunta"]."\", $opciones Tipo=\"".$_POST["Tipo"]."\" WHERE id= ".$_POST["pregunta"]." ";
}else{
    //vamos a borrarla
    $sql = "DELETE FROM pregunta WHERE id= ".$_POST["pregunta"]." ";
}
    $link->query($sql);
    echo "
<script>
window.location.href = \"https://rpbots.000webhostapp.com/admin_examen/banco_preguntas.php?id=".$_POST["banco"]."\"; 
</script>
";

?>