import tkinter as tk
import keyboard
import yaml
import json
from keyboard.__init__ import _os_keyboard
import time

#pip install keyboard

with open('logger.yaml', 'w') as fp:
    data = {'keyCombos': {}}
    yaml.safe_dump(data, fp)


def convToDict(event):
    '''
    converts keyboardEvent object into a dictionary
    `event`: valid keyboardEvent object
    '''
    return {'device': event.device, 
            'event_type': event.event_type, 
            'is_keypad': event.is_keypad, 
            'modifiers': event.modifiers,
            'name': event.name,
            'scan_code': event.scan_code,
            'time': event.time}

def convToKeyEvent(dict):
    '''
    converts dictionary into a keyboardEvent object
    `dict`: valid dictionary representation of keyboardEvent object
    '''
    return keyboard.KeyboardEvent(event_type = dict['event_type'],
                                  is_keypad = dict['is_keypad'],
                                  scan_code = dict['scan_code'],
                                  name = dict['name'],
                                  time = dict['time'])

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x250+400+200")
        self.startBtn = tk.Button(text = 'start', command = self.startAction).pack()
        self.stopBtn = tk.Button(text = 'stop', command = self.stopAction).pack()
        self.playBtn = tk.Button(text = 'play', command = executeKeys).pack()
        self.keyList = None

    def startAction(self):
        self.keyList = []
        def hookAction(action):
            self.keyList.append(action)

        self.listener = keyboard.hook(callback = lambda key: hookAction(key))

    def stopAction(self):
        # self.recording = keyboard.stop_recording()
        keyboard.unhook(self.listener)
        
        newEvents = list((event.to_json()) for event in self.keyList)

        with open('logger.yaml', 'r') as fp:
            data = yaml.safe_load(fp)
        size = len(data['keyCombos'])
        data['keyCombos'][f"combo #{size}"] = []
        with open('logger.yaml', 'w') as fp:
            yaml.safe_dump(data, fp)

        for event in newEvents:
            with open("logger.yaml", 'r') as fp:
                data = yaml.safe_load(fp)

            data['keyCombos'][f"combo #{size}"].append(event)

            with open("logger.yaml", 'w') as fp:

                yaml.safe_dump(data, fp)

def executeKeys():

    with open("logger.yaml", 'r') as fp:
        data = yaml.safe_load(fp)

    eventList = []
    for keyEvent in data['keyCombos']['combo #0']:
        event = convToKeyEvent(json.loads(keyEvent))

        (keyboard.press(event.name)) if event.event_type == 'down' else (keyboard.release(event.name))





if __name__ == "__main__":
    app = App()
    app.mainloop()  