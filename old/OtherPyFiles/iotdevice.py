import time
import random
import json
from azure.iot.device import IoTHubDeviceClient, MethodResponse
from azure.iot.device import MethodRequest


# Initialize global variables
device_is_in_use = False
is_running = False
user_data = None


def run(request: MethodRequest):
    if request.name == "start":
        start(request)
    elif request.name == "stop":
        stop(request)

def start(request: MethodRequest):

def stop(request: MethodRequest):



connection_string = "HostName=boundiothub.azure-devices.net;DeviceId=ChestMachine;SharedAccessKey=lfuuB5CoYDOVrMxmu0qwDEyzu+Qz3r6xL4VyEMEnaRs="


# Initialize the device client
device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)


# Set the method handler
device_client.on_method_request_received = run

# Connect to IoT Hub
device_client.connect()

try:
    print("Device started")
    input("Press Enter to exit...\n")
finally:
    is_running = False
    device_client.disconnect()

