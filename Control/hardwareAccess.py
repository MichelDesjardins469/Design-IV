import numpy as np
from collections import namedtuple
import serial
import RPi.GPIO as GPIO

PIN_HEATER = 0
PIN_VOLETS = 0
PIN_VENT = 0
PIN_WATER_PUMP = 0
PIN_LIGHTS = 0
PIN_VALVE_1 = 0
PIN_VALVE_2 = 0
PIN_VALVE_3 = 0
PIN_VALVE_4 = 0

LIST_PORTS = ["/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyACM2"]


# pour fins de démonstrations
heat_on = False
lights_on = False

complete_readings = namedtuple(
    "complete_readings", "temp_int temp_ext hum_int hum_ext CO2_int"
)
station_reading = namedtuple("station_reading", "temp hum CO2")


class HardwareAccess:
    list_serials = []

    def __init__(self):
        pass

    def setup_hardware_access(self):
        self.setup_gpios()
        self.setup_serials()

    def setup_gpios(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIN_HEATER, GPIO.OUT)
        GPIO.setup(PIN_VOLETS, GPIO.OUT)
        GPIO.setup(PIN_VENT, GPIO.OUT)
        GPIO.setup(PIN_WATER_PUMP, GPIO.OUT)
        GPIO.setup(PIN_LIGHTS, GPIO.OUT)
        GPIO.setup(PIN_VALVE_1, GPIO.OUT)
        GPIO.setup(PIN_VALVE_2, GPIO.OUT)
        GPIO.setup(PIN_VALVE_3, GPIO.OUT)
        GPIO.setup(PIN_VALVE_4, GPIO.OUT)

    def setup_serials(self):
        for port in LIST_PORTS:
            ser = serial.Serial(
                port=port,
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=10,
            )
            self.list_serials.append(ser)

    def traitement_actions(self, actions):
        if actions == 1:
            self.turn_on_heat()
        elif actions == 2:
            self.turn_on_lights()
        elif actions == 3:
            self.turn_on_heat()
            self.turn_on_lights()

    def turn_on_water_pump(self):
        pass

    def turn_on_water_valve(self, section_id):
        pass

    def turn_on_co2(self):
        pass

    def turn_on_fan(self):
        pass

    def open_volets(self):
        pass

    def close_volet(self):
        pass

    def turn_on_lights(self):
        global lights_on
        if not lights_on:
            print("lumières activées")

            lights_on = True

    def turn_on_heat(self):
        global heat_on
        heat_on = True
        print("chauffage activé")

    def get_lecture_sensors(self):

        results = []
        for ser in self.list_serials:
            ser.write(b"run\n")
            reading = ser.readline()
            if reading == b"":
                print("couldn't not contact one station")
                results.append(None)
            else:
                results.append(reading)

        reading_int_1 = self.get_lecture_interieur_1()
        reading_int_2 = self.get_lecture_interieur_2()
        reading_ext = self.get_lecture_exterieur()

        temp_int = np.mean([reading_int_1.temp, reading_int_2.temp])
        hum_int = np.mean([reading_int_1.hum, reading_int_2.hum])
        CO2_int = np.mean([reading_int_1.CO2, reading_int_2.CO2])

        return complete_readings(
            temp_int, reading_ext.temp, hum_int, reading_ext.hum, CO2_int
        )

    def get_lecture_interieur_1(self):
        return station_reading(0, 0, 0)

    def get_lecture_interieur_2(self):
        return station_reading(0, 0, 0)

    def get_lecture_exterieur(self):
        return station_reading(0, 0, 0)

    def get_lecture_sensors_test_random(self):
        if heat_on or np.random.random_integers(0, 10) <= 8:
            temp_int = np.random.normal(23, 2)
        else:
            temp_int = np.random.normal(18, 2)

        readings = complete_readings(temp_int, 0, 0, 0, 0)
        return readings
