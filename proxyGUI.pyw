import threading
import os
import tkinter as tk
from tkinter import ttk
from serial.tools.list_ports import comports
import hotkeyProxy as proxy
import yaml
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
from tkinter import filedialog
import keylogger

# Create the thread here so as to remove errors within the class
box_thread = threading.Thread(target=proxy.runBox)
# Set application priority
proxy.setpriority(priority = 4)

BACKGROUND = '#36393f'
BUTTONBG = '#565b65'
TEXTFG = '#dcddde'

#N8620H

class App(tk.Tk):
    def __init__(self, box_thread):
        self.showOnStart = proxy.checkYaml()

        # self.wm_attributes('-toolwindow', True)
        self.box_thread = box_thread
        super().__init__()
        self.geometry("500x250+400+200")
        self.title('Hotkey Settings')      
        self.protocol('WM_DELETE_WINDOW', self.hide_window)
        self.PortLabel = tk.Label(self, text = f"Current Port: {(proxy.getSerial())['ComPort']}", bg = BACKGROUND, fg = TEXTFG)
        self.makeChangeButton()
        self.keyEditButtons()
        self.option_var = tk.StringVar()
        self.resizable(False, False)
        self.configure(bg=BACKGROUND)
        
    def changePort(self,  *args):
        '''
        Change the connected port from the drowdown list
        '''
        # Set port names and com ports
        portNames = []
        portDevice = []
        for port in comports():
            portNames.append(port.description)
            portDevice.append(port.device)

        # get the com port using the ID
        # read all data and store in a dictionary
        com = portDevice[portNames.index(self.option_var.get())]
        with open('config.yaml', 'r') as f:
            data = yaml.safe_load(f)

        # change the comport
        data['COMPORT'] = com

        # dump entire dictionary into the file
        with open('config.yaml', 'w') as f:    
            yaml.safe_dump(data, f)
 
        # Restart the proxy thread   
        self.box_thread.do_run=False
        self.box_thread.join()
        self.box_thread = threading.Thread(target=proxy.runBox)
        self.box_thread.start()

        # Change the label from the original window
        self.PortLabel.configure(text = f"Current Port: {(proxy.getSerial())['ComPort']}")

    def portButton(self):
        '''
        Define the action for when the change port button is pressed
        Create a window
        '''

        # Disable use of other window while this window is active
        def exitButton():
            self.deiconify()
            popup.destroy()
        self.withdraw()

        # create popup data
        popup = tk.Toplevel(self)
        popup.title("Select Port")
        popup.protocol('WM_DELETE_WINDOW', exitButton)
        popup.resizable(False, False)
        # popup.attributes("-topmost", True)
        # popup.overrideredirect(True)
        popup.geometry("500x100+400+200")
        popup.configure(bg = BACKGROUND)

        # create a label
        label = tk.Label(popup, text='Select port:', bg = BACKGROUND, fg = TEXTFG)
        label.place(x = 10, y = 20)

        # Create a list of the names
        portNames = []
        for port in comports():
            portNames.append(port.description)

        # Create a option menu with the action changePort
        self.option_var.set(f"Current Port: {(proxy.getSerial())['ComPort']}")
        option_menu = tk.OptionMenu(
            popup,
            self.option_var,
            *portNames,
            command = self.changePort
        )
        option_menu.configure(bg = BUTTONBG, fg = TEXTFG, width=40)
        option_menu["menu"].config(bg=BUTTONBG, fg = TEXTFG)
        option_menu.place(x = 80, y = 17)

        # create an exit button
        exitButton = tk.Button(popup, text = 'Done', command=exitButton, bg = BUTTONBG, fg = TEXTFG)
        exitButton.place(x = 380, y = 19)

    def makeChangeButton(self):
        def startupButton():
            if(not proxy.checkStartup()):
                self.startupButton.configure(text = "Dont run on Startup")
                proxy.addStartup()
            else:
                self.startupButton.configure(text = "Run on Startup")
                proxy.removeStartup()

        self.PortLabel.place(x = 0, y = 0)

        self.COMButton = tk.Button(self, text = "Change Port", command = self.portButton, bg = BUTTONBG, fg = TEXTFG, width = 15)
        self.COMButton.place(x = 0, y = 20)

        self.startupButton = tk.Button(self, command = startupButton, bg = BUTTONBG, fg = TEXTFG, width = 15)
        if(proxy.checkStartup()):
            self.startupButton.configure(text = "Dont run on Startup")
        else:
            self.startupButton.configure(text = "Run on Startup")
        self.startupButton.place(x = 0, y = 50)

    def quit_window(self, icon, item):
        icon.stop()
        self.destroy()

    def show_window(self, icon, item):
        icon.stop()
        self.after(0,self.deiconify())
        self.PortLabel.configure(text=f"Current Port: {(proxy.getSerial())['ComPort']}")

    def hide_window(self):
        self.withdraw()
        image=Image.open("hotkey.ico")
        menu=(item('Quit', self.quit_window),
            item('Show', self.show_window)
        )
        icon=pystray.Icon("name", image, 'HotKey Box', menu)
        icon.run()

    def keyButton(self, key):
        # Disable use of other window while this window is active
        def exitButton():
            self.deiconify()
            popup.destroy()
        self.withdraw()

        def set_text(text):
            fileEntry.delete(0,tk.END)
            fileEntry.insert(0,text)
            return

        def getFile():
            filename = filedialog.askopenfilename(initialdir = "/",
                                                title = "Select a File",
                                                filetypes = (("executables", "*.exe"), ("all files", "*.*")))
            # # Change label contents
            # label.configure(text=filename)
            fileEntryVar.set(filename)
            set_text(filename)

        # Parse the selected file and set it to a start command
        def applyAppOpen():
            if fileEntry.get() == 'File Name' or fileEntry.get() == '':
                label.configure(text = "Please select a file", fg = "red")
                return
            # Parse the input to create the command variable
            path = os.path.normpath(fileEntry.get())
            filePath = (path.split('\\'))
            file = filePath.pop()
            path = '\\'.join(filePath)
            command = f"start /d\"{path}\" {file}"
            
            # Copy all data from yaml file
            with open('config.yaml', 'r') as f:
                data = yaml.safe_load(f)

            # change the keys command to command
            data['KeyCommands'][key] = command

            # dump entire dictionary back into the file
            with open('config.yaml', 'w') as f:    
                yaml.safe_dump(data, f)
            
            label.configure(text = f"Directory saved to key #{key+1}", fg = "green")

        def applyCMD():
            cmd = f"{commandEntry.get()}"
            if cmd == '':
                label.configure(text = "You must enter a command", fg = "red")
                return

            # Copy all data from yaml file
            with open('config.yaml', 'r') as f:
                data = yaml.safe_load(f)

            # change the keys command to command
            data['KeyCommands'][key] = cmd

            # dump entire dictionary back into the file
            with open('config.yaml', 'w') as f:    
                yaml.safe_dump(data, f)
            
            label.configure(text = f"Command saved to key #{key+1}", fg = "green")

        def clearKey():
            with open('config.yaml', 'r') as f:
                data = yaml.safe_load(f)

            # change the keys command to command
            data['KeyCommands'][key] = None

            # dump entire dictionary back into the file
            with open('config.yaml', 'w') as f:    
                yaml.safe_dump(data, f)
            
            label.configure(text = f"Key #{key+1} cleared!", fg = "green")

        def keyLogger_btn():
            def start_recording(self):
                stopBtn.place(x = 20, y = 200)
                keyBind.remove_combo()
                keyBind.startRecord()

            def stop_recording(self):
                keyBind.stopRecord()
                keyLabel.configure(text = f"Key Bind: {keyBind}")
                startBtn.place_forget()
                stopBtn.place_forget()
                        
            def applyKeys(keybind_obj):
                strList = keylogger.combo_to_str(keyBind)

                with open('config.yaml', 'r') as fp:
                    data = yaml.safe_load(fp)

                data['KeyCommands'][key] = {'key_bind': strList}

                with open('config.yaml', 'w') as fp: 
                    yaml.safe_dump(data, fp)

            keyBind = keylogger.keyCombo()
            keyLabel.place(x = 150, y = 140)
            startBtn = tk.Button(popup, text = 'Start Recording', fg = TEXTFG, bg = BUTTONBG, width = 15, command = lambda: start_recording(popup))
            startBtn.place(x = 20, y = 170)
            stopBtn = tk.Button(popup, text = 'Stop Recording', fg = TEXTFG, bg = BUTTONBG, widt = 15, command = lambda: stop_recording(popup))
            applyLoggerBtn = tk.Button(popup, text = 'Apply Keys', fg = TEXTFG, bg = BUTTONBG, width = 9, command = lambda: applyKeys(keyBind)).place(x = 410, y = 160)




        # create popup data
        popup = tk.Toplevel(self)
        popup.protocol('WM_DELETE_WINDOW', exitButton)
        popup.resizable(False, False)
        # popup.attributes("-topmost", True)
        popup.title(f"Change Key #{key+1} Command")
        popup.geometry("500x250+400+200")
        popup.configure(bg = BACKGROUND)

        # create open file explorer button
        fileBtn = ttk.Button(popup, text = "Open File", command = getFile)
        fileBtn.place(x=10, y=45)

        # create a label
        label = tk.Label(popup, text='Select a file or enter a terminal command', bg = BACKGROUND, fg = TEXTFG)
        label.pack(pady=15)
        # Create file entry box
        fileEntryVar = tk.StringVar()
        fileEntryVar.set("File Name")
        fileEntry = ttk.Entry(popup, textvariable=fileEntryVar, width=50)
        fileEntry.place(x=90, y = 47)


        # Command entry zone
        cmdlabel = tk.Label(popup, text = "Enter Cmd:", bg = BACKGROUND, fg = TEXTFG)
        cmdlabel.place(x =20, y = 95)

        commandEntryVar = tk.StringVar()
        commandEntry = tk.Entry(popup, textvariable=commandEntryVar, width=50)
        commandEntry.place(x=90, y = 97)

        # Make keyLabel
        keyLabel = tk.Label(popup, text = '', fg = TEXTFG, bg = BACKGROUND)

        # assign the button
        clearBtn = tk.Button(popup, text= 'Clear Key', fg = TEXTFG, bg = BUTTONBG, width = 9, command = clearKey).place(x = 410, y = 30)
        applyFileBtn = tk.Button(popup, text= 'Apply File', fg = TEXTFG, bg = BUTTONBG, width= 9, command = applyAppOpen).place(x = 410, y = 60)
        applyCmdBtn = tk.Button(popup, text = 'Apply CMD', fg = TEXTFG, bg = BUTTONBG, width=9, command = applyCMD).place(x = 410, y = 90)
        exitBtn = tk.Button(popup, text = 'Done', fg = TEXTFG, bg = BUTTONBG, width= 9, command = exitButton).place(x = 410, y = 120)
        loggerBtn = tk.Button(popup, text = 'Create Keybind', fg = TEXTFG, bg = BUTTONBG, widt = 15, command = keyLogger_btn).place(x = 20, y = 140)
        

    def keyEditButtons(self):
        height = 3
        width = 6
        setX = 200
        setY = 60
        offSet = 60
        key0 = tk.Button(master = self, text = "1", height = height, width = width, bg = BUTTONBG, fg = TEXTFG, command = lambda: self.keyButton(0))
        key1 = tk.Button(master = self, text = "2", height = height, width = width, bg = BUTTONBG, fg = TEXTFG, command = lambda: self.keyButton(1))
        key2 = tk.Button(master = self, text = "3", height = height, width = width, bg = BUTTONBG, fg = TEXTFG, command = lambda: self.keyButton(2))
        key3 = tk.Button(master = self, text = "4", height = height, width = width, bg = BUTTONBG, fg = TEXTFG, command = lambda: self.keyButton(3))
        key0.place(x = setX, y = setY)
        key1.place(x = setX + offSet, y = setY)
        key2.place(x = setX + offSet*2, y = setY)
        key3.place(x = setX + offSet*3, y = setY)
        key4 = tk.Button(master = self, text = "5", height = height, width = width, bg = BUTTONBG, fg = TEXTFG, command = lambda: self.keyButton(4))
        key5 = tk.Button(master = self, text = "6", height = height, width = width, bg = BUTTONBG, fg = TEXTFG, command = lambda: self.keyButton(5))
        key6 = tk.Button(master = self, text = "7", height = height, width = width, bg = BUTTONBG, fg = TEXTFG, command = lambda: self.keyButton(6))
        key7 = tk.Button(master = self, text = "8", height = height, width = width, bg = BUTTONBG, fg = TEXTFG, command = lambda: self.keyButton(7))
        key4.place(x = setX, y = setY+offSet)
        key5.place(x = setX + offSet, y = setY+offSet)
        key6.place(x = setX + offSet*2, y = setY+offSet) 
        key7.place(x = setX + offSet*3, y = setY+offSet)
        


if __name__ == "__main__":
    app = App(box_thread)
    connect_thread = threading.Thread(target=proxy.checkConnection, args=(app,), daemon = True)
    app.box_thread.start()
    connect_thread.start()
    if(not app.showOnStart):
        app.hide_window()
    app.mainloop()

    connect_thread.do_run=False
    app.box_thread.do_run=False

    connect_thread.join()
    app.box_thread.join()