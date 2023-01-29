import tkinter
from tkinter import *

class Active_Button(tkinter.Button):
    def __init__(self, master, **kw):
        tkinter.Button.__init__(self,master=master,**kw)

class Interface_App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x300")
        self.title('Hotkey Interface')
        self.overrideredirect(True)
        self._createTitleBar()


    def _createTitleBar(self):
        tbar = tkinter.Frame(self, bg = 'blue', relief = 'raised', bd = 2)
        close_btn = tkinter.Button(tbar, text='X', width = 2, bd = 0, bg = 'blue', activebackground = "red", command=self.destroy)
        # window = tkinter.Canvas(self, bg='black')

        tbar.pack(fill = X)
        close_btn.pack(side=RIGHT)
        # window.pack(expand=1)


App = Interface_App()
App.mainloop()