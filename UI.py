import PySimpleGUI as sg
import control

sg.theme("DarkTeal12")
layout = [
    [sg.Text("Contrôle des paramètres")],
    [
        sg.Text("Température (°C)"),
        sg.Slider(
            range=(0, 35),
            default_value=20,
            size=(20, 15),
            orientation="horizontal",
            font=("Helvetica", 12),
        ),
        sg.Button("Modifier la température"),
    ],
    [
        sg.Text("CO2 (ppm)"),
        sg.Slider(
            range=(0, 35),
            default_value=20,
            size=(20, 15),
            orientation="horizontal",
            font=("Helvetica", 12),
        ),
        sg.Button("Modifier le CO2"),
    ],
    [
        sg.Text("Humidité (%)"),
        sg.Slider(
            range=(0, 35),
            default_value=20,
            size=(20, 15),
            orientation="horizontal",
            font=("Helvetica", 12),
        ),
        sg.Button("Modifier l'humidité"),
    ],
    [sg.Button("Calibrer les instruments")],
    [sg.Output(size=(80, 5))],
    [sg.Button("Soumettre"), sg.Cancel()],
]
co2value = 0
window = sg.Window("Contrôle de la serre", layout, element_justification="c")
while True:  # The Event Loop
    event, values = window.read(timeout=500)
    co2value += 1
    if co2value > 20:
        sg.popup("Niveau de CO2 trop élevé. Veuillez intervenir", button_color="red")
        co2value = 0
    if event in (None, "Exit", "Cancel"):
        break
    elif event == "Modifier la température":
        control.updateTemp(values[0])
    elif event == "Modifier le CO2":
        control.updateCO2(values[1])
    elif event == "Modifier l'humidité":
        control.updateHumidity(values[2])
    elif event == "Soumettre" and allNumValues(values) == True:
        print(values)
