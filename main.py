# from hardwareAccess import HardwareAccess
from Utils.ValuesSaver import ValuesSaver
from UI.Interface import Interface
from UI.UI import Components
from Control.ControlLogic import ControlLogic
import time
import json
from threading import Thread

config_file = "Utils/config.json"
config = {}
# hardware = HardwareAccess()
logic = ControlLogic()
valuesSaver = ValuesSaver(config_file)
components = Components()
interface = Interface(components)


def main():
    setup()
    t1 = Thread(target=interface.runInterface)
    t2 = Thread(target=actionLoop)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def actionLoop():
    CO2Level = 0
    while True:
        # ping_watchdog()
        if interface.windowDown:
            break
        changements = interface.checkChangements()
        if changements:
            logic.update(changements)
            valuesSaver.updateValues(interface.getValues())
        CO2Level += 1
        if CO2Level > 5:
            interface.CO2NiveauCritiquePopup()
            CO2Level = 0
        # readings = hardware.get_lecture_sensors_test_random()
        # print("La température est de :" + str(readings.temp_int) + "˚C")
        # actions = logic.logic_loop(readings)
        # hardware.traitement_actions(actions)
        time.sleep(1)


def setup():
    # hardware.setup_hardware_access()
    load_config()


def load_config():
    config = valuesSaver.getValues()


def ping_watchdog():
    f = open("/dev/watchdog", "w")
    f.write("S")
    f.close()


if __name__ == "__main__":
    main()
