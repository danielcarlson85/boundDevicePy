from sense_hat import SenseHat
import iothubManager
from azure.iot.device import IoTHubDeviceClient, exceptions, Message
import start
import subprocess
import utils
import time
import json
import excersiceAlgorithms

sense = SenseHat()

def stopped(accelerator_value):
    return abs(accelerator_value) < 0.17

def startExcersice():
    utils.show0()

    if start.UserData.data == None:
        utils.createNewUserDataObject()

    while start.UserData.startExcersice:
        acceleration = sense.get_accelerometer_raw()
        accelerator_value = acceleration['z'] - 1.0
        short_accelerator_value = float(str(accelerator_value)[:5])
        
        if short_accelerator_value >0:
            break
    loop()
            
def loop():
      
    while start.UserData.startExcersice:
        if start.UserData.count == 10: start.UserData.count = 0
        time.sleep(start.UserData.delaytime / 1000)
        acceleration = sense.get_accelerometer_raw()
        accelerator_value = acceleration['z'] - 1.0
        
        if start.UserData.count >= 0 and start.UserData.count < 10:
            print("")
            utils.showLetter(start.UserData.count)
        if start.UserData.moving:
            if stopped(accelerator_value):
                start.UserData.deviceSensitivity += 1
                if start.UserData.deviceSensitivity >= 15:
                    if start.UserData.direction =="up":
                        start.UserData.count += 1
                    start.UserData.deviceSensitivity = 0
                    start.UserData.moving = False
            else:
                start.UserData.deviceSensitivity += 1
                start.UserData.direction="up"
        else:
            if not stopped(accelerator_value):
                start.UserData.deviceSensitivity += 1
                if start.UserData.deviceSensitivity >= 15:
                    start.UserData.direction="up"
                    start.UserData.deviceSensitivity = 0
                    start.UserData.moving = True
            else:
                start.UserData.deviceSensitivity += 1
                start.UserData.direction = "down"
            
        if start.UserData.count >-1:
            start.UserData.data['TrainingData'].append({'X': start.UserData.count, 'Y': start.UserData.weight, 'Z': int(time.time())})
          
        short_accelerator_value = float(str(accelerator_value)[:5])
     
        print(short_accelerator_value)

        lowerLimit = -0.07
        upperLimit = -0.02

     
        if lowerLimit <= short_accelerator_value <= upperLimit:
            start.UserData.totalPause = start.UserData.totalPause +1
            print("Checking pause")
            if start.UserData.totalPause == 100:
                start.UserData.totalPause = 0
                training_data = json.dumps(utils.replace_empty_with_string(start.UserData.data))
                #print(training_data)
                iothubManager.Program.send_data_to_iothub(training_data)
                start.UserData.count=0
                utils.setBlackColor()
                start.UserData.startExcersice=True
                startExcersice()
                break

        else:
            start.UserData.totalPause = 0
    return -1
