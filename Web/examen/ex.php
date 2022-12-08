<?php
session_start();?>
<link rel="stylesheet" href="https://rpbots.000webhostapp.com/style.css" type="text/css" />
<?php
include __DIR__.'/../connection.php';
echo "
<style>
  
  .hp-section {
      background: #ffb6b6;
      padding: 10px;
      margin: 0 0 20px 0;
      border-top: 1px solid #ebf3ff;
      border-bottom: 1px solid #ebf3ff;
      font-weight: normal;
      overflow: hidden;
      border-radius: 3px;
  }
  
</style>";
echo "<form action=\"examen_send.php\" method=\"post\">";

$sql = "SELECT examen FROM examen_asigna WHERE entidad = ".$_GET["e"]." AND empleado = ".$_GET["d"].""; // cogemos el examen
$id_examen = -1;
$result = $link->query($sql);
    if (!empty($result) AND mysqli_num_rows($result) > 0) {
       // output data of each row
       while($row=$result->fetch_assoc()) {
        $id_examen = $row["examen"]; // cogemos el id del examen
       }
}
$sql = "SELECT * FROM examen WHERE examen.id = " . $id_examen;
echo "<input type='hidden' name='id_examen' value='$id_examen' />";
echo "<input type='hidden' name='entidad' value=".$_GET["e"]." />";
echo "<input type='hidden' name='discord' value=".$_GET["d"]." />";
$num_preguntas = 0;
$banco = -1;

$logo = "https://static.wikia.nocookie.net/gtawiki/images/2/21/Lossantos_seal.png"; // si no hay logo
$result = $link->query($sql);
    if (!empty($result) AND mysqli_num_rows($result) > 0) {
       // output data of each row
       while($row=$result->fetch_assoc()) {
        
        $num_preguntas = $row["num_preguntas"];
        $banco = $row["banco_preguntas"];
        $sql_logo = "SELECT logo FROM entidad WHERE id = ".$row["entidad"]."";
        $result_logo = $link->query($sql_logo);
        if (!empty($result_logo) AND mysqli_num_rows($result_logo) > 0) {
            // output data of each row
            while($row_logo=$result_logo->fetch_assoc()) {
                $logo = $row_logo["logo"];
            }
        }
        echo "<img src=\"$logo\" style=\"width: 7%;
        margin: 10px;height:auto;float:right\">";
        echo "<h1>".$row["Titulo"]."</h1>";
       }
    }
    echo "<input type='hidden' name='preguntas' value=".$num_preguntas." />";
    echo "<input type='hidden' name='banco' value=".$banco." />";
    echo "<div class=\"
    descriptionsContainer
    clearfix
    hp-section
    hp-policies-block
    \" style=\"font-size:14px; padding-top:0; padding-bottom:1.2em; width: 95%; margin: auto;\" id=\"hotelPoliciesInc\">";
    echo "<p>A continuación, debe rellenar los siguientes campos con su información de contacto.</p>
    <p>(Todos los datos solicitados en este apartado y durante toda la prueba son IC)</p>";
    $sql = "SELECT nombre FROM empleados WHERE entidad = ".$_GET["e"]." AND discord_id = ".$_GET["d"]."";
    $result = $link->query($sql);
    if (!empty($result) AND mysqli_num_rows($result) > 0) {
       // output data of each row
       while($row=$result->fetch_assoc()) {
        echo "<p><strong>Nombre y Apellidos (IC)</strong></p>";
        echo "<input type=\"text\" name=\"nombre\" id=\"nombre\" value=\"".$row['nombre']."\" disabled>";
       }
    }
    echo "<p><strong>Fecha de Nacimiento (IC)</strong></p>";
    echo "<input type=\"date\" name=\"nacimiento\" id=\"nacimiento\"  required>";
    echo "<p><strong>Nacionalidad (IC)</strong></p>";
    echo "<input type=\"text\" name=\"nacionalidad\" id=\"nacionalidad\" required >";
    echo "<p><strong>Número de Teléfono (IC) </strong></p>";
    echo "<input type=\"text\" name=\"telefono\" id=\"telefono\" required  >";
    echo "<p><strong>Estudios y experiencia con el mundo de la medicina (IC)</strong></p>";
    echo "<textarea name=\"experiencia\" rows=\"15\" cols=\"15\" style=\"width: 95%; margin:auto;\"  required></textarea>";
    echo "</div><br>";
    echo "<div class=\"
    descriptionsContainer
    clearfix
    hp-section
    hp-policies-block
    \" style=\"font-size:14px; padding-top:0; padding-bottom:1.2em; width: 95%; margin: auto;\" id=\"hotelPoliciesInc\">";
    echo "<p><strong>Se procede a iniciar el examen, el departamento de instrucción le desea mucha suerte</strong></p></div><br>";
$sql = "SELECT * FROM pregunta WHERE banco = " .$banco ." ORDER BY RAND() LIMIT $num_preguntas";
$result = $link->query($sql);
    if (!empty($result) AND mysqli_num_rows($result) > 0) {
       // output data of each row
       while($row=$result->fetch_assoc()) {
        echo "<div class=\"
        descriptionsContainer
        clearfix
        hp-section
        hp-policies-block
        \" style=\"font-size:14px; padding-top:0; padding-bottom:1.2em; width: 95%; margin: auto;\" id=\"hotelPoliciesInc\">";
            echo "<p><strong>".$row["Pregunta"]."</strong></p>";
            if($row["Tipo"] ==0){
                // si es de opción múltiple
                $ok = random_int(0,$row["opcion_ko_num"]);
                $_SESSION["ok_".$row["id"]]=$ok;
                $ko = 1;
                for ($i = 0; $i < ($row["opcion_ko_num"]+1); $i++) {
                    if($i == $ok){
                        // es la correcta
                        $pregunta = $row["opcion_ok"];
                    }else{
                        // no es la correcta
                        $pregunta = $row["opcion_ko_$ko"];
                        $ko ++;
                    }
                    echo "<label style=\"width: 100%;\"><input type=\"radio\" value=\"$i\" name=\"pregunta_".$row["id"]."\" id=\"pregunta_".$row["id"]."\" >";
                    echo "<p style='font-size:15px; margin-left: 5px;
                    display: inline-block;'><i class=\"fas fa-percent\"></i>".$pregunta." </p>";
                    
                    
                    echo "<hr>";
                    echo "</input></label>";
                }
            }else if($row["Tipo"]==1){
                echo "<textarea name=\"pregunta_".$row["id"]."\" rows=\"15\" cols=\"15\" style=\"width: 95%; margin:auto;\"  required></textarea>";
            }
            echo "</div><br>";
       }
   }
   echo "<p>Entregando este examen usted es consciente de la existencia de mecanismos de detección del plagio y usted afirma que las respuestas que aquí constan son fruto de su conocimiento.</p>";

echo "<button style=\"width: 100%;
height: 50px;


color: #000;
background-color: #fc0000;
border-radius: 0.25rem;
border-color: #fc0000;     margin-top: 15; color: white;
font-size: 25px;\><input type=\"submit\"  value=\"\">Entregar el examen</button>";
echo "</form>";
$sql = "SELECT servidores.nombre, servidores.logo FROM servidores WHERE servidores.id = (SELECT entidad.servidor FROM entidad WHERE entidad.id =  ".$_GET["e"].")";
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