<?php
session_start();
include __DIR__.'/../connection.php';
// procedemos a tratar las respuestas para mandarlas al servidor
$sql = "SELECT * FROM pregunta WHERE banco = " .$_POST["banco"];
$result = $link->query($sql);
    if (!empty($result) AND mysqli_num_rows($result) > 0) {
       // output data of each row
       while($row=$result->fetch_assoc()) {
        if(isset($_POST["pregunta_".$row["id"].""])){
            // básicamente si existe la pregunta
            if($row["Tipo"] ==0){
                // si es de opción múltiple
                $ok = $_SESSION["ok_".$row["id"]];
                if($_POST["pregunta_".$row["id"]] == $ok){
                    // es la respuesta correcta
                    $puntuacion = $row["puntuacion_max"];
                    $respuesta = $row["opcion_ok"];
                }else{
                    $puntuacion = 0; // está incorrecta
                    $respuesta = $_POST["pregunta_".$row["id"]];
                }
                
            }else if($row["Tipo"]==1){
                // no sabemos hasta que se corriga manualmente
                $puntuacion = -1;
                $respuesta = $_POST["pregunta_".$row["id"]];
            }
            $sql_insert = "INSERT INTO respuestas (examen, pregunta, puntuacion, texto, empleado_discord, empleado_entidad) VALUES (
                ".$_POST["id_examen"].",".$row["id"].",$puntuacion,\"$respuesta\",".$_POST["discord"].",".$_POST["entidad"].")";
            $link->query($sql_insert);  
        }
       }

    }
    $sql = "UPDATE examen_asigna SET info_adicional =\"".$_POST["experiencia"]."\" WHERE examen = ".$_POST["id_examen"]." AND entidad = ".$_POST["entidad"]." AND empleado = ".$_POST["discord"]."";

    $link->query($sql);  
    $sql = "UPDATE empleados SET telefono = \"".$_POST["telefono"]."\" , Nacionalidad = \"".$_POST["nacionalidad"]."\", Nacimiento =\"".$_POST["nacimiento"]."\" WHERE entidad = ".$_POST["entidad"]." AND discord_id = ".$_POST["discord"]."";
   
    $link->query($sql);  

    
?>
<h1>Su respuesta ha sido registrada con éxito</h1>
<p>El departamento de formación le informa que en el plazo de 2 o 3 días recibirá el resultado del examen </p>
<?php
$sql = "SELECT servidores.nombre, servidores.logo FROM servidores WHERE servidores.id = (SELECT entidad.servidor FROM entidad WHERE entidad.id =  ".$_POST["entidad"].")";
$result = $link->query($sql);
    if (!empty($result) AND mysqli_num_rows($result) > 0) {
       // output data of each row
       while($row=$result->fetch_assoc()) {
        echo "<table style=\"border: 0px solid\"><tr><td style=\"border: 0px solid\"><img src=\"".$row["logo"]."\" style=\"
        margin: 10px;height:25px;float:left\">";
        echo "</td><td style=\"border: 0px solid\"><p style=\"font-size: 12px;\">Desarrollado por RPBots para ".$row["nombre"]."</p></td></tr></table>";
       }
    }
?>