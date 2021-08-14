import json
import time
import plotly.graph_objects as go
import schedule
from . import contracts  # type: ignore
from colorama import init, Fore, Back, Style

def update_contracts():
    with open(r"contract_data.json", "r") as infile:
        contract_data = json.load(infile)
    return contract_data


with open(r"contract_data.json", "r") as infile:
    contract_data = json.load(infile)

# w3 = Web3(EthereumTesterProvider(PyEVMBackend()))
from web3.auto.gethdev import w3


class ExecInterrupt(Exception):
    pass

def get_imports(package):
    with open("retel/libraries/"+package + ".py","r") as f:
        result = f.read()
    imports = result.split("#End_Imports")[0]
    functions = result.split("#End_Imports")[1]
    return (imports, functions)

def read(contract,sub_contracts,key):
    print(Fore.LIGHTCYAN_EX,"Reading:", key, "Type:",
          contract.functions.return_type().call(), Style.RESET_ALL)
    if contract.functions.return_type().call() == "device":
        contract.functions.step1().transact()
    length = contract.functions.get_event_length().call()
    i = 0
    instruction = ""
    # Get Instruction
    while i < length:
        instruction += contract.functions.get_event(i).call()
        i += 1
    instruction_list = instruction.split("::")
    if instruction_list == ['']:
        return
    imports_file = ""
    functions_file = ""
    instruction_list_filtered = []
    for element in instruction_list:
        if "retel_import" in element:
            (imports, functions) = get_imports(element.split(" ")[1])
            imports_file += imports
            functions_file += functions
        elif "schedule" in element:
            time = int(element.split(",")[1])
            key = element.split(",")[2]
            loop_exec(time,key)
        else:
            instruction_list_filtered.append(element)
    instruction_list = instruction_list_filtered
    with open("retel/read.py", "a") as f:
        f.write(imports_file)
        f.write(functions_file)
        f.write(sub_contracts)
    for element in instruction_list:
        if element == '':
            continue
        with open("retel/read.py", "a") as f:
            f.write("\n"+element+"\n")
    execute_transact()
    erase()

def erase():
    print(Fore.LIGHTRED_EX, "Erasing", Style.RESET_ALL)
    open("retel/read.py", "w").close()
    print(Fore.LIGHTGREEN_EX, "Looping\n", Style.RESET_ALL)

def loop():
    while True:
        schedule.run_pending()
        time.sleep(2)

def execute_transact():
    print(Fore.LIGHTBLUE_EX, "Executing", Style.RESET_ALL)
    try:
        exec(open('retel/read.py').read(), globals())
    except ExecInterrupt:
        pass
    print(Fore.LIGHTMAGENTA_EX, "Transacting", Style.RESET_ALL)


def retel_initialize():
    erase()
    contract_data = update_contracts()
    print("Initializing Physician Smart Contracts")
    for key in contract_data.keys():
        contract = w3.eth.contract(
            address=contract_data[key][2],
            abi=contract_data[key][0],
            bytecode=contract_data[key][1])
        if contract.functions.return_type().call() == "physician":
            contract.functions.initalize().transact()
            sub_contracts = contracts.init_contracts_physician(key)
        else:
            continue
        read(contract, sub_contracts, key)

    contract_data = update_contracts()
    print("Initializing Patient Smart Contracts")
    for key in contract_data.keys():
        contract = w3.eth.contract(
            address=contract_data[key][2],
            abi=contract_data[key][0],
            bytecode=contract_data[key][1])
        if contract.functions.return_type().call() == "patient":
            sub_contracts = contracts.init_contracts_patient(key)
        else:
            continue
        read(contract, sub_contracts,key)

    contract_data = update_contracts()
    print("Initializing Device Smart Contracts")
    for key in contract_data.keys():
        contract = w3.eth.contract(
            address=contract_data[key][2],
            abi=contract_data[key][0],
            bytecode=contract_data[key][1])
        if contract.functions.return_type().call() == "device":
            sub_contracts = contracts.init_contracts_device(key,contract)
        else:
            continue
        read(contract, sub_contracts, key)



def loop_exec(time,key):
    contract_data = update_contracts()
    contract = w3.eth.contract(
        address=contract_data[key][2], abi=contract_data[key][0], bytecode=contract_data[key][1])
    print(Fore.LIGHTYELLOW_EX,"Scheduling:", key, "Type:",
          contract.functions.return_type().call(), Style.RESET_ALL)
    if contract.functions.return_type().call() == "device":
        sub_contracts = contracts.init_contracts_device(key, contract)
        schedule.every(int(time)).seconds.do(read,contract=contract,sub_contracts=sub_contracts,key=key)
    if contract.functions.return_type().call() == "patient":
        sub_contracts = contracts.init_contracts_patient(key, contract)
        schedule.every(int(time)).seconds.do(
            read, contract=contract, sub_contracts=sub_contracts, key=key)
    if contract.functions.return_type().call() == "physician":
        sub_contracts = contracts.init_contracts_physician(key, contract)
        schedule.every(int(time)).seconds.do(
            read, contract=contract, sub_contracts=sub_contracts, key=key)
