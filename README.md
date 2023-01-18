# Hotkey-Proxy
The first time this script is run, all required installations must be installed. Then run the file 'proxyGUI.pyw' you should be met with a window. It is advised to allow this script to run on startup.

This script can continue to run if the box is not plugged in, it will not scan the serial data if there is no device matching the one saved in the .yaml file. This file will be created after running for the first time

App will start with no window visible, open window by right clicking icon at bottom right and select 'show'. To exit the script you must right click the icon and select 'quit'. 

This app does not show a terminal, to change this change the extension of the proxyGUI.pyw file to '.py'

# Required Installations
Requires the following libraries to be installed, can be installed by pip (as written):
* PySerial
* pyyaml
* pystray
* pywin32
* keyboard

***

Requires installation of Python 3.9 or later
