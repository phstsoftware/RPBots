<?php
include __DIR__.'/../connection.php';

$sql = "DELETE FROM examen_asigna WHERE examen = ".$_GET["ex"]." AND empleado = ".$_GET["id"]." AND entidad = ".$_GET["e"]."";
$link->query($sql);

echo "
<script>
window.location.href = \"https://rpbots.000webhostapp.com/admin_examen/main.php?e=".$_GET["e"]."\"; 
</script>
";

?>