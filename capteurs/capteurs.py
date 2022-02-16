import Adafruit_DHT as dht
from time import sleep
import serial

DHT = 4
ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=0.5)
ser.flushInput()

#when message recu:
while True:
    h, t = dht.read_retry(dht.DHT22, DHT)

    ser.flushInput()
    ser.write(b"\xFE\x44\x00\x08\x02\x9F\x25")
    resp = ser.read(7)

    try:
        high = resp[3]
        low = resp[4]
    except IndexError: #à changer
        print("Lecture du capteur de CO2 pas possible") #envoyé -2

    co2 = (high * 256) + low

    #envoie info:
    print(h +";" + t + ";"+ str(co2))
