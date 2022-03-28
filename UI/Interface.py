import PySimpleGUI as sg
from UI import ComponentKeys, UI

sg.theme("DarkTeal12")


class Interface:
    def __init__(self, components):
        self.layout = components.layout
        self.value_changed = None
        self.window_down = False
        self.values = None
        self.event = None
        self.co2_danger = False
        self.window = sg.Window(
            "Contrôle de la serre", self.layout, element_justification="c"
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
        self.values.update(stateValues)

    def runInterface(self, config_file, q):
        self.event, self.values = self.window.read(timeout=500)
        self.setValues(config_file)
        time_count = 0
        while True:
            self.event, self.values = self.window.read(timeout=500)
            time_count += 1
            if self.co2_danger and time_count > 7200:
                event, values = UI.CO2NiveauCritiquePopup()
                self.co2_danger = False
                time_count = 0
            readings = q.get()
            for key in readings._asdict():
                self.window[key].update(getattr(readings, key))
            self.window["HumidMoy"].update(
                (getattr(readings, "hum_int_1") + getattr(readings, "hum_int_2")) / 2
            )
            self.window["TempMoy"].update(
                (getattr(readings, "temp_int_1") + getattr(readings, "temp_int_2")) / 2
            )
            q.task_done()
            # main logic from down here
            if self.event in (None, "Exit", "Cancel"):
                self.window_down = True
                break
            else:
                self.value_changed = True
                if self.event == ComponentKeys.allKeys["Lumiere"]["TimerUsed"]:
                    # sg.popup('Bonjour')
                    self.value_changed = True
                    self.controlTimers("Lumiere")
                if self.event == "MotorOnButton":
                    self.window["MotorOnButton"].update(button_color="green")
                    self.window["MotorOffButton"].update(button_color="grey")
                if self.event == "MotorOffButton":
                    self.window["MotorOffButton"].update(button_color="green")
                    self.window["MotorOnButton"].update(button_color="grey")
                if self.event == ComponentKeys.allKeys["Pompe"]["OnOffManual"]:
                    self.controlOnOffs("Pompe")
                    self.window[ComponentKeys.allKeys["Pompe"]["StateImage"]].update(
                        filename="UI/green_power_sign.png"
                    )
                if self.event == ComponentKeys.allKeys["Pompe"]["Sub"]:
                    self.updateSlider("Pompe", False, 5)
                if self.event == ComponentKeys.allKeys["Pompe"]["Add"]:
                    self.updateSlider("Pompe", True, 5)
                # if self.event == ComponentKeys.allKeys["Pompe"]["Slider"]:
                #    zone = self.values[ComponentKeys.allKeys["Pompe"]["Zone"]]
                #    self.values["FreqWater" + str(zone)] = self.values[
                #        ComponentKeys.allKeys["Pompe"]["Slider"]
                #    ]
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
                if self.event == "Soumettre":
                    print(self.values)
