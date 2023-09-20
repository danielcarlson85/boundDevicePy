# open a terminal and write:

# sudo apt-get update
# sudo apt-get install sense-hat
# pip install azure-iot-device
# sudo reboot

import os
from sense_hat import SenseHat
import random
import time
from azure.iot.device import Message
from azure.iot.device import IoTHubDeviceClient
import json

delaytime = 20
count = -1
moving = True
previous = 0

data = []

sense = SenseHat()
conn_str = ""


def setRedColor():
    sense.clear(255, 0, 0)


def setGreenColor():
    sense.clear(0, 255, 0)


def setBlackColor():
    sense.clear(0, 0, 0)


def showS():
    sense.show_letter("S")


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
        setBlackColor()
        print("Device started")
        conn_str = open("connectionstring", "r").readlines()[0]
        print(conn_str)
        Program.client = IoTHubDeviceClient.create_from_connection_string(conn_str)
        Program.client.on_method_request_received = Program.on_method_request_received

        try:
            Program.client.connect()
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
            setGreenColor()

            loop()

    @staticmethod
    def stop(request):
        if Program.UserData is not None and Program.IsRunning:
            print("Stop method invoked")
            Program.IsRunning = False
            Program.DeviceIsInUse = False
            stopwatch = time.perf_counter()
            training_data = json.dumps(replace_empty_with_string(Program.UserData))
            setRedColor()
            Program.UserData['TrainingData'].clear()
            Program.send_training_data_to_iothub(training_data)

    @staticmethod
    def send_training_data_to_iothub(data_to_send):
        print("Sending data to IoTHub...")
        message = Message(data_to_send)
        Program.client.send_message(message)
        time.sleep(1)
        showS()
        time.sleep(1)
        sense.clear()
        print("DONE, data sent to IoTHub.")

    @staticmethod
    def log_to_console(stopwatch):
        print("Lägnden på listan: " + str(len(Program.UserData['TrainingData'])) + " rader")
        print("Device stopped")
        print("Username: " + Program.UserData['ObjectId'])

        print(f"{stopwatch} seconds to upload data")


def stopped(az):
    return abs(az) < 0.17


def loop():
    global count, moving, previous

    while Program.IsRunning:

        if count == 10: count = 0
        acceleration = sense.get_accelerometer_raw()
        az = acceleration['z'] - 1.0  # gravity
        print("az =", az)

        if moving:
            if stopped(az):
                previous += 1
                if previous >= 15:
                    count += 1
                    previous = 0
                    moving = False
            else:
                previous += 1
        else:
            if not stopped(az):
                previous += 1
                if previous >= 15:
                    previous = 0
                    moving = True
            else:
                previous += 1

        print(count)
        if len(str(count)) != 2:
            sense.show_letter(f"{count}", text_colour=[0, 255, 0])

        acc = float(str(az)[:5])

        print(acc)
        print(Program.totalPause)

        lowerLimit = -0.07
        upperLimit = -0.02

        if lowerLimit <= acc <= upperLimit:
            Program.totalPause = Program.totalPause + 1
            print("Checking pause")
            if Program.totalPause == 100:
                Program.IsRunning = False
                print(Program.totalPause)
        else:
            Program.totalPause = 0


if __name__ == "__main__":
    Program.main()
