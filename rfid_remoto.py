from boto3.dynamodb.conditions import Key
import boto3
import datetime
import MFRC522
import RPi.GPIO as GPIO
import time

dynamodb = boto3.resource('dynamodb')
tabelaTags = dynamodb.Table('tags')
tabelaLogs = dynamodb.Table('logs')

LeitorRFID = MFRC522.MFRC522()


def le_tag():
    while True:
        # Verifica se existe TAG no leitor
        (status, TagType) = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)

        # Leitura da TAG
        if status == LeitorRFID.MI_OK:
            print('TAG Detectada!')
            (status, uid) = LeitorRFID.MFRC522_Anticoll()
            uid = ''.join(str(registro) for registro in uid)
            break
    return uid

def consulta_db(uid):
    resultado_consulta = tabelaTags.query(
        KeyConditionExpression=Key('id').eq(uid)
    )
    #print(resultado_consulta)
    return resultado_consulta


def valida_tag(resultado_consulta):
    if len(resultado_consulta['Items'])==1:
        usuario = resultado_consulta['Items'][0]['usuario']
        print('Usuario: {} - Acesso Liberado!'.format(usuario))
        acesso = 'Liberado'
    else:
        print('Usuario: Inválido - Acesso Negado!')
        acesso = 'Negado'
    return acesso


def registra_acesso(uid,acesso):
    timestamp = str(datetime.datetime.now())
    tabelaLogs.put_item(
            Item={
                'timestamp': timestamp,
                'id': uid,
                'acesso': acesso
            }
        )


try:
    while True:
        uid = le_tag()
        resultado_consulta = consulta_db(uid)
        acesso = valida_tag(resultado_consulta)
        registra_acesso(uid,acesso)
        time.sleep(.5)
except KeyboardInterrupt:
    GPIO.cleanup()

