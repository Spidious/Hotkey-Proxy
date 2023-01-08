import serial
import serial.tools.list_ports as list_ports
import os
import yaml
from yaml.loader import SafeLoader
import threading
import time



# Get the COM port and baud rate from the config file
def checkYaml():
    if not os.path.exists("config.yaml"):
        with open("config.yaml", "w") as fp:
            data = {'DEVICE_NAME': 'Arduino Micro', 'BAUDRATE': 115200, 'COMPORT': None, 'KeyCommands': [None]*8}
            yaml.safe_dump(data, fp)
        return True
    return False

# Get information about the serial port from config.yaml
def getSerial():
    with open("config.yaml") as fp:
        file = yaml.load(fp, Loader=SafeLoader)
        device = file['DEVICE_NAME']
        comport = file['COMPORT']
        baudrt = file['BAUDRATE']
    output = {'Device': device, 'ComPort': comport, 'BaudRate': baudrt}
    return output

# Runs from gui file, this is the actual proxy
def runBox( *args):
    # Initialize SerialPort
    serial_Port = getSerial()
    if(serial_Port['ComPort'] == None):
        return
    try:
        serialPort = serial.Serial(port = serial_Port['ComPort'], baudrate=serial_Port['BaudRate'],
                                    bytesize=8, timeout=0, stopbits=serial.STOPBITS_ONE)
    except Exception as e:
        print(e)    # Most likely cannot connect to comport or access denied (port is busy)
        return
    # Continuously loop forever
    t = threading.current_thread()
    print("starting serial read thread")
    while getattr(t, "do_run", True):   # Loop while the do_run attribute of thread is true
        # Wait until there is data waiting in the serial buffer
        try:
            if(serialPort.in_waiting > 0):

                # Read data out of the buffer until a carraige return / new line is found
                serialString = (serialPort.readline()).decode('Ascii')

                # for every character in the input execute it as a command
                for i in serialString:
                    try:
                        os.system(getCommand(int(i)))
                    except:
                        pass
        except Exception as e:  # If something causes error, print error and break
            print(e)
            break

        time.sleep(.25) # Delay .2 seconds to keep resources down
    print("exiting serial read thread")


# Get a command from the yaml file
def getCommand(key):
    with open("config.yaml") as fp:
        file = yaml.load(fp, Loader=SafeLoader)
        if file == None: 
            return "echo Nothing assigned to key"
        return file['KeyCommands'][key]

def checkConnection(app = None):
    # Get the current thread for checking if it should continue to run
    t = threading.current_thread()
    print("starting connection thread")
    while getattr(t, "do_run", True):   # Loop while the do_run attribute of thread is true

        if(app == None):
            break

        # Start of checkConnection Processes
        # Get list of comports
        ports = list(list_ports.comports())
        # flip through serial devices checking if it is a 'device' (arduino micro)
        for port in ports:
            if getSerial()['Device'] in port.description:
                if not app.box_thread.is_alive():    # If in serial list and thread is not running
                    time.sleep(.2)
                    if app.box_thread.is_alive():    # Wait a moment and double check, just incase this hasent been timed at the exact same instant the thread is being restarted
                        continue                    

                    # Change the current port incase this is the issue
                    with open("config.yaml", 'r') as fp:
                        data = yaml.safe_load(fp)

                    data['COMPORT'] = port.device

                    with open("config.yaml", 'w') as fp:
                        data = yaml.safe_dump(data, fp)

                    # try starting the thread again
                    app.box_thread = threading.Thread(target = runBox)
                    app.box_thread.start()
                    app.PortLabel.configure(text = f"Current Port: {port.device}")

        time.sleep(2) # Delay one second to keep resources down
    print("exiting connection thread")




# for running the file on its own
class App:
    box_thread = threading.Thread(target=runBox)


if __name__ == "__main__":

    app = App()
    app.box_thread.start()

    checkConnection(app)