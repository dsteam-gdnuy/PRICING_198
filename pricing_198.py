from utils import snowflake_login, enviar_email
import os
from datetime import date
import sys

#Logueamos
user, cursor, snowflake_connection = snowflake_login()

#Contamos cuantas fechas distintas hay desde la última corrida. Debiera haber 2
cursor.execute('''SELECT COUNT(DISTINCT TIEM_DIA_ID) FROM SANDBOX_PLUS.DWH.RETAIL_COMPETENCIAS_UNIFICADO
        WHERE TIEM_DIA_ID > (SELECT MAX(FECHA_EJECUCION) FROM SANDBOX_PLUS.DWH.RESULTADO_MODELO_PRICING_198);
               ''')
cont = cursor.fetchall()

#Si no hay 2 se informa
if cont[0][0] > 1:
    print('Ok')
else:
    enviar_email(sender='marcos.larran@tata.com.uy', receiver=['ds-team@gdn.com.uy'],
                 subject='Modelo Pricing Ecommerce', body='Checkear task', files=[])

#Si no hay datos no continuamos
if cont[0][0] == 0:
    sys.exit()

try:
    #Se descarga resultado del modelo
    cursor.execute('SELECT * FROM SANDBOX_PLUS.DWH.RESULTADO_MODELO_PRICING_198 WHERE FECHA_EJECUCION = CURRENT_DATE')
    df = cursor.fetch_pandas_all()

    #Se define mes y dia actual
    if len(str(date.today().month)) > 1:
        mes = str(date.today().month)
    else:
        mes = '0' + str(date.today().month)
    
    if len(str(date.today().day)) > 1:
        dia = str(date.today().day)
    else:
        dia = '0' + str(date.today().day)
    
    #Se guarda
    df.to_excel('INFO PRICING 198 ' + str(date.today().year) + mes + dia + '.xlsx', index=False)

    #Se envía mail
    enviar_email(sender='marcos.larran@tata.com.uy', receiver=['marcela.moreira@tata.com.uy', 'nahuel.hartwig@tata.com.uy'],
                 subject='Modelo Pricing Ecommerce',
                 body='Buenas tardes\n\nSe envía el resultado del modelo de pricing de ecommerce del día de la fecha.\n\nSaludos,',
                 files=['INFO PRICING 198 ' + str(date.today().year) + mes + dia + '.xlsx'])
except:
    #Si algo falla avisamos
    enviar_email(sender='marcos.larran@tata.com.uy', receiver=['ds-team@gdn.com.uy'],
                 subject='Modelo Pricing Ecommerce', body='Hubo un problema con el modelo', files=[])