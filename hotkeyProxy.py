import serial
import serial.tools.list_ports as list_ports
import os
from pathlib import Path
from win32com.client import Dispatch
import yaml
from yaml.loader import SafeLoader
import threading
import time
import keylogger

def setpriority(pid=None,priority=1):
    """ Set The Priority of a Windows Process.  Priority is a value between 0-5 where
        2 is normal priority.  Default sets the priority of the current
        python process but can take any valid process ID. """
        
    import win32api,win32process,win32con
    
    priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
                       win32process.BELOW_NORMAL_PRIORITY_CLASS,
                       win32process.NORMAL_PRIORITY_CLASS,
                       win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                       win32process.HIGH_PRIORITY_CLASS,
                       win32process.REALTIME_PRIORITY_CLASS]
    if pid == None:
        pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, priorityclasses[priority])



# Create a shortcut to proxyGUI.pyw
# Create in current path if no other path is provided
def createShortcut(dest_path = Path.cwd()):
    cur_path = Path.cwd()
    path = os.path.join(dest_path, 'HotKey Interface.lnk')
    target = os.path.join(cur_path, "proxyGUI.pyw")
    icon = os.path.join(cur_path, 'hotkey.ico')

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = str(cur_path)
    shortcut.IconLocation = icon
    shortcut.save()


# Check if added to startup folder :: TODO If not in startup folder create a popup within the main window that asks if you want to add it to startup, only if its the first time opening the window this session
def checkStartup():
    startup = f'C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
    path = os.path.join(startup, "HotKey Interface.lnk")
    return os.path.exists(path)

# Adds shortcut to startup
def addStartup():
    path = f'C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
    createShortcut(path)

# Removes shortcut from startup
def removeStartup():
    path = f'C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
    os.remove(os.path.join(path, 'HotKey Interface.lnk'))

# Create the Yaml file using default settings
def checkYaml():
    ######## Default Settings ############
    dev_name = 'Arduino Micro'
    startup = False
    baudrate = 9600
    comport = None
    base_comm = None
    num_keys = 8
    ######################################

    # Create the shortcut in folder if not currently there
    if not os.path.exists('HotKey Interface.lnk'):
        createShortcut()

    
    if not os.path.exists("config.yaml"):
        with open("config.yaml", "w") as fp:
            data = {'DEVICE_NAME': dev_name, 'BAUDRATE': baudrate, 'COMPORT': comport, 'STARTUP': startup, 'KeyCommands': [base_comm]*num_keys}
            yaml.safe_dump(data, fp)
        return True
    return False

# Get information about the serial port from config.yaml
def getSerial():
    with open("config.yaml") as fp:
        file = yaml.safe_load(fp)
        device = file['DEVICE_NAME']
        startup = file['STARTUP']
        comport = file['COMPORT']
        baudrt = file['BAUDRATE']
    output = {'Device': device, 'Startup': startup, 'ComPort': comport, 'BaudRate': baudrt}
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
                    comm = getCommand(int(i))
                    if 'key_bind' in comm:
                        keyLogger = keylogger.keyCombo(comm['key_bind'])
                        keyLogger.run()
                    else:
                        try:
                            os.system(comm)
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
                    try:
                        app.PortLabel.configure(text = f"Current Port: {port.device}")
                    except:
                        pass

        time.sleep(2) # Delay one second to keep resources down
    print("exiting connection thread")




# for running the file on its own
class App:
    box_thread = threading.Thread(target=runBox)


if __name__ == "__main__":

    app = App()
    app.box_thread.start()

    checkConnection(app)