# import os,json
# if os.path.isfile("contract_data.json") == False:
#     with open(r"contract_data.json", "x") as infile:
#         json.dump({}, infile)

from threading import Thread
from register import * # type: ignore
from blockchain import * # type: ignore
from oracle import * # type: ignore

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
            "url": "https://ripple-health.net/api/medication/000203",
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
registration(command)
oracle()
