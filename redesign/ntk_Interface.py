import tkinter
from tkinter import *

class Active_Button(Button):
    def __init__(self, master, **kw): # background = 'grey', foreground = 'white',
        Button.__init__(self, master=master, **kw)
        self.backg = self['bg']
        self.forg = self['fg']
        self.hovbg = self['activebackground']
        self.hovfg = self['activeforeground']
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_exit)
    
    def on_enter(self, *args):
        self.configure(background = self.hovbg, fg = self.hovfg)
    def on_exit(self, *args):
        self.configure(background = self.backg, fg = self.forg)


class Interface_App(Tk):
    def __init__(self, **kw):
        Tk.__init__(self)
        self.geometry("500x300")
        try:
            self.title(kw['title'])
        except:
            self.title(self.title())
        try:
            try:
                self.configure(background = kw['background'])
            except:
                self.configure(background = kw['bg'])
        except:
            self.configure(background = 'white')
        page = App_Page(self, background = 'blue')
        page.pack(fill = BOTH)



class App_Page(Canvas):
    def __init__(self, master, **kw):
        Canvas.__init__(self, master = master, **kw)


App = Interface_App()
App.mainloop()