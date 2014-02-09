# coding=utf-8

__author__ = 'nacho'

from ConfigManager import ConfigManager
from Tkinter import Tk
from Interfaz import Interfaz



def main():

    Parametros=ConfigManager("./gesbol.ini")


    root = Tk()
    gui=Interfaz(root,Parametros)
    gui.mainloop();


if __name__ == '__main__':
    main()

