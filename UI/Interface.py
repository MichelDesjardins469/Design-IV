import PySimpleGUI as sg
from UI import ComponentKeys, UI
import time

sg.theme("DarkTeal12")


class Interface:
    def __init__(self, components):
        self.layout = components.layout
        self.values = None
        self.valueChanged = None
        self.windowDown = False
        self.CO2Danger = False
        self.event = None
        self.window = sg.Window(
            "Contrôle de la serre", self.layout, element_justification="c"
        )

    def __del__(self):
        self.layout = None
        self.values = None
        self.valueChanged = None
        self.windowDown = None
        self.event = None
        self.window = None

    def controlTimers(self, componentKey):
        if self.values[ComponentKeys.allKeys[componentKey]["TimerUsed"]] == True:
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
        if self.values[ComponentKeys.allKeys[componentKey]["OnOffManual"]] == True:
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
            newValue = (
                self.values[ComponentKeys.allKeys[componentKey]["Slider"]] - increment
            )
            self.window[ComponentKeys.allKeys[componentKey]["Slider"]].update(newValue)
        else:
            newValue = (
                self.values[ComponentKeys.allKeys[componentKey]["Slider"]] + increment
            )
            self.window[ComponentKeys.allKeys[componentKey]["Slider"]].update(newValue)
        if componentKey == "Pompe":
            zone = self.values[ComponentKeys.allKeys["Pompe"]["Zone"]]
            self.values["FreqWater" + str(zone)] = newValue

    def getValues(self):
        return self.values

    def checkChangements(self):
        valueChangedTemp = self.valueChanged
        if self.valueChanged == True:
            self.valueChanged = False
        return valueChangedTemp

    def CO2NiveauCritiquePopup(self):
        self.CO2Danger = True

    def runInterface(self):
        timeCount = 0
        while True:
            self.event, self.values = self.window.read(timeout=500)
            timeCount += 1
            if self.CO2Danger and timeCount > 7200:
                event, values = UI.CO2NiveauCritiquePopup()
                self.CO2Danger = False
                timeCount = 0
            # main logic from down here
            if self.event in (None, "Exit", "Cancel"):
                self.windowDown = True
                break
            else:
                self.valueChanged = True
                if self.event == ComponentKeys.allKeys["Lumiere"]["TimerUsed"]:
                    # sg.popup('Bonjour')
                    self.valueChanged = True
                    self.controlTimers("Lumiere")
                if self.event == ComponentKeys.allKeys["Moteur"]["TimerUsed"]:
                    self.controlTimers("Moteur")
                if self.event == ComponentKeys.allKeys["Lumiere"]["OnOffManual"]:
                    self.controlOnOffs("Lumiere")
                if self.event == ComponentKeys.allKeys["Moteur"]["OnOffManual"]:
                    self.controlOnOffs("Moteur")
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
                    self.updateSlider("Humidity", Truea, 2)
                if self.event == "Soumettre":
                    print(self.values)
