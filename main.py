#Bot creado por davidoc1109
# 

#---------------
# YOUR DATA
#---------------
TOKEN = #Discord token

# enter your server IP address/domain name
HOST = # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = 
# this is the user you create
USER = 
# user password
PASSWORD = 


#----------------
# DO NOT TOUCH BEHIND HERE UNLESS YOU KNOW
#----------------
import base64
from facciones import LSFD,LSPD,Mecanico

from fpdf import FPDF
from PIL import ImageFont, ImageDraw, Image
from datetime import date
from datetime import datetime
from datetime import timedelta
from time import sleep
from timeit import default_timer as timer
import random
import requests
import time
import os
import sys

from discord.ext import commands, tasks
import discord
import pymongo

from pymongo import MongoClient
import requests



global datos_persona



import mysql.connector as mysql


global mydb
# connect to MySQL server

# enter your code here!
r = requests.head(url="https://discord.com/api/v1")
try:
    print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
except:
    print("No rate limit")



URL = "YOUR_URL/?e={0}&t={1}"



bot = commands.Bot

def restart_bot(): 
 os.execv(sys.executable, ['python'] + sys.argv)






from dateutil.parser import parse

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False
def calculate_age(born):
    today = date.today()
    inter =  today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    print(inter*-1)
    return inter*-1
    
def calc_edad(born):
    today = date.today()
    inter =  today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    
    return inter
async def actualiza_monitor(id):
  
    mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
    mycursor = mydb.cursor() 
    mycursor.execute("SELECT `mensaje`,`canal` FROM monitor WHERE entidad = "+str(id))
    myresult_auth = mycursor.fetchall()
    for x in myresult_auth:
      channel = client.get_channel(x[1]) # the message's channel
      msg_id = x[0] # the message's id
      message_cod = str(id)
      message_bytes = message_cod.encode('ascii')
      base64_bytes = base64.b64encode(message_bytes)
      base64_message = base64_bytes.decode('ascii')
      
      msg = await channel.fetch_message(msg_id)
      await msg.edit(content=URL.format(base64_message, time.time()))
async def mandar_mensaje(channel, texto):
  """
  :param channel: int,  canal en el cual mandar el mensaje
  :param texto: str, Texto a mandar
  """
  await channel.send(texto,delete_after = 60)
async def pregunta_md_join(member, client, texto):
  """
  :param mensaje: int, mensaje principal
  :param texto: str, Texto a mandar
  """
  
  await member.send("```{0}```".format(texto))

  def check(m):
      global volver
      volver = m.content
      return m.content != "" and m.author == member

  await client.wait_for("message", check=check)
  time.sleep(1)
  
  return volver
async def pregunta_md(mensaje, client, texto):
  """
  :param mensaje: int, mensaje principal
  :param texto: str, Texto a mandar
  """
  
  await mensaje.author.send("```{0}```".format(texto))

  def check(m):
      global volver
      volver = m.content
      return m.content != "" and m.author == mensaje.author

  await client.wait_for("message", check=check)
  time.sleep(1)
  
  return volver
async def pregunta(mensaje, texto):
  """
  :param mensaje: int, mensaje principal
  :param texto: str, Texto a mandar
  """
  
  await mensaje.channel.send(texto,delete_after = 60)

  def check(m):
      global volver
      volver = m.content
      return m.content != "" and m.channel == mensaje.channel and m.author == mensaje.author

  await client.wait_for("message", check=check)
  time.sleep(1)
  msg = await mensaje.channel.fetch_message(mensaje.channel.last_message_id)
        
  await msg.delete()
  return volver
def entidad_name(id, mycursor):
  """
  Funcion que devuelve el nombre de una entidad a partir de su id
  :param id: int, id de la entidad
  :param mycursor: de la base de datos
  """
  mycursor.execute("SELECT `nombre` FROM entidad WHERE id = "+str(id))
  myresult_auth = mycursor.fetchall()
  ok = False
  for x in myresult_auth:
    return x[0] #devolvemos el nombre
def entidad_existe(message, mycursor):
  """
  Funcion que busca si el servidor de Discord que se ha mandado el mensaje existe com entidad
  :param mensaje: int, mensaje principal
  """
  mycursor.execute("SELECT * FROM entidad WHERE discord = "+str(message.guild.id))
  myresult_auth = mycursor.fetchall()
  ok = False
  for x in myresult_auth:
    ok = True
  return ok
    

global entidad
global actualizado
global tipo_entidad


intents = discord.Intents.all()
intents.members = True

client = discord.Client(intents=intents)
@client.event
async def on_member_join(member):
    print("Entrado Discord")
    print("SELECT `id`,`nombre` FROM entidad WHERE  discord = {0}".format(member.guild.id))
    mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
    mycursor = mydb.cursor()  
    mycursor.execute("SELECT `id`,`nombre` FROM entidad WHERE  discord = {0}".format(member.guild.id))
    #busquem si ha estat enviat desde una facci??
    myresult = mycursor.fetchall()
    encontrado = False
    for x in myresult:
      #hem trobat la facci??, volem saber el seu id i el seu nom
      entidad = x[0]
      nombre = x[1]
      encontrado = True
    if encontrado == True:
      
      m = await pregunta_md_join(member, client, "Hola ????\nNecesito saber si has entrado para trabajar ic en {0}\n\nResponde con 1 o \"s??\" si vienes a trabajar IC y quieres ser dado de alta en la m??quina de fichar, responde 0 o \"no\" y desaparecer?? lentamente de tus mds".format(nombre))
      
      if m == "s??" or m == "1" or m == "si":
        #toca registrarlo
        m = await pregunta_md_join(member, client, "Ind??came tu nombre ic por favor")
        
        
        sql = "INSERT INTO empleados (entidad, discord_id, nombre, rango, trabajado, entrado_trabajar, en_servicio, numero_de_placa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (entidad, member.id, m, "Alumno", 0, 0, 0, "0")
        mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
        mycursor = mydb.cursor() 
        mycursor.execute(sql, val)
        
        mydb.commit()
        await member.send("```Gracias, ya puedes usar el comando -fichar```")
      else:
        #pedimos perdon
        await member.send("```Perfecto, discupla las molestias```")
    else:
      print(member.guild.id)
@client.event
async def on_ready():
    print("conectado")
    

    

@client.event
async def on_message(message):
    if message.author.bot:
      return

    if message.content.startswith('/') or message.content.startswith('-'):
        mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
        mycursor = mydb.cursor()
        
        autorizado = 0
        server = 0
        tipo_entidad = ""

        mycursor.execute("SELECT * FROM entidad WHERE discord = {0}".format(message.guild.id))
        print (message.guild.id)
        myresult = mycursor.fetchall()
        for x in myresult:
          server = x[1] #nos guaramos el server
          print(x)  
          entidad = x[0]
          actualizado = x[4]
          tipo_entidad = x[5]
          mycursor.execute("SELECT `disc_id` FROM autorizado WHERE entidad = "+str(x[0])+"")
          myresult_auth = mycursor.fetchall()
          for t in myresult_auth:
            if(t[0]==message.author.id):
              autorizado = 1
        #Vamos a buscar en qu?? servidor se ha mandado el mensaje
      #  cluster = pymongo.MongoClient(mongo_nom)
        #cluster = pymongo.MongoClient("mongodb+srv://AdolfoFormo:adolfoformohores@control-hores.g7r5s.mongodb.net/LSFD?retryWrites=true&w=majority")
        
        
        if message.content == "-fichar":
          #manda el mensaje para fichar
          
            mycursor.execute("SELECT * FROM empleados WHERE entidad = "+str(entidad)+" AND discord_id = "+str(message.author.id))
            myresult_auth = mycursor.fetchall()
            encontrado = False
            for t in myresult_auth:
                #si encontramos el usuario que buscamos
                encontrado = True #apuntamos que hemos encontrado a la persona
                print(t)
                global datos_persona
                datos_persona = t
                break #rompemos el bucle para ahorrar memoria
           

            if  encontrado == True and datos_persona[6]==1 :
              #si est?? en servicio
              
              #caluculamos el tiempo trabajado
              now = time.time()
              
              trabajado = now - datos_persona[5]
              trabajado = trabajado + datos_persona[4]
              print ("datos persona {0}, ahora {1}, trabajado {2}".format(datos_persona[5],now,trabajado))
              
             
              sql = "UPDATE empleados SET trabajado = {0}, en_servicio = 0 WHERE entidad = {1} and discord_id ={2}".format(trabajado,datos_persona[0],datos_persona[1])

              mycursor.execute(sql)
              
              mydb.commit()
              
              await mandar_mensaje(message.channel,"{0} ha salido de servicio".format(datos_persona[2])) 
              #mandamos actualizacion
            elif encontrado == True:
              #entra ahora de servicio
              await mandar_mensaje(message.channel,"{0} ha entrado de servicio".format(datos_persona[2])) 
              now = time.time()
              print(now)
              sql = "UPDATE empleados SET entrado_trabajar = {0}, en_servicio = 1 WHERE entidad = {1} and discord_id ={2}".format(now,datos_persona[0],datos_persona[1])
              mycursor.execute(sql)          
              mydb.commit()
            else:
              #en caso de que no exista en la base de datos
              await mandar_mensaje(message.channel,"Error, usted no existe en la base de datos.")
              si = await pregunta_md(message,client,"Hola ????\nVeo que no est??s dado de alta en la m??quina de fichar. ??Quieres que te tramite el alta yo mismo? (En caso afirmativo 1 o s??, de lo contrario responde 0 o no)")
              if si=="1" or si == "si" or si == "s??":
                nombre = await pregunta_md(message, client, "Ind??came tu nombre ic, por favor")
                rango = await pregunta_md(message,client,"Dime tu rango ic ahora mismo")
                id_pers = message.author.id
                num_placa = await pregunta_md(message,client,"Escribe tu n??mero de placa/identificaci??n, por favor")
                sql = "INSERT INTO empleados (entidad, discord_id, nombre, rango, trabajado, entrado_trabajar, en_servicio, numero_de_placa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (entidad, id_pers, nombre, rango, 0, 0, 0, num_placa)
                mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
                mycursor = mydb.cursor() 
                mycursor.execute(sql, val)
                
          
                mydb.commit()
                await message.author.send("```Hecho, te he a??adido a la m??quina de fichajes. Ahora tendr??s una menci??n en ```<#{0}>```aseg??rate que te ha llegado, por favor```".format(message.channel.id))
                await mandar_mensaje(message.channel,"He a??adido {0} (<@{1}>)".format(nombre,id_pers))
              else:
                await  message.author.send("```Perfecto, cualquier cosa me dices :)```")
            await actualiza_monitor(entidad)
            try:
              await message.delete()
            except:
              print("no se puede borrar")
        elif message.content == "/resumen" and autorizado==1:
          
          
          await message.channel.send("Resumen desde {0}".format(actualizado))
          sql = "UPDATE entidad SET actualizado = \"{0}\" WHERE id = {1}".format(str(datetime.today().strftime('%Y-%m-%d')),entidad)
          mycursor.execute(sql)          
          mydb.commit()
          print(str(datetime.today().strftime('%Y-%m-%d')))
          mycursor.execute("SELECT * FROM empleados WHERE entidad = "+str(entidad))
          myresult_auth = mycursor.fetchall()
          for x in myresult_auth:
         
            trabajado = x[4] #leemos lo trabajado
            horas = (trabajado/60)/60
            await message.channel.send("{0} ({2}) -  {1} horas .".format(x[2],round(horas,2),x[3])) #mostramos el mensaje
            
            
            sql = "UPDATE empleados SET trabajado = 0 WHERE entidad = {0} AND discord_id = {1} ".format(entidad,x[1])
            mycursor.execute(sql)          
            mydb.commit()
          try:
              await message.delete()
          except:
              print("no se puede borrar")
        elif message.content == "/diploma":
                  await message.delete()
                  
                  mycursor.execute("SELECT `nombre`,`rango`,`numero_de_placa`, `discord_id` FROM empleados WHERE entidad = {0} AND tablon = {1}".format(entidad,message.channel.id))
                  myresult = mycursor.fetchall()
                  enc = 0
                  for p in myresult:
                        recibe_nombre = p[0] #guardamos el nombre
                        recibe_rango = p[1] #guardamos el rango
                        recibe_placa = p[2] #guardamos el numero de placa
                        recibe_discord = p[3]
                        enc=1
                  if enc == 0:
                    await message.channel.send("Tabl??n no encontrado. Escriba /tablon para enlazarlo.",delete_after = 60)
                  else:
                    
                  #  db = cluster["Clientes"]
                    mycursor.execute("SELECT `nombre`,`numero_de_placa` FROM empleados WHERE entidad = {0} AND discord_id = {1}".format(entidad,message.author.id))
                    myresult = mycursor.fetchall()
                    enc = 0
                    for x in myresult:
                        expide_nombre = x[0]
                       
                        expide_placa = x[1]
                        enc=1
                    if enc == 1:
                      mensaje = "Otorgado a {0} (#{1}) por su gran esfuerzo realizando el curso de:".format(recibe_nombre, recibe_placa)
                      motivo = await pregunta_md(message, client,"Escriba el certificado por el que se le atorga el diploma")
                      nombre_correo = recibe_nombre
                      
                      correo = "-----------------------------------------------\nDe: **no-reply@lsfd.gov**\nPara: **{0}@lsfd.gov**\nAsunto: Diploma\n-------------------------------------------------\n\nHola <@{1}>\nDesde la jefatura del departamento de ingenieros nos congraturla hacerle llegar un nuevo diploma sobre una instrucci??n realizada.\nEn concreto le hacemos llegar el diploma correspondiente a: \n\n**_{2}_**\n\nEsperamos que siga obteniendo muchos m??s\n\nSaludos cordiales,\nJefatura del Condado de Los Santos Fire Departament\n\n-------------------------------------------------\n_Este correo ha sido enviado desde una direcci??n que no acepta correos, NO RESPONDA A ESTE CORREO. Puede ponerse en contacto con jefatura@lsfd.gov_".format(nombre_correo.replace(" ",""),recibe_discord,motivo)
                      await message.channel.send(correo)
                      today = date.today()  
                      fecha = today.strftime("%Y-%m-%d")
    
                      img = Image.open("plant_diploma.png")
                      draw = ImageDraw.Draw(img)
                      font = ImageFont.truetype('Roboto-Regular.ttf', 14)
                      
                      W, H = (936,460) # tama??o del archivo
                      eje_x = W/6 #una cuarta parte del tama??o   
                      eje_x_2 = 530
                      w, h = draw.textsize(mensaje,font)
                      draw.text(((W-w)/2,175), mensaje, (0,0,0), font=font)
                      font_2 = ImageFont.truetype('Raleway-Black.ttf', 37)
                      w, h = draw.textsize(motivo, font_2)
                    
                      
                      draw.text(((W-w)/2,210), motivo, (0,0,0), font=font_2)
                      font_mano = ImageFont.truetype('DancingScript-Regular.ttf', 20)
                      draw.text((eje_x,370), expide_nombre, (0,0,0), font=font_mano) 
                      draw.text((eje_x,410), "#{0}".format(expide_placa), (0,0,0), font=font) 
                      draw.text((eje_x*4,370), "Los Santos", (0,0,0), font=font_mano) 
                      draw.text((eje_x*4,410),today.strftime("%d/%m/%Y") , (0,0,0), font=font) 
                      img.save("diploma.png")
                      await message.channel.send(file=discord.File("diploma.png")) 
                    
        elif message.content == "/actualiza" and autorizado == 1:
        
          await message.channel.send("Resumen desde {0}".format(actualizado))
          sql = "UPDATE entidad SET actualizado = {0} WHERE id = {1}".format(str(datetime.today().strftime('%Y-%m-%d')),entidad)
          mycursor.execute(sql)          
          mydb.commit()
         
          mycursor.execute("SELECT * FROM empleados WHERE entidad = "+str(entidad))
          myresult_auth = mycursor.fetchall()
          for x in myresult_auth:
            
            trabajado = x[4] #leemos lo trabajado
            await message.channel.send("{0} ({5}) - {1} d??as, {2} horas, {3} minutos, {4} segundos.".format(x[2],time.gmtime(trabajado).tm_yday-1,time.gmtime(trabajado).tm_hour-1,time.gmtime(trabajado).tm_min,time.gmtime(trabajado).tm_sec,x[3])) #mostramos el mensaje
            
            
          try:
            await message.delete()
          except:
            print("no se puede borrar")
        elif message.content == "/incentivos" and autorizado == 1:
          # Procedemos a mandar por md a todo el mundo su incentivo
          await message.channel.send("Procedo a enviar incentivos, un momento....")
          mycursor.execute("SELECT * FROM empleados WHERE entidad = "+str(entidad))
          myresult_auth = mycursor.fetchall()
          for x in myresult_auth:
            trabajado = x[4] #leemos lo trabajado
            horas = (trabajado/60)/60
            cantidad = int(horas) * 100
            horas_trab = cantidad
            suplemento = 0
            if(horas > 10):
              suplemento += 2000
              if(horas > 20):
                suplemento += 3000
                if(horas > 30):
                  suplemento += 4000
            cantidad = cantidad + suplemento #le sumamos el suplemento
            certificados = x[8]*500 #total de certificados
            certificados_aviacion = x[10]*750 #total de certificados de aviacion
            alumnos = (x[9]/4)*1500 #lo que corresponde por alumno
            cantidad = cantidad + alumnos + certificados_aviacion + certificados
            usuario = await client.fetch_user(x[1]); #cogemos el usurio a partir de su id de discord
            embedVar = discord.Embed(title="Incentivos", description="Desc", color=0x00ff00)
            embedVar.add_field(name="Field1", value="Hola {0}\nSe le adjunta la liquidaci??n de incentivos correspondiente a esta quincena".format(x[2]), inline=False)
            embedVar.add_field(name="Field2", value="Horas trabajadas ({0}): {1}\nIncentivo horas: {2}\nCertificados M??dicos: {3}\nCertificados Aviaci??n: {4}\nAlumnos: {5}\nTotal: {6}".format(int(horas),horas_trab,suplemento,certificados, certificados_aviacion,alumnos,cantidad), inline=False)
            await usuario.send(embed=embedVar)
            
        elif message.content == "/autoriza" and autorizado == 1:
          await message.delete()
          pers = await pregunta_md(message,client,"Escriba el id del nuevo autorizado")
          nombre = await pregunta_md(message,client, "Escriba el nombre ic")
          sql = "INSERT INTO autorizado (disc_id, entidad, nombre) VALUES (%s, %s, %s)"
          val = (pers, entidad, nombre)
          mycursor.execute(sql, val)
          
          mydb.commit()
          
          print("actualizado")
          print(x)
          print(pers)
          await mandar_mensaje(message.channel,"A??adido <@{0}> como autorizado".format(pers))
        elif message.content == "/changelog" and autorizado == 1:
          await message.delete()
          await message.channel.send("```Changelog del bot\n- A??adido el comando /monitorear para establecer el monitoreo de una facci??n\n- A??adido el comando /autoriza para a??adir a un nuevo autorizado al bot\n- A??adido el /acepta_cita para establecer el canal de recibir citas\n- Ahora el bot pregunta por md para no molestar.\n- Mejorada la estabilidad (ahora no se ber??a caer, en toer??a).\n- A??adido al f??n el comando /cita para pedir cita con polic??a, EMS o Mec??nico.\n- Funciones mejoradas para las facciones (desc??brelo IC)```")
        elif message.content == "/placa":
          num_placa = await pregunta_md(message, client, "Indique su n??mero de placa")
          sql = "UPDATE empleados set numero_de_placa = {0} WHERE entidad = {1} AND discord_id = {2}".format(num_placa,entidad,message.author.id)
          await mandar_mensaje(message.channel,"Cambiado")
          try:
            await message.delete()
          except:
            print("no se puede borrar")
        elif message.content == "/alta" and autorizado == 1:
          await message.delete()
          nombre = await pregunta_md(message,client,"Escriba el nombre del nuevo miembro")
          rango = await pregunta_md(message,client,"Escriba el rango del nuevo miembro")
          id_pers = await pregunta_md(message,client,"Escriba el id de Discord del nuevo miembro")
          num_placa = await pregunta_md(message,client,"Escriba el n??mero de placa/identificaci??n del nuevo miembro")
          sql = "INSERT INTO empleados (entidad, discord_id, nombre, rango, trabajado, entrado_trabajar, en_servicio, numero_de_placa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
          val = (entidad, id_pers, nombre, rango, 0, 0, 0, num_placa)
          mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
          mycursor = mydb.cursor() 
          mycursor.execute(sql, val)
          
          mydb.commit()
          
          await mandar_mensaje(message.channel,"A??adido {0} (<@{1}>)".format(nombre,id_pers))
        elif message.content == "/placa":
          print("Placa")
          num_placa = await pregunta_md(message, client, "Indique su n??mero de placa")
          sql = "UPDATE empleados set numero_de_placa = {0} WHERE entidad = {1} AND discord_id = {2}".format(num_placa,entidad,message.author.id)
          await mandar_mensaje(message.channel,"Cambiado")
          try:
            await message.delete()
          except:
            print("no se puede borrar")
        elif message.content == "/baja" and autorizado == 1:
          
          id_pers = await pregunta_md(message,client,"Escriba el id de Discord del miembro a eliminar")
          
          sql = "DELETE FROM empleados WHERE discord_id = {0}".format(id_pers)
         
          mycursor.execute(sql)
          
          mydb.commit()
      
          await mandar_mensaje(message.channel,"hecho")
          try:
            await message.delete()
          except:
            print("no se puede borrar")
        elif message.content == "/entidad" and entidad_existe(message,mycursor) == False:
          await message.delete()
          await mandar_mensaje(message.channel,"```Bienvenido al nuevo bot```")
          nombre = await pregunta_md(message,client,"Escriba el nombre de la nueva entidad")
          server = await pregunta_md(message,client,"Introduzca la clave da activaci??n de su servidor, si no la conoce pregunte a ```<@418102275974758419>") # si no es correcta se rechazar?? por la bd
          mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
          mycursor = mydb.cursor() 
          sql = "INSERT INTO entidad (nombre, discord, actualizado, servidor) VALUES (%s, %s, %s, %s)"
          val = (nombre, message.guild.id, str(datetime.today().strftime('%Y-%m-%d')), server)
          
          mycursor.execute(sql, val)
          
          mydb.commit()
          #vamos a buscar el id de entidad
          mycursor.execute("SELECT (`id`) FROM entidad WHERE discord = {0}".format(message.guild.id))
          print (message.guild.id)
          myresult = mycursor.fetchall()
          id = -1
          for x in myresult:
            id = x[0] #cogemos el id
          if id != -1:
            sql = "INSERT INTO autorizado (disc_id, entidad, nombre) VALUES (%s, %s, %s)"
            val = (message.author.id, id, message.author.name)
            
            mycursor.execute(sql, val)
            
            mydb.commit()
          
            await mandar_mensaje(message.channel,"```Hecho, te explicamos los comandos\n- -fichar: fichar/desfichar\n- /alta: a??adir un trabajador\n- /baja: quitar a un trabajador\n- /resumen: Resumen de las horas hechas por los trabajadores (se reiniciar??n despu??s de mostrarlo\n -/monitor: para poner un monitor y poder ver los empleados de servicio\n -/aceptar_cita: si se quiere usar el comando /cita para aceptar citas \n*Se dispone de m??s comandos dependiendo de cada facci??n*```")
            await mandar_mensaje(message.channel,"```Ante cualquier bug. Por favor rep??rtelo, con captura de pantalla a poder ser, a ```<@418102275974758419>```. Gracias")
            try:
              await message.delete()
            except:
              print("no se puede borrar")
          else:
            await mandar_mensaje((message.channel),"Ha ocurrido un error, aseg??erese que la clave de activaci??n del servidor sea correcta ")
        elif message.content == "/liquidar" and autorizado == 1:
            await message.delete()
            #liquida dispensable
            messages = await message.channel.history(limit=200).flatten()
            vendidos = 0
            for mes in messages:
              try:
                mes_reaction = await message.channel.fetch_message(mes.id) 
                print(mes_reaction.reactions)
                
                reaction = mes_reaction.reactions
                print(reaction[0].emoji)
                for ids, val in enumerate(reaction):
                  if  reaction[ids].count>1:
                      vendidos = vendidos +1
                
                print(mes_reaction.reactions)
                try:
                    await mes.delete()
                except:
                  print("no delete")
              except Exception as e:
                print(e)
                print("messsage not correct")
            precio = 0
            nom_disp = ""
            entidad=""
            entidad_id = 0
            
            mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
            mycursor = mydb.cursor() 
            mycursor.execute("SELECT * FROM sincronizaciones WHERE canal = {0}".format(message.channel.id))
            myresult = mycursor.fetchall()
            for x in myresult:
                precio = x[3]
                nom_disp=x[0]
                entidad_origen = entidad_name(x[1],mycursor) #entidad_origen 
                entidad_id = x[4]
                entidad = entidad_name(x[4],mycursor) #entidad de destino
            cobrar = int(precio)*vendidos
            if entidad_id != -1:
              await message.author.send("_Factura de {0}_\n**Entidad de origen:** *{1}*\n**Entidad de destino:** *{2}*\n**Cantidad dispensada:** *{3}*\n**Precio unitario:** *{4}*\n***Total a pagar:*** *{5}*".format(nom_disp,entidad_origen,entidad,vendidos,precio,cobrar))
             # mydb = cluster[entidad]
              mycursor.execute("SELECT `nombre`,`numero_de_placa` FROM empleados WHERE entidad = {0} ORDER BY numero_de_placa".format(entidad_id))
              myresult = mycursor.fetchall()
              for x in myresult:
                
                mensaje = await message.channel.send("`{0} ({1})`".format(x[0],x[1]))
                await mensaje.add_reaction('\N{THUMBS UP SIGN}')
        
        elif message.content == "/dispensable" and autorizado == 1:
            await message.delete()
            id = -1
            await message.author.send("```Bienvenido al sistema de sincronizaci??n de base de datos para dispensables\n```")
           
            encontrar = False
            while(encontrar==False):
              nombre = await pregunta_md(message,client,"Introduzca el nombre de la entidad a sincronizar");
              encontrar = False
              mycursor.execute("SELECT `id` FROM entidad WHERE nombre = \"{0}\" AND servidor = {1}".format(nombre,server))
              myresult = mycursor.fetchall()
              for x in myresult:
                encontrar = True
                id = x[0] #nos guardamos el id de la entidad de destino
           
            
            dispensable = await pregunta_md(message,client, "escriba el nombre del dispensable a controlar")
            precio = await pregunta_md(message,client, "introduzca el precio por unidad a cobrar a la entidad")
            
            mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
            mycursor = mydb.cursor() 
            sql = "INSERT INTO sincronizaciones (nombre_dispensable, entidad_origen, entidad_destino, canal, precio) VALUES (%s, %s, %s, %s, %s)"
            val = (dispensable, entidad, id, message.channel.id, precio)
            
            mycursor.execute(sql, val)
            
            mydb.commit()
          
            mycursor.execute("SELECT `nombre`,`numero_de_placa` FROM empleados WHERE entidad = {0}".format(id)) #cargamos los de la entidad de destino
            myresult = mycursor.fetchall()
            for x in myresult:
                
                mensaje = await message.channel.send("`{0} ({1})`".format(x[0],x[1]))
                await mensaje.add_reaction('\N{THUMBS UP SIGN}')
        elif message.content == "/monitorear" and autorizado==1:
            await message.delete()
            encontrar = False
            while(encontrar==False):
              nombre = await pregunta_md(message,client,"Introduzca el nombre de la entidad a monitorear");
              encontrar = False
              
              mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
              mycursor = mydb.cursor() 
              
              mycursor.execute("SELECT `id` FROM entidad WHERE nombre = \"{0}\" AND servidor = {1}".format(nombre,server))
            
              myresult = mycursor.fetchall()
              for x in myresult:
                encontrar = True
                id = x[0] #nos guardamos el id de la entidad de destino
            
            message_cod = str(id)
            message_bytes = message_cod.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('ascii')
            mens = await message.channel.send(URL.format(base64_message,time.time()))
            mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
            mycursor = mydb.cursor() 
            sql = "INSERT INTO monitor (entidad, mensaje, canal) VALUES (%s, %s, %s)"
            val = (id, mens.id, message.channel.id)
              
            mycursor.execute(sql, val)
              
            mydb.commit()
        elif message.content == "/acepta_cita" and autorizado==1:
              sql = "UPDATE entidad SET canal_cita = {0} WHERE id = {1}".format(message.channel.id,entidad)

              mycursor.execute(sql)
              
              mydb.commit()
              await message.channel.send("```Se ha configurado este canal para recibir citas```")
              await message.delete()
        elif message.content == "/cita":
          mycursor.execute("SELECT `id` FROM servidores WHERE server_id = {0}".format(message.guild.id)) #cargamos el servidor
          myresult = mycursor.fetchall()
          await message.delete()
          servidor_id = -1
          for x in myresult:
            servidor_id = x[0] # nos guardamos el id
          if servidor_id!=-1:
            volver = await pregunta_md(message,client,"Bienvenido al software de citas, por favor indique con que facci??n desea una cita: LSPD, LSFD o MEC (para mec??nico)")
          
            
            while volver!="LSPD" and volver!="LSFD" and volver!="Mec??nico":
              volver = await pregunta_md(message,client,"Por favor escriba correctamente la facci??n: LSPD, LSFD o MEC (para mec??nico)")
              print (volver)
            
            pre_dia = await pregunta_md(message,client,"Por favor, indica que d??a quieres la cita, por ejemplo 2022-05-01 en formato YYYY-MM-DD")
           
            z_dia = pre_dia
            print(z_dia)
            time.sleep(1)
            close = 0
            while is_date(z_dia)==0 and close == 0:
              #not valid
                loco_dia = await pregunta_md(message,client,"Por favor, introduce una fecha en formato YYYY-MM-DD o escribe \"cancelar\"")
             
                dia = loco_dia
                z_dia = loco_dia
                if dia == "cancelar":
                  close = 1
                  await message.author.send("Cancelado, sin problema. Si quieres volver a empezar pon /cita en el discord")
                  break
                
                time.sleep(1)
            if close == 0:
              
              dia = z_dia
              while calculate_age(datetime. strptime(dia, '%Y-%m-%d')) <= 0:
                  l_dia = await pregunta_md(message,client,"Por favor, introduze una fecha en el futuro")
                  await message.author.send("Por favor, introduze una fecha en el futuro")

                  
                  dia = l_dia

              
              franja = await pregunta_md(message,client, "Ind??came brevemente en qu?? franja horaria te gustar??a que te atenid??semos")
              mensaje = await pregunta_md(message,client,"De acuerdo, cita el {0} . ??Podr??as explicar brevemente el motivo de tu visita?".format(dia,volver))
              
              res = await pregunta_md(message,client,"Perfecto, en resumen tienes una cita el d??a {} con qualquier miembro que se encuentre disponible para {}. Si es correcto escribe 1 o \"s??\" si no es correcto escribe 0 o \"no\"".format(dia,mensaje))
                
            
              if res == "1" or res == "s??" or res == "si" or res == "s" or res == "i":
                name = await pregunta_md(message,client,"vale, por favor ind??came tu nombre IC")
              
                
                
               
              
                mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
                mycursor = mydb.cursor()  
                mycursor.execute("SELECT `id`,`canal_cita` FROM entidad WHERE tipo_entidad = \"{0}\" AND servidor = {1}".format(volver,servidor_id))
                
                myresult = mycursor.fetchall()
                canal_id = 0
                for x in myresult:
                    canal_id = x[1]
                    entidad = x[0]
                channel = client.get_channel(canal_id)
                
                
               
        

                mensado = await channel.send("```Cita\nNombre: {0} (<@{1}>)\n Fecha: {2}\n Franja horaria: {3}\n Motivo: {4}\n\nPara confirmar la cita pulsa en ????\n Para rechazar la cita pulsa en ????\nPara marcar la cita como atendida pulsa en ???```".format(name,message.author,dia,franja,mensaje))
                
                mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
                mycursor = mydb.cursor()   
                
                sql = "INSERT INTO cita (server,entidad, persona_id, fecha, franja, message_id, motivo, nombre_ic) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"
                val = (servidor_id, entidad, message.author.id, dia, franja, mensado.id, mensaje, name)
                mycursor.execute(sql, val)
                
                mydb.commit()
                if mycursor.rowcount == 1:
                  #ok
                  await mensado.add_reaction("????")
                  
                  await mensado.add_reaction("????")
                  await mensado.add_reaction("???")
                  await message.author.send("```Perfecto, que tengas un buen d??a, en breves te confirmaremos tu cita para el d??a {}```".format(dia))
                  

                else:
                  await mensado.delete
                  await message.author.send("```Ups, ha ocurrido un error. Aseg??rate que todos los campos se han escrito con el formato indicado. Si el error persiste contacta a <@418102275974758419>``")
                
              else:
                await message.author.send("Cancelado, sin problema. Si quieres volver a empezar pon /cita en el discord")
        elif tipo_entidad == "LSFD":
          #si se trata del server de la ems
          print("LSFD")
          await LSFD(mydb, mycursor,message,client,entidad)
        elif tipo_entidad == "LSPD":
          await LSPD(mydb, mycursor, entidad,message,client)
          


@client.event
async def on_raw_reaction_add(payload):
    mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
    mycursor = mydb.cursor()   
    
    mycursor.execute("SELECT `id`,`canal_cita` FROM entidad WHERE discord = {0}".format(payload.guild_id))
       
    myresult = mycursor.fetchall()
    for x in myresult:
    
      mycursor.execute("SELECT * FROM cita WHERE entidad = {0} AND estado != \"Cancelada\" AND estado!= \"Atendida\"".format(x[0]))
                  
      myresulte = mycursor.fetchall()
  
      for p in myresulte:
        si = p[10] #cargamos los si
        no = p[11]
  
        if payload.message_id == p[5]:
          message = await client.get_channel(x[1]).fetch_message(p[5])
          reaction = message.reactions
          print(reaction[0].emoji)
          usuario = await client.fetch_user(p[2])
          for ids, val in enumerate(reaction):
            if reaction[ids].emoji == "???" and reaction[ids].count == 2:
             
              await usuario.send("```Hola, tu cita acaba de ser marcada como atendida, muchas gracias por confiar en nosotros```")
              await message.delete()
              sql = "DELETE FROM cita WHERE id = {0}".format(p[8]) #borramos la cita

              mycursor.execute(sql)
              
              mydb.commit()
                            
            elif reaction[ids].emoji == "????" and reaction[ids].count == 2 and no == 0:
              
              no= 1
            
              await usuario.send("```Lo sentimos, el d??a que has concertado cita no va haber nadie disponible la franja seleccionada, por favor pru??balo otro d??a u otra franja que pueda estar disponible```")
              
              await message.delete()
              sql = "DELETE FROM cita WHERE id = {0}".format(p[8]) #borramos la cita

              mycursor.execute(sql)
              
              mydb.commit()
            elif reaction[ids].emoji == "????" and reaction[ids].count == 2 and si == 0:
              
              await usuario.send("```Hola ????\nMe acaban de confirmar que habr?? alguien disponible para atenderte el {0} en la franja seleccionada.\nGracias :) ```\n".format(p[3]))
              si = 1
              sql = "UPDATE cita SET si = {0}, no = {1}, estado = \"Confirmada\" WHERE id = {2}".format(si, no, p[8])

              mycursor.execute(sql)
              
              mydb.commit()
         
    
     
client.run(TOKEN)