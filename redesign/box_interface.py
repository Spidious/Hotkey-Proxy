import yaml
import threading
import os
import serial
import time

CONFIG_FILE = 'config.yaml'

def execute_keypress(SerialVal: str = None):
    '''
    Intended to be called when a key is pressed.
    Sends the listening thread back to its function after breaking a second thread off.\n
    *This function should be interrupted if the main program is terminating*\n
    `SerialVal`  The raw value being read from the serial port. (TODO: Needs '.decode("Ascii")')
    '''
    # check if the running thread is the execution thread
    if not (threading.current_thread()).name == '_exeThread':
        # Create and start the execution thread
        exeThread = threading.Thread(name = '_exeThread', target = execute_keypress, args = SerialVal, daemon = True)
        exeThread.start()
        # go back to calling function
        return

    # TODO: Write execution code here


def get_info(stream: str = CONFIG_FILE):
    '''
    Retrieve all data from a yaml file and returns a dictionary. Creates default file if not found and no parameter is passed.\n
    `stream`  name or path of the target file (CONFIG_FILE by default)\n
    Returns `dict` upon success or `None` upon failure
    '''
    try:
        with open(stream, 'r') as fp:
            data = yaml.safe_load(fp)
        return data
    except:
        if(stream == CONFIG_FILE and not os.path.exists(CONFIG_FILE)):
            # TODO: finish create CONFIG_FILE
            # with open(CONFIG_FILE, 'w') as fp:
            #     yaml.safe_dump()
            pass
        return None

def _check_thread(thread: threading.Thread, des_name: str) -> bool:
    '''
    Check if specific thread is desired thread return bool value.\n
    `thread` threading module Thread Object.\n
    `des_name` desired name for comparison, string var.
    '''
    if des_name == None or thread == None:
        print('Provide name and thread for comparison')
        return False
    return des_name == thread.name

    


def serial_listener():
    '''
    Continuously check the serial port for new input\n
    run `execute_keypress` for every value in input
    '''

    # get serial info
    serial_info = get_info()
    if(serial_info['ComPort'] == None):
        return

    # Get Serial Port TODO: Reset if error
    try:
        serialPort = serial.Serial(port = serial_info['ComPort'], baudrate = serial_info['Baudrate'], bytesize = 8, timeout = 0, stopbits = serial.STOPBITS_ONE)
    except Exception as e:
        # TODO: Handle Exception
        print(e)
        return

    # Get and check the current thread
    _listenThread = threading.current_thread()
    if not _check_thread(_listenThread, '_serial_listener'):
        print(f'current thread is not intended thread\n\tCurrent Thread: {_listenThread.name}\n')
        return Exception(f'thread in wrong location -> Current Thread: \'{_listenThread.name}\'')

    # Start the loop
    print("Starting Serial Read Loop")
    while getattr(_listenThread, "do_run", True):
          time.sleep(.25)
    