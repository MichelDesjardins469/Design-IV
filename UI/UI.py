import PySimpleGUI as sg
from UI import ComponentKeys, TimeStamps

# option pour choisir le type de plante
# Ajouter une option rajouter de la lumiere instant si exemple is annonce gris


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


def CO2NiveauCritiquePopup():
    return sg.Window(
        "Avertissement du CO2",
        [
            [sg.T("Niveau de CO2 critique!")],
            [sg.B("OK", button_color="red", auto_size_button=True)],
        ],
        element_justification="c",
    ).read(close=True)


def nouvelAppareilPopup():
    return [sg.OptionMenu(["Unité de chauffage", "Ventilateur", "Lumière"], s=(15, 2))]


def controleHeures(
    keyHeuresA, keyMinutesA, keyHeuresE, keyMinutesE, keyCheckBoxTimers, keyControlTimer
):
    return [
        [
            sg.Text("Heure d'allumage"),
            sg.Combo(TimeStamps.hours, key=keyHeuresA, default_value=8),
            sg.Combo(TimeStamps.minutes, key=keyMinutesA, default_value=0),
            sg.Text("Heure d'éteignement"),
            sg.Combo(TimeStamps.hours, key=keyHeuresE, default_value=16),
            sg.Combo(TimeStamps.minutes, key=keyMinutesE, default_value=0),
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


def etatMachine(textDescription):
    return [
        sg.T(textDescription),
        sg.Image(
            key=ComponentKeys.allKeys[textDescription]["StateImage"],
            filename="UI/red_power_sign.png",
            background_color=sg.theme_background_color(),
        ),
    ]


class Components:
    def __init__(self):
        self.frame_inputs_layout = [
            Slider2button(
                "Température désirée (°C) ",
                ComponentKeys.allKeys["Temp"]["Sub"],
                "SliderTemp",
                ComponentKeys.allKeys["Temp"]["Add"],
                0,
                35,
                20,
            ),
            Slider2button(
                "Humidité désirée(%)",
                ComponentKeys.allKeys["Humidity"]["Sub"],
                "SliderHumid",
                ComponentKeys.allKeys["Humidity"]["Add"],
                0,
                100,
                80,
            ),
        ]
        self.frame_hours_control_pompe = controleHeures(
            ComponentKeys.allKeys["Pompe"]["AllumeH"],
            ComponentKeys.allKeys["Pompe"]["AllumeM"],
            ComponentKeys.allKeys["Pompe"]["EteintH"],
            ComponentKeys.allKeys["Pompe"]["EteintM"],
            ComponentKeys.allKeys["Pompe"]["TimerUsed"],
            ComponentKeys.allKeys["Pompe"]["OnOffManual"],
        )
        self.frame_hours_control_moteur = controleHeures(
            ComponentKeys.allKeys["Moteur"]["AllumeH"],
            ComponentKeys.allKeys["Moteur"]["AllumeM"],
            ComponentKeys.allKeys["Moteur"]["EteintH"],
            ComponentKeys.allKeys["Moteur"]["EteintM"],
            ComponentKeys.allKeys["Moteur"]["TimerUsed"],
            ComponentKeys.allKeys["Moteur"]["OnOffManual"],
        )
        self.frame_hours_control_lumiere = controleHeures(
            ComponentKeys.allKeys["Lumiere"]["AllumeH"],
            ComponentKeys.allKeys["Lumiere"]["AllumeM"],
            ComponentKeys.allKeys["Lumiere"]["EteintH"],
            ComponentKeys.allKeys["Lumiere"]["EteintM"],
            ComponentKeys.allKeys["Lumiere"]["TimerUsed"],
            ComponentKeys.allKeys["Lumiere"]["OnOffManual"],
        )
        self.frame_machines_state = [
            etatMachine("Ventilateur"),
            etatMachine("Moteur"),
            etatMachine("Pompe"),
            etatMachine("Temp"),
            etatMachine("Lumiere"),
        ]

        self.layout = [
            [
                sg.Frame(
                    "Variables contrôlables",
                    self.frame_inputs_layout,
                    font="Any 12",
                    title_color="white",
                )
            ],
            [
                sg.Frame(
                    "Contrôle des Pompes",
                    self.frame_hours_control_pompe,
                    font="Any 12",
                    title_color="white",
                )
            ],
            [
                sg.Frame(
                    "Contrôle des moteurs des volets",
                    self.frame_hours_control_moteur,
                    font="Any 12",
                    title_color="white",
                )
            ],
            [
                sg.Frame(
                    "Contrôle de la lumière",
                    self.frame_hours_control_lumiere,
                    font="Any 12",
                    title_color="white",
                )
            ],
            [sg.Output(size=(80, 5))],
            [
                sg.Frame(
                    "État de la machinerie",
                    self.frame_machines_state,
                    font="Any 12",
                    title_color="white",
                    element_justification="right",
                )
            ],
            [sg.Button("Soumettre", bind_return_key=True), sg.Cancel()],
        ]
