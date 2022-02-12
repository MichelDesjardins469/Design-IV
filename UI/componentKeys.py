import PySimpleGUI as sg
import control


tempKeys = {"sub": "TempSub", "slider": "SliderTemp", "add": "TempAdd"}

humidityKeys = {"sub": "HumidSub", "slider": "SliderHumid", "add": "HumidAdd"}

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
    "temp": tempKeys,
    "humidity": humidityKeys,
    "pompe": pompeKeys,
    "moteur": moteurKeys,
    "lumiere": lumiereKeys,
}
