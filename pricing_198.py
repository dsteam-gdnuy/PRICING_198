from utils import snowflake_login, enviar_email, get_credentials
import os
from datetime import date
import sys

credentials_snowflake = get_credentials("snow")

#Logueamos
user, cursor, snowflake_connection = snowflake_login(
                                    user = credentials_snowflake['USER'],
                                    password = credentials_snowflake['PASS'],
                                    account = credentials_snowflake['ACCOUNT']
                                    )

try:
    #Se descarga resultado del modelo
    cursor.execute('SELECT * FROM SANDBOX_PLUS.DWH.RESULTADO_MODELO_PRICING_198 WHERE FECHA_EJECUCION = CURRENT_DATE')
    df = cursor.fetch_pandas_all()

    if df.shape[0] == 0:
        enviar_email(sender='marcos.larran@tata.com.uy', receiver=['ds-team@gdn.com.uy'],
                     subject='Modelo Pricing Ecommerce', body='Checkear task', files=[])
        sys.exit()

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
    enviar_email(sender='marcos.larran@tata.com.uy', receiver=['marcela.moreira@tata.com.uy', 'nahuel.hartwig@tata.com.uy', 'meinller.barosic@tata.com.uy'],
                 subject='Modelo Pricing Ecommerce',
                 body='Buenas tardes\n\nSe envía el resultado del modelo de pricing de ecommerce del día de la fecha.\n\nSaludos,',
                 files=['INFO PRICING 198 ' + str(date.today().year) + mes + dia + '.xlsx'])
    
    #Se elimina el excel
    os.remove('INFO PRICING 198 ' + str(date.today().year) + mes + dia + '.xlsx')
except:
    #Si algo falla avisamos
    enviar_email(sender='marcos.larran@tata.com.uy', receiver=['ds-team@gdn.com.uy'],
                 subject='Modelo Pricing Ecommerce', body='Hubo un problema con el modelo', files=[])
    try:
        #Se elimina el excel
        os.remove('INFO PRICING 198 ' + str(date.today().year) + mes + dia + '.xlsx')
    except:
        pass