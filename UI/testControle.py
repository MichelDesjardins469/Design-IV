import Interface
import UI
import PySimpleGUI as sg
import control
import componentKeys
import time
from multiprocessing import Process


sg.theme("DarkTeal12")


def printValues():
    while True:
        print(interface.getValues())
        time.sleep(5)


components = UI.Components()
interface = Interface.Interface(components)
p1 = Process(target=interface.getValuesTest())
p1.start()
p1.join()
