<?php

include "connection.php";

foreach ($_GET as $key => $value){
    if($key != "entidad"&&$key != "discord_id"){
        // es el que hay qeu actualizar
        $update = "$key = \"$value\"";
    }
}

if(isset($_GET['certificados'])){
    $update = "certificados = " . $_GET['certificados'];
}else if(isset($_GET['certificados_aviacion'])){
    $update = "certificados_aviacion = " . $_GET['certificados_aviacion'];
}else if(isset($_GET['alumnos'])){
    $update = "alumnos = " . $_GET['alumnos'];
}else if(isset($_GET['servicio'])){
    if($_GET['servicio'] == "1"){
        $servicio = ", entrado_trabajar = \"CURRENT_TIMESTAMP\"";
    }else{
        $servicio = "";
    }
    $update = "en_servicio = " . $_GET['servicio']." $servicio"; 
}else if(isset($_GET['añadir'])){
    $update = "trabajado = trabajado + ".($_GET['añadir']*3600);
}else if(isset($_GET['tablon'])){
    $update = "tablon = \"" . $_GET['tablon']."\"";
}
$sql = "UPDATE empleados SET $update WHERE entidad = ".$_GET["entidad"]." AND discord_id = ".$_GET["discord_id"];
$link->query($sql);
echo "
<script>
window.location.href = \"https://rpbots.000webhostapp.com/?e=".base64_encode($_GET["entidad"])."&t=1656284601.0730627&admin=1#\"; 
</script>
";
?>