import requests
import time
import ciso8601
from web3.auto.gethdev import w3
import json
import schedule
with open(r"contract_data.json", "r") as infile:
    contract_data = json.load(infile)
import requests
import time
import ciso8601
from web3.auto.gethdev import w3
import json
import schedule
with open(r"contract_data.json", "r") as infile:
    contract_data = json.load(infile)


def ripplehealth(url):
    r = requests.get(url)
    result = r.json()
    data = dict()
    rtime = 0
    for element in result.keys():
        # ts = ciso8601.parse_datetime(element)
        rtime = int(element) - int(element) % 86400
        if (str(rtime) in data):
            data[str(rtime)] = str(int(data[str(rtime)]) + 1)
        else:
            data[str(rtime)] = str(1)
    return str(data)




def ripplehealth(url):
    r = requests.get(url)
    result = r.json()
    data = dict()
    rtime = 0
    for element in result.keys():
        # ts = ciso8601.parse_datetime(element)
        rtime = int(element) - int(element) % 86400
        if (str(rtime) in data):
            data[str(rtime)] = str(int(data[str(rtime)]) + 1)
        else:
            data[str(rtime)] = str(1)
    return str(data)


contract = w3.eth.contract(address=contract_data['aDoO5kETqZnduTNIkIxqo'][2], abi=contract_data['aDoO5kETqZnduTNIkIxqo'][0], bytecode=contract_data['aDoO5kETqZnduTNIkIxqo'][1])
device_key = 'aDoO5kETqZnduTNIkIxqo'
patient_contract = w3.eth.contract(address=contract_data['aVczkyG9gGL4B33KJLDvy'][2],abi=contract_data['aVczkyG9gGL4B33KJLDvy'][0],bytecode=contract_data['aVczkyG9gGL4B33KJLDvy'][1])
device_data = ripplehealth('http://127.0.0.1:8000/sample.json')

patient_contract.functions.set_device_data(device_key,device_data,'adherence').transact()

contract.functions.clear_event().transact()

contract.functions.step2().transact()

patient_contract.functions.step1().transact()

device_data = ripplehealth('http://127.0.0.1:8000/sample.json')

patient_contract.functions.set_device_data(device_key,device_data,'adherence').transact()

contract.functions.clear_event().transact()

contract.functions.step2().transact()

patient_contract.functions.step1().transact()
