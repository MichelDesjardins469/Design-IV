import numpy as np
from collections import namedtuple
import serial
import RPi.GPIO as GPIO
import threading

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


complete_readings = namedtuple(
    "complete_readings", "temp_int_1 temp_int_2 temp_ext hum_int_1 hum_int_2 hum_ext CO2_int_1 CO2_int_2"
)
station_reading = namedtuple("station_reading", "temp hum CO2")


class HardwareAccess:
    list_serials = []
    heat_on = False
    lights_on = False
    volet_opened = False
    fan_on = False

    def __init__(self):
        self._key_lock = threading.Lock()

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
        self.control_lights(actions.lights_turn_on)

        if actions.heat_turn_on:
            self.control_heat(True)
        if actions.heat_turn_off:
            self.control_heat(False)

        if actions.vent_turn_on:
            self.control_fan(True)
            self.open_volets()
        if actions.vent_turn_off:
            self.control_fan(False)
            self.close_volet()
        # TODO traitement water
        # TODO traitement pulse

    def turn_on_water_pump(self):
        pass

    def turn_on_water_valve(self, section_id):
        pass

    def control_fan(self, on):
        if on:
            GPIO.output(PIN_VENT, GPIO.HIGH)
            self.fan_on = True
        else:
            GPIO.output(PIN_VENT, GPIO.LOW)
            self.fan_on = False

    def open_volets(self):
        self.volet_opened = True
        t = threading.Thread(target=self.open_volets_thread)
        t.start()

    def open_volets_thread(self):
        # TODO do the open
        return True

    def close_volet(self):
        self.volet_opened = False
        t = threading.Thread(target=self.close_volets_thread)
        t.start()

    def close_volets_thread(self):
        # TODO do the close
        return True

    def control_lights(self, on):
        if on:
            GPIO.output(PIN_LIGHTS, GPIO.HIGH)
            self.lights_on = True
        else:
            GPIO.output(PIN_LIGHTS, GPIO.LOW)
            self.lights_on = False

    def control_heat(self, on):
        if on:
            GPIO.output(PIN_HEATER, GPIO.HIGH)
            self.heat_on = True
        else:
            GPIO.output(PIN_HEATER, GPIO.LOW)
            self.heat_on = False

    def get_lecture_sensors(self):

        results_int = []
        result_ext = []
        for ser in self.list_serials:
            ser.write(b"run\n")
            reading = ser.readline()
            if reading == b"":
                print("couldn't not contact one station")
                # results_int.append(None)
            else:
                splits = reading.decode('utf-8').split(":")
                if splits[2] == -1:
                    result_ext = splits
                else:
                    results_int.append(splits)
                
        return complete_readings(
            results_int[0][0], results_int[1][0], result_ext[0], results_int[0][1], results_int[1][1], result_ext[1], 
            results_int[0][2], results_int[1][2]
        )

    def get_lecture_sensors_threaded(self):
        results_int = []
        result_ext = []
        threads = []
        for ser in self.list_serials:
            t = threading.Thread(target=self.contact_sensor, args=(ser, results_int, result_ext,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
                
        return complete_readings(
            results_int[0][0], results_int[1][0], result_ext[0][0], results_int[0][1], results_int[1][1], result_ext[1], 
            results_int[0][2], results_int[1][2]
        )

    def contact_sensor(self, serial, output_int, output_ext):
        serial.write(b"run\n")
        reading = serial.readline()
        if reading == b"":
            print("couldn't not contact one station")
            # results_int.append(None)
        else:
            splits = reading.decode('utf-8').split(":")
            if splits[2] == -1:
                output_ext.append(splits)
            else:
                self._key_lock.acquire()
                output_int.append(splits)
                self._key_lock.release()

    def get_lecture_sensors_test_random(self):
        if self.heat_on or np.random.random_integers(0, 10) <= 8:
            temp_int = np.random.normal(23, 2)
        else:
            temp_int = np.random.normal(18, 2)

        readings = complete_readings(temp_int, temp_int, 0, 0, 0, 0, 0, 0)
        return readings
