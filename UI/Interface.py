import PySimpleGUI as sg
from UI import ComponentKeys

sg.theme("DarkTeal12")


class Interface:
    def __init__(self, components):
        self.layout = components.layout
        self.values = None
        self.valueChanged = None
        self.event = None
        self.window = sg.Window(
            "Contrôle de la serre", self.layout, element_justification="c"
        )

    def __del__(self):
        self.layout = None
        self.values = None
        self.valueChanged = None
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

    def updateSlider(self, componentKey, Add):
        if not Add:
            newValue = self.values[ComponentKeys.allKeys[componentKey]["Slider"]] - 0.5
            self.window[ComponentKeys.allKeys[componentKey]["Slider"]].update(newValue)
        else:
            newValue = self.values[ComponentKeys.allKeys[componentKey]["Slider"]] + 0.5
            self.window[ComponentKeys.allKeys[componentKey]["Slider"]].update(newValue)

    def getValues(self):
        return self.values

    def checkChangements(self):
        valueChangedTemp = self.valueChanged
        if self.valueChanged == True:
            self.valueChanged = False
        return valueChangedTemp

    def runInterface(self):
        while True:
            self.event, self.values = self.window.read(timeout=500)
            if self.event in (None, "Exit", "Cancel"):
                break
            else:
                self.valueChanged = True
                if self.event == ComponentKeys.allKeys["Lumiere"]["TimerUsed"]:
                    self.valueChanged = True
                    self.controlTimers("Lumiere")
                if self.event == ComponentKeys.allKeys["Moteur"]["TimerUsed"]:
                    self.controlTimers("Moteur")
                if self.event == ComponentKeys.allKeys["Pompe"]["TimerUsed"]:
                    self.controlTimers("Pompe")
                    self.window[ComponentKeys.allKeys["Lumiere"]["StateImage"]].update(
                        filename="UI/green_power_sign.png"
                    )
                if self.event == ComponentKeys.allKeys["Lumiere"]["OnOffManual"]:
                    self.controlOnOffs("Lumiere")
                if self.event == ComponentKeys.allKeys["Moteur"]["OnOffManual"]:
                    self.controlOnOffs("Moteur")
                if self.event == ComponentKeys.allKeys["Pompe"]["OnOffManual"]:
                    self.controlOnOffs("Pompe")
                if self.event == ComponentKeys.allKeys["Temp"]["Sub"]:
                    self.updateSlider("Temp", False)
                if self.event == ComponentKeys.allKeys["Temp"]["Add"]:
                    self.updateSlider("Temp", True)
                if self.event == ComponentKeys.allKeys["Humidity"]["Sub"]:
                    self.updateSlider("Humidity", False)
                if self.event == ComponentKeys.allKeys["Humidity"]["Add"]:
                    self.updateSlider("Humidity", True)
                if self.event == "Soumettre":
                    print(self.values)
