import serial
import time

ser = serial.Serial("/dev/serial0", baudrate= 9600, timeout = .5)
print("Debut du capteur de CO2 par UART\n")
ser.flushInput()
time.sleep(1)


for i in range(1,69):
    ser.flushInput()
    ser.write(b'\xFE\x44\x00\x08\x02\x9F\x25')
    time.sleep(.5)
    resp = ser.read(7)
    high = resp[3]
    low = resp[4]
    co2 = (high*256) +low
    print("i = ", i, "CO2 = " + str(co2) + "ppm")
    time.sleep(.1)