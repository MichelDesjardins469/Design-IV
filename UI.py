import PySimpleGUI as sg

layout = [
    [
        sg.Text("Température"),
        sg.InputText(),
    ],
    [sg.Text("CO2"), sg.InputText()],
    [sg.Text("Humidité"), sg.InputText()],
    [sg.Output(size=(90, 20))],
    [sg.Button("Soumettre"), sg.Cancel()],
]


def isNumber(caracter):
    try:
        n = int(caracter)
        return True
    except ValueError:
        return False


window = sg.Window("Contrôle de la serre", layout)
while True:  # The Event Loop
    event, values = window.read()
    if event in (None, "Exit", "Cancel"):
        break
    elif event == "Soumettre" and isNumber(values[0]) == True:
        print(values)
