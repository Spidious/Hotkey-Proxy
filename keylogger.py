import keyboard
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


def combo_to_str(key_combo: object) -> list:
    '''
    Return a list of string representations of each keyboard event in key_combo.combination
    `key_combo`: valid keyCombo object with stored combinatinon
    '''
    # check if combo is stored
    if(len(key_combo.combination) == 0):
        print('No combination stored. One must be recorded or pulled')
        return

    return list((event.to_json()) for event in key_combo.combination)


class keyCombo(object):
    combination = []
    listener = None
    blocker = None

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
        '''pull events from the passed list'''
        # Prevent writing on top of another combination without just reseting it
        if(not len(self.combination) == 0):
            print(f'Combination is currently: {self}\ncombination must first be removed')
            return

        self.combination = [convToKeyEvent(json.loads(item)) for item in list]


    def remove_combo(self):
        ''' Clear the stored combination'''
        # Having to call this function makes it harder to do this on accident
        self.combination = []

    def startRecord(self):
        ''' Start a new recording'''
        def log_event(event):
            # log the event on callback
            self.combination.append(event)
        
        # Prevent writing on top of another combination without just reseting it
        if(not len(self.combination) == 0):
            print(f'Combination is currently: {self}\ncombination must first be removed')
            return
        # start the listener
        self.listener = keyboard.hook(callback = lambda e: log_event(e), suppress = True)

    def stopRecord(self):
        '''
        Stop the currently running recording
        '''
        # stop the listener
        keyboard.unhook(self.listener)

    def run(self):
        '''
        Run the stored combination if one exists
        '''
        # Check if a combination exists
        if(len(self.combination) == 0):
            print('No combination stored. One must be recorded or pulled')
            return

        # Run each stored event
        for event in self.combination:
            (keyboard.press(event.name)) if event.event_type == 'down' else (keyboard.release(event.name))

        self._release_all()

    def _release_all(self):
        '''Release all keys in Combination'''

        # add all names to name_list
        name_list = []
        for item in self.combination:
            name_list.append(item.name)
        
        # list all first occurances of string in new_list in order
        seen = set()
        seenadd = lambda x: seen.add(x)
        reduced_list = [x for x in name_list if not (x in seen or seenadd(x))]

        for key in reduced_list:
            keyboard.release(key)




    

    


if __name__ == "__main__":

    newKeybind = keyCombo()
