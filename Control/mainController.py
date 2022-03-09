from hardwareAccess import HardwareAccess
from Utils.ValuesSaver import ValuesSaver
from UI.Interface import Interface
from UI.UI import Components
from controlLogic import ControlLogic
import time
import json
from multiprocessing import Process

config_file = "config.json"
config = {}
hardware = HardwareAccess()
logic = ControlLogic()
valuesSaver = ValuesSaver(config_file)
components = Components()
interface = Interface(components)


def main():
    setup()
    p1 = Process(target=interface.runInterface())
    p1.start()
    p2 = Process(target=actionLoop())
    p2.start()
    p1.join()
    p2.join()


def actionLoop():
    while True:
        # ping_watchdog()
        changements = interface.checkChangements()
        if changements:
            logic.update(changements)
            valuesSaver.updateValues(interface.getValues())
        readings = hardware.get_lecture_sensors_test_random()
        print("La température est de :" + str(readings.temp_int) + "˚C")
        actions = logic.logic_loop(readings)
        hardware.traitement_actions(actions)
        time.sleep(5)


def setup():
    hardware.setup_hardware_access()
    load_config()


def load_config():
    config = valuesSaver.getValues()


def ping_watchdog():
    f = open("/dev/watchdog", "w")
    f.write("S")
    f.close()


if __name__ == "__main__":
    main()
