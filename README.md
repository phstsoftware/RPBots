BOT + web para Servidores de Roleplay


#####################
Requisitos
#####################
- Una web senzilla con php (puede ser hosting gratuito)
- Base de datos SQL accesbile remotamente

#####################
Instalación
#####################
1- Abre el main.py
2- Pega el token del bot
3- Pega los datos de la base de datos
4- Corre el rp_bots.sql en la base de datos
5- Carga la carpeta web en el php
#####################
Configuración
#####################
1- Invita al bot a un servidor
2- Escribe /entidad para dar de alta una entidad (LSFD o LSPD)
3- La contraseña por defecto es 1
4- La persona que conteste y hable al bot será el primer autorizado
5- SE RECOMIENDA QUE CADA EMPLEADO TENGA SU CANAL DE DISCORD A MODO DE TABLON
#####################
Comandos bot
#####################
- -fichar : (entrar o salir de servicio)
- /seguro : permite renovar el seguro (el bot os preguntará por md cuántos días y lo actualizará solo)
- /actualiza : (solo para autorizados) muestra horas de servicio pero no las reinicia
- /resumen: (solo para autorizados) muestra horas de servicio y las reinicia
- /analisis : (Saca análisis de sangre y orina)
- /psicotecnico : (Hace las preguntas del psicotécnico y dice si el paciente es apto o no)
- /resguardo : (Saca el resguardo del psicotécnico )
- /baja medica: se tramita una baja
- /sangre : se hace un análisis de sangre y si el paciente no lo sabe se le dice su grupo sanguíneo 
- /enlazar paciente : se enlaza el canal de un paciente con el paciente (antes de esto probad de hacer un /analisis).
- /nuevo paciente : crea un canal para el paciente y lo enlaza.
- /cita : (Permite a la gente pedir cita desde el servidor de Destino-RP)
  ---> 👍 -> Aceptáis la cita y se le confirma al paciente automáticamente
  ---> 👎 -> Denegáis la cita, se le informa al paciente automáticamente y se borra el mensaje con la cita (podéis denegar una cita después de aceptarla, pero una vez denegada ya nada)
  ---> 🚑 -> El paciente ya ha sido atendido, se le mandan las gracias automáticamente por mensaje y se borra el mensaje con la cita
- /monitor : crea un monitor para ver quien está de servicio
- /dispensable : crea una lista de dispensables vinculada con la base de datos de otra entidad del mismo servidor
  ---> /liquidar : Se liquida los dispensables
- /placa : pone un numero de placa
- /alta : da de alta como empleado
- /baja : da de baja como empleado
- /autoriza : añade un autorizado
- /incentivos : reparte incentivos según horas trabajadas

#####################
WEB
#####################
Con el codigo en PHP puedes ver quien está de servicio, si pones &admin=1 tienes la versión para añadir/quitar horas

También se pueden crear examenes con sus bancos de preguntas. Si pones /examen en un tablón mandas el enlace del examen.
######################
No dudes en comentar cualquier bug/error o mejora

Estamos aquí para ayudar :)

Creado por davidoc1109 con ayuda de Joel_247 y Gery
