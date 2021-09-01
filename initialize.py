import os,json
import retel.retel as retel
import hashlib
import base64
from web3.auto.gethdev import w3
from retel.libraries.deploy import deploy
import time
import threading
import multiprocessing

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
    # f = open("Published/Physician/"+str(key) + ".sol", "w")
    # f.write(pt_contract)
    # f.close()
    deploy(str(key), physician=True,data=pt_contract)

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

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

def chunk_register(chunk):
    for element in chunk:
        register_init_physician(element)

def chunk_add(chunk):
    for element in chunk:
        key = generate_key(element, str(element["Physician"]))
        key = str(key)
        add_physician_data(element, key)

def initialize():
    physicians = {}
    with open(r"config.json", "r") as infile:
        physicians = json.load(infile)
    #1,5,10,20,40,80,160,320,640
    for j in [1,3,5,7,10,15]:
        with open(r"config.json", "w") as outfile:
            json.dump({},outfile)
        for i in range(0,j):
            with open(r"template.json", "r") as infile:
                template = json.load(infile)
            template["Patient"]["first_name"] = str(i)
            template["Physician"]["first_name"] = str(i)
            template["Device"]["RH_pill_bottle"]["medication_name"] = str(i)
            physicians[str(i)] = template
        with open(r"config.json", "w") as outfile:
            json.dump(physicians,outfile)
        with open(r"config.json", "r") as infile:
            physicians = json.load(infile)
        jobs = []
        for element in chunkIt(list(physicians.values()),10):
            chunk_register(element)
        #     p = multiprocessing.Process(target=chunk_register,args=(element,))
        #     jobs.append(p)
        #     p.start()
        # for job in jobs:
        #     job.join()
        for element in chunkIt(list(physicians.values()),10):
            chunk_add(element)
            #p = multiprocessing.Process(target=chunk_add,args=(element,))
        #     jobs.append(p)
        #     p.start()
        # for job in jobs:
        #     job.join()
        #p = multiprocessing.Process(target=register,args=(element))
        # for value in physicians.values():
        #     t1 = Thread(target=oracle_handler).start()
        #     register_init_physician(value)
        print("Finished")
        contract_data = update_contracts()
        with open(r"contract_data.json", "r") as infile:
            config = json.load(infile)
        retel.retel_initialize()
        retel.loop()
        if os.path.isfile("exec_time.json"):
            os.remove("exec_time.json")
        with open(r"exec_time.json", "x") as infile:
            json.dump([], infile)
