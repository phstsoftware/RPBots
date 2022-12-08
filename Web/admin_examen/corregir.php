<?php
session_start();?>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<link rel="stylesheet" href="https://rpbots.000webhostapp.com/style.css" type="text/css" />
<script>
    function suma(){
        var sum = 0;
        $('.nota').each(function(){
            sum += parseFloat(this.value);
        });
        $('nota_t').val(sum);
    }
    
</script>
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
  .nota_pregunta{
    display: inline;
    float: right;
    }
</style>";
echo "<form action=\"corr_examen.php\" method=\"post\">";

$id_examen = $_GET["e"]; // cogemos el id del examen
$sql = "SELECT * FROM examen WHERE examen.id = " . $id_examen;
echo "<input type='hidden' name='id_examen' value='$id_examen' />";
echo "<input type='hidden' name='entidad' value=".$_GET["ent"]." />";
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
    $sql = "SELECT * FROM examen_asigna WHERE entidad = ".$_GET["ent"]." AND empleado = ".$_GET["d"]." AND examen = $id_examen";
    $result_p = $link->query($sql);
    $nota = -1;
    $info = ""; // en principio no sabemos nada
    if (!empty($result_p) AND mysqli_num_rows($result_p) > 0) {
       // output data of each row
       while($row_p=$result_p->fetch_assoc()) {
        $info = $row_p["info_adicional"];
        if($row_p["nota"] != -1) {
        $nota = "value = ".$row_p["nota"];
        }
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
    echo "<div style=\"float:right; display: inline\">";
    echo "<h2>Nota: </h2><input type=\"number\"  id=\"nota_t\"   min =0 max=10 step=0.01 placeholder=\"Nota\" $nota>";
    echo "</div>";
    echo "<p>A continuación, debe rellenar los siguientes campos con su información de contacto.</p>
    <p>(Todos los datos solicitados en este apartado y durante toda la prueba son IC)</p>";
    $sql = "SELECT * FROM empleados WHERE entidad = ".$_GET["ent"]." AND discord_id = ".$_GET["d"]."";
    $result = $link->query($sql);
    if (!empty($result) AND mysqli_num_rows($result) > 0) {
       // output data of each row
       while($row=$result->fetch_assoc()) {
            echo "<p><strong>Nombre y Apellidos (IC)</strong></p>";
            echo "<input type=\"text\" name=\"nombre\" id=\"nombre\" value=\"".$row['nombre']."\" disabled>";
            echo "<p><strong>Fecha de Nacimiento (IC)</strong></p>";
            echo "<input type=\"date\" name=\"nacimiento\" id=\"nacimiento\" value=\"".$row['Nacimiento']."\"  disabled>";
            echo "<p><strong>Nacionalidad (IC)</strong></p>";
            echo "<input type=\"text\" name=\"nacionalidad\" id=\"nacionalidad\"  value=\"".$row['Nacimiento']."\" disabled >";
            echo "<p><strong>Número de Teléfono (IC) </strong></p>";
            echo "<input type=\"text\" name=\"telefono\" id=\"telefono\" value=\"".$row['telefono']."\" disabled  >";
       }
    }
    
    echo "<p><strong>Estudios y experiencia con el mundo de la medicina (IC)</strong></p>";
    echo "<textarea name=\"experiencia\" rows=\"15\" cols=\"15\" style=\"width: 95%; margin:auto;\"  disabled>$info</textarea>";
    echo "</div><br>";
    echo "<div class=\"
    descriptionsContainer
    clearfix
    hp-section
    hp-policies-block
    \" style=\"font-size:14px; padding-top:0; padding-bottom:1.2em; width: 95%; margin: auto;\" id=\"hotelPoliciesInc\">";
    $sql = "SELECT * FROM respuestas WHERE empleado_entidad = ".$_GET["ent"]." AND empleado_discord = ".$_GET["d"]." AND examen = $id_examen";
    $result_resp = $link->query($sql);
    if (!empty($result_resp) AND mysqli_num_rows($result_resp) > 0) {
       // output data of each row
       while($row_res=$result_resp->fetch_assoc()) {
        // cargamos la respuesta
        $sql = "SELECT * FROM pregunta WHERE id = ".$row_res["pregunta"];
        $result_preg = $link->query($sql);
            if (!empty($result_preg) AND mysqli_num_rows($result_preg) > 0) {
            // output data of each row
                while($row_p=$result_preg->fetch_assoc()) {
                    // cargamos la pregunta
                    echo "<div class=\"
                    descriptionsContainer
                    clearfix
                    hp-section
                    hp-policies-block
                    \" style=\"font-size:14px; padding-top:0; padding-bottom:1.2em; width: 95%; margin: auto;\" id=\"hotelPoliciesInc\">";
                        echo "<p><strong>".$row_p["Pregunta"]."</strong></p>";
                        if($row_p["Tipo"] ==0){
                            echo "<div style=\"width:85%; float:left\">";
                            // si es de opción múltiple
                            $ok = random_int(0,$row_p["opcion_ko_num"]);
                            if($row_res["puntuacion"]==1){
                                // ha acertado
                                $acertado = true;
                            }else{
                                $respuesta = $row_res["texto"];
                                $acertado = false;
                            }
                            $_SESSION["ok_".$row_p["id"]]=$ok;
                            $ko = 1;
                            for ($i = 0; $i < ($row_p["opcion_ko_num"]+1); $i++) {
                                if($i == $ok){
                                    // es la correcta
                                    $pregunta = $row_p["opcion_ok"];
                                    $color = "color: green;";
                                }else{
                                    // no es la correcta
                                    $pregunta = $row_p["opcion_ko_$ko"];
                                    $ko ++;
                                    if(!$acertado && $respuesta == $pregunta){
                                        // es esta la que ha marcado
                                        $color = "color: red;";
                                    }else{
                                        $color = "";
                                    }
                                }
                               
                                echo "<p style='font-size:15px; margin-left: 5px;
                                display: inline-block;$color'><i class=\"fas fa-percent\"></i>".$pregunta." </p>";
                                
                                
                                echo "<hr>";
                                
                            }
                            echo "</div>";
                        }else if($row_p["Tipo"]==1){

                            echo "<textarea name=\"pregunta_".$row_p["id"]."\" rows=\"15\" cols=\"15\" style=\"width:85%; float:left; margin:auto;\"  disabled>".$row_res["texto"]."</textarea>";
                        }
                        if($row_res["puntuacion"]!=-1){
                            $val = "value=".$row_res["puntuacion"];
                        }else{
                            $val = "";
                        }
                        echo "<div class=\"nota_pregunta\" ><input type=\"number\" onkeyup=\"suma()\" name=\"nota_".$row_p["id"]."\" class=\"nota\" $val placeholder=\"Nota\" step=0.01 min=0 max=".$row_p["puntuacion_max"]."></div>";
                        echo "</div><br>";
                }
            }
       
       }
   }

    echo "<button style=\"width: 100%;
    height: 50px;


    color: #000;
    background-color: #fc0000;
    border-radius: 0.25rem;
    border-color: #fc0000;     margin-top: 15; color: white;
    font-size: 25px;\><input type=\"submit\"  value=\"\">Finalizar correccion</button>";
    echo "</form>";
    $sql = "SELECT servidores.nombre, servidores.logo FROM servidores WHERE servidores.id = (SELECT entidad.servidor FROM entidad WHERE entidad.id =  ".$_GET["ent"].")";
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
