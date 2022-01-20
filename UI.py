import PySimpleGUI as sg
import control

layout = [
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
        sg.Text("CO2 (%)"),
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
    [sg.Output(size=(80, 20))],
    [sg.Button("Soumettre"), sg.Cancel()],
]


def allNumValues(caracters):
    for i in range(len(caracters)):
        try:
            n = int(caracters[i])
        except ValueError:
            return False
    return True


window = sg.Window("Contrôle de la serre", layout, element_justification="c")
while True:  # The Event Loop
    event, values = window.read()
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
