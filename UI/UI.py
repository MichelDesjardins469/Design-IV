import PySimpleGUI as sg
import control
import componentKeys

# option pour choisir le type de plante
# Ajouter une option rajouter de la lumiere instant si exemple is annonce gris
sg.theme("DarkTeal12")


def slider2button(text, keySub, keySlider, keyAdd, minValue, maxValue, defaultValue):
    return [
        sg.Text(text),
        sg.Button(
            "",
            key=keySub,
            button_color=(sg.theme_background_color(), sg.theme_background_color()),
            image_filename="./minus_sign.png",
            image_size=(25, 25),
            image_subsample=2,
        ),
        sg.Slider(
            key=keySlider,
            range=(minValue, maxValue),
            default_value=defaultValue,
            size=(20, 15),
            orientation="horizontal",
            font=("Helvetica", 12),
            resolution=0.5,
        ),
        sg.Button(
            "",
            key=keyAdd,
            button_color=(sg.theme_background_color(), sg.theme_background_color()),
            image_filename="./plus_sign.png",
            image_size=(25, 25),
            image_subsample=2,
        ),
    ]


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
    slider2button(
        "Température désirée (°C) ", "TempSub", "SliderTemp", "TempAdd", 0, 35, 20
    ),
    slider2button(
        "Humidité désirée(%)", "HumidSub", "SliderHumid", "HumidAdd", 0, 100, 80
    ),
]
frame_hours_control_pompe = controleHeures(
    componentKeys.allKeys["pompe"]["AllumeH"],
    componentKeys.allKeys["pompe"]["AllumeM"],
    componentKeys.allKeys["pompe"]["EteintH"],
    componentKeys.allKeys["pompe"]["EteintM"],
    componentKeys.allKeys["pompe"]["TimerUsed"],
    componentKeys.allKeys["pompe"]["OnOffManual"],
)
frame_hours_control_moteur = controleHeures(
    componentKeys.allKeys["moteur"]["AllumeH"],
    componentKeys.allKeys["moteur"]["AllumeM"],
    componentKeys.allKeys["moteur"]["EteintH"],
    componentKeys.allKeys["moteur"]["EteintM"],
    componentKeys.allKeys["moteur"]["TimerUsed"],
    componentKeys.allKeys["moteur"]["OnOffManual"],
)
frame_hours_control_lumiere = controleHeures(
    componentKeys.allKeys["lumiere"]["AllumeH"],
    componentKeys.allKeys["lumiere"]["AllumeM"],
    componentKeys.allKeys["lumiere"]["EteintH"],
    componentKeys.allKeys["lumiere"]["EteintM"],
    componentKeys.allKeys["lumiere"]["TimerUsed"],
    componentKeys.allKeys["lumiere"]["OnOffManual"],
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
            "Contrôle des pompes",
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
    [sg.Button("Soumettre"), sg.Cancel()],
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


while True:  # The Event Loop
    event, values = window.read(
        timeout=500
    )  # this sets the time between each "refresh"
    co2value += 1
    if co2value > 200000:
        sg.popup("Niveau de CO2 trop élevé. Veuillez intervenir", button_color="red")
        co2value = 0
    if event in (None, "Exit", "Cancel"):
        break
    elif event == componentKeys.allKeys["lumiere"]["TimerUsed"]:
        controlTimers("lumiere")
    elif event == componentKeys.allKeys["moteur"]["TimerUsed"]:
        controlTimers("moteur")
    elif event == componentKeys.allKeys["pompe"]["TimerUsed"]:
        controlTimers("pompe")
    elif event == "pompeOnOffManual":
        if values["pompeOnOffManual"] == True:
            window["pompeOnOffManual"].update(text="On")
            window["pompeOnOffManual"].update(True)
        else:
            window["pompeOnOffManual"].update(text="Off")
            window["pompeOnOffManual"].update(False)
    elif event == "TempSub":
        newValue = values["SliderTemp"] - 0.5
        window["SliderTemp"].update(newValue)
    elif event == "TempAdd":
        newValue = values["SliderTemp"] + 0.5
        window["SliderTemp"].update(newValue)

    elif event == "HumidSub":
        newValue = values["SliderHumid"] - 1
        window["SliderHumid"].update(newValue)
    elif event == "HumidAdd":
        newValue = values["SliderHumid"] + 1
        window["SliderHumid"].update(newValue)

    elif event == "AllumageSubLum":
        newValue = values["SliderAllumageLum"] - 1
        window["SliderAllumageLum"].update(newValue)
    elif event == "AllumageAddLum":
        newValue = values["SliderAllumageLum"] + 1
        window["SliderAllumageLum"].update(newValue)
    elif event == "Soumettre" and allNumValues(values) == True:
        print(values)
