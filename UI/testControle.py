import Interface
import UI
import PySimpleGUI as sg
import control
import componentKeys
import time
import threading

sg.theme("DarkTeal12")


def printBonjour():
    while True:
        print("Bonjour")
        time.sleep(10)

components = UI.Components()
interface = Interface.Interface(components)
threadId1 = threading.Thread(target=interface.getValuesTest)
threadId2 = threading.Thread(target=printBonjour)

threadId1.start()
threadId2.start()
