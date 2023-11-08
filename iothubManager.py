from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
import start
import utils
import iothubMethods
import time
import sys

class Program:

    method_request = {}

    def on_message_received(message):
        message = message.data.decode("utf-8")
        print("Incomming message: " +message)
        
                
        result = message.split("****")
        
        if result[0] == "login":
            print("User is logged in")
            utils.setGreenColor()
            
        elif result[0] == "restartRPI":
                utils.restartRPI()
                
        elif result[0] == "shutdownRPI":
                utils.shutdownRPI()

        elif result[0] == "restartDevice":
                print("Restarting device...")
                utils.restart_bound_script()

        elif result[0] == "start":
                print(result[0])
                print(result[1])
                iothubMethods.startnow(result[1])

    @staticmethod
    def send_data_to_iothub(data_to_send):
        global method_request
        print("Sending data to IoTHub...")
        utils.sendTotalReps()
        start.UserData.startExcersice = True
        start.UserData.hasDeviceBeenMoved = False
        message = Message(data_to_send)
        Program.client.send_message(message)
        print(data_to_send)
        utils.showS()
        time.sleep(2)
        utils.setGreenColor()
        time.sleep(1)
        print("DONE, data sent to IoTHub.")
        return
        
    @staticmethod
    def setup(conn_str):
        print(conn_str)
        Program.client = IoTHubDeviceClient.create_from_connection_string(conn_str)
        Program.client.on_message_received = Program.on_message_received
        Program.client.connect()
        input("Press Enter to exit...")

