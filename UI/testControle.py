import Interface
import UI
import PySimpleGUI as sg
import control
import componentKeys
import time
import threading

sg.theme("DarkTeal12")


def printValues():
    while True:
        print(interface.getValues())
        time.sleep(5)

components = UI.Components()
interface = Interface.Interface(components)
threadId1 = threading.Thread(target=interface.runInterface)
threadId2 = threading.Thread(target=printValues)

threadId1.start()
threadId2.start()
