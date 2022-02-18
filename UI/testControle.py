import Interface
import UI
import PySimpleGUI as sg
import control
import componentKeys
import time
from multiprocessing import Process

sg.theme("DarkTeal12")


def printBonjour():
    print("Bonjour")


components = UI.Components()
interface = Interface.Interface(components)
p1 = Process(target=interface.getValuesTest())
p1.start()
p2 = Process(target=printBonjour())
p2.start()
p1.join()
p2.join()
