from builtins import tuple
import MFRC522
import RPi.GPIO as GPIO
import time

tags_liberadas = {
    (42, 42, 228, 89, 189): 'Julio',
    (70, 84, 191, 73, 228): 'Tiago'
}

LeitorRFID = MFRC522.MFRC522()

print('Aproxime a TAG')

while True:

    # Verifica se existe TAG no leitor
    (status, TagType) = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)
    # Leitura da TAG
    if status == LeitorRFID.MI_OK:
        print('TAG Detectada!')
        (status, uid) = LeitorRFID.MFRC522_Anticoll()
        uid = tuple(uid)

        if uid in tags_liberadas.keys():
            print('ID: {} - Acesso Liberado'.format(tags_liberadas[uid]))
        else
            print('ID: {} - Acesso Bloqueado'.format(tags_liberadas[uid]))



        print('uid: ', uid)
    time.sleep(.5)
