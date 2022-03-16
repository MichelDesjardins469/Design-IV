from datetime import datetime
from collections import namedtuple
import numpy as np

TRESHOLD_TEMP_EXT = 15
TRESHOLD_TOO_HUM = 0.15

actions = namedtuple(
    "actions", "heat_turn_on heat_turn_off vent_turn_on vent_turn_off lights_turn_on water_1_on water_2_on water_3_on water_4_on heat_pulse_on"
)

class ControlLogic:
    target_temp = 0
    range_temp = 0
    target_hum = 0
    range_hum = 0
    time_light_open = 0
    time_light_close = 0
    freq_water_1 = 0
    next_water_1 = 0
    freq_water_2 = 0
    next_water_2 = 0
    freq_water_3 = 0
    next_water_3 = 0
    freq_water_4 = 0
    next_water_4 = 0
    free_hum = False

    def load_config(self, config):
        self.target_temp = config.target_temp
        self.range_temp = config.range_temp
        self.target_hum = config.target_hum
        self.range_hum = config.range_hum
        self.time_light_open = config.time_light_open
        self.time_light_close = config.time_light_close
        self.freq_water_1 = config.freq_water_1
        self.next_water_1 = config.next_water_1
        self.freq_water_2 = config.freq_water_2
        self.next_water_2 = config.next_water_2
        self.freq_water_3 = config.freq_water_3
        self.next_water_3 = config.next_water_3
        self.freq_water_4 = config.freq_water_4
        self.next_water_4 = config.next_water_4

    def update(self, changes):
        pass

    def logic_loop(self, sensorReadings):
        mean_temp = np.mean([sensorReadings.temp_int_1, sensorReadings.temp_int_2])
        mean_hum = np.mean([sensorReadings.hum_int_1, sensorReadings.hum_int_2])
        retour_lights = self.check_lights()
        retour_water_1 = self.check_water(1)
        retour_water_2 = self.check_water(2)
        retour_water_3 = self.check_water(3)
        retour_water_4 = self.check_water(4)
        id_temp = self.check_temp(mean_temp, sensorReadings.temp_ext)
        id_hum = self.check_hum(mean_hum, sensorReadings.hum_ext)
        retour_heat_on = False
        retour_heat_off = False
        retour_vent_on = False
        retour_vent_off = False
        retour_pulse_on = False
        match id_temp:
            case 1:
                retour_heat_on = True
                retour_vent_off = True
            case 2:
                retour_heat_off = True
            case 3:
                retour_vent_on = True

        match id_hum:
            case 1:
                retour_vent_off = True
            case 2:
                retour_vent_on = True
            case 3:
                retour_vent_on = True
                retour_pulse_on = True
                
        return actions(retour_heat_on, retour_heat_off, retour_vent_on, retour_vent_off, 
                        retour_lights, retour_water_1, retour_water_2,  retour_water_3,  retour_water_4, retour_pulse_on)        

    def check_lights(self):
        open = False
        if (
            datetime.now().time() > self.time_light_open.time()
            and datetime.now().time() < self.time_light_close.time()
        ):
            open = True
        return open

    def check_water(self, id):
        now = datetime.now.time()
        retour = False
        match id:
            case 1:
                if now > self.next_water_1:
                    retour = True
                    self.next_water_1 = self.next_water_1 + datetime.timedelta(hours=self.freq_water_1)
            case 2:
                if now > self.next_water_2:
                    retour = True
                    self.next_water_2 = self.next_water_2 + datetime.timedelta(hours=self.freq_water_2)
            case 3:
                if now > self.next_water_3:
                    retour = True
                    self.next_water_3 = self.next_water_3 + datetime.timedelta(hours=self.freq_water_3)
            case 4:
                if now > self.next_water_4:
                    retour = True
                    self.next_water_4 = self.next_water_4 + datetime.timedelta(hours=self.freq_water_4)
        return retour



    def check_temp(self, temp_int, temp_ext):
        retour = 0
        if temp_int < (self.target_temp - self.range_temp):
            # start_chauffage
            # stop_vent
            retour = 1
            self.free_hum = False
        elif temp_int > (self.target_temp + self.range_temp):
            if temp_ext > TRESHOLD_TEMP_EXT:
                # stop_chauffage
                retour = 2
                pass
            else:
                # start_vent
                retour = 3
                pass      
            self.free_hum = False
        else:
            self.free_hum = True
        return retour

    def check_hum(self, hum_int, hum_ext):
        retour = 0
        if self.free_hum:
            if hum_int < (self.target_hum - self.range_hum):
                # stop_vent
                retour = 1
                pass
            elif hum_int > (self.target_hum + self.range_hum):
                # start_vent
                retour = 2
                if hum_int > (self.target_hum + self.range_hum + TRESHOLD_TOO_HUM):
                    # pulse_chauffage
                    retour = 3
                    pass
        return retour

