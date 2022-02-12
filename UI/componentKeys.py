import PySimpleGUI as sg
import control


tempKeys = {"Sub": "TempSub", "Slider": "SliderTemp", "Add": "TempAdd"}

humidityKeys = {"Sub": "HumidSub", "Slider": "SliderHumid", "Add": "HumidAdd"}

pompeKeys = {
    "AllumeH": "AllumePompeH",
    "AllumeM": "AllumePompeM",
    "EteintH": "EteintPompeH",
    "EteintM": "EteintPompeM",
    "TimerUsed": "TimerPompeUsed",
    "OnOffManual": "pompeOnOffManual",
}
moteurKeys = {
    "AllumeH": "AllumeMoteurH",
    "AllumeM": "AllumeMoteurM",
    "EteintH": "EteintMoteurH",
    "EteintM": "EteintMoteurM",
    "TimerUsed": "TimerMoteurUsed",
    "OnOffManual": "MoteurOnOffManual",
}
lumiereKeys = {
    "AllumeH": "AllumeLumiereH",
    "AllumeM": "AllumeLumiereM",
    "EteintH": "EteintLumiereH",
    "EteintM": "EteintLumiereM",
    "TimerUsed": "TimerLumiereUsed",
    "OnOffManual": "LumiereOnOffManual",
}
allKeys = {
    "Temp": tempKeys,
    "Humidity": humidityKeys,
    "Pompe": pompeKeys,
    "Moteur": moteurKeys,
    "Lumiere": lumiereKeys,
}
