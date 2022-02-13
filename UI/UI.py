import PySimpleGUI as sg
import control
import componentKeys

# option pour choisir le type de plante
# Ajouter une option rajouter de la lumiere instant si exemple is annonce gris
sg.theme("DarkTeal12")


def Slider2button(text, keySub, keySlider, keyAdd, minValue, maxValue, defaultValue):
    return [
        sg.Text(text),
        sg.Button(
            "",
            key=keySub,
            button_color=(sg.theme_background_color(), sg.theme_background_color()),
            image_filename="UI/minus_sign.png",
            image_size=(25, 25),
            image_subsample=2,
        ),
        sg.Slider(
            key=keySlider,
            range=(minValue, maxValue),
            default_value=defaultValue,
            size=(20, 5),
            orientation="horizontal",
            font=("Helvetica", 12),
            resolution=0.5,
            enable_events=True,
        ),
        sg.Button(
            "",
            key=keyAdd,
            button_color=(sg.theme_background_color(), sg.theme_background_color()),
            image_filename="UI/plus_sign.png",
            image_size=(25, 25),
            image_subsample=2,
        ),
    ]
def nouvelAppareilPopup():
    return [sg.OptionMenu(['Unité de chauffage', 'Ventilateur', 'Lumière',],s=(15,2))]

def controleHeures(
    keyHeuresA, keyMinutesA, keyHeuresE, keyMinutesE, keyCheckBoxTimers, keyControlTimer
):
    return [
        [
            sg.Text("Heure d'allumage"),
            sg.Combo(control.hours, key=keyHeuresA, default_value=8),
            sg.Combo(control.minutes, key=keyMinutesA, default_value=0),
            sg.Text("Heure d'éteignement"),
            sg.Combo(control.hours, key=keyHeuresE, default_value=16),
            sg.Combo(control.minutes, key=keyMinutesE, default_value=0),
            sg.Checkbox(
                "Ne pas considérer les minuteurs",
                key=keyCheckBoxTimers,
                default=False,
                enable_events=True,
            ),
            sg.Checkbox(
                "Off",
                key=keyControlTimer,
                default=False,
                disabled=True,
                enable_events=True,
            ),
        ]
    ]


frame_inputs_layout = [
    Slider2button(
        "Température désirée (°C) ", componentKeys.allKeys["Temp"]["Sub"], "SliderTemp", componentKeys.allKeys["Temp"]["Add"], 0, 35, 20
    ),
    Slider2button(
        "Humidité désirée(%)", componentKeys.allKeys["Humidity"]["Sub"], "SliderHumid", componentKeys.allKeys["Humidity"]["Add"], 0, 100, 80
    ),
]
frame_hours_control_pompe = controleHeures(
    componentKeys.allKeys["Pompe"]["AllumeH"],
    componentKeys.allKeys["Pompe"]["AllumeM"],
    componentKeys.allKeys["Pompe"]["EteintH"],
    componentKeys.allKeys["Pompe"]["EteintM"],
    componentKeys.allKeys["Pompe"]["TimerUsed"],
    componentKeys.allKeys["Pompe"]["OnOffManual"],
)
frame_hours_control_moteur = controleHeures(
    componentKeys.allKeys["Moteur"]["AllumeH"],
    componentKeys.allKeys["Moteur"]["AllumeM"],
    componentKeys.allKeys["Moteur"]["EteintH"],
    componentKeys.allKeys["Moteur"]["EteintM"],
    componentKeys.allKeys["Moteur"]["TimerUsed"],
    componentKeys.allKeys["Moteur"]["OnOffManual"],
)
frame_hours_control_lumiere = controleHeures(
    componentKeys.allKeys["Lumiere"]["AllumeH"],
    componentKeys.allKeys["Lumiere"]["AllumeM"],
    componentKeys.allKeys["Lumiere"]["EteintH"],
    componentKeys.allKeys["Lumiere"]["EteintM"],
    componentKeys.allKeys["Lumiere"]["TimerUsed"],
    componentKeys.allKeys["Lumiere"]["OnOffManual"],
)

layout = [
    [
        sg.Frame(
            "Variables contrôlables",
            frame_inputs_layout,
            font="Any 12",
            title_color="white",
        )
    ],
    [
        sg.Frame(
            "Contrôle des Pompes",
            frame_hours_control_pompe,
            font="Any 12",
            title_color="white",
        )
    ],
    [
        sg.Frame(
            "Contrôle des moteurs des volets",
            frame_hours_control_moteur,
            font="Any 12",
            title_color="white",
        )
    ],
    [
        sg.Frame(
            "Contrôle de la lumière",
            frame_hours_control_lumiere,
            font="Any 12",
            title_color="white",
        )
    ],
    [sg.Output(size=(80, 5))],
    [sg.Button("Soumettre", bind_return_key=True), sg.Cancel()],
]
co2value = 0
window = sg.Window(
    "Contrôle de la serre", layout, element_justification="c", size=(1050, 730)
)


def controlTimers(componentKey):
    if values[componentKeys.allKeys[componentKey]["TimerUsed"]] == True:
        window[componentKeys.allKeys[componentKey]["OnOffManual"]].update(
            disabled=False
        )
        window[componentKeys.allKeys[componentKey]["AllumeH"]].update(disabled=True)
        window[componentKeys.allKeys[componentKey]["AllumeM"]].update(disabled=True)
        window[componentKeys.allKeys[componentKey]["EteintH"]].update(disabled=True)
        window[componentKeys.allKeys[componentKey]["EteintM"]].update(disabled=True)
    else:
        window[componentKeys.allKeys[componentKey]["OnOffManual"]].update(disabled=True)
        window[componentKeys.allKeys[componentKey]["AllumeH"]].update(disabled=False)
        window[componentKeys.allKeys[componentKey]["AllumeM"]].update(disabled=False)
        window[componentKeys.allKeys[componentKey]["EteintH"]].update(disabled=False)
        window[componentKeys.allKeys[componentKey]["EteintM"]].update(disabled=False)


def controlOnOffs(componentKey):
    if values[componentKeys.allKeys[componentKey]["OnOffManual"]] == True:
        window[componentKeys.allKeys[componentKey]["OnOffManual"]].update(text="On")
        window[componentKeys.allKeys[componentKey]["OnOffManual"]].update(True)
    else:
        window[componentKeys.allKeys[componentKey]["OnOffManual"]].update(text="Off")
        window[componentKeys.allKeys[componentKey]["OnOffManual"]].update(False)

def updateSlider(componentKey, Add):
    if not Add:
        newValue = values[componentKeys.allKeys[componentKey]["Slider"]] - 0.5
        window[componentKeys.allKeys[componentKey]["Slider"]].update(newValue)
    else:
        newValue = values[componentKeys.allKeys[componentKey]["Slider"]] + 0.5
        window[componentKeys.allKeys[componentKey]["Slider"]].update(newValue)
while True:  # The Event Loop
    event, values = window.read(
        timeout=500
    )  # this sets the time between each "refresh"
    co2value += 1
    if co2value > 5:
        #20sg.popup('Jadore les lapins',title='Nouvel appareil detect',  button_color="red")
        co2value = 0
        confirmation, appareilChoisi = sg.Window('NOUVEL APAREIL DÉTECTÉ', [[sg.T("Veuillez sélectionner l'appareil correspondant")], [nouvelAppareilPopup()], [sg.Yes('Confirmer', s=10), sg.No('Annuler', s=10)]], disable_close=True).read(close=True)
        print( appareilChoisi[0])
    if event in (None, "Exit", "Cancel"):
        break
    elif event == componentKeys.allKeys["Lumiere"]["TimerUsed"]:
        controlTimers("Lumiere")
    elif event == componentKeys.allKeys["Moteur"]["TimerUsed"]:
        controlTimers("Moteur")
    elif event == componentKeys.allKeys["Pompe"]["TimerUsed"]:
        controlTimers("Pompe")
    elif event == componentKeys.allKeys["Lumiere"]["OnOffManual"]:
        controlOnOffs("Lumiere")
    elif event == componentKeys.allKeys["Moteur"]["OnOffManual"]:
        controlOnOffs("Moteur")
    elif event == componentKeys.allKeys["Pompe"]["OnOffManual"]:
        controlOnOffs("Pompe")
    elif event == componentKeys.allKeys["Temp"]["Sub"]:
        updateSlider("Temp", False)
    elif event == componentKeys.allKeys["Temp"]["Add"]:
        updateSlider("Temp", True)
    elif event == componentKeys.allKeys["Humidity"]["Sub"]:
        updateSlider("Humidity", False)
    elif event == componentKeys.allKeys["Humidity"]["Add"]:
        updateSlider("Humidity", True)
    elif event == "Soumettre" :
        print(values)
