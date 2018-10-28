from boto3.dynamodb.conditions import Key
import boto3
import datetime
import MFRC522
import RPi.GPIO as GPIO
import time

dynamodb = boto3.resource('dynamodb')

tabelaTag = dynamodb.Table('tags')
tabelaLogs = dynamodb.Table('logs')

LeitorRFID = MFRC522.MFRC522()
print('Aproxime a TAG')


def le_tag():
    while True:
        # Verifica se existe TAG no leitor
        (status, TagType) = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)
        # Leitura da TAG
        if status == LeitorRFID.MI_OK:
            print('TAG Detectada!')
            (status, uid) = LeitorRFID.MFRC522_Anticoll()
            # pega o id da tag e remove as ,
            uid = ''.join(str(registro) for registro in uid)
            print(uid)
            break
    return uid


# consulta o registro
def consulta_db(uid):
    # cria uma consulta
    resultado_consulta = tabelaTag.query(
        # busca pela chave
        KeyConditionExpression=Key('id').eq(uid)
    )
    print(resultado_consulta)
    return resultado_consulta


def valida_cartao(resultado_consulta):
    if len(resultado_consulta['items']) == 1:
        usuario = resultado_consulta['items'][0]['usuario']
        print('Usuario: {} - Acesso Liberado'.format(usuario))
        acesso = 'Liberado'
    else:
        print('Usuario Invalido - Acesso Negado! ')
        acesso = 'Negado'
    return acesso


def registra_acesso(uid, acesso):
    timestamp = str(datetime.datetime.now())
    for id, usuario in cartoes.items():
        tabelaLogs.put_item(
            Item={
                'timestamp' : timestamp,
                'id': uid,
                'acesso': acesso
            }
        )
        print(id, ': ', usuario)


try:
    while True:
        uid = le_tag()
        resultado_consulta = consulta_db(uid)
        acesso = valida_cartao(resultado_consulta)
        registra_acesso(uid, acesso)
        time.sleep(.5)
except KeyboardInterrupt:
    GPIO.cleanup()
