<?php
date_default_timezone_set("Europe/Madrid");
?>
<style>
    table, th, td {
  border: 1px solid;
  padding: 5px;
}
table {
  border-collapse: collapse;
}
p{
    font-family: Arial, Helvetica, sans-serif;
}
    </style>
    
<?php
  
    include "connection.php";
    // procedemos a actualizar los rangos
   


    $_GET["e"] = base64_decode($_GET["e"]);
    $sql = "SELECT * FROM `entidad` WHERE id = ".$_GET["e"]."";
    $result = $link->query($sql);
    if (!empty($result) AND mysqli_num_rows($result) > 0) {
       // output data of each row
       while($row=$result->fetch_assoc()) {
           $tipo = $row["tipo_entidad"];
           $logo = $row["logo"]; //metemos el logo
       }
   }
   
   
   if($tipo == "LSFD"){
       $nombre = "EMS";
       if(!isset($logo)){
       $logo = "https://i.imgur.com/wUl92x6.png";
        }
   }else if($tipo == "LSPD"){
       $nombre = "Agentes";
       if(!isset($logo)){
        $logo = "https://sacjrp.net/assets/images/0bf0b1236401f5ba95b1c72a95c7df96.png";
         }
   }else if($tipo == "MEC"){
       $nombre = "Mecánicos";
       if(!isset($logo)){
        $logo = "https://static.wikia.nocookie.net/esgta/images/8/8e/Los_Santos_Customs_logo.png";
         }
   }else{
       $nombre = "Trabajadores";
       if(!isset($logo)){
        $logo = "https://static.wikia.nocookie.net/gtawiki/images/2/21/Lossantos_seal.png";
         }
   }
   $url = $logo;

// Image path
    $img = "images/".$_GET["e"].".png";

    // Save image 
    file_put_contents($img, file_get_contents($url));
   $ems = "";
   $sql = "SELECT * FROM `empleados` WHERE entidad = ".$_GET["e"]." AND en_servicio=1";
   $result = $link->query($sql);
   if (!empty($result) AND mysqli_num_rows($result) > 0) {
      // output data of each row
      while($row=$result->fetch_assoc()) {
        $ems.="\n- ".$row["nombre"]." (".$row["rango"].")";
      }
    }else{
        $ems = "No en servicio";
    }
    $ems.="\n\nActualizado: ".date("d/m/Y H:i:s");
    echo "<head><title>$nombre de servicio</title>
    <link rel = \"icon\" href = \"$logo\"type = \"image/x-icon\">";
    echo "<meta name=\"twitter:card\" content=\"summary_large_image\">";
    echo "<meta name=\"title\" content=\"$nombre de servicio:\">";
    echo "<meta name=\"twitter:title\" content=\"$nombre de servicio:\">";
    echo "<meta name=\"description\" content=\"".$ems."\">";

    echo "<meta name=\"twitter:description\" content=\"".$ems."\">";
    echo "</head>";
    echo "<img src=\"$logo\" style=\"width:100px; height:auto;float:right\">";
   echo "<h1>$nombre de servicio</h1>";
   if(isset($_GET["admin"])&&$_GET["admin"]==1){
    echo "<button style=\"    width: 150px;
    height: 40px;
    margin: 5px;\"><a href=\"pdf_horas.php?e=".$_GET["e"]."\">Horas en PDF</a></button>";
    echo "<button style=\"    width: 150px;
    height: 40px;
    margin: 5px;\"><a href=\"admin_examen/main.php?e=".$_GET["e"]."\">Portal de exámenes</a></button>";
   }
?>
<table><tr><th>
    Nombre
</th>
<th>Rango</th>
<th>Número Placa</th>
<th>Desde las</th>

</tr>

<?php 
    $ems = "$nombre de servicio";
     $sql = "SELECT * FROM `empleados` WHERE entidad = ".$_GET["e"]." AND en_servicio=1";
     $result = $link->query($sql);
     if (!empty($result) AND mysqli_num_rows($result) > 0) {
        // output data of each row
        while($row=$result->fetch_assoc()) {
            $ems.="\n".$row["nombre"]." (".$row["rango"].")";
            echo "<tr><td>".$row["nombre"]."</td><td>".$row["rango"]."</td><td>".$row["numero_de_placa"]."</td><td>".date("d/m/Y H:i:s",$row["entrado_trabajar"])."</td>";
            if(isset($_GET["admin"])&&$_GET["admin"]==1){
                sacar_servicio($row["discord_id"],$row["entidad"]);
            }
            echo "</tr>";
        }
    }

?>
</table>
<table>
<hr>
<h2> <?php echo "Horas registradas:"?></h2>
<table>
<tr>
<?php
if(isset($_GET["admin"])&&$_GET["admin"]==1){
    echo "
    <th>
    Nombre
</th>
    <th>Rango</th>
    <th>Número Placa</th>
    
    <th>Horas</th>
    <th>Certificados</th>
    <th>Certificados Aviación</th>
    <th>Tablon personal</th>
    <th>Alumnos</th>
    <th>Modificar Horas</th>";
}else{
    echo "
    <th>
    Nombre
</th>
<th>Rango</th>
<th>Número Placa</th>
<th>Trabajado</th>
<th>Horas</th>
    ";
}
?>
</tr>
<?php
 $sql = "SELECT * FROM `empleados` WHERE entidad = ".$_GET["e"]." ORDER BY trabajado DESC ";
 $result = $link->query($sql);
 if (!empty($result) AND mysqli_num_rows($result) > 0) {
    // output data of each row
    while($row=$result->fetch_assoc()) {
        $ems.="\n".$row["nombre"]." (".$row["rango"].")";
        $horas = round(($row["trabajado"]/60)/60,2);
        if($horas >= 24){
            $trabajado = strval(date("d",$row["trabajado"])-1)." días ";
            $trabajado .= strval(date("H",$row["trabajado"])-1);
        }else{
            $trabajado = floor($horas); // no llega al día
        }
        
        $placa = sprintf('%04d',$row["numero_de_placa"]);
        echo "<tr>";
        if(isset($_GET["admin"])&&$_GET["admin"]==1){
            edita_empleado($row);
        }else{
            echo "<td>".$row["nombre"]."</td><td>".$row["rango"]."</td><td>".$placa."</td><td>".$trabajado.":".date("i:s",$row["trabajado"])."</td><td>".floor($horas)."</td>";

        }
        echo "</tr>";
    }
}
/**
 * Llena una celda con un input y un form para editar ese campo
 * @param array $row array con los datos
 * @param string $campo Campo a editar
 */
function campo_edit($row, $campo, $tipo = "number"){
    $restricciones = "";
    if($tipo == "number"){
        // si es un numero no permitimos negativos
        $restricciones .= " min = 0 ";
    }

    $restricciones .= " required";
    
        $valor = $row[$campo];
    
    echo "<td><form action=\"empleado_edit.php\">";
    echo "<input type=\"hidden\" name=\"discord_id\" value=\"".$row["discord_id"]."\" />";
            echo "<input type=\"hidden\" name=\"entidad\" value=\"".$row["entidad"]."\" />";
            echo "<input type=\"$tipo\" value=\"".$valor."\" name=\"$campo\" id=\"$campo\" $restricciones />";
            echo "</form></td>";
}
/**
 * Muestra una celda con el boton para sacar de servicio
 * @param string discord_id Id de discord
 * @param string entidad Entidad 
 */
function sacar_servicio($discord_id, $entidad){
    echo "<td><form action=\"empleado_edit.php\">";
    echo "<input type=\"submit\" value=\"Sacar de servicio\" />";
    echo "<input type=\"hidden\" value=\"0\" name=\"servicio\" id=\"servicio\"  />";
    echo "<input type=\"hidden\" name=\"discord_id\" value=\"".$discord_id."\" />";
        echo "<input type=\"hidden\" name=\"entidad\" value=\"".$entidad."\" />";
        
        echo "</form></td>";
}
/**
 * Funcion que pone las columnas correspondientes a editar el empleado
 * @param $row array con los datos del empleado
 */
function edita_empleado($row){
    echo "
    <style>
    .overlay_flight_traveldil {
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(0, 0, 0, 0.7);
        transition: opacity 500ms;
        visibility: hidden;
        opacity: 0;
      }
      .overlay_flight_traveldil:target {
        visibility: visible;
        opacity: 1;
      }
      .popup_flight_travlDil {
        margin: 70px auto;
        padding: 20px;
        background: #fff;
        border-radius: 5px;
        width: 70%;
        height: 80%;
        position: relative;
        transition: all 2s ease-in-out;
      }
      .popup_flight_travlDil .close_flight_travelDl {
        position: absolute;
        top: 20px;
        right: 30px;
        transition: all 200ms;
        font-size: 30px;
        font-weight: bold;
        text-decoration: none;
        color: #333;
      }
      .popup_flight_travlDil .content_flightht_travel_dil {
        max-height: 85%;
        overflow: auto;
      }
    </style>
    ";
    
    campo_edit($row,"nombre","text"); // el nombre de la persona
    campo_edit($row, "rango","text"); // el rango de la persona
    campo_edit($row, "numero_de_placa","text"); // el numero de placa de la persona
    $horas = floor(round(($row["trabajado"]/60)/60,2));
    echo "<td>".$horas."</td>";
    campo_edit($row,"certificados"); // certificados normales
    campo_edit($row,"certificados_aviacion"); // ceritificados aviacion

    campo_edit($row,"tablon", "text"); //tablon personal
            
    echo "<td><a class=\"button\" href=\"#popup_".$row["discord_id"]."\">Alumnos</a></td> ";
    echo "<td><a class=\"button\" href=\"#horas_".$row["discord_id"]."\">Añadir/Quitar horas</a></td> ";
    if($row["en_servicio"]==1){
        sacar_servicio($row["discord_id"],$row["entidad"]);
       
    }
  // metemos un cuadro para añadir/quitar horas
  echo "
  <div id=\"horas_".$row["discord_id"]."\" class=\"overlay_flight_traveldil\">
  <div class=\"popup_flight_travlDil\">
  <h2>Añadir/Quitar horas a ".$row["nombre"]."</h2>
      <a class=\"close_flight_travelDl\" href=\"#\">&times;</a>
          <div class=\"content_flightht_travel_dil\">";
          echo "<form action=\"empleado_edit.php\">";
          echo "<input type=\"hidden\" name=\"discord_id\" value=\"".$row["discord_id"]."\" />";
                  echo "<input type=\"hidden\" name=\"entidad\" value=\"".$row["entidad"]."\" />";
                 
                  echo "<input type=\"number\" name=\"añadir\" id=\"añadir\" />";
                  echo "<p>Para añadir horas simplemente escibir el número para añadir, para quitar poner el número en negativo</p>";
                  echo "</form></td>";
          echo "</form></div>
          </div>
      </div>
      ";
      $titulos = ["No forma parte del departamento","Poca implicación","Implicación media-baja","Implicación alta","Muy Implicado/a"];
      $mensaje = ["No forma parte del departamento","Ha acudido con poca frecuencia y no conoce a los alumnos","Conoce a los alumnos pero no viene lo suficiente para instruirlos"
      ,"Se le ve implicado aunque no está por ellos","Está muy implicado y se dedica en cuerpo y alma al departamento"];
  
    echo "
    <div id=\"popup_".$row["discord_id"]."\" class=\"overlay_flight_traveldil\">
	<div class=\"popup_flight_travlDil\">
		<h2>Actitud con los alumnos</h2>
		<a class=\"close_flight_travelDl\" href=\"#\">&times;</a>
            <div class=\"content_flightht_travel_dil\">";
            echo "<form action=\"empleado_edit.php\">";
            echo "<input type=\"hidden\" name=\"discord_id\" value=\"".$row["discord_id"]."\" />";
            echo "<input type=\"hidden\" name=\"entidad\" value=\"".$row["entidad"]."\" />";
            for ($i = 0; $i < 5; $i++) {
                
                if($row["alumnos"]==$i){
                    $check = "checked";
                }else{
                    $check = "";
                }
                echo "<label style=\"width: 100%;\"><input type=\"radio\" value=\"$i\" name=\"alumnos\" id=\"alumnos\" $check>";
                echo "<p style='font-size:15px; margin-left: 5px;
                display: inline-block;'><i class=\"fas fa-percent\"></i> <strong>".$titulos[$i]." </strong></p>";
                
                echo "<p>".$mensaje[$i]."</p>";
                echo "<hr>";
                echo "</input></label>";
            }
            
            echo "<input type=\"submit\" value=\"Guardar\">";
            echo "</form></div>
	</div>
</div>
";
}
?>
</table>
</table>