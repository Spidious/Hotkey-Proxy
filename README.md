# Hotkey-Proxy
Currently needs to be manually added to the startup folder to run on start. Open the run window 'WIN + R' and search 'shell:startup'. Copy and paste a shortcut to the path of the proxyGUI.pyw file. This script can continue to run if the box is not plugged in, it will not scan the serial data if there is no device matching the one saved in the .yaml file. This file will be created after running for the first time

App will start with no window visible, open window by right clicking icon at bottom right and select 'show'. To exit the script you must right click the icon and select 'quit'. 

This app does not show a terminal, to change this change the extension of the proxyGUI.pyw file to '.py'

# Required Installations
Requires the following libraries to be installed, can be installed by pip (as written):
*PySerial
*pyyaml
*pystray
*pywin32