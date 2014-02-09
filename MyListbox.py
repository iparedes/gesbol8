__author__ = 'nacho'

from Tkinter import *

class MyListbox(Frame):
    def __init__(self, parent, title, ancho, elementos, dobleclick, alto=5):
        Frame.__init__(self, parent)

        # Frame 1 para el listbox y scrollbar
        self.Frame1 = Frame(self)
        # Frame 2 para los botones up y down
        self.Frame2 = Frame(self)

        self.elementos=elementos
        self.titulo = Label(self.Frame1, text=title)
        self.titulo.grid(row=0)

        self.scrollbar = Scrollbar(self.Frame1)
        self.ListBox = Listbox(self.Frame1, width=ancho, height=alto, yscrollcommand=self.scrollbar.set)
        self.ListBox.bind("<Double-Button-1>", dobleclick)
        #self.ListBox.pack(side=LEFT,fill=BOTH)
        self.ListBox.grid(row=1, column=0, sticky=N)
        #scrollbar.pack(side=RIGHT,fill=Y)
        self.scrollbar.grid(row=1, column=1, sticky=N+S)
        self.scrollbar.config(command=self.ListBox.yview)

        self.fill(self.elementos)

        self.butUp = Button(self.Frame2, text="^")
        self.butUp.configure(command=self.up)
        self.butDown = Button(self.Frame2, text="v")
        self.butDown.configure(command=self.down)

        self.butUp.grid(row=0)
        self.butDown.grid(row=1)

        self.Frame1.grid(row=0, column=0)
        self.Frame2.grid(row=0, column=1)

    def seleccion(self):
        i = int(self.ListBox.curselection()[0])
        return i


    def up(self):
        i = int(self.ListBox.curselection()[0])
        if (i > 0):
            item = self.elementos.pop(i)
            i = i - 1
            self.elementos.insert(i, item)
            self.fill(self.elementos)
            self.ListBox.selection_set(i)

    def down(self):
        i = int(self.ListBox.curselection()[0])
        if (i < len(self.elementos)):
            item = self.elementos.pop(i)
            i = i + 1
            self.elementos.insert(i, item)
            self.fill(self.elementos)
            self.ListBox.selection_set(i)

    def fill(self, elementos):
        self.elementos=elementos
        self.ListBox.delete(0, len(self.elementos))
        for i in self.elementos:
            self.ListBox.insert(END, i)