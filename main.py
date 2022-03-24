# from hardwareAccess import HardwareAccess
from Control.DummyHardwareAccess import DummyHardwareAccess
import time
from threading import Thread
from UI.Interface import Interface
from UI.UI import Components
from Control.ControlLogic import ControlLogic
from Utils.ValuesSaver import ValuesSaver
from queue import Queue

# config_file = "Utils/config.json"
config_file_path = "Utils/config_test.json"
hardware = DummyHardwareAccess()
logic = None  # ControlLogic()
valuesSaver = ValuesSaver(config_file_path)
components = Components()
interface = Interface(components)
q = Queue()


def main():
    config_file = setup()
    t_1 = Thread(target=interface.runInterface, args=(config_file, q))
    t_2 = Thread(target=actionLoop)
    t_1.start()
    t_2.start()
    t_1.join()
    t_2.join()


def actionLoop():
    co2_level = 0
    while True:
        # ping_watchdog()
        if interface.window_down:
            break
        changements = interface.checkChangements()
        if changements:
            # logic.update(changements)
            valuesSaver.updateValues(interface.getValues())
        co2_level += 1
        if co2_level > 5:
            interface.CO2NiveauCritiquePopup()
            # readings = hardware.get_lecture_sensors_test_simulated("test_winter_focus_temp")
            co2_level = 0
        readings = hardware.get_lecture_sensors_test_random()
        q.put(readings)
        q.join()
        # print("La température est de :" + str(readings.temp_int) + "˚C")
        actions = logic.logic_loop(readings)
        # hardware.traitement_actions(actions)
        time.sleep(0.5)


def setup():
    hardware.setup_hardware_access()
    return load_config()


def load_config():
    config = valuesSaver.getValues()
    global logic
    logic = ControlLogic(config)
    return config


def ping_watchdog():
    file_to_open = open("/dev/watchdog", "w")
    file_to_open.write("S")
    file_to_open.close()


if __name__ == "__main__":
    main()
