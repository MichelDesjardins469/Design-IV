import serial

ser = serial.Serial("/dev/serial0", baudrate=9600, timeout=0.5)
ser.flushInput()
count = 0
ser.close()
ser.open()
ser.write(b"test")
ser.close()
