<?php
session_start();?>
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
    </style>
    <script>
        function atras(){
            window.location.href = "https://rpbots.000webhostapp.com/admin_examen/main.php?e=<?php echo $_GET["e"]?>"; 

        }
        </script>
<link rel="stylesheet" href="https://rpbots.000webhostapp.com/style.css" type="text/css" />
<button onclick="atras()">Atrás</button>
<?php
echo "<h1>Banco de preguntas #" .$_GET["id"] ."</h1>";
include __DIR__.'/../connection.php';
$id = 0;
$sql = "SELECT * FROM pregunta WHERE banco = " .$_GET["id"] ."";
$result = $link->query($sql);
    if (!empty($result) AND mysqli_num_rows($result) > 0) {
       // output data of each row
       while($row=$result->fetch_assoc()) {
        $id = $row["id"];
        echo "<div class=\"
        descriptionsContainer
        clearfix
        hp-section
        hp-policies-block
        \" style=\"font-size:14px; padding-top:0; padding-bottom:1.2em; width: 95%; margin: auto;\" id=\"hotelPoliciesInc\">";
        echo "<form action=\"pregunta_edit.php\" method=\"post\">";

        echo "<input type=\"hidden\" name=\"banco\" value=\"".$_GET["id"]."\" />";
        echo "<input type=\"hidden\" name=\"pregunta\" value=\"".$row["id"]."\" />";
            echo "<p>Pregunta #".$row["id"]."</p><input type=\"submit\" name=\"submit\" id=\"submit\"  value=\"Eliminar\" /><br><textarea name=\"Pregunta\" style=\"width:90%\" id=\"Pregunta\">".$row["Pregunta"]."</textarea><br>";
            
            echo "<table><tr><th>Tipo de pregunta</th><th>Puntuación máxima</th></tr>
            <tr><td><select name=\"Tipo\" id=\"Tipo\">
            <option value=\"0\"";
            if($row["Tipo"] ==0){
                echo "selected";
            }
            echo ">Opción Múltiple</option>
            <option value=\"1\"";
            if($row["Tipo"] ==1){
                echo "selected";
            }
            echo ">Desarrollar</option>
            </select></td><td><input type=\"number\" name=\"puntuacion_max\" value=".$row["puntuacion_max"]."></td></tr></table>";
            if($row["Tipo"] ==0){
                // si es de opción múltiple
                echo "<input type=\"hidden\" name=\"opcion_ko_num\" value=".$row["opcion_ko_num"]." />";
                for ($i = 0; $i < ($row["opcion_ko_num"]+1); $i++) {
                    if($i == 0){
                        // es la correcta
                        $pregunta = $row["opcion_ok"];
                        $nombre = "opcion_ok";
                        $style = "color:green;";
                    }else{
                        // no es la correcta
                        $pregunta = $row["opcion_ko_$i"];
                        $nombre = "opcion_ko_$i";
                        $style = "color:red;";
                        
                    }
                    echo "<input type=\"text\" style=\"width:90%;$style\" value=\"$pregunta\" name=\"$nombre\" id=\"$nombre\" ><br>";
                    
                    
                    
                    
                    
                }
            }else if($row["Tipo"]==1){
               // no hace falta poner nada
            }
            echo "<input type=\"submit\" name=\"submit\" id=\"submit\" value=\"Guardar\" />";
            echo "</form></div><br>";
       
       }
    }
    echo "<div class=\"
        descriptionsContainer
        clearfix
        hp-section
        hp-policies-block
        \" style=\"font-size:14px; padding-top:0; padding-bottom:1.2em; width: 95%; margin: auto;     background: #ffd6d6;\" id=\"hotelPoliciesInc\">";
        echo "<form action=\"pregunta_create.php\" method=\"post\">";
        echo "<input type=\"hidden\" name=\"banco\" value=\"".$_GET["id"]."\" />";
            echo "<p>Nueva pregunta</p><textarea name=\"Pregunta\" style=\"width:90%\" id=\"Pregunta\" placeholder=\"Escriba aquí la pregunta\"></textarea><br>";
            echo "<table><tr><th>Tipo de pregunta</th><th>Puntuación máxima</th></tr>
            <tr><td><select name=\"Tipo\" id=\"Tipo\">
            <option value=\"0\"";
            
            echo ">Opción Múltiple</option>
            <option value=\"1\"";
            
            echo ">Desarrollar</option>
            </select></td><td><input type=\"number\" name=\"puntuacion_max\" id=\"puntuacion_max\" required></td></tr></table>";
            echo "<input type=\"submit\" value=\"crear\">";
            echo "</form></div><br>";
       
?>