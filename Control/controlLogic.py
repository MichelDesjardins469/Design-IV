from datetime import datetime


TARGET_TEMP = 20
TIME_LUMIERE = datetime(1970, 1, 1, 16, 46, 00)


def load_config(config):
    global TARGET_TEMP
    TARGET_TEMP = config.target_temp

def logic_loop(sensorReadings):
    return_value = 0
    if sensorReadings.temp_int < TARGET_TEMP:
        print("temperature sous " + str(TARGET_TEMP) + "˚C")
        return_value = 1
    if datetime.now().time() > TIME_LUMIERE.time():
        print("Il est passé " + TIME_LUMIERE.strftime("%H:%M:%S"))
        if return_value > 0:
            return_value = 3
        else:
            return_value = 2

    return return_value
