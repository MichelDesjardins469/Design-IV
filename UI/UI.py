import PySimpleGUI as sg
import control

# option pour choisir le type de plante
# Ajouter une option rajouter de la lumiere instant si exemple is annonce gris
sg.theme("DarkTeal12")
layout = [
    [sg.Text("Contrôle des paramètres")],
    [
        sg.Text("Température (°C)"),
        sg.Button(
            "",
            key="TempSub",
            button_color=(sg.theme_background_color(), sg.theme_background_color()),
            image_filename="./minus_sign.png",
            image_size=(25, 25),
            image_subsample=2,
        ),
        sg.Slider(
            key="SliderTemp",
            range=(0, 35),
            default_value=20,
            size=(20, 15),
            orientation="horizontal",
            font=("Helvetica", 12),
        ),
        sg.Button(
            "",
            key="TempAdd",
            button_color=(sg.theme_background_color(), sg.theme_background_color()),
            image_filename="./plus_sign.png",
            image_size=(25, 25),
            image_subsample=2,
        ),
    ],
    [
        sg.Text("CO2 (ppm)"),
        sg.Button(
            "",
            key="CO2Sub",
            button_color=(sg.theme_background_color(), sg.theme_background_color()),
            image_filename="./minus_sign.png",
            image_size=(25, 25),
            image_subsample=2,
        ),
        sg.Slider(
            key="SliderCO2",
            range=(0, 35),
            default_value=20,
            size=(20, 15),
            orientation="horizontal",
            font=("Helvetica", 12),
        ),
        sg.Button(
            "",
            key="CO2Add",
            button_color=(sg.theme_background_color(), sg.theme_background_color()),
            image_filename="./plus_sign.png",
            image_size=(25, 25),
            image_subsample=2,
        ),
    ],
    [
        sg.Text("Humidité (%)"),
        sg.Button(
            "",
            key="HumidSub",
            button_color=(sg.theme_background_color(), sg.theme_background_color()),
            image_filename="./minus_sign.png",
            image_size=(25, 25),
            image_subsample=2,
        ),
        sg.Slider(
            key="SliderHumid",
            range=(0, 35),
            default_value=20,
            size=(20, 15),
            orientation="horizontal",
            font=("Helvetica", 12),
        ),
        sg.Button(
            "",
            key="HumidAdd",
            button_color=(sg.theme_background_color(), sg.theme_background_color()),
            image_filename="./plus_sign.png",
            image_size=(25, 25),
            image_subsample=2,
        ),
    ],
    [
        sg.Text("Nombre d'heures de lumiere par jour : "),
        sg.Slider(
            key="SliderHeure",
            range=(0, 24),
            default_value=8,
            size=(20, 15),
            orientation="horizontal",
            font=("Helvetica", 12),
        ),
    ],
    [
        sg.Text("Heure d'allumage "),
        sg.Button(
            "",
            key="AllumageSubLum",
            button_color=(sg.theme_background_color(), sg.theme_background_color()),
            image_filename="./minus_sign.png",
            image_size=(25, 25),
            image_subsample=2,
        ),
        sg.Slider(
            key="SliderAllumageLum",
            range=(0, 35),
            default_value=20,
            size=(20, 15),
            orientation="horizontal",
            font=("Helvetica", 12),
        ),
        sg.Button(
            "",
            key="AllumageAddLum",
            button_color=(sg.theme_background_color(), sg.theme_background_color()),
            image_filename="./plus_sign.png",
            image_size=(25, 25),
            image_subsample=2,
        ),
    ][sg.Output(size=(80, 5))],
    [sg.Button("Soumettre"), sg.Cancel()],
]
co2value = 0
window = sg.Window(
    "Contrôle de la serre", layout, element_justification="c", size=(1050, 730)
)
while True:  # The Event Loop
    event, values = window.read(timeout=500)
    co2value += 1
    if co2value > 200000:
        sg.popup("Niveau de CO2 trop élevé. Veuillez intervenir", button_color="red")
        co2value = 0
    if event in (None, "Exit", "Cancel"):
        break
    elif event == "TempSub":
        newValue = values["SliderTemp"] - 1
        window["SliderTemp"].update(newValue)
    elif event == "TempAdd":
        newValue = values["SliderTemp"] + 1
        window["SliderTemp"].update(newValue)

    elif event == "CO2Sub":
        newValue = values["SliderCO2"] - 1
        window["SliderCO2"].update(newValue)
    elif event == "CO2Add":
        newValue = values["SliderCO2"] + 1
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
