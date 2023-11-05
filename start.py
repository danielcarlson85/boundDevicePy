#open a terminal and write:

#sudo apt-get update
#sudo apt-get install sense-hat
#pip install azure-iot-device
#pip install requests
#sudo reboot

import os
from sense_hat import SenseHat
from azure.iot.device import IoTHubDeviceClient, exceptions, Message
import random
import utils
import iothubManager

class UserData:
    delaytime = 20
    count = 0
    moving = True
    previous = 0
    sense = SenseHat()
    conn_str = ""
    startExcersice = False
    hasDeviceBeenMoved = False
    totalPause=0
    weight = 0
    hasLoggedInOnDevice = False
    pauseSinceLastRep = 0
    currentMethod=None
    email = ""
    firstname= "sdfsdf"
    lastname= "sdfsdf"
    machinename = ""
    status = ""
    
    
    
if __name__ == "__main__":
    try:
        print("Device started")
        conn_str = open("connectionstring","r").readlines()
        iothubManager.Program.setup(conn_str)
        
    except Exception as e:
        print(e)
    finally:     
        utils.setBlackColor()
