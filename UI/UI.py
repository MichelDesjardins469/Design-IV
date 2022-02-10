import PySimpleGUI as sg
import control

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


frame_inputs_layout = [
    slider2button("Température (°C)", "TempSub", "SliderTemp", "TempAdd", 0, 35, 20),
    slider2button("CO2 (ppm)", "CO2Sub", "SliderCO2", "CO2Add", 0, 1000, 4000),
    slider2button("Humidité (%)", "HumidSub", "SliderHumid", "HumidAdd", 0, 100, 80),
]
frame_light_layout = [
    slider2button(
        "Nombre d'heures d'éclairage par jour",
        "AllumageSubLum",
        "SliderAllumageLum",
        "AllumageAddLum",
        0,
        24,
        8,
    ),
    [
        sg.Text("Heure d'allumage"),
        sg.Combo(
            [
                "Minuit",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "Midi",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
            ],
            default_value=8,
        ),
        sg.Combo(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
                "27",
                "28",
                "29",
                "30",
                "31",
                "32",
                "33",
                "34",
                "35",
                "36",
                "37",
                "38",
                "39",
                "40",
                "41",
                "42",
                "43",
                "44",
                "45",
                "46",
                "47",
                "48",
                "49",
                "50",
                "51",
                "52",
                "53",
                "54",
                "55",
                "56",
                "57",
                "58",
                "59",
            ],
            default_value=0,
        ),
        sg.Text("Heure d'éteignement"),
        sg.Combo(
            [
                "Minuit",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "Midi",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
            ],
            default_value=16,
        ),
        sg.Combo(
            [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
                "27",
                "28",
                "29",
                "30",
                "31",
                "32",
                "33",
                "34",
                "35",
                "36",
                "37",
                "38",
                "39",
                "40",
                "41",
                "42",
                "43",
                "44",
                "45",
                "46",
                "47",
                "48",
                "49",
                "50",
                "51",
                "52",
                "53",
                "54",
                "55",
                "56",
                "57",
                "58",
                "59",
            ],
            default_value=0,
        ),
    ],
]
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
            "Contrôle de la lumière",
            frame_light_layout,
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
    elif event == "TempSub":
        newValue = values["SliderTemp"] - 0.5
        window["SliderTemp"].update(newValue)
    elif event == "TempAdd":
        newValue = values["SliderTemp"] + 0.5
        window["SliderTemp"].update(newValue)

    elif event == "CO2Sub":
        newValue = values["SliderCO2"] - 10
        window["SliderCO2"].update(newValue)
    elif event == "CO2Add":
        newValue = values["SliderCO2"] + 10
        window["SliderCO2"].update(newValue)

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
