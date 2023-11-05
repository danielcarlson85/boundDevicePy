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
    
def startnow(usertext):
    print(f"Method started startnow")
    print(usertext)
            
            
    user = json.loads(usertext)        
    
    print(user["Email"])
    
    start.UserData.email = user["Email"]
    start.UserData.machinename=user["DeviceData"]["MachineName"]
    start.UserData.firstname = user["FirstName"]
    start.UserData.lastname = user["LastName"]
    start.UserData.status = user["Device"]["AzureIoTHubDevice"]["connectionState"]
    
    weight = (user["DeviceData"]["Weight"])
    start.UserData.weight = weight
    
    clean_object = json.dumps(utils.replace_empty_with_string(user["DeviceData"]))
    start.UserData.data = json.loads(clean_object)
    start.UserData.data['TrainingData'] = []
                    
    start.UserData.startExcersice = True        
    excersiceAlgorithms.checkForDeviceMovements()
    
    print("Startnow method exited")
    
    
#    except Exception as e:
#        print("Wrong json format" + e)
#    finally:
#        utils.restart_bound_script()
#        return-1
        
def loggin_on_device():
    if not (hasLoggedInOnDevice):
        utils.setGreenColor()
        start.UserData.hasLoggedInOnDevice=True
    
def loggin_out_device():
    if (hasLoggedInOnDevice):
        utils.setBlackColor()
        start.UserData.hasLoggedInOnDevice=False
    

