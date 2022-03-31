import PySimpleGUI as sg
from UI import ComponentKeys, UI

sg.theme("DarkTeal12")
# calcul du next water lorsque ça éteint


class Interface:
    def __init__(self, components):
        self.layout = components.layout
        self.value_changed = None
        self.window_down = False
        self.values = None
        self.event = None
        self.co2_danger = False
        self.states = {
            "heat_on": False,
            "water_on": False,
            "vents_on": False,
            "lights_on": False,
        }
        self.window = sg.Window(
            "Contrôle de la serre",
            self.layout,
            element_justification="c",
            no_titlebar=True,
        )

    def __del__(self):
        self.layout = None
        self.values = None
        self.value_changed = None
        self.window_down = None
        self.event = None
        self.window = None

    def controlTimers(self, componentKey):
        if self.values[ComponentKeys.allKeys[componentKey]["TimerUsed"]]:
            self.window[ComponentKeys.allKeys[componentKey]["OnOffManual"]].update(
                disabled=False
            )
            self.window[ComponentKeys.allKeys[componentKey]["AllumeH"]].update(
                disabled=True
            )
            self.window[ComponentKeys.allKeys[componentKey]["AllumeM"]].update(
                disabled=True
            )
            self.window[ComponentKeys.allKeys[componentKey]["EteintH"]].update(
                disabled=True
            )
            self.window[ComponentKeys.allKeys[componentKey]["EteintM"]].update(
                disabled=True
            )
        else:
            self.window[ComponentKeys.allKeys[componentKey]["OnOffManual"]].update(
                disabled=True
            )
            self.window[ComponentKeys.allKeys[componentKey]["AllumeH"]].update(
                disabled=False
            )
            self.window[ComponentKeys.allKeys[componentKey]["AllumeM"]].update(
                disabled=False
            )
            self.window[ComponentKeys.allKeys[componentKey]["EteintH"]].update(
                disabled=False
            )
            self.window[ComponentKeys.allKeys[componentKey]["EteintM"]].update(
                disabled=False
            )

    def controlOnOffs(self, componentKey):
        if self.values[ComponentKeys.allKeys[componentKey]["OnOffManual"]]:
            self.window[ComponentKeys.allKeys[componentKey]["OnOffManual"]].update(
                text="On"
            )
            self.window[ComponentKeys.allKeys[componentKey]["OnOffManual"]].update(True)
        else:
            self.window[ComponentKeys.allKeys[componentKey]["OnOffManual"]].update(
                text="Off"
            )
            self.window[ComponentKeys.allKeys[componentKey]["OnOffManual"]].update(
                False
            )

    def updateSlider(self, componentKey, Add, increment):
        if not Add:
            new_value = (
                self.values[ComponentKeys.allKeys[componentKey]["Slider"]] - increment
            )
            self.window[ComponentKeys.allKeys[componentKey]["Slider"]].update(new_value)
        else:
            new_value = (
                self.values[ComponentKeys.allKeys[componentKey]["Slider"]] + increment
            )
            self.window[ComponentKeys.allKeys[componentKey]["Slider"]].update(new_value)
        if componentKey == "Pompe":
            zone = self.values[ComponentKeys.allKeys["Pompe"]["Zone"]]
            self.values["FreqWater" + str(zone)] = new_value

    def getValues(self):
        return self.values

    def setValues(self, updatedValues):
        for key in self.values:
            self.window[key].update(updatedValues[key])

    def checkChangements(self):
        value_changed_temp = self.value_changed
        if self.value_changed:
            self.value_changed = False
        return value_changed_temp

    def CO2NiveauCritiquePopup(self):
        self.co2_danger = True

    def updateRealTimeValues(self, dictValues):
        for key in dictValues._asdict():
            self.window[key].update(getattr(dictValues, key))

    def updateStateValues(self, stateValues):
        if stateValues.heat_turn_on or stateValues.heat_pulse_on:
            self.updateStateImage("Temp", True)
        else:
            self.updateStateImage("Temp", False)
        if stateValues.vent_turn_on:
            self.updateStateImage("Ventilateur", True)
        else:
            self.updateStateImage("Ventilateur", False)
        if stateValues.lights_turn_on:
            self.updateStateImage("Lumiere", True)
        else:
            self.updateStateImage("Lumiere", False)
        if (
            stateValues.water_1_on
            or stateValues.water_2_on
            or stateValues.water_3_on
            or stateValues.water_4_on
        ):
            self.updateStateImage("Pompe", True)
        else:
            self.updateStateImage("Pompe", False)

    def updateStateImage(self, componentKey, state):
        if state:
            self.window[ComponentKeys.allKeys[componentKey]["StateImage"]].update(
                filename="UI/green_power_sign.png"
            )
        else:
            self.window[ComponentKeys.allKeys[componentKey]["StateImage"]].update(
                filename="UI/red_power_sign.png"
            )

    def runInterface(self, config_file, q):
        self.event, self.values = self.window.read(timeout=500)
        self.setValues(config_file)
        time_count = 0
        while True:
            self.event, self.values = self.window.read(timeout=1)
            time_count += 1
            if self.co2_danger and time_count > 10000:
                event, values = UI.CO2NiveauCritiquePopup()
                self.co2_danger = False
                time_count = 0
            if not q.empty():
                readings = q.get()
                q.task_done()
                for key in readings._asdict():
                    self.window[key].update(getattr(readings, key))
                self.window["HumidMoy"].update(
                    round(
                        (
                            getattr(readings, "hum_int_1")
                            + getattr(readings, "hum_int_2")
                        )
                        / 2,
                        2,
                    )
                )
                self.window["TempMoy"].update(
                    round(
                        (
                            getattr(readings, "temp_int_1")
                            + getattr(readings, "temp_int_2")
                        )
                        / 2,
                        2,
                    )
                )

            # main logic from down here
            if self.event in (None, "Exit", "Fermer", sg.WINDOW_CLOSED):
                self.window_down = True
                break
            else:
                if self.event != sg.TIMEOUT_KEY:
                    self.value_changed = True
                if self.event == ComponentKeys.allKeys["Lumiere"]["TimerUsed"]:
                    self.controlTimers("Lumiere")
                if self.event == ComponentKeys.allKeys["Lumiere"]["OnOffManual"]:
                    self.controlOnOffs("Lumiere")
                if self.event == "MotorOnButton":
                    self.window["MotorOnButton"].update(button_color="green")
                    self.window["MotorOffButton"].update(button_color="grey")
                    self.updateStateImage("Moteur", True)
                if self.event == "MotorOffButton":
                    self.window["MotorOffButton"].update(button_color="green")
                    self.window["MotorOnButton"].update(button_color="grey")
                    self.updateStateImage("Moteur", False)
                if self.event == ComponentKeys.allKeys["Pompe"]["Sub"]:
                    self.updateSlider("Pompe", False, 5)
                if self.event == ComponentKeys.allKeys["Pompe"]["Add"]:
                    self.updateSlider("Pompe", True, 5)
                if self.event == ComponentKeys.allKeys["CO2"]["Sub"]:
                    self.updateSlider("CO2", False, 10)
                if self.event == ComponentKeys.allKeys["CO2"]["Add"]:
                    self.updateSlider("CO2", True, 10)
                if self.event == ComponentKeys.allKeys["Temp"]["Sub"]:
                    self.updateSlider("Temp", False, 0.5)
                if self.event == ComponentKeys.allKeys["Temp"]["Add"]:
                    self.updateSlider("Temp", True, 0.5)
                if self.event == ComponentKeys.allKeys["Humidity"]["Sub"]:
                    self.updateSlider("Humidity", False, 2)
                if self.event == ComponentKeys.allKeys["Humidity"]["Add"]:
                    self.updateSlider("Humidity", True, 2)
