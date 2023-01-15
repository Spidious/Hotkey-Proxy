import keyboard
import yaml
import json


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


class key_combo(object):
    combination = []
    listener = None

    def __init__(self, event_list = None):
        self.pull_events(event_list) if not event_list == None else None

    def __repr__(self):
        # add all names to name_list
        name_list = []
        for item in self.combination:
            name_list.append(item.name)
        
        # list all first occurances of string in new_list in order
        seen = set()
        seenadd = lambda x: seen.add(x)
        reduced_list = [x for x in name_list if not (x in seen or seenadd(x))]

        # join list with ' + '
        finalString = ' + '.join(reduced_list)
        return finalString

    def pull_events(self, list):
        # Prevent writing on top of another combination without just reseting it
        if(not len(self.combination) == 0):
            print(f'Combination is currently: {self}\ncombination must first be removed')

        self.combination = [convToKeyEvent(json.loads(item)) for item in list]


    def remove_combo(self):
        # Having to call this function makes it harder to do this on accident
        self.combination = []

    def startRecord(self):
        def log_event(event):
            # log the event on callback
            self.combination.append(event)
        
        # Prevent writing on top of another combination without just reseting it
        if(not len(self.combination) == 0):
            print(f'Combination is currently: {self}\ncombination must first be removed')
        # start the listener
        self.listener = keyboard.hook(callback = lambda e: log_event(e))

    def stopRecord(self):
        # stop the listener
        keyboard.unhook(self.listener)

    

    


if __name__ == "__main__":
    with open('logger.yaml', 'r') as fp:
        data = yaml.safe_load(fp)

    events = data['keyCombos']['combo #0']

    newKeybind = key_combo(events)

    print(newKeybind)