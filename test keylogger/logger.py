import tkinter as tk
import keyboard
import yaml
import json
#pip install keyboard

with open('test keylogger/logger.yaml', 'w') as fp:
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

        with open('test keylogger/logger.yaml', 'r') as fp:
            data = yaml.safe_load(fp)
        size = len(data['keyCombos'])
        data['keyCombos'][f"combo #{size}"] = []
        with open('test keylogger/logger.yaml', 'w') as fp:
            yaml.safe_dump(data, fp)

        for event in newEvents:
            with open("test keylogger/logger.yaml", 'r') as fp:
                data = yaml.safe_load(fp)

            data['keyCombos'][f"combo #{size}"].append(event)

            with open("test keylogger/logger.yaml", 'w') as fp:

                yaml.safe_dump(data, fp)

def executeKeys():
    with open("test keylogger/logger.yaml", 'r') as fp:
        data = yaml.safe_load(fp)

    eventList = []
    for event in data['keyCombos']['combo #0']:
        event = convToKeyEvent(json.loads(event))

        key = event.scan_code or event.name
        keyboard.press(key) if event.event_type == keyboard.KEY_DOWN else keyboard.release(key)
        print(event.event_type)


        




# class smallkeyEvent(object):
#     type = None
#     key = None
#     code = None
#     time = None

#     def __init__(self, event):
#         self.type = event.event_type
#         self.key = event.name
#         self.code = event.scan_code
#         self.time = event.time

#     def to_dict(self):
#         return dict((attr, getattr(self, attr)) for attr in ['type', 'code', 'time'] if not attr.startswith('_'))

#     def __repr__(self):
#         return f"keyEvent({self.type}, {self.code}, {self.time})"

    


if __name__ == "__main__":
    app = App()
    app.mainloop()