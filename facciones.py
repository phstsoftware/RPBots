import string
import time
import mysql.connector as mysql
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
from discord.ext import commands, tasks
import discord
# enter your server IP address/domain name
HOST = "sql586.main-hosting.eu" # or "domain.com"
# database name, if you want just to connect to MySQL server, leave it empty
DATABASE = "u197027072_rp_bots"
# this is the user you create
USER = "u197027072_rp"
# user password
PASSWORD = "]3gRyy!?L]"

def calculate_age(born):
    today = date.today()
    inter =  today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    print(inter*-1)
    return inter*-1
#====================================
# ANALISIS + HEMOGRAMA
#=====================================
async def analisis(message,inciales,nombre,sexo,nacimiento):
  """
    :param message: int, mensaje principal
    :param inciales: str, iniciales del paciente
    :param nombre: str, nombre del paciente
    :param sexo: str, sexo del paciente
    :param nacimineto: str, fecha de nacimiento en formato YYYY-MM-DD
  """
  maxval_normal_h = [
                        5.65, 16.6, 48.6, 5.9, 22.0, 101, 35, 37, 317, 15, 9.6, 5, 575,
                        1.5, 175, 75, 7.5, 40, 4.5, 8, 800, 10.5, 150, 5, 4.5, 145, 5,
                        110, 0.5, 1.3, 8.5, 200, 90, 160, 280, 1, 0.3, 1.9, 60, 34, 240
                    ]
  minval_normal_h = [
                        4.35, 13.2, 38.3, 4.5, 1.0, 80.0, 25.0, 28.0, 135.0, 5.0, 3.4,
                        1.0, 100.0, 0.2, 10.0, 45.0, 2.0, 20.0, 1.0, 2.0, 200.0, 8.0,
                        50.0, 3.5, 3.5, 135.0, 3.5, 70.0, 0.1, 0.7, 4.0, 80, 42, 0, 30,
                        0.3, 0, 0.3, 7, 6, 130
                    ]
                    
  maxval_normal_m = [
                        5.13, 15, 44.9, 5.2, 22.0, 101, 35, 37, 371, 15, 9.6, 5, 575,
                        1.5, 175, 75, 7.5, 40, 4.5, 8, 800, 10.5, 150, 5, 4.5, 145, 5,
                        110, 0.5, 1.2, 7.5, 200, 90, 160, 220, 1, 0.3, 1.9, 35, 40, 240
                    ]
  minval_normal_m = [
                        3.92, 11.6, 35.4, 4, 1.0, 80.0, 25.0, 28.0, 157.0, 5.0, 3.4,
                        1.0, 100.0, 0.2, 10.0, 45.0, 2.0, 20.0, 1.0, 2.0, 200.0, 8.0,
                        50.0, 3.5, 3.5, 135.0, 3.5, 70.0, 0.1, 0.5, 2.5, 80, 42, 0, 30,
                        0.3, 0, 0.3, 7, 8, 130
                    ]
                  
  textos = [
      "Recuento de glóbulos rojos: {} millones de células",
      "Hemoglobina: {} gramos/dL", "Hematocrito: {} por cada 100",
      "Hematíes: {}",
      "IDH (Índice de Dispersión de los Hematíes): {}",
      "VCM (Volumen corpuscular medio): {} fL",
      "HCM (Hemoglobina corpuscular media): {} pg",
      "CHCM (Concentración de Hemoglobina Corpuscular Media): {} g/dL",
      "Recuento de plaquetas: {} mil/mcL",
      "VPM (Volumen Plaquetario Medio): {} fL",
      "Recuento de glóbulos blancos / Leucocitos: {} millones de células/mcL",
      "Eosinófilos: {} %", "Eosinófilos: {} /mcL", "Basófilos: {} %",
      "Basófilos: {} /mcL", "Neutrófilos: {} %",
      "Neutrófilos: {} mil/mcL", "Linfocitos: {} %",
      "Linfocitos: {} mil/mcL", "Monocitos: {} %", "Monocitos: {} /mcL",
      "Calcio: {} mg/dL", "Hierro: {} mg/dL", "Fósforo: {} mg/dL",
      "Potasio: {} meq/L", "Sodio: {} meq/L",
      "Albúmina sérica: {} g/dL", "Glucosa: {} mg/dL",
      "Nitrógeno de urea: {} g/L", "Creatinina: {} mg/dL",
      "Ácido úrico: {} mg/dL", "Colesterol: {} mg/dL (<200)",
      "Lipoproteína de baja densidad / LDL: {} mg/dL",
      "Lipoproteína de alta densidad / HDL: {} mg/dL",
      "Triglicéridos: {} mg/dL", "Bilirrubina total: {} mg/dL",
      "Bilirrubina directa: {} mg/dL",
      "Bilirrubina indirecta: {} mg/dL",
      "Transaminasa alcalina (ALT): {} UI/L",
      "Aspartato de amnitransferasa (AST): {} UI/L",
      "Lactato Deshidrogenasa (LDH): {} UI/L"
  ]
  maxval = []
  minval = []
  valor = []
  lectura = []

  # Hemograma
  class PDF(FPDF):
      def header(self):
        self.image('https://i.imgur.com/qTGi7fA.png', 10, 10, 40, 17)
        self.image('https://i.imgur.com/TQqxnrO.png', 170, 5, 28, 28)
        self.ln(20)

  pdf = PDF()
  cip = "{}759214538".format(inciales)
  pdf.add_page()
  pdf.set_font('Arial', "BU", 12)
  pdf.write(10, "Datos del paciente:")
  pdf.ln(10)
  pdf.set_font('Arial', "", 12)
  pdf.write(10, "Paciente: {}".format(nombre))
  pdf.ln(10)
  pdf.write(10, "CIP: {}".format(cip))
  pdf.ln(10)
  pdf.write(10, "Fecha de nacimiento: {}".format(nacimiento))
  pdf.set_font('Arial', "BU", 12)
  pdf.ln(10)
  pdf.write(10, "Hemograma:")
  pdf.ln(10)
  pdf.set_font('Arial', "", 12)

  if sexo == "h":
      for idx, val in enumerate(maxval_normal_h):
          print(idx)

          probabilidad = round(random.uniform(1, 100), 2)
          if probabilidad <= 90:

              maxval.append(maxval_normal_h[idx])
              minval.append(minval_normal_h[idx])

          elif probabilidad <= 95:
              global puestos
              puestos = 0
              porcentaje = round(random.uniform(40, 80), 2)
              tot = porcentaje / 100
              global maxval_abajo_h
              maxval_abajo_h = []
              operacion = tot * maxval_normal_h[idx]
              global minval_abajo_h
              minval_abajo_h = []
              maxval_abajo_h.append(operacion)
              operacion = tot * minval_normal_h[idx]
              minval_abajo_h.append(operacion)
              maxval.append(maxval_abajo_h[puestos])
              minval.append(minval_abajo_h[puestos])
              puestos = puestos +1

          else:
              
              time.sleep(0.5)
              
              global puestos2
              puestos2 = 0
              porcentaje = round(random.uniform(105, 140), 2)
              tot = porcentaje / 100
              operacion = tot * maxval_normal_h[idx]
              global maxval_arriba_h
              maxval_arriba_h = []
              maxval_arriba_h.append(operacion)
              global minval_arriba_h
              minval_arriba_h = []
              operacion = tot * minval_normal_h[idx]
              minval_arriba_h.append(operacion)
              maxval.append(maxval_arriba_h[puestos2])
              minval.append(minval_arriba_h[puestos2])
              puestos2 = puestos2+1

          valor.append(
              round(random.uniform(minval[idx], maxval[idx]), 2))
          print(maxval[idx])
          print(minval[idx])
          if (valor[idx] > maxval_normal_h[idx]
                  or valor[idx] < minval_normal_h[idx]):

              pdf.set_text_color(255, 0, 0)
          else:
              pdf.set_text_color(0, 0, 0)
          lectura.append(textos[idx].format(valor[idx]))

          pdf.write(10, lectura[idx])
          pdf.ln(10)
          pdf.set_text_color(0, 0, 0)
          maximo_texto = "VN: {} - {}".format(round(minval_normal_h[idx],2),round(maxval_normal_h[idx],2))
          pdf.set_font('Arial', "I", 12)
          pdf.write(12,maximo_texto)
          pdf.set_font('Arial', "", 12)
          pdf.ln(10)

          if (idx == 14):
              pdf.set_font('Arial', "U", 12)
              pdf.ln(10)
              pdf.write(10, "Perfil renal:")
              pdf.ln(10)
              pdf.set_font('Arial', "", 12)
          if (idx == 30):
              pdf.set_font('Arial', "U", 12)
              pdf.ln(10)
              pdf.write(10, "Perfil lipídico:")
              pdf.ln(10)
              pdf.set_font('Arial', "", 12)
          if (idx == 34):
              pdf.set_font('Arial', "U", 12)
              pdf.ln(10)
              pdf.write(10, "Perfil hepático:")
              pdf.ln(10)
              pdf.set_font('Arial', "", 12)
  else:
      for idx, val in enumerate(maxval_normal_m):
          print(idx)

          probabilidad = round(random.uniform(1, 100), 2)
          if probabilidad <= 90:

              
              maxval.append(maxval_normal_m[idx])
              minval.append(minval_normal_m[idx])

          elif probabilidad <= 95:
              global puestos3
              puestos3 = 0
              porcentaje = round(random.uniform(40, 80), 2)
              tot = porcentaje / 100
              global maxval_abajo_m
              maxval_abajo_m = []
              operacion = tot * maxval_normal_m[idx]
              global minval_abajo_m
              minval_abajo_m = []
              maxval_abajo_m.append(operacion)
              operacion = tot * minval_normal_m[idx]
              minval_abajo_m.append(operacion)
              maxval.append(maxval_abajo_m[puestos3])
              minval.append(minval_abajo_m[puestos3])
              puestos3 = puestos3 +1

          else:
              global puestos4
              puestos4 = 0
              porcentaje = round(random.uniform(105, 140), 2)
              tot = porcentaje / 100
              operacion = tot * maxval_normal_m[idx]
              global maxval_arriba_m
              maxval_arriba_m = []
              maxval_arriba_m.append(operacion)
              global minval_arriba_m
              minval_arriba_m = []
              operacion = tot * minval_normal_m[idx]
              minval_arriba_m.append(operacion)
              maxval.append(maxval_arriba_m[puestos4])
              minval.append(minval_arriba_m[puestos4])
              puestos4 = puestos4+1


          valor.append(
              round(random.uniform(minval[idx], maxval[idx]), 2))
          print(maxval[idx])
          print(minval[idx])
          if (valor[idx] > maxval_normal_m[idx]
                  or valor[idx] < minval_normal_m[idx]):

              pdf.set_text_color(255, 0, 0)
          else:
              pdf.set_text_color(0, 0, 0)
          lectura.append(textos[idx].format(valor[idx]))

          pdf.write(10, lectura[idx])
          pdf.ln(10)
          pdf.set_text_color(0, 0, 0)
          maximo_texto = "VN: {} - {}".format(round(minval_normal_m[idx],2),round(maxval_normal_m[idx],2))
          pdf.set_font('Arial', "I", 12)
          pdf.write(12,maximo_texto)
          pdf.set_font('Arial', "", 12)
          pdf.ln(10)
          if (idx == 14):
              pdf.set_font('Arial', "U", 12)
              pdf.ln(10)
              pdf.write(10, "Perfil renal:")
              pdf.ln(10)
              pdf.set_font('Arial', "", 12)
          if (idx == 30):
              pdf.set_font('Arial', "U", 12)
              pdf.ln(20)
              pdf.write(10, "Perfil lipídico:")
              pdf.ln(10)
              pdf.set_font('Arial', "", 12)
          if (idx == 34):
              pdf.set_font('Arial', "U", 12)
              pdf.ln(10)
              pdf.write(10, "Perfil hepático:")
              pdf.ln(10)
              pdf.set_font('Arial', "", 12)
  pdf.ln(5)
  pdf.set_font('Arial', "I", 12)

  file_name = "{}-hemograma.pdf".format(inciales)

  pdf.output(file_name, 'F')
  await message.channel.send(file=discord.File(file_name))


  
  await message.channel.send("Procesando el análisis de orina de {}, un momento".format(nombre),delete_after = 30)
  
  maxval_normal_h = [
    8.0,1.03,1,1,1,1,1,1,1
  ]
  minval_normal_h = [
    4.6,1.006,0,0,0,0,0,0,0
  ]
  
  

  textos = [
      "- Acidez (ph): {}",
      "- Concentración: {}",
      "- Proteína: {}",
      "- Glucosa: {}",
      "- Cuerpos cetónicos: {}", 
      "- Bilirrubina: {}",
      "- Indicios de infección: {}",
      "- Sangre:\nHematíes (glóbulos rojos): {}","Leucocitos (glóbulos blancos): {}"
  ]

  maxval = []
  minval = []
  valor = []
  lectura = []

  # orina
  class PDF(FPDF):
      def header(self):
        self.image('https://i.imgur.com/qTGi7fA.png', 10, 10, 40, 17)
        self.image('https://i.imgur.com/TQqxnrO.png', 170, 5, 28, 28)
        self.ln(20)
      

  pdf = PDF()
  cip = "{}759214538".format(inciales)
  pdf.add_page()
  pdf.set_font('Arial', "BU", 12)
  pdf.write(10, "Datos del paciente:")
  pdf.ln(10)
  pdf.set_font('Arial', "", 12)
  pdf.write(10, "Paciente: {}".format(nombre))
  pdf.ln(10)
  pdf.write(10, "CIP: {}".format(cip))
  pdf.ln(10)
  pdf.write(10, "Fecha de nacimiento: {}".format(nacimiento))
  pdf.set_font('Arial', "BU", 12)
  pdf.ln(10)
  pdf.write(10, "Análisis de orina:")
  pdf.ln(10)
  pdf.set_font('Arial', "", 12)


  for idx, val in enumerate(maxval_normal_h):
          print(idx)

          probabilidad = round(random.uniform(1, 100), 2)
          if probabilidad <= 90:

              maxval.append(maxval_normal_h[idx])
              minval.append(minval_normal_h[idx])

          elif probabilidad <= 95 and idx <2:
              
              pdf.ln(12)
              global esc
              esc = 0
              porcentaje = round(random.uniform(40, 80), 2)
              tot = porcentaje / 100
              global n_maxval_abajo_h
              n_maxval_abajo_h = []
              operacion = tot * maxval_normal_h[idx]
              global n_minval_abajo_h
              n_minval_abajo_h = []
              n_maxval_abajo_h.append(operacion)
              operacion = tot * minval_normal_h[idx]
              n_minval_abajo_h.append(operacion)
              maxval.append(n_maxval_abajo_h[esc])
              minval.append(n_minval_abajo_h[esc])
              esc = esc +1

          elif idx < 2:
              
              time.sleep(0.5)
              pdf.ln(11)
              global n_puestos2
              n_puestos2 = 0
              porcentaje = round(random.uniform(105, 140), 2)
              tot = porcentaje / 100
              operacion = tot * maxval_normal_h[idx]
              global n_maxval_arriba_h
              n_maxval_arriba_h = []
              n_maxval_arriba_h.append(operacion)
              global n_minval_arriba_h
              n_minval_arriba_h = []
              operacion = tot * minval_normal_h[idx]
              n_minval_arriba_h.append(operacion)
              maxval.append(n_maxval_arriba_h[n_puestos2])
              minval.append(n_minval_arriba_h[n_puestos2])
              n_puestos2 = n_puestos2+1
          if idx > 1:
            valor.append(
              round(random.uniform(0, 100), 0))
            if valor[idx] < 20:
                lectura.append(textos[idx].format("Positivo"))
            else:
              lectura.append(textos[idx].format("Negativo"))
          else:
            valor.append(
              round(random.uniform(minval[idx], maxval[idx]), 2))
          
            if (valor[idx] > maxval_normal_h[idx]
                    or valor[idx] < minval_normal_h[idx]):
                pdf.set_text_color(255, 0, 0)
            else:
                pdf.set_text_color(0, 0, 0)
            lectura.append(textos[idx].format(valor[idx]))

          pdf.write(10, lectura[idx])
          pdf.ln(10)
          pdf.set_text_color(0, 0, 0)
          if idx < 2:
            maximo_texto = "VN: {} - {}".format(round(minval_normal_h[idx],2),round(maxval_normal_h[idx],2))
          else:
            maximo_texto = "VN: Negativo"
          pdf.set_font('Arial', "I", 12)
          pdf.write(12,maximo_texto)
          pdf.set_font('Arial', "", 12)
          pdf.ln(10)

          
  


  pdf.set_font('Arial', "BU", 12)
  pdf.ln(10)
  pdf.write(10, "Prueba de detección de drogas:")
  pdf.ln(10)
  pdf.set_font('Arial', "", 12)
  time.sleep(0.5)
  pdf.write(12," - Marihuana: Negativo\n - Opiáceos: Negativo\n - Anfetaminas: Negativo\n - Cocaína: Negativo\n - Cannabis: Negativo\n - Éxtasis: Negativo\n - Benzodiacepinas: Negativo")
  
  file_name = "{}-orina.pdf".format(inciales)

  pdf.output(file_name, 'F')
  await message.channel.send(file=discord.File(file_name))
async def pregunta(mensaje, client, texto):
  """
  :param mensaje: int, mensaje principal
  :param texto: str, Texto a mandar
  """
  
  await mensaje.channel.send("```{0}```".format(texto),delete_after = 60)

  def check(m):
      global volver
      volver = m.content
      return m.content != "" and m.channel == mensaje.channel and m.author == mensaje.author

  await client.wait_for("message", check=check)
  time.sleep(1)
  msg = await mensaje.channel.fetch_message(mensaje.channel.last_message_id)
        
  await msg.delete()
  return volver
async def pregunta_md(mensaje, client, texto):
  """
  :param mensaje: int, mensaje principal
  :param texto: str, Texto a mandar
  """
  
  await mensaje.author.send("```{0}```".format(texto),delete_after = 60)

  def check(m):
      global volver
      volver = m.content
      return m.content != "" and m.author == mensaje.author

  await client.wait_for("message", check=check)
  time.sleep(1)
  
  return volver
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
           
def calc_edad(born):
    today = date.today()
    inter =  today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    
    return inter

async def LSFD(mydb, mycursor,message,client, entidad):
        """
        :param mydb: Base de datos
        :param mycursor: My cursor de la base de datos
        :param message: mensaje
        :param client: cliente
        :param entidad: id de la entidad
        """
        grupos_sanguíneos = ["0-","0+","A-","A+","B-","B+","AB-","AB+"]
        
        print("LSFD")
        if message.content == "/nuevo paciente":
          #create object
            await message.delete()
            nom = await pregunta_md(message,client,"Introduzca el nombre del paciente:")
            sex = await pregunta_md(message,client,"Escriba \"h\" si es un hombre y \"m\" si es una mujer:")

            nace = await pregunta_md(message,client,"Escriba la fecha de nacimiento del paciente en formato YYYY-MM-DD:")
            telefono = await pregunta_md(message,client, "Escriba el número de teléfono del paciente:")
            al_db = await pregunta_md(message,client,"En el caso de que tenga alergias descríbalas, en caso contrario escriba \"-\"")
            med_db = await pregunta_md(message,client,"En el caso de que tenga problemas médicos descríbalas, en caso contrario escriba \"-\"")
            sang_db = await pregunta_md(message,client,"En el caso de que sepa su grupo sanguíneo indíquelo, si no lo sabe escriba \"-\"")
            seg_db = await pregunta_md(message, client, "En el caso de que tenga seguro médico escríba la fecha de vencimiento en formato YYYY-MM-DD, si no tiene escriba \"-\"")
            iniciales_pac = await pregunta_md(message,client,  "Escriba EN MAYÚSCULAS las 2 primeras letras del nombre y las 2 primeras letras del apellido:  ")
            
            

            guild = message.author.guild
            channl = await guild.create_text_channel(nom)
            
            ms = await channl.send("```Nombre: {}\nSexo: {}\nFecha nacimiento: {}\nGrupo sanguíneo: {}\nTeléfono Contacto: {}\nAlergias Conocidas: {}\nProblemas Mèdicos: {}\nSeguro Médico Hasta: {}```".format(
              nom,sex,nace,sang_db,telefono,al_db,med_db,seg_db))
            mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
            mycursor = mydb.cursor()   
           
            sql = "INSERT INTO clientes (entidad,nombre, sexo, sangre, nace, tel, al, med, chan, ms, ini, seguro_med) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (entidad,nom, sex, sang_db, nace, telefono, al_db, med_db, channl.id, ms.id, iniciales_pac, seg_db)
            
            mycursor.execute(sql, val)
            
            mydb.commit()
            await message.author.send("Creado <#{0}>".format(channl.id))
           
        elif message.content == "/mostrar paciente":
            mycursor.execute("SELECT nombre, sexo, sangre, nace, tel, al, med, seguro_med FROM clientes WHERE entidad = {0} AND chan = {1}".format(entidad,message.channel.id)) #buscamos al paciente, si no existe se le pregunta_mdran los datos
            myresult = mycursor.fetchall()
            enc = 0
            for x in myresult:
                  enc = 1
                  nom = x[0]
                  sex = x[1]
                  sang_db = x[2]
                  nace = x[3]
                  telefono = x[4]
                  al_db = x[5]
                  med_db = x[6]
                  seg_db = x[7]
            await message.delete()
            #except:
            if enc==1:
              #si existe
              channl = message.channel
              ms = await channl.send("```Nombre: {}\nSexo: {}\nFecha nacimiento: {}\nGrupo sanguíneo: {}\nTeléfono Contacto: {}\nAlergias Conocidas: {}\nProblemas Mèdicos: {}\nSeguro Médico Hasta: {}```".format(
              nom,sex,nace,sang_db,telefono,al_db,med_db,seg_db))
            else:
              await message.channel.send("```El paciente no ha sido encontrado en la base de datos```",delete_after = 20)
        elif message.content == "/enlazar paciente":
            await message.delete()
            nom = await pregunta_md(message,client,"Introduzca el nombre del paciente:")
            sex = await pregunta_md(message,client,"Escriba \"h\" si es un hombre y \"m\" si es una mujer:")

            nace = await pregunta_md(message,client,"Escriba la fecha de nacimiento del paciente en formato YYYY-MM-DD:")
            telefono = await pregunta_md(message,client, "Escriba el número de teléfono del paciente:")
            al_db = await pregunta_md(message,client,"En el caso de que tenga alergias descríbalas, en caso contrario escriba \"-\"")
            med_db = await pregunta_md(message,client,"En el caso de que tenga problemas médicos descríbalas, en caso contrario escriba \"-\"")
            sang_db = await pregunta_md(message,client,"En el caso de que sepa su grupo sanguíneo indíquelo, si no lo sabe escriba \"-\"")
            seg_db = await pregunta_md(message, client, "En el caso de que tenga seguro médico escríba la fecha de vencimiento en formato YYYY-MM-DD, si no tiene escriba \"-\"")
            iniciales_pac = await pregunta_md(message,client,  "Escriba EN MAYÚSCULAS las 2 primeras letras del nombre y las 2 primeras letras del apellido:  ")
            
            
            channl = message.channel
            ms = await channl.send("```Nombre: {}\nSexo: {}\nFecha nacimiento: {}\nGrupo sanguíneo: {}\nTeléfono Contacto: {}\nAlergias Conocidas: {}\nProblemas Mèdicos: {}\nSeguro Médico Hasta: {}```".format(
              nom,sex,nace,sang_db,telefono,al_db,med_db,seg_db))
            mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
            mycursor = mydb.cursor()   
            print("conectado")
            sql = "INSERT INTO clientes (entidad,nombre, sexo, sangre, nace, tel, al, med, chan, ms, ini, seguro_med) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (entidad,nom, sex, sang_db, nace, telefono, al_db, med_db, channl.id, ms.id, iniciales_pac, seg_db)
            
            mycursor.execute(sql, val)
            
            mydb.commit()
          
            await message.author.send("Creado <#{0}>".format(channl.id))
         
        
        
        
        elif message.content == "/analisis":
#                  db = cluster["Clientes"]
                    #try:
                    enc = 0
                    mycursor.execute("SELECT `nombre`,`sexo`,`nace`, `ini`, `chan` FROM clientes WHERE entidad = {0} AND chan = {1}".format(entidad,message.channel.id)) #buscamos al paciente, si no existe se le pregunta_mdran los datos
                    myresult = mycursor.fetchall()
                    for x in myresult:
                          print(x)
                          nombre = x[0]
                          inciales = x[3]
                          nacimiento = x[2]
                          sexo =x[1]
  
                          enc=1
                   
                     
                    
                    await message.delete()
                    
                    
                    #except:
                    if enc!=1:
                      nombre = await pregunta_md(message, client,"Escriba el nombre del paciente")
                      inciales = await pregunta_md(message, client,"Del CIP, escriba las iniciales del paciente (en mayúscula)")
                      nacimiento = await pregunta_md(message, client,"Escriba la fecha de naciemiento del pacient en format YYYY-MM-DD")
                      sexo = await pregunta_md(message, client, "Escriba h si es un hombre o m si es una mujer")
                    #llamamos a la funcion que realiza el analisis
                    await analisis(message,inciales,nombre, sexo, nacimiento)
                  
                   
        elif message.content == "/seguro":
            await message.delete()
            enc = 0
            mycursor.execute("SELECT * FROM clientes WHERE entidad = {0} AND chan = {1}".format(entidad,message.channel.id)) #buscamos al paciente, si no existe se le pregunta_mdran los datos
            myresult = mycursor.fetchall()
            for x in myresult:
              nombre2 = x[3]
              sexo2 = x[4]
              nacimiento2 = x[6]
              id_mens = x[11]
              seguro =str(x[13])
              sab_sang = x[5]
              tel = x[7]
              al = x[8]
              med = x[9]
              print(x)
              print(seguro)
              enc = 1         
            if enc == 0:
                    await message.channel.send("```Paciente no encontrado, escriba /enlazar paciente para enlazarlo```",delete_after = 60)
            else:
              dias_seguro = await pregunta_md(message, client,"Introduzca cuantos días ha contratado el seguro")
              if str(seguro)!="None" :
               #ya hay uno
                if calculate_age(datetime.strptime(seguro,"%Y-%m-%d"))>0:
                 #no ha caducado
                  end_date = date.today() + timedelta(days=int(dias_seguro))
                  mens_edit = await message.channel.fetch_message(id_mens)
                  await mens_edit.edit(content = "```Nombre: {}\nSexo: {}\nFecha nacimiento: {}\nGrupo sanguíneo: {}\nTeléfono Contacto: {}\nAlergias Conocidas: {}\nProblemas Mèdicos: {}\nSeguro Médico Hasta: {}```".format(nombre2,sexo2,nacimiento2,sab_sang,tel,al,med,end_date.strftime("%Y-%m-%d")))
                  #db = cluster["Clientes"]
                  mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
                  mycursor = mydb.cursor()  
                  sql = "UPDATE clientes SET seguro_med = \"{0}\" WHERE chan = {1}".format(str(end_date.strftime("%Y-%m-%d")),message.channel.id)
                  print(sql)
                  mycursor.execute(sql)
                  
                  mydb.commit()
                  await message.channel.send("```Actualizado```",delete_after = 60)
                 
                  
                else:
                  end_date = date.today() + timedelta(days=int(dias_seguro))
                  print(end_date)
                  mens_edit = await message.channel.fetch_message(id_mens)
                  print(id_mens)
                  await mens_edit.edit(content = "```Nombre: {}\nSexo: {}\nFecha nacimiento: {}\nGrupo sanguíneo: {}\nTeléfono Contacto: {}\nAlergias Conocidas: {}\nProblemas Mèdicos: {}\nSeguro Médico Hasta: {}```".format(nombre2,sexo2,nacimiento2,sab_sang,tel,al,med,end_date.strftime("%Y-%m-%d")))
                 # db = cluster["Clientes"]

                  mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
                  mycursor = mydb.cursor()  
                  sql = "UPDATE clientes SET seguro_med = \"{0}\" WHERE chan = {1}".format(str(end_date.strftime("%Y-%m-%d")),message.channel.id)
                  print(sql)
                  mycursor.execute(sql)
                  
                  mydb.commit()
                  await message.channel.send("```Actualizado```",delete_after = 60)
              else:
                  

                  end_date = date.today() + timedelta(days=int(dias_seguro))
                  print(end_date)
                  mens_edit = await message.channel.fetch_message(id_mens)
                  print(id_mens)
                  await mens_edit.edit(content = "```Nombre: {}\nSexo: {}\nFecha nacimiento: {}\nGrupo sanguíneo: {}\nTeléfono Contacto: {}\nAlergias Conocidas: {}\nProblemas Mèdicos: {}\nSeguro Médico Hasta: {}```".format(nombre2,sexo2,nacimiento2,sab_sang,tel,al,med,end_date.strftime("%Y-%m-%d")))
                 # db = cluster["Clientes"]

                  mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
                  mycursor = mydb.cursor()  
                  sql = "UPDATE clientes SET seguro_med = \"{0}\" WHERE chan = {1}".format(str(end_date.strftime("%Y-%m-%d")),message.channel.id)
                  print(sql)
                  mycursor.execute(sql)
                  
                  mydb.commit()
                  await message.channel.send("```Actualizado```",delete_after = 60)
        elif message.content == "/psicotecnico":
                  await message.delete()
                  await message.channel.send(
                      "Lea el siguiente mensaje al paciente: \"Se le van a formular una serie de oraciones, por favor responda del 1 al 3 cuando le sucede siendo 1 muchas veces y 3 nunca\"\n 1  -> Muchas veces\n 3  -> Nunca\nSe procede a inciar el test, responda con el carácter numérico"
                  ,delete_after = 500)
                  time.sleep(2)
                  oraciones_psico = ["Cuando trabajo bajo presión, me pongo nervioso/a","Me gusta indagar e investigar sobre el por qué de las cosas","Se me da bien resolver problemas de una manera rápida y eficaz","Me gusta dejarme llevar por mis sentimientos y corazonadas","Mi pensamiento suele ser muy ordenado","Me considero una persona creativa e innovadora","Mi objetivo en la vida es escalar puestos y ser reconocido/a","Soy una persona bastante despistada","Me exijo constantemente efectividad y buenos resultados en mis estudios","Me gusta escuchar a los demás y comprender sus sentimientos","Soy capaz de entender mis emociones y expresarlas correctamente","Tengo facilidad para pensar y razonar de forma lógica","Soy una persona muy curiosa y me gusta estudiar los fenómenos de todo lo que nos rodea"]
                  oraciones_armas = ["Cuando estoy frustrado/a, muestro mi enfado","A menudo tengo mal humor","Cuando la gente dice algo que me molesto, discuto sin dudarlo","Si me provocan, puedo llegar a pegar a la otra persona","Soy una persona tranquila y sosegada","Puedo llegar a amenazar con violencia","Pierdo los nervios sin razón aparente","Me cuesta bastante controlar mi genio"]
                  global psico_count
                  psico_count = 0
                  for idx, val in enumerate(oraciones_psico):
                    texto = "-{} ->  \"{}\"".format(idx,oraciones_psico[idx])
                    await message.channel.send(texto,delete_after = 120)
                    def check(m):
                      global puntos
                      puntos = m.content
                      return m.content != "" and m.channel == message.channel

                    await client.wait_for("message", check=check)
                    psico_count += int(puntos)
                    time.sleep(2)
                    msg = await message.channel.fetch_message(message.channel.last_message_id)
                    
                    await msg.delete()
                  await message.channel.send(
                      "Parte finalizada, pasamos a la siguiente batería de oraciones\nLea el siguiente mensaje al paciente: \"Se le van a formular una serie de oraciones, por favor responda del 1 al 5 como se encuentra siendo 1 Totalmente en desacuerdo y 5 Totalmente en acuerdo\"\n 1  -> Totalmente en desacuerdo\n 5  -> Totalmente en acuerdo\nSe procede a inciar el test, responda con el carácter numérico"
                  ,delete_after = 500)
                  global armas_count
                  armas_count = 0
                  for idx, val in enumerate(oraciones_armas):     
                    texto = "-{} ->  \"{}\"".format(idx,oraciones_armas[idx])
                    await message.channel.send(texto,delete_after = 120)
                    def check(m):
                      global puntos
                      puntos = m.content
                      return m.content != "" and m.channel == message.channel and m.author == message.author

                    await client.wait_for("message", check=check)
                    armas_count += int(puntos)
                    time.sleep(1)
                    msg = await message.channel.fetch_message(message.channel.last_message_id)
                    
                    await msg.delete()
                  #Hacemos una regla de 3 para sacar la nota
                  tot_1 = armas_count * 10
                  tot_2 = tot_1/(len(oraciones_armas)*5)
                  resultado = []
                  
                  
                  if tot_2 < 9:
                    #aprobado
                    resultado.append(1)
                  else:
                    resultado.append(0)
                  pruebas = ["vista","oído","tensión"]
                  for idx, val in enumerate(pruebas):    
                    await message.channel.send(
                        "Haga al paciente una prueba de {}, anote un \"1\" si el resultado es correcto o un \"0\" si no es correcto".format(pruebas[idx])
                    ,delete_after = 500)
                    def check(m):
                        global respuesta
                        time.sleep(1)
                        respuesta = m.content
                        return m.content != "" and m.channel == message.channel and m.author == message.author

                    await client.wait_for("message", check=check)
                    resultado.append(int(respuesta))
                    time.sleep(1)
                    msg = await message.channel.fetch_message(message.channel.last_message_id)
                    
                    await msg.delete()
                  global result
                  result = ""
                  for idx, val in enumerate(resultado):
                    if resultado[idx] == 1:
                      result = "APTO"
                    else:
                      result = "NO APTO"
                      break
                  if result == "APTO":
                    await message.channel.send(
                      "El resultado de esta parte es APTO, por favor concerte cita con el paciente para el análisis de sangre/orina, recuérdele la importancia de venir en AYUNAS."
                  ,delete_after = 500)
                  else:
                    await message.channel.send(
                      "El resultado de esta parte es NO APTO, por favor indique al paciente que venga otro día para volver a realizar el test"
                  ,delete_after = 500)
                  
        elif message.content == "/resguardo":
                  await message.delete()
                  
                  mycursor.execute("SELECT `nombre`,`sexo`,`nace`, `ini`, `ms`, `sangre` FROM clientes WHERE entidad = {0} AND chan = {1}".format(entidad,message.channel.id))
                  myresult = mycursor.fetchall()
                  enc = 0
                  for p in myresult:
                        nombre = p[0]
                        inciales2 = p[3]
                        nacimiento = p[2]
                        sexo2 =p[1]
                        sab_sang = p[5]
                        id_mens = p[4]
                        enc=1
                 # db = cluster["Clientes"]

                 
                    
                 
                  

                  if enc == 0:
                    await message.channel.send("Paciente no encontrado, escriba /enlazar paciente para enlazarlo",delete_after = 60)
                  else:
                    global pers_name
                    global num_placa
                  #  db = cluster["Clientes"]
                    mycursor.execute("SELECT `nombre`,`numero_de_placa` FROM empleados WHERE entidad = {0} AND discord_id = {1}".format(entidad,message.author.id))
                    myresult = mycursor.fetchall()
                   
                    for x in myresult:
                        pers_name = x[0]
                       
                        num_placa = x[1]
                    
                   
                    
                  
                  
                    today = date.today()  
                    fecha = today.strftime("%Y-%m-%d")
  
                    img = Image.open("plant_psicotecnico.png")
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.truetype('Roboto-Regular.ttf', 14)
                    eje_x = 310   #Ponlo bien porfa xd
                    eje_x_2 = 530
                    draw.text((eje_x,135), nombre, (0,0,0), font=font)
                    draw.text((eje_x_2,157), str(nacimiento), (0,0,0), font=font)
                    draw.text((eje_x,178), "APTO", (0,0,0), font=font)
                    draw.text((eje_x,225), pers_name, (0,0,0), font=font)
                    draw.text((eje_x_2,245), num_placa, (0,0,0), font=font)
                    draw.text((eje_x_2,265), fecha, (0,0,0), font=font)
                    draw.text((eje_x,290), pers_name, (0,0,0), font=font)          
                    img.save("psicotecnico.png")
                    await message.channel.send(file=discord.File("psicotecnico.png")) 
                    #BUENO:
                    channel = client.get_channel(can_resultados)
                    #TEST:
                    #channel = client.get_channel(862358903949361192)
  
                    await channel.send(file=discord.File("psicotecnico.png"))
        
        elif message.content == "/sangre":
                  await message.delete()
                  enc = 0
                #  db = cluster["Clientes"]
                  mycursor.execute("SELECT `nombre`,`sexo`,`nace`, `ini`, `ms`, `sangre`, `tel`, `al`, `med`, `seguro_med` FROM clientes WHERE entidad = {0} AND chan = {1}".format(entidad,message.channel.id))
                  myresult = mycursor.fetchall()
                  for p in myresult:
                        nombre2 = p[0]
                        inciales2 = p[3]
                        nacimiento2 = str(p[2])
                        sexo2 =p[1]
                        sab_sang = p[5]
                        id_mens = p[4]
                        tel = p[6]
                        al = p[7]
                        med = p[8]
                        seg = p[9]
                        enc=1
                  
                  if enc == 0:
                    await message.channel.send("Paciente no encontrado, escriba /enlazar paciente para enlazarlo",delete_after = 60)
                  else:
                    
                  
                
                    if sab_sang == "no" or sab_sang == "0" or sab_sang == "-":
                      indice = round(random.uniform(0, len(grupos_sanguíneos)-1), 0)
                      print(indice)
                      grupo_paciente = grupos_sanguíneos[int(indice)]
                      mens_edit = await message.channel.fetch_message(id_mens)
                      await mens_edit.edit(content = "Nombre: {}\nSexo: {}\nFecha nacimiento: {}\nGrupo sanguíneo: {}\nTeléfono Contacto: {}\nAlergias Conocidas: {}\nProblemas Médicos: {}\nSeguro Médico Hasta: {}".format(nombre2,sexo2,nacimiento2,grupo_paciente,tel,al,med,seg))
                    #  db = cluster["Clientes"]

                      mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
                      mycursor = mydb.cursor()  
                      sql = "UPDATE clientes SET sangre = \"{0}\" WHERE chan = {1}".format(grupo_paciente,message.channel.id)
                      print(sql)
                      mycursor.execute(sql)
                      
                      mydb.commit()
                      
                    
                      
                    else:
                      
                      grupo_paciente = sab_sang
                    
                    
                    
                  #  db = cluster["Clientes"]

                 
                  t = 0
                  mycursor.execute("SELECT `nombre`,`numero_de_placa` FROM empleados WHERE entidad = {0} AND discord_id = {1}".format(entidad,message.author.id))
                  myresult = mycursor.fetchall()
           
                  global pers_med
                  pers_med = ""
                  global pers_placa
                  pers_placa = "0000"
                  for x in myresult:
                    pers_med = x[0]
                    pers_placa = str(x[1])
                   
                    
                    
                    
                    
                  today = date.today()  
                  fecha = today.strftime("%Y-%m-%d")
                  edad2 = calc_edad(datetime.strptime(nacimiento2,"%Y-%m-%d"))
                  img = Image.open("plant_sangre.png")
                  draw = ImageDraw.Draw(img)
                  font = ImageFont.truetype("Roboto-Regular.ttf", 14)
                  eje_x = 310   #Ponlo bien porfa xd
                  eje_x_2 = 530
                  draw.text((eje_x,134), nombre2, (0,0,0), font=font)
                  draw.text((eje_x,176), grupo_paciente, (0,0,0), font=font)
                  draw.text((eje_x,155), str(edad2), (0,0,0), font=font)
                  
                  
                  draw.text((eje_x,225), pers_med, (0,0,0), font=font)
                  draw.text((eje_x_2,245), pers_placa, (0,0,0), font=font)
                  draw.text((eje_x_2,265), fecha, (0,0,0), font=font)
                  
                  draw.text((eje_x,288), pers_med, (0,0,0), font=font)          
                  img.save("sangre.png")
                  await message.channel.send(file=discord.File("sangre.png")) 
                  #BUENO:
                  channel = client.get_channel(sangre_id)
                  #TEST:
                  #channel = client.get_channel(862358903949361192)

                  await channel.send(file=discord.File("sangre.png"))
                  await analisis(message,inciales2,nombre2, sexo2, nacimiento2)
        elif message.content == "/bajamed":
#                  db = cluster["Clientes"]
                  mycursor.execute("SELECT `nombre`,`sexo`,`nace`, `ini`, `ms`, `sangre`, `tel`, `al`, `med`, `seguro_med` FROM clientes WHERE entidad = {0} AND chan = {1}".format(entidad,message.channel.id))
                  myresult = mycursor.fetchall()
                  for p in myresult:
                    nombre_baj = p[0]
                    inciales = p[3]
                    nacimiento_baj = str(p[2])
                    sexo = p[1]
                    enc = 1
              
                   
                  
                 
                  if enc == 0:
                    await message.channel.send("Paciente no encontrado, escriba /enlazar paciente para enlazarlo",delete_after = 60)
                  else:
#                    db = cluster["Clientes"]
                    global pers_name_baj
                    pers_name_baj = ""
                    global num_placa_baj
                    num_placa_baj = 0000
                    mycursor.execute("SELECT `nombre`,`numero_de_placa` FROM empleados WHERE entidad = {0} AND discord_id = {1}".format(entidad,message.author.id))
                    myresult = mycursor.fetchall()
           
                 
                    for x in myresult:
                      pers_name_baj = x[0]
                      num_placa_baj = str(x[1])
                    motivos = await pregunta_md(message,client,"Escriba brevemente los motivos de la baja:")
                    dias_baja = await pregunta_md(message,client,"Escriba en cuantos días deberá acudir a consulta el paciente para revisar la baja")  
                    
                  
                    today = date.today()  
                    fecha = today.strftime("%Y-%m-%d")
                    baj_edad = calc_edad(datetime.strptime(nacimiento_baj,"%Y-%m-%d"))
                    img = Image.open('baja-plant.png')
                    draw = ImageDraw.Draw(img)
                    font = ImageFont.truetype('Roboto-Regular.ttf', 14)
                    eje_x = 310   #Ponlo bien porfa xd
                    eje_x_2 = 530
                    draw.text((eje_x,130), nombre_baj, (0,0,0), font=font)
                    draw.text((eje_x,150), str(baj_edad), (0,0,0), font=font)
                    draw.text((eje_x_2,169), nacimiento_baj, (0,0,0), font=font)
                    draw.text((eje_x,210), motivos, (0,0,0), font=font)
                    draw.text((eje_x,345), pers_name_baj, (0,0,0), font=font)
                    draw.text((eje_x_2,360), num_placa_baj, (0,0,0), font=font)
                    draw.text((eje_x_2,380), fecha, (0,0,0), font=font)
                    baja_abajo = "El paciente deberá guardar reposo y acudir a revisión en periodos alternos de {} dias.".format(dias_baja)
                    
                    draw.text((10,410), baja_abajo, (0,0,0), font=font)
                    draw.text((eje_x,452), pers_name_baj, (0,0,0), font=font)          
                    img.save("baja.png")
                    await message.channel.send(file=discord.File("baja.png")) 
                    #BUENO:
                    channel = client.get_channel(can_resultados)
                    #TEST:
                    #channel = client.get_channel(862358903949361192)

                    await channel.send(file=discord.File("baja.png"))
#===========================================================     #=========================================================== #===========================================================
                    #LSPD
#===========================================================     #=========================================================== #===========================================================
async def LSPD(mydb,mycursor,entidad,message,client):
          print("LSPD")
          if message.content == "/DNI":
            await message.delete()
            nom = await pregunta_md(message, client,"Introduzca el nombre del nuevo ciudadano:")
            nace = await pregunta_md(message, client, "Escriba la fecha de nacimiento del ciudadano en formato YYYY-MM-DD:")
            
            name = 'EXPEDIENTES ANTIGUOS'
            try:
              category = discord.utils.get(message.author.guild.categories, id=936679464400744518) 
              channl2 = await message.author.guild.create_text_channel(nom,category=category)
            except:
              channl2 = await message.author.guild.create_text_channel(nom)
            txt = "```Nombre: {}\nFecha nacimiento: {}```".format(nom,nace)
            #ms = await message.channel.send(txt)
            ms2 = await channl2.send(txt)
           # db = cluster["DNI"]
            mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
            mycursor = mydb.cursor()   
            print("conectado")
            sql = "INSERT INTO clientes (entidad,nombre, nace, chan) VALUES (%s,%s, %s, %s)"
            val = (entidad,nom, nace, channl2.id)
            mycursor.execute(sql, val)
            
            mydb.commit()
          
            await channl2.send("```Responda al mensaje anterior donde viene la información completa con la fotografía del ciudadano:```")
            await message.author.send("```Ciudadano dado de alta```")
#Armas 
          elif message.content == "/armas":
            await message.delete()
            global nace_armas
            global nom_armas
            mycursor.execute("SELECT `nombre`,`nace`,`cliente_id` FROM clientes WHERE entidad = {0} AND chan = {1}".format(entidad,message.channel.id)) #buscamos al paciente, si no existe se le pregunta_mdran los datos
            myresult = mycursor.fetchall()
            enc = 0
            for x in myresult:
                nombre = x[0]
                nacimiento = x[1]
                cliente = x[2]
                enc = 1
           
            if(enc == 0):
              await message.channel.send("```Ciudadano no encontrado, asegurese de estar en el canal del ciudadano que quiere registrar el permiso```",delete_after=20)
             
            else:
              nom_armas = nombre
              nace_armas = nacimiento
              psic = await pregunta_md(message, client,"Escriba si o no, si el ciudadano presenta el examen psicotecnico:" )
              
              
              channl = message.channel
              ms = await channl.send("```PERMISO ARMAS:\nNombre: {}\nFecha nacimiento: {}\nPsicotecnico: {}```".format(nom_armas,nace_armas,psic))
              mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
              mycursor = mydb.cursor() 
              sql = "INSERT INTO armas (entidad,cliente_id, psico) VALUES (%s,%s, %s)"
              val = (entidad,cliente,psic)
              
              mycursor.execute(sql, val)
              
              mydb.commit()
              await message.author.send("```Hecho, gracias```")
  #Fallecidos
          elif message.content == "/fallecido":
            await message.delete()
            mycursor.execute("SELECT `nombre`,`nace`,`cliente_id` FROM clientes WHERE entidad = {0} AND chan = {1}".format(entidad,message.channel.id)) #buscamos al paciente, si no existe se le pregunta_mdran los datos
            myresult = mycursor.fetchall()
            enc = 0
            for x in myresult:
                nombre = x[0]
                nacimiento = x[1]
                cliente = x[2]
                enc = 1
           
            if(enc == 0):
              await message.channel.send("```Ciudadano no encontrado, asegurese de estar en el canal del ciudadano que quiere registrar el fallecimiento```",delete_after=20)
             
            else:
              
              muere = await pregunta_md(message, client,"Escriba la fecha de defunción del ciudadano fallecido en formato YYYY-MM-DD:" )
              nomfor = await pregunta_md(message, client,"Escriba el nombre del medicos forenses a cargo del anailisis forense:" )
              carfor = await pregunta_md(message, client, "Escriba el cargo del medico forense:")
              causas = await pregunta_md(message, client,"Escriba las causas de la defunción de las evaluaciones entregadas por los medicos forenses del hospital de Pillbox Hill:" )
              
  
              channl = message.channel
              ms = await channl.send("```FALLECIDO\nFecha defunción: {}\nNombre forense: {}\nCargo forense: {}\nCausas: {}```".format(muere,nomfor,carfor,causas)) 
              #db = cluster["Muertos"]
              mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
              mycursor = mydb.cursor() 
              sql = "INSERT INTO fallecimiento (entidad,nombre, fecha_nacimiento, fecha_defuncion, forenses_encargados, cargo_med_forense, causas) VALUES (%s,%s, %s, %s,%s,%s,%s)"
              val = (entidad,nombre,nacimiento,muere,nomfor,carfor,causas)
              
              mycursor.execute(sql, val)
              
              mydb.commit()
              sql = "DELETE FROM clientes WHERE cliente_id = {0}".format(cliente) #borramos a la persona porque está muerta
              mycursor.execute(sql)
              
              mydb.commit()
              await message.channel.edit(name = "☠ {0}".format(nombre))
              await message.author.send("```Fallecimiento anotado, DEP```")
             
  #Vehiculos
          elif message.content == "/vehiculo":
            mycursor.execute("SELECT `nombre`,`nace`,`cliente_id` FROM clientes WHERE entidad = {0} AND chan = {1}".format(entidad,message.channel.id)) #buscamos al paciente, si no existe se le pregunta_mdran los datos
            myresult = mycursor.fetchall()
            enc = 0
            for x in myresult:
                nombre = x[0]
                nacimiento = x[1]
                cliente = x[2]
                enc = 1
           
            if(enc == 0):
              await message.channel.send("```Ciudadano no encontrado, asegurese de estar en el canal del ciudadano que quiere registrar el vehículo```",delete_after=20)
            else:
              
              tipo = await pregunta_md(message, client,"Introduzca el tipo del vehículo:" )
              mar = await pregunta_md(message, client, "Introduzca la marca del vehículo:")
              mod = await pregunta_md(message, client, "Introduzca el modelo del vehículo:")
              mat = await pregunta_md(message, client, "Introduzca la matricula del vehículo:")
            
              
  
              channl = message.channel
              ms = await channl.send("```Nombre: {}\nTipo del Vehículo: {}\nMarca del Vehículo: {}\nModelo del Vehículo: {}\nMatricula del Vehículo: {}```".format(nombre,tipo,mar,mod,mat)) 
  
             # db = cluster["Vehiculos"]
              mydb  = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)   
              mycursor = mydb.cursor() 
              sql = "INSERT INTO vehiculo (entidad,cliente_id, tipo, marca, modelo, matricula) VALUES (%s,%s, %s, %s,%s,%s)"
              val = (entidad,cliente, tipo, mar, mod, mat)
              
              mycursor.execute(sql, val)
              
              mydb.commit()
              await message.author.send("```Vehículo dado de alta```")
  #Busqueda y captura 
          elif message.content == "/busqueda":
            await message.channel.send("Introduzca el nombre y las razones de busqueda y captura",delete_after = 60)

            def check(m):
                global buscap
                buscap = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id) 
            await msg.delete()

            channl = message.channel
            ms = await channl.send("Nombre y razone {}:".format(buscap))
            #db = cluster["Busqueda_Captura"]

            
#Atracos
          elif message.content == "/atraco":
            await message.channel.send("Introduzca el nombre del agresor, en caso de no tenerlo poner desconocido:",delete_after = 60)

            def check(m):
                global na
                na = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id) 
            
            await msg.delete()
            await message.channel.send("escriba los nombres de los agentes involucrados en la negociacióin",delete_after = 120)

            def check(m):
                global an 
                an = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)
                  
            await msg.delete()
            await message.channel.send("escriba los numeros de placa de los agentes involucrados en la negociacióin",delete_after = 120)

            def check(m):
                global npan
                npan = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)

            await msg.delete()
            await message.channel.send("escriba los nombres de los agentes de apoyo",delete_after = 120)

            def check(m):
                global ap 
                ap = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)
                  
            await msg.delete()
            await message.channel.send("escriba los numeros de placa de los agentes de apoyo",delete_after = 120)

            def check(m):
                global npaa
                npaa = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)

            await msg.delete()
            await message.channel.send("Escriba los delitos con los respectivos números que concuerden con la constitución",delete_after = 120) 

            def check(m):
                global art 
                art = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)
                  
            await msg.delete()
            await message.channel.send("escriba la multa económica únicamente con números",delete_after = 120)

            def check(m):
                global mul
                mul = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)
            
            await msg.delete()
            await message.channel.send("Escriba los meses en prisión",delete_after = 60)

            def check(m):
                global mes
                mes = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author



            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)
                  
            await msg.delete()
            
            channl = message.channel
            ms = await channl.send("Nombre Agresor: {}\nAgentes En Negociación: {}\nNúmero De Placas Agentes En Negociación: {}\nAgentes De Apoyo: {}\nNúmero De Placas Agentes De Apoyo: {}\nArticulos: {}\nMulta Economica: {}\nMeses En Prisión: {}".format(na,an,npan,npaa,ap,art,mul,mes))
            #db = cluster["Atracos"]

            
          
#Procesados             
          elif message.content == "/procesado":
            await message.channel.send("Introduzca el nombre del detenido:",delete_after = 60)

            def check(m):
                global np
                np = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)

            await msg.delete()
            await message.channel.send("Escriba los delitos con los respectivos números que concuerden con la constitución",delete_after = 120)

            def check(m):
                global art 
                art = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)
                  
            await msg.delete()
            await message.channel.send("Escriba la multa econimica del detenido",delete_after = 120)

            def check(m):
                global mul 
                mul = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)
                  
            await msg.delete()
            await message.channel.send("Escriba los meses de prision del detenido",delete_after = 120)

            def check(m):
                global mes 
                mes = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)
                  
            await msg.delete()
            await message.channel.send("Escriba observaciones",delete_after = 120)

            def check(m):
                global obs 
                obs = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)
                  
            await msg.delete()

            channl = message.channel
            ms = await channl.send("Nombre Procesado: {}\nArticulos: {}\nMulta Economica: {}\nMeses En Prisión: {}\nObservaciones: {}".format(np,art,mul,mes,obs))
            #db = cluster["Procesados"]

           
            await message.channel.send("Responda al mensaje anterior donde viene la información completa con la fotografía del ciudadano detenido:")  
#Sospechosos
          elif message.content == "/sospechoso":
            await message.channel.send("Introduzca el nombre del caso:",delete_after = 60)

            def check(m):
                global nc
                nc = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)

            await msg.delete()
            await message.channel.send("Escriba los nombres de los agentes en la investigación",delete_after = 120)

            def check(m):
                global nai
                nai = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)
                  
            await msg.delete()
            await message.channel.send("Escriba los números de placa los agentes a cargo de la investigación",delete_after = 120)

            def check(m):
                global npai
                npai = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)
                  
            await msg.delete()
            await message.channel.send("Escriba los nombre/s de los Sospecho/s",delete_after = 120)

            def check(m):
                global ns
                ns = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)
                  
            await msg.delete()
            await message.channel.send("Escriba el numero telefónico de los Sospecho/s",delete_after = 120)

            def check(m):
                global ts
                ts = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)
                  
            await msg.delete()
            await message.channel.send("Escriba las evidencias encontradas",delete_after = 120)

            def check(m):
                global evi
                evi = m.content
                return m.content != "" and m.channel == message.channel and m.author == message.author

            await client.wait_for("message", check=check)
            time.sleep(1)
            msg = await message.channel.fetch_message(message.channel.last_message_id)
                  
            await msg.delete()

            channl = message.channel
            ms = await channl.send("Nombre Del Caso: {}\nNombre De Los Agentes En La Investigación: {}\nNumero De Placas De Los Agentes: {}\nNombre Del Sospechoso/s: {}\nTelefono Del Sospechoso/s: {}\nEvidencias: {}".format(nc,nai,npai,ns,ts,evi))
          #  db = cluster["Sospechosos"]

          
def Mecanico():
  print("Mecanico")