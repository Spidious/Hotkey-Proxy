import serial
import os
import yaml
from yaml.loader import SafeLoader
import threading
import time

# Get the COM port and baud rate from the config file
def checkYaml():
    if not os.path.exists("hotKeys.yaml"):
        with open("hotKeys.yaml", "w") as fp:
            data = {'BAUDRATE': 115200, 'COMPORT': None, 'KeyCommands': [None]*8}
            yaml.safe_dump(data, fp)
        return True
    return False

def getSerial():
    with open("hotKeys.yaml") as fp:
        file = yaml.load(fp, Loader=SafeLoader)
        comport = file['COMPORT']
        baudrt = file['BAUDRATE']
    output = {'ComPort': comport, 'BaudRate': baudrt}
    return output

# Runs from gui file, this is the actual proxy
def runBox( *args):
    # Initialize SerialPort
    serial_Port = getSerial()
    if(serial_Port['ComPort'] == None):
        return
    serialPort = serial.Serial(port = serial_Port['ComPort'], baudrate=serial_Port['BaudRate'],
                        bytesize=8, timeout=0, stopbits=serial.STOPBITS_ONE)
    # Continuously loop forever
    t = threading.current_thread()
    print("starting thread")
    while getattr(t, "do_run", True):   # Loop while the do_run attribute of thread is true
        # Wait until there is data waiting in the serial buffer
        if(serialPort.in_waiting > 0):

            # Read data out of the buffer until a carraige return / new line is found
            serialString = (serialPort.readline()).decode('Ascii')

            # for every character in the input execute it as a command
            for i in serialString:
                try:
                    os.system(getCommand(int(i)))
                except:
                    pass
        time.sleep(.25)
    print("exiting thread")


# Get a command from the yaml file
def getCommand(key):
    with open("hotKeys.yaml") as fp:
        file = yaml.load(fp, Loader=SafeLoader)
        if file == None: 
            return "echo Nothing assigned to key"
        return file['KeyCommands'][key]

if __name__ == "__main__":
    runBox()