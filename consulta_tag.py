import MFRC522
import RPi.GPIO as GPIO
import time

LeitorRFID = MFRC522.MFRC522()


print('Aproxime a TAG')


while True:

    # Verifica se existe TAG no leitor
    (status, TagType) = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)

    # Leitura da TAG
    if status == LeitorRFID.MI_OK:
        print('TAG Detectada!')
        (status, uid) = LeitorRFID.MFRC522_Anticoll()
        print('uid: ', uid)

    time.sleep(.5)
