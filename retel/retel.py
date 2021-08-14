import json
from register import *  # type: ignore
from blockchain import *  # type: ignore
import time
from threading import Thread
# from web3.auto.gethdev import w3
from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3
# from eth_tester import PyEVMBackend

import plotly.graph_objects as go
import schedule
import ast
import copy
import subprocess
import pretty_errors
from . import contracts  # type: ignore
# from contracts import init_contracts
import timeit

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

def read(contract,sub_contracts):
    print("running")
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

def erase():
    open("retel/read.py", "w").close()

def loop():
    while True:
        schedule.run_pending()
        time.sleep(1)

def execute_transact():
    try:
        exec(open('retel/read.py').read(), globals())
    except ExecInterrupt:
        pass


def retel_initialize():
    erase()
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
        read(contract,sub_contracts)
        input()
        execute_transact()
        erase()
    for key in contract_data.keys():
        contract = w3.eth.contract(
            address=contract_data[key][2],
            abi=contract_data[key][0],
            bytecode=contract_data[key][1])
        if contract.functions.return_type().call() == "patient":
            sub_contracts = contracts.init_contracts_patient(key)
        else:
            continue
        read(contract, sub_contracts)
        input()
        execute_transact()
        erase()
    for key in contract_data.keys():
        contract = w3.eth.contract(
            address=contract_data[key][2],
            abi=contract_data[key][0],
            bytecode=contract_data[key][1])
        if contract.functions.return_type().call() == "device":
            sub_contracts = contracts.init_contracts_device(key,contract)
        else:
            continue
        read(contract, sub_contracts)
        input()
        execute_transact()
        erase()


def loop_exec(time,key):
    with open(r"contract_data.json", "r") as infile:
        contract_data = json.load(infile)
    contract = w3.eth.contract(
        address=contract_data[key][2], abi=contract_data[key][0], bytecode=contract_data[key][1])
    if contract.functions.return_type().call() == "device":
        sub_contracts = contracts.init_contracts_device(key, contract)
        schedule.every(int(time)).seconds.do(read,contract=contract,sub_contracts=sub_contracts)
    if contract.functions.return_type().call() == "patient":
        sub_contracts = contracts.init_contracts_patient(key, contract)
        schedule.every(int(time)).seconds.do(
            read, contract=contract, sub_contracts=sub_contracts)
    if contract.functions.return_type().call() == "physician":
        sub_contracts = contracts.init_contracts_physician(key, contract)
        schedule.every(int(time)).seconds.do(
            read, contract=contract, sub_contracts=sub_contracts)
