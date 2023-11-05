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
        
        result = message.split("****")
        
        if result[0] == "online":
            print("User is logged in")
            utils.setGreenColor() 
        
        if result[0] == "restart":
            print("Excersice done restarting device...")
            utils.restart_bound_script()
        
        if len(result) == 2:
            if result[0] == "start":
                print(result[0])
                print(result[1])
                iothubMethods.startnow(result[1])       
    
    def send_method_request():   
        payload = '{"parap1":"value1"}'
        method_request= MethodRequest("MethodName", method_payload)
        response = Program.client.invoke_method(method_request)

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
    def send_back_method_request_result(method_request):
        response_payload = "ok"
        response_status = 200
        response = MethodResponse.create_from_method_request(method_request, response_payload, response_payload)
        Program.client.send_method_response(response)
    

    @staticmethod
    def recieved_method_request_from_mobile(method_request):

#         if method_request.name == "start":
#             iothubMethods.startnow(method_request)
 
         if method_request.name == "reboot":
             iothubMethods.reboot_rpi()
         if method_request.name == "shutdown":
             iothubMethods.shutdown_rpi()
            
         print("End start method")
        
        #Program.client.disconnect()
        
    @staticmethod
    def setup(conn_str):
        print(conn_str)
        Program.client = IoTHubDeviceClient.create_from_connection_string(conn_str[0])
        Program.client.on_method_request_received = Program.recieved_method_request_from_mobile
        Program.client.on_message_received = Program.on_message_received
        Program.client.connect()
        utils.setGreenDot()
        #utils.setBlackColor()
        input("Press Enter to exit\n")
