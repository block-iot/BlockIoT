from web3.auto.gethdev import w3
import json
import ast
import os
import hashlib
import base64
import time
#End_Imports


def update_contracts():
    with open(r"contract_data.json", "r") as infile:
        contract_data = json.load(infile)
    return contract_data


def register_init_patient(config, contract_data, contract):
    with open(r"contract_data.json", "r") as infile:
        contract_data = json.load(infile)
    if check_config(config) == False:
        return False
    if os.path.isdir("Published/Patient/") == False:
        os.mkdir("Published/Patient/")
    file1 = open(r"Contracts/Patient.sol", "r")
    pt_contract = str(file1.read())
    key = generate_key(config, str(config["Patient"]))
    key = str(key)
    patient_key = str(key)
    pt_contract = pt_contract.replace("{{patient}}", str(key))
    f = open("Published/Patient/"+str(key) + ".sol", "w")
    f.write(pt_contract)
    f.close()
    deploy(str(key), patient=True)
    contract_data = update_contracts()
    add_patient_data(config, key)
    contract.functions.create_patients(patient_key).transact()
    patient_contract = w3.eth.contract(
        address=contract_data[patient_key][2], abi=contract_data[patient_key][0], bytecode=contract_data[patient_key][1])
    patient_contract.functions.create_devices(str(patient_key)).transact()


def register_init_device(config,patient_key,contract_data,contract):
    with open(r"contract_data.json", "r") as infile:
        contract_data = json.load(infile)
    for element in list(config["Device"].keys()):
        file1 = open(r"Contracts/Devices/"+element+".sol", "r")
        pt_contract = str(file1.read())
        key = generate_key(config, str(config["Device"][element]))
        key = str(key)
        pt_contract = pt_contract.replace("{{device}}", str(key))
        f = open("Published/Device/"+str(key) + ".sol", "w")
        f.write(pt_contract)
        f.close()
        deploy(str(key), device=True)
        contract_data = update_contracts()
        add_device_data(config, key, element, patient_key)
        device_contract = w3.eth.contract(
            address=contract_data[key][2], abi=contract_data[key][0], bytecode=contract_data[key][1])
        contract.functions.set_device_data(
            str(generate_key(config)), "", "").transact()
        device_contract.functions.step1().transact()



def check_config(config):
    config = config["Patient"]
    if "first_name" in config.keys() and "last_name" in config.keys() and "dob" in config.keys():
        if config["dob"].count('-') == 2:
            return True
        else:
            return False
    else:
        return False


def generate_key(config, device=""):
    config1 = config["Patient"]
    key = ""
    hashed_config = "first=" + \
        config1["first_name"] + "last=" + \
        config1["last_name"]+"dob="+config1["dob"]
    if device != "":
        hashed_config += "device=" + device
    hasher = hashlib.md5(hashed_config.encode('utf-8'))
    key = base64.urlsafe_b64encode(hasher.digest()[:15]).decode("utf-8")
    key = key.replace("-", "c")
    return "a" + key


def add_patient_data(config, key):
    contract_data = dict()
    with open(r"contract_data.json", "r") as infile:
        contract_data = json.load(infile)
    contract = w3.eth.contract(
        address=contract_data[key][2], abi=contract_data[key][0], bytecode=contract_data[key][1])
    for element in config["Patient"].keys():
        contract.functions.set_details(
            element, config["Patient"][element]).transact()
        contract.functions.set_config(
            str(json.dumps(config))).transact()
    return True


def add_device_data(config, key, device, patient_key):
    contract_data = dict()
    with open(r"contract_data.json", "r") as infile:
        contract_data = json.load(infile)
    contract = w3.eth.contract(
        address=contract_data[key][2], abi=contract_data[key][0], bytecode=contract_data[key][1])
    for element in config["Device"][device].keys():
        contract.functions.set_details(
            element, config["Device"][device][element]).transact()
    contract.functions.set_patient_addr(
        contract_data[patient_key][-1], str(patient_key)).transact()
    contract.functions.set_device_addr(
        contract_data[key][-1], str(key)).transact()
    return True
