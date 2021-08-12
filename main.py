import os,json
import shutil
# shutil.rmtree("Published/")
# os.remove("contract_data.json")
# with open(r"contract_data.json", "x") as infile:
#     json.dump({}, infile)

from threading import Thread
import register
import blockchain
import retel.retel as retel

# Keywords such as BL_timestamp signify what type of data will be present there. 

command = {
    "Patient":{
        "first_name":"Jianjing",
        "last_name":"Lin",
        "dob":"01-12-1990",
        "phone":"5162708383",
        "email":"linj17@rpi.edu"
    },
    "Device":{
        "RH_pill_bottle":{
            "url": "http://127.0.0.1:8000/sample.json",
            "medication_name":"Vitamin D",
            "Dosage":"10 mg",
            "Times per day":"1"
        }
    },
    "Physician":{
        "Dr.Pulmonologist":{
        }   
    }
}

#When command arrives
register.registration(command)
retel.retel()
