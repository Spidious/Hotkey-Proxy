import tkinter as tk
import keyboard
import yaml
#pip install keyboard

def convDict(event):
    return {'device': event.device, 
            'event_type': event.event_type, 
            'is_keypad': event.is_keypad, 
            'modifiers': event.modifiers,
            'name': event.name,
            'scan_code': event.scan_code,
            'time': event.time}


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x250+400+200")
        self.startBtn = tk.Button(text = 'start', command = self.startAction).pack()
        self.stopBtn = tk.Button(text = 'stop', command = self.stopAction).pack()

    def startAction(self):
        self.listener = keyboard.hook(callback = lambda key: print(f"keystroke: {key}"))

    def stopAction(self):
        # self.recording = keyboard.stop_recording()
        keyboard.unhook(self.listener)

if __name__ == "__main__":
    app = App()
    app.mainloop()