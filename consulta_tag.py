import MFRC522
import RPi.GPIO as GPIO
import time
# Create an object of the class MFRC522
LeitorRFID = MFRC522.MFRC522()

# Welcome message
print("Aproxime a Tag")
# print("Press Ctrl-C to stop.")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while True:

    # Verificar se existe tag no leitor
    (status, TagType) = LeitorRFID.MFRC522_Request(LeitorRFID.PICC_REQIDL)

    # Leitura da TAG
    if status == LeitorRFID.MI_OK:
        print("Cartão detectado")
        # Get the UID of the card
        (status, uid) = LeitorRFID.MFRC522_Anticoll()
        print('uid', uid)

    time.sleep(5)
