import random
import time
from azure.iot.device import Message
from azure.iot.device import IoTHubDeviceClient
import json


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
    ChestMachine = "HostName=boundiothub.azure-devices.net;DeviceId=ChestMachine;SharedAccessKey=lfuuB5CoYDOVrMxmu0qwDEyzu+Qz3r6xL4VyEMEnaRs="
    IsRunning = False
    DeviceIsInUse = False
    UserData = None

    @staticmethod
    def main():
        print("Device started")

        Program.client = IoTHubDeviceClient.create_from_connection_string(Program.ChestMachine)
        Program.client.on_method_request_received = Program.on_method_request_received

        try:
            Program.client.connect()
            input("Press Enter to exit\n")
        finally:
            Program.client.disconnect()

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

            while Program.IsRunning:
                time.sleep(0.1)
                x = random.randint(0, 255)
                y = random.randint(0, 255)
                z = int(time.time())

                print(f"{x}, {y}, {z}")

                Program.UserData['TrainingData'].append({'X': x, 'Y': y, 'Z': z})

                print(Program.UserData)

    @staticmethod
    def stop(request):
        if Program.UserData is not None and Program.IsRunning:
            print("Stop method invoked")
            Program.IsRunning = False
            Program.DeviceIsInUse = False
            stopwatch = time.perf_counter()
            training_data = json.dumps(replace_empty_with_string(Program.UserData))
            Program.send_training_data_to_iothub(training_data)
            Program.log_to_console(stopwatch)
            Program.UserData['TrainingData'].clear()

    @staticmethod
    def send_training_data_to_iothub(data_to_send):
        message = Message(data_to_send)
        Program.client.send_message(message)

    @staticmethod
    def log_to_console(stopwatch):
        print("Lägnden på listan: " + str(len(Program.UserData['TrainingData'])) + " rader")
        print("Device stopped")
        print("Username: " + Program.UserData['ObjectId'])

        print(f"{stopwatch} seconds to upload data")


if __name__ == "__main__":
    Program.main()
