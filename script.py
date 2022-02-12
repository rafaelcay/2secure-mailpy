import imaplib
import email
from email.header import decode_header
import webbrowser
import os
from getpass import getpass
import json
import requests
from virus_total_apis import PublicApi
from hashlib import md5
from virus_total_apis import PublicApi

# Datos del usuario
username = input("Correo: ")
password = getpass("Password: ")

# Crear conexión
imap = imaplib.IMAP4_SSL("imap.gmail.com")
# iniciar sesión
imap.login(username, password)
#obtener correos
status, mensajes = imap.select("INBOX")
msj = int(mensajes[0])
#
print("Actualmente tienes " + str(msj) +"   Correos en bandeja de entrada")

Nmail=int(input("Porfavor,digite el numero de correo a analizar: "))

res, mensaje = imap.fetch(str(Nmail), "(RFC822)")

valor= any(x is None for x in mensaje)
#condicianal para validar numero de correo
if valor==True:
    print("Numero invalido")
     
else:

    print("Trabajando.......")
     
    
print("*********Estos son los datos del correo*********")
for respuesta in mensaje:
    if isinstance(respuesta, tuple):
            # Obtener el contenido
        mensaje = email.message_from_bytes(respuesta[1])
            # decodificar el contenido
        subject = decode_header(mensaje["Subject"])[0][0]

        if isinstance(subject, bytes):        
        # convertir a string
            subject = subject.decode()
            # de donde viene el correo
    
        from_ = mensaje.get("From")
        print("Subject:", subject)
        print("From:", from_)
       # print("****Correo obtenido con exito****")

##################parte de lectura de adjuntos#################3
        print("Estos son los archivos adjuntos al correo: ")
        if mensaje.is_multipart():
       
                # Recorrer las partes del correo
                for part in mensaje.walk():
                    # Extraer el contenido
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                   #condicional para descartar correos sin archivos adjuntos
                    if content_disposition != "None":
                      
                        print(content_disposition)
                    
                        no = False
                while not no:
                    print("¿Desea descargar los archivos adjuntos y analizar en busca de amenzas?")
                    opc=input("Digite si o no: ")
                        
                    if opc == "si":
                        print("se estan descargando los archivos...")
                        if "attachment" in content_disposition:
                        #Descarga de archivos adjuntos
                            nombre_archivo = part.get_filename()
                            if nombre_archivo:
                                if not os.path.isdir(subject):
                                # crear una carpeta para el mensaje
                                    os.mkdir(subject)
                                ruta_archivo = os.path.join(subject, nombre_archivo)
                                    # guardar archivo adjunto
                                open(ruta_archivo, "wb").write(part.get_payload(decode=True))
                        print("Se descargaron los archivos...")
                        print("Analizando achivos.....")
    ####################anlisis de archivos con api virus total####################################
                        API_KEY = "1092a7815708c644d938fcea89c2fff986f121a7fbf8a868156c9d5c77b810fd"
                        api = PublicApi(API_KEY)
                        #abrir ruta del archivo a analizar
                        with open(ruta_archivo, "rb") as f:
                            file_hash = md5(f.read()).hexdigest()
                        #respuesta del analisis
                            response = api.get_file_report(file_hash)

                        if response["response_code"] == 200:
                            if response["results"]["positives"] > 0:
                             print("El archivo que se analizo tiene problemas de seguridad puede contener malware")
                            else:
                             print("El archivo no tiene ningun problema de seguridad,esta libre de malware ")
  
                            print("Escaneo Finalizado")
                            preus=input("¿Desea ver el informe completo del escaneo? Digite si o no : ")
                            if preus=="si":
                                print(json.dumps(response, sort_keys=False, indent=4))
                                break
                            else:
                                print("...")

                    elif opc =="no":
                        no=True

                    else:
                        print("Opcion no valida")
                       
print("BYE")