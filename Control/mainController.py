from hardwareAccess import HardwareAccess
import controlLogic
import time
import json

config_file = "config.json"
hardware = HardwareAccess()
logic = controlLogic()


def main():
    setup()

    while True:
        # ping_watchdog()
        changements = interface.checkChangements()
        if changements:
            logic.update(changements)
        readings = hardware.get_lecture_sensors_test_random()
        print("La température est de :" + str(readings.temp_int) + "˚C")
        actions = logic.logic_loop(readings)
        hardware.traitement_actions(actions)
        time.sleep(5)


def setup():
    hardware.setup_hardware_access()
    load_config()


def load_config():
    f = open(config_file)
    config = json.load(f)
    logic.load_config(config)


def ping_watchdog():
    f = open("/dev/watchdog", "w")
    f.write("S")
    f.close()


if __name__ == "__main__":
    main()
