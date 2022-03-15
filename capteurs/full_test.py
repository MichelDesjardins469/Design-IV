#import Adafruit_DHT as dht
from time import sleep
import serial

DHT = 4
#ser_co = serial.Serial("/dev/serial0", baudrate=9600, timeout=0.5)
#ser_co.flushInput()


def getValeurs():
    #h, t = dht.read_retry(dht.DHT22, DHT)
    h,t=1
    co2 = -1

    try:
        i = 1/0
        #ser_co.flushInput()
        #ser_co.write(b"\xFE\x44\x00\x08\x02\x9F\x25")
        #resp = ser_co.read(7)
        #high = resp[3]
        #low = resp[4]
        #co2 = (high * 256) + low
    except:
        print(t,h,-1)
        return (t, h, -1)

    # envoie info:
    return (t, h, co2)


sleep(30)


def lecture():
    sleep(3)
    return "THIS IS A TEST\n"


ser = serial.Serial(
    port="/dev/ttyGS0",
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=None,
)

while 1:
    x = ser.readline()
    # print(x)
    if x == b"run\n":
        valeurs = getValeurs()
        msg = str(valeurs[0]) + ":" + str(valeurs[1]) + ":" + str(valeurs[2])
        ser.write(bytes(msg, "UTF-8"))
    sleep(0.1)
