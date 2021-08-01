
from web3.auto.gethdev import w3
import json,os
from blockchain import * # type: ignore
from oracle import * # type: ignore
from pathlib import Path
import hashlib,base64

# with open(r"contract_data.json","w") as infile:
#         json.dump({},infile)
with open(r"contract_data.json","r") as infile:
    contract_data = json.load(infile)

def registration(config):
    #Initial Checks
    if os.path.isdir("Published/") == False:
        os.mkdir("Published/")
    if check_config(config) == False:
        return False
    if os.path.isdir("Published/Patient/") == False:
        os.mkdir("Published/Patient/")
    file1 = open(r"Contracts/Patient.sol","r")
    pt_contract = str(file1.read())
    key = generate_key(config,str(config["Patient"]))
    key = str(key)
    patient_key = str(key)
    pt_contract = pt_contract.replace("{{patient}}",str(key))
    f = open("Published/Patient/"+str(key) + ".sol", "w")
    f.write(pt_contract)
    f.close()
    deploy(str(key),patient=True)
    add_patient_data(config,key)
    for element in list(config["Device"].keys()):
        if os.path.isdir("Published/Device/") == False:
            os.mkdir("Published/Device/")
        file1 = open(r"Contracts/Devices/"+element+".sol","r")
        pt_contract = str(file1.read())
        key = generate_key(config,str(config["Device"][element]))
        key = str(key)
        pt_contract = pt_contract.replace("{{pill_bottle}}",str(key))
        f = open("Published/Device/"+str(key) + ".sol", "w")
        f.write(pt_contract)
        f.close()
        deploy(str(key),device=True)
        add_device_data(config,key,element,patient_key)

    
def check_config(config):
    config = config["Patient"]
    if "first_name" in config.keys() and "last_name" in config.keys() and "dob" in config.keys():
            if config["dob"].count('-') == 2:
                return True
            else:
                return False
    else:
        return False

def generate_key(config,device=""):
    config1 = config["Patient"]
    key = ""
    hashed_config = "first=" + config1["first_name"] + "last=" + config1["last_name"]+"dob="+config1["dob"]
    if device != "":
        hashed_config += "device=" + device
    hasher = hashlib.md5(hashed_config.encode('utf-8'))
    key = base64.urlsafe_b64encode(hasher.digest()[:15]).decode("utf-8")
    key = key.replace("-","c")
    return "a" + key

def add_device_data(config,key,device,patient_key):
    contract_data = dict()
    with open(r"contract_data.json","r") as infile:
        contract_data = json.load(infile)
    contract = w3.eth.contract(address=contract_data[key][2],abi=contract_data[key][0],bytecode=contract_data[key][1])
    for element in config["Device"][device].keys():
        contract.functions.set_details(element,config["Device"][device][element]).transact()
    contract.functions.set_patient_addr(contract_data[patient_key][-1],str(patient_key)).transact()
    return True

def add_patient_data(config,key):
    contract_data = dict()
    with open(r"contract_data.json","r") as infile:
        contract_data = json.load(infile)
    contract = w3.eth.contract(address=contract_data[key][2],abi=contract_data[key][0],bytecode=contract_data[key][1])
    for element in config["Patient"].keys():
        contract.functions.set_details(element,config["Patient"][element]).transact()
    return True
