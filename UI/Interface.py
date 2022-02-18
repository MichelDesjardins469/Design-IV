import PySimpleGUI as sg
import UI
import componentKeys

sg.theme("DarkTeal12")
# trouver pour faire fonctionner les boutons et executer la fonction getValuesTest en background


class Interface:
    def __init__(self, components):
        self.layout = components.layout
        self.window = sg.Window(
            "Contrôle de la serre", self.layout, element_justification="c"
        )

    def controlTimers(self, componentKey):
        if self.values[componentKeys.allKeys[componentKey]["TimerUsed"]] == True:
            self.window[componentKeys.allKeys[componentKey]["OnOffManual"]].update(
                disabled=False
            )
            self.window[componentKeys.allKeys[componentKey]["AllumeH"]].update(
                disabled=True
            )
            self.window[componentKeys.allKeys[componentKey]["AllumeM"]].update(
                disabled=True
            )
            self.window[componentKeys.allKeys[componentKey]["EteintH"]].update(
                disabled=True
            )
            self.window[componentKeys.allKeys[componentKey]["EteintM"]].update(
                disabled=True
            )
        else:
            self.window[componentKeys.allKeys[componentKey]["OnOffManual"]].update(
                disabled=True
            )
            self.window[componentKeys.allKeys[componentKey]["AllumeH"]].update(
                disabled=False
            )
            self.window[componentKeys.allKeys[componentKey]["AllumeM"]].update(
                disabled=False
            )
            self.window[componentKeys.allKeys[componentKey]["EteintH"]].update(
                disabled=False
            )
            self.window[componentKeys.allKeys[componentKey]["EteintM"]].update(
                disabled=False
            )

    def controlOnOffs(self, componentKey):
        if self.values[componentKeys.allKeys[componentKey]["OnOffManual"]] == True:
            self.window[componentKeys.allKeys[componentKey]["OnOffManual"]].update(
                text="On"
            )
            self.window[componentKeys.allKeys[componentKey]["OnOffManual"]].update(True)
        else:
            self.window[componentKeys.allKeys[componentKey]["OnOffManual"]].update(
                text="Off"
            )
            self.window[componentKeys.allKeys[componentKey]["OnOffManual"]].update(
                False
            )

    def updateSlider(self, componentKey, Add):
        if not Add:
            newValue = self.values[componentKeys.allKeys[componentKey]["Slider"]] - 0.5
            self.window[componentKeys.allKeys[componentKey]["Slider"]].update(newValue)
        else:
            newValue = self.values[componentKeys.allKeys[componentKey]["Slider"]] + 0.5
            self.window[componentKeys.allKeys[componentKey]["Slider"]].update(newValue)

    def getValuesTest(self):
        while True:
            self.event, self.values = self.window.read(timeout=500)
            if self.event in (None, "Exit", "Cancel"):
                break
            elif self.event == componentKeys.allKeys["Lumiere"]["TimerUsed"]:
                self.controlTimers("Lumiere")
            elif self.event == componentKeys.allKeys["Moteur"]["TimerUsed"]:
                self.controlTimers("Moteur")
            elif self.event == componentKeys.allKeys["Pompe"]["TimerUsed"]:
                self.controlTimers("Pompe")
            elif self.event == componentKeys.allKeys["Lumiere"]["OnOffManual"]:
                self.controlOnOffs("Lumiere")
            elif self.event == componentKeys.allKeys["Moteur"]["OnOffManual"]:
                self.controlOnOffs("Moteur")
            elif self.event == componentKeys.allKeys["Pompe"]["OnOffManual"]:
                self.controlOnOffs("Pompe")
            elif self.event == componentKeys.allKeys["Temp"]["Sub"]:
                self.updateSlider("Temp", False)
            elif self.event == componentKeys.allKeys["Temp"]["Add"]:
                self.updateSlider("Temp", True)
            elif self.event == componentKeys.allKeys["Humidity"]["Sub"]:
                self.updateSlider("Humidity", False)
            elif self.event == componentKeys.allKeys["Humidity"]["Add"]:
                self.updateSlider("Humidity", True)
            elif self.event == "Soumettre":
                print(self.values)
