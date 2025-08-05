import os
import snowflake.connector
import json
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

def snowflake_login():

    if os.getcwd().upper() == 'C:\\USERS\\ARTURO.BOTATA12\\DOCUMENTS\\GITHUB\\PRICING_198':

        user = "PLUS_VM1_NEW"

        snowflake_connection = snowflake.connector.connect(
            user=user,
            password="aK09fWyh4i5oVcI9A31Ea4vXMcquhMMlIE9sXRoil3oSw9faD9",
            account="XZ23267-dp32414",
            database="SANDBOX_PLUS",
            schema="DWH"
        )
        cursor = snowflake_connection.cursor()
    else:
        counter = 0
        while True:
            if counter + 1 < 4:
                print(f"Intento {counter + 1}")

                try:
                    user = input("INGRESAR USUARIO: ")
                    psw = input("INGRESAR CONTRASEÑA: ")
                    pass_ = input("INGRESAR PASSCODE: ")

                    # Establish Snowflake connection
                    snowflake_connection = snowflake.connector.connect(
                        user=user,
                        password=psw,
                        account="XZ23267-dp32414",
                        passcode=pass_,
                        database='SANDBOX_PLUS',
                        schema='DWH'
                    )

                    cursor = snowflake_connection.cursor()

                    print('Correct Password - connected to SNOWFLAKE')

                    break

                except FileNotFoundError:
                    print("Error: 'credentials.json' file not found.")
                    break
                except json.JSONDecodeError:
                    print("Error: 'credentials.json' file is not valid JSON.")
                    break
                except Exception as e:
                    counter += 1
                    print(f'Error: {e}')
                    print('Incorrect Password - provide again')

            else:
                print('3 Intentos fallidos')
                break

    return user, cursor, snowflake_connection

def get_credentials(type: str) -> dict:

    if type == 'credentials_mail_servicio':
        with open('leo_usuario_servicio_credenciales.json') as f:
            credentials = json.load(f)#[type]

    else:
        with open('credentials.json') as f:
            credentials = json.load(f)[type]

    return credentials

def enviar_email(sender, receiver, subject, body, files:list):
    smtp_server = "fast.smtpok.com"  # Reemplaza con el servidor SMTP que uses
    smtp_port = 587  # Usualmente 587 para TLS o 465 para SSL
    sender_email = sender                       #Reemplaza con tu email
    credentials = get_credentials('correo_autom')
    sender_user = credentials['USER']
    sender_password = credentials['PASS']       #Reemplaza con tu contraseña
    recipient_email = receiver                  #Email del destinatario
 

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje["From"] = sender_email
    mensaje["To"] = ", ".join(recipient_email)
    mensaje["Subject"] = subject #"Error Maestro productos Hist"
      
    mensaje.attach(MIMEText(body, "plain"))

    # Attach the Excel file
    if len(files) > 0:
        for file_path in files:
            attachment_name = os.path.basename(file_path)
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={attachment_name}')
                mensaje.attach(part)
    try:
        # Conectar al servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Iniciar cifrado TLS
        server.login(sender_user, sender_password)  # Autenticación
        
        # Enviar el correo
        server.sendmail(sender_email, recipient_email, mensaje.as_string())
        print("Correo enviado exitosamente.")
        
        # Cerrar la conexión
        server.quit()
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False