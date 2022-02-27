import serial
import time

ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=0.5)
print("Debut du capteur de CO2 par UART\n")
ser.flushInput()


while True:
    ser.flushInput()
    ser.write(b"\xFE\x44\x00\x08\x02\x9F\x25")
    time.sleep(1)
    resp = ser.read(7)
    co2 = 0

    if len(resp) > 2:
        high = resp[3]
        low = resp[4]
        co2 = (high * 256) + low
        print("CO2 = " + str(co2) + "ppm")
    # try:

    # except IndexError:
    # print("Erreur dans la lecture du capteur de co2")

    # time.sleep(3)
