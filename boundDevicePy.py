#open a terminal and write:

#sudo apt-get update
#sudo apt-get install sense-hat
#pip install azure-iot-device
#sudo reboot

import os
from sense_hat import SenseHat
import random
import time
from azure.iot.device import Message
from azure.iot.device import IoTHubDeviceClient
import json

delaytime = 20
count = 0
moving = True
previous = 0
data = []
sense = SenseHat()
conn_str = ""

def setRedColor():
    sense.clear(255,0,0)

def setGreenColor():
    sense.clear(0,255,0)
   
def setBlackColor():
    sense.clear(0,0,0)

def showS():
    sense.show_letter("S")
   
def setgreentext():
    return [0, 255, 0]


def replace_empty_with_string(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = replace_empty_with_string(value)
        return obj
    elif isinstance(obj, list):
        return [replace_empty_with_string(item) for item in obj]
    else:
        return "Empty" if obj is None or obj == "" else obj


class Program:
    IsRunning = False
    DeviceIsInUse = False
    UserData = None
    totalPause = 0

    @staticmethod
    def main():
        
        print("Device started")
        conn_str = open("connectionstring","r").readlines()[0]
        print(conn_str)
        Program.client = IoTHubDeviceClient.create_from_connection_string(conn_str)
        Program.client.on_method_request_received = Program.on_method_request_received

        try:
            Program.client.connect()
            setGreenColor()
            input("Press Enter to exit\n")
        except:
            print("Cannot connect to IotHub")

    @staticmethod
    def on_method_request_received(request):
        method_name = request.name

        if method_name == "start":
            Program.start(request)
        elif method_name == "stop":
            Program.stop(request)

    def start(self):
        if not Program.DeviceIsInUse and not Program.IsRunning:
            print("Start method invoked")
            Program.DeviceIsInUse = True
            Program.IsRunning = True
            clean_object = json.dumps(replace_empty_with_string(self.payload))
            Program.UserData = json.loads(clean_object)
            Program.UserData['TrainingData'] = []           
            loop()

    @staticmethod
    def stop(self):
        global count
        if Program.UserData is not None:
            print("Stop method invoked")
            Program.IsRunning = False
            Program.DeviceIsInUse = False
            stopwatch = time.perf_counter()
            training_data = json.dumps(replace_empty_with_string(Program.UserData))
            print(Program.UserData)
            setRedColor()
            Program.send_training_data_to_iothub(training_data)
            count=0

           

    @staticmethod
    def send_training_data_to_iothub(data_to_send):
        print("Sending data to IoTHub...")
        message = Message(data_to_send)
        Program.client.send_message(message)
        time.sleep(1)
        showS()
        time.sleep(1)
        setGreenColor()
        time.sleep(1)
        sense.show_letter("0", text_colour= setgreentext())
        print("DONE, data sent to IoTHub.")


    @staticmethod
    def log_to_console(stopwatch):
        print("Lägnden på listan: " + str(len(Program.UserData['TrainingData'])) + " rader")
        print("Device stopped")
        print("Username: " + Program.UserData['ObjectId'])
        print(f"{stopwatch} seconds to upload data")


def stopped(accelerator_value):
    return abs(accelerator_value) < 0.17


def loop():
    global count, moving, previous, delaytime
   
    direction = ""
   
    while Program.IsRunning:
        if count == 10: count = 0
        time.sleep(delaytime / 1000)
        acceleration = sense.get_accelerometer_raw()
        accelerator_value = acceleration['z'] - 1.0
        if count >= 0 and count < 10:
            sense.show_letter(f"{count}", text_colour= setgreentext())
       
        if moving:
            if stopped(accelerator_value):
                previous += 1
                if previous >= 15:
                    if direction =="up":
                        count += 1
                    previous = 0
                    moving = False
            else:
                previous += 1
                direction="up"
        else:
            if not stopped(accelerator_value):
                previous += 1
                if previous >= 15:
                    direction="up"
                    previous = 0
                    moving = True
            else:
                previous += 1
                direction = "down"
       
        #print(count)
        #print(direction)


        if count >-1:
            Program.UserData['TrainingData'].append({'X': count, 'Y': 0, 'Z': int(time.time())})


        short_accelerator_value = float(str(accelerator_value)[:5])
       
        print(short_accelerator_value)

        lowerLimit = -0.07
        upperLimit = -0.02
       
        if lowerLimit <= short_accelerator_value <= upperLimit:
            Program.totalPause = Program.totalPause +1
            print("Checking pause")
            if Program.totalPause == 100:
                Program.IsRunning = False
                Program.totalPause = 0    
                Program.stop(None);
                count=0
        else:
            Program.totalPause = 0
   
if __name__ == "__main__":
    #Program.IsRunning = True
    #loop()
    Program.main()
