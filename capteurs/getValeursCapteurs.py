import Adafruit_DHT as dht
from time import sleep
import serial

DHT = 4
ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=0.5)
ser.flushInput()

def getValeurs():
    h, t = dht.read_retry(dht.DHT22, DHT)

    ser.flushInput()
    ser.write(b"\xFE\x44\x00\x08\x02\x9F\x25")
    resp = ser.read(7)
    co2 = -1

    try:
        high = resp[3]
        low = resp[4]
        co2 = (high * 256) + low
    except TypeError:
        return(t, h, -1)

    #envoie info:
    return(t, h, co2)