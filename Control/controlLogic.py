from datetime import datetime

TRESHOLD_TEMP_EXT = 15



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
        retour_lights = self.check_lights
        retour_water = self.check_water
        retour_temp = self.check_temp
        retour_hum = self.check_hum

    def check_lights(self):
        open = False
        if datetime.now().time() > self.time_light_open.time() and datetime.now().time() < self.time_light_close.time():
            open = True
        return open

    def check_water(self, id):
        pass

    def check_temp(self, temp_int, temp_ext):
        if temp_int < (self.target_temp - self.range_temp):
            #start_chauffage
            self.free_hum = False
        elif temp_int > (self.target_temp + self.range_temp):
            if temp_ext > TRESHOLD_TEMP_EXT:
                #stop_chauffage
                pass
            else:
                #start_vent
                pass      
            self.free_hum = False
        else:
            self.free_hum = True

    def check_hum(self, hum_int, hum_ext):
        if self.free_hum:
            if hum_int < (self.target_hum - self.range_hum):
                #stop_vent
                pass
            elif hum_int > (self.target_hum + self.range_hum):
                #start_vent
                if hum_int > (self.target_hum + self.range_hum + 0.15):
                    #pulse_chauffage
                    pass