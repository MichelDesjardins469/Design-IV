import Adafruit_DHT as dht
from time import sleep
import serial
import time

ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=0.5)
ser.flushInput()

DHT = 4

while True:
    h, t = dht.read_retry(dht.DHT22, DHT)
    print("Temp={0:0.1f}*C Humidity={1:0.1f}%".format(t,h))
    ser.flushInput()
    ser.write(b"\xFE\x44\x00\x08\x02\x9F\x25")
    time.sleep(1)
    resp = ser.read(7)
    co2 = 0

    if len(resp) > 2:
        high = resp[3]
        low = resp[4]
        co2 = (high * 256) + low
        print(
            "CO2 = "
            + str(co2)
            + "ppm "
            + " température : "
            + str(t)
            + ", humidité : "
            + str(h)
        )
    sleep(3)
