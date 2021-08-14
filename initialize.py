import os,json
import retel.retel as retel
import hashlib
import base64
from web3.auto.gethdev import w3
from retel.libraries.deploy import deploy

def update_contracts():
    with open(r"contract_data.json", "r") as infile:
        contract_data = json.load(infile)
    return contract_data

def check_config(config):
    config = config["Patient"]
    if "first_name" in config.keys() and "last_name" in config.keys() and "dob" in config.keys():
        if config["dob"].count('-') == 2:
            return True
        else:
            return False
    else:
        return False

def register_init_physician(config):
    if os.path.isdir("Published/Physician/") == False:
        os.mkdir("Published/")
        os.mkdir("Published/Physician/")
    file1 = open(r"Contracts/physician.sol", "r")
    pt_contract = str(file1.read())
    key = generate_key(config, str(config["Physician"]))
    key = str(key)
    pt_contract = pt_contract.replace("{{physician}}", str(key))
    f = open("Published/Physician/"+str(key) + ".sol", "w")
    f.write(pt_contract)
    f.close()
    deploy(str(key), physician=True)
    add_physician_data(config, key)
    contract_data = update_contracts()
    contract = w3.eth.contract(
        address=contract_data[key][2],
        abi=contract_data[key][0],
        bytecode=contract_data[key][1])

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

def add_physician_data(config, key):
    contract_data = dict()
    with open(r"contract_data.json", "r") as infile:
        contract_data = json.load(infile)
    contract = w3.eth.contract(
        address=contract_data[key][2], abi=contract_data[key][0], bytecode=contract_data[key][1])
    for element in config["Physician"].keys():
        contract.functions.set_details(
            element, config["Physician"][element]).transact()
        contract.functions.set_config(str(json.dumps(config))).transact()
    return True

physicians = {}
with open(r"config.json", "r") as infile:
    physicians = json.load(infile)

for value in physicians.values():
    register_init_physician(value)
    retel.retel_initialize()

retel.loop()
