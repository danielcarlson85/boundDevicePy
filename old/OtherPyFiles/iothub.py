import asyncio
import json

from azure.iot.device.aio import IoTHubDeviceClient

connectionString = "HostName=boundiothub.azure-devices.net;DeviceId=ChestMachine;SharedAccessKey=lfuuB5CoYDOVrMxmu0qwDEyzu+Qz3r6xL4VyEMEnaRs="

json_data = '''
{
  "MachineName": "ChestMachine",
  "ObjectId": "6bc00f44-9a73-47da-a542-ee87d1e3981d",
  "TrainingData": [
    { "X": 42, "Y": 4, "Z": 1694878614 },
    { "X": 180, "Y": 111, "Z": 1694878614 }
  ]
}
'''

# Parse the JSON data into a Python variable


async def send_message():
    device_client = IoTHubDeviceClient.create_from_connection_string(connectionString)

    await device_client.connect()

    data = json.loads(json_data)

    await device_client.send_message(json_data)

    await device_client.disconnect()


