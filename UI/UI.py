import PySimpleGUI as sg
import control

# option pour choisir le type de plante
# Ajouter une option rajouter de la lumiere instant si exemple is annonce gris
sg.theme("DarkTeal12")
def slider2button(text, keySub, keySlider, keyAdd, minValue, maxValue, defaultValue):
    return [sg.Text(text),
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
        ),
        sg.Button(
            "",
            key=keyAdd,
            button_color=(sg.theme_background_color(), sg.theme_background_color()),
            image_filename="./plus_sign.png",
            image_size=(25, 25),
            image_subsample=2,
        )]
frame_inputs_layout = [
        slider2button('Température (°C)', 'TempSub','SliderTemp', 'TempAdd', 0, 35, 20),
        slider2button('CO2 (ppm)', 'CO2Sub', 'SliderCO2', 'CO2Add', 4000, 8000, 4000),
        slider2button('Humidité (%)', 'HumidSub', 'SliderHumid', 'HumidAdd', 0, 100, 80)
]
frame_light_layout = [
    [
        sg.Text("Nombre d'heures de luminosité par jour : "),
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
        sg.Text("Heure d'allumage"),
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
            range=(0, 24),
            default_value=8,
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
