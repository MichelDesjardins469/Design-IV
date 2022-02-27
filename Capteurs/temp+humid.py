import Adafruit_DHT as dht
from time import sleep

DHT = 4

while True:
    h, t = dht.read_retry(dht.DHT22, DHT)
    print("Temp={0:0.1f}*C Humidity={1:0.1f}%".format(t, h))
    sleep(3)
