<?php
session_start();?>
<link rel="stylesheet" href="https://rpbots.000webhostapp.com/style.css" type="text/css" />
<?php
include __DIR__.'/../connection.php';

echo "<h1>Exámenes creados</h1>";
echo "<a href=\"https://rpbots.000webhostapp.com/?e=".base64_encode($_GET["e"])."&t=1656361271.4050398&admin=1\" >Menú principal</a>";
echo "<table>";
echo "<tr>";
echo "<th>Título</th>";
echo "<th>Número de preguntas</th>";
echo "<th>Banco de preguntas</th>";
echo "<th>Personas asignadas</th>";
echo "</tr>";
$sql = "SELECT * FROM examen WHERE entidad = ".$_GET["e"]."";
$result = $link->query($sql);
    if (!empty($result) AND mysqli_num_rows($result) > 0) {
       
       // output data of each row
       while($row=$result->fetch_assoc()) {
        echo "<tr>";
        echo "<form action=\"asigna.php\" method=\"post\">";
        echo "<input type=\"hidden\" name=\"id\" value=\"".$row['id']."\" />";
        echo "<input type=\"hidden\" name=\"entidad\" value=\"".$_GET["e"]."\" />";
        echo "<td><input type=\"text\" name=\"Titulo\" value=\"".$row["Titulo"]."\" id=\"Titulo\" placeholder=\"Título del examen\"</td>";
        echo "<td><input type=\"number\" name=\"num_preguntas\" id=\"num_preguntas\" value=".$row["num_preguntas"]." min=1></td>";
        echo "<td><a href=\"banco_preguntas.php?id=".$row["banco_preguntas"]."&e=".$_GET["e"]."\">#".$row["banco_preguntas"]."</a></td>";
        $sql_asignados = "SELECT empleados.Nombre as Nombre, empleados.discord_id as discord_id  FROM empleados WHERE (empleados.discord_id, empleados.entidad) IN (SELECT examen_asigna.empleado, examen_asigna.entidad FROM examen_asigna WHERE examen = ".$row['id'].");";
        $result_asignados = $link->query($sql_asignados);
        echo "<td>";
        if (!empty($result_asignados) AND mysqli_num_rows($result_asignados) > 0) {
            while($row_asignados=$result_asignados->fetch_assoc()) {
                $id = $row_asignados["discord_id"]."_".$_GET["e"]."_".$row['id'];
                echo "<a onclick=\"confirmAction_".$id."()\" style=\"color: -webkit-link;
                cursor: pointer;
                text-decoration: underline;\" > ".$row_asignados["Nombre"]."</a> ,";
                echo "
                <script>
        // The function below will start the confirmation dialog
        function confirmAction_".$id."() {
          let confirmAction = confirm(\"¿Está seguro que quiere desasignarle de este examen? LA NOTA SE PERDERÁ\");
          if (confirmAction) {
            window.location.href = \"desasigna.php?id=".$row_asignados["discord_id"]."&e=".$_GET["e"]."&ex=".$row['id']."\"; 
          } else {
            alert(\"Acción cancelada\");
          }
        }
      </script>";
            }
        }
        echo "<select name=\"asignado_nuevo\" id=\"asignado_nuevo\" onchange=\"this.form.submit()\">";
        echo "<option value=\"null\">Asignar a</option>";
        $sql_asignados = "SELECT empleados.Nombre as Nombre, empleados.discord_id as Discord FROM empleados WHERE  entidad = ".$_GET["e"]." AND (empleados.discord_id) NOT IN (SELECT examen_asigna.empleado FROM examen_asigna WHERE examen = 1);";
        $result = $link->query($sql_asignados);
        if (!empty($result) AND mysqli_num_rows($result) > 0) {
            while($row_asignados=$result->fetch_assoc()) {
                echo "<option value=\"".$row_asignados["Discord"]."\">".$row_asignados["Nombre"]."</option>";
            }
        }
        
        echo "</select></td>";
        echo "</form>";
        echo "</tr>";
       }
      
    }
    echo "<tr><td><a href=\"crear_examen.php?e=".$_GET["e"]."\">Crear</a></td></tr>";
    echo "</table>";
    echo "<h2>Examenes Entregados</h2>";
    echo "<table>";
    echo "<tr>";
    echo "<th>Nombre</th>";
    echo "<th>Información pregunta adicional</th>";
    echo "<th>Nota</th>";
    echo "</tr>";
    $sql = "SELECT * FROM examen_asigna WHERE examen IN (SELECT id FROM examen WHERE  entidad = ".$_GET["e"].") AND info_adicional IS NOT NULL";
    $result = $link->query($sql);
    if (!empty($result) AND mysqli_num_rows($result) > 0) {
       
       // output data of each row
       while($row=$result->fetch_assoc()) {
        echo "<tr>";
        $sql_asignados = "SELECT empleados.Nombre as Nombre FROM empleados WHERE empleados.discord_id = ".$row["empleado"]." AND empleados.entidad = ".$row["entidad"];
        
        $result_examenes = $link->query($sql_asignados);
        if (!empty($result_examenes) AND mysqli_num_rows($result_examenes) > 0) {
            while($row_asignados=$result_examenes->fetch_assoc()) {
                echo "<td>".$row_asignados["Nombre"]."</td>";
            }
        }
        echo "<td>".$row["info_adicional"]."</td>";
        echo "<td>".$row["nota"]."</td>";
        echo "<td><a href=\"corregir.php?e=".$row["examen"]."&d=".$row["empleado"]."&ent=".$row["entidad"]."\">Revisar</a></td>";
        echo "</tr>";
       }
    }
?>