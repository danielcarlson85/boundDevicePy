import start
import subprocess
import utils
import time
import json
import excersiceAlgorithms

def reboot_rpi():
    print("reboot")
    utils.sense.show_letter("R", text_colour= utils.setredtext())
    subprocess.run(["sudo","reboot"])


def shutdown_rpi():
    print("shutting down...")
    utils.sense.show_letter("S", text_colour= utils.setredtext())
    time.sleep(2)
    utils.setBlackColor()
    subprocess.run(["sudo","poweroff"])
    
def startnow(method_request):
    try:
        print(f"Method started {method_request.name}")
        print(method_request.payload)
                
        start.UserData.email = method_request.payload["Email"]
        start.UserData.machinename=method_request.payload["DeviceData"]["MachineName"]
        start.UserData.firstname = method_request.payload["FirstName"]
        start.UserData.lastname = method_request.payload["LastName"]
        start.UserData.status = method_request.payload["Device"]["AzureIoTHubDevice"]["connectionState"]
        
        weight = (method_request.payload["DeviceData"]["Weight"])
        start.UserData.weight = weight
        
        clean_object = json.dumps(utils.replace_empty_with_string(method_request.payload["DeviceData"]))
        start.UserData.data = json.loads(clean_object)
        start.UserData.data['TrainingData'] = []
                        
        start.UserData.startExcersice = True        
        excersiceAlgorithms.startExcersice()
        
        
        print("startnow method exited")
        
    except Exception as e:
        print("Wrong json format" + e)
    finally:
        utils.restart_bound_script()
        return-1
        
def loggin_on_device():
    if not (hasLoggedInOnDevice):
        utils.setGreenColor()
        start.UserData.hasLoggedInOnDevice=True
    
def loggin_out_device():
    if (hasLoggedInOnDevice):
        utils.setBlackColor()
        start.UserData.hasLoggedInOnDevice=False
    

