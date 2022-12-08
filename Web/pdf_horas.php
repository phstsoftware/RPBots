<?php
require 'vendor/autoload.php';
// reference the Dompdf namespace
use Dompdf\Dompdf;
ob_start();

include "connection.php";
// instantiate and use the dompdf class

$dompdf = new Dompdf();
$dompdf->set_option('isRemoteEnabled', TRUE);

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
   

// Image path
    $img = $logo;

  
$html="
<style>

h1 {
    text-align: center;
    font-family: Arial, Helvetica, sans-serif;
  }
  h2{
    text-align: center;
    font-family: Arial, Helvetica, sans-serif;
  }
  p {
    text-align: justify;
    font-family: Arial, Helvetica, sans-serif;
  }
  .salto {page-break-before: always;}
  
</style>

<img src=\"$img\" style=\"width:10%; height:auto;float:right\">
<h1 style=\"width:75%;display: block;\">Registro de horas a ".date("d/M/Y H:i:s")."</h1>
<br>
<table>
<tr><th>
    Nombre
</th>
<th>Rango</th>
<th>Número Placa</th>
<th>Trabajado</th>
<th>Horas</th>
<th>Total Horas</th>
<th>Ceritificados</th>
<th>Ceritificados Aviación</th>
<th>Alumnos</th>
<th>Total</th>
</tr>
";
include "connection.php";

$sql = "SELECT * FROM `empleados` WHERE entidad = ".$_GET["e"]." ORDER BY trabajado DESC ";
$result = $link->query($sql);
if (!empty($result) AND mysqli_num_rows($result) > 0) {
   // output data of each row
   while($row=$result->fetch_assoc()) {
       
       $horas = round(($row["trabajado"]/60)/60,2);
       
           $trabajado = floor($horas); // no llega al día
       
       
       $placa = sprintf('%04d',$row["numero_de_placa"]);
       
       $cantidad = 100 * $trabajado; // cantidad a pagar
       if($trabajado > 10){
        $cantidad += 2000;
        if($trabajado > 20){
            $cantidad += 3000;
            if($trabajado > 30){
                $cantidad += 4000;
            }
        }
       }
       $horas_pagar = $cantidad; // cantidad que corresponde por las horas realizadas
       $certificados = 500 * $row["certificados"];
       $cerificados_aviacion = 750 * $row["cerificados_aviacion"];
       $alumnos = (($row["alumnos"])/4)*1500;
       $cantidad = $cantidad + $cerificados_aviacion + $certificados + $alumnos;
       $html.= "<tr><td>".$row["nombre"]."</td><td>".$row["rango"]."</td><td>".$placa."</td><td>".$trabajado.":".date("i:s",$row["trabajado"])."</td><td>".floor($horas)."</td>
       <td>$horas_pagar $</td><td>$certificados $</td><td>$certificados_aviacion $</td><td>$alumnos $</td><td><strong>$cantidad $</strong></td></tr>";
   }
}
$html.= "</table>";

//$hmtl .= "</tr></tbody></table></fieldset>";
$dompdf->loadHtml($html);

// (Optional) Setup the paper size and orientation
$dompdf->setPaper('A4', 'landscape');

// Render the HTML as PDF
$dompdf->render();

ob_end_clean();
// Render the HTML as PDF

$output = $dompdf->output();
    file_put_contents('Brochure.pdf', $output);
// Output the generated PDF to Browser

$dompdf->stream("$nombre ".date("d/M/Y H:i:s").".pdf");

?>