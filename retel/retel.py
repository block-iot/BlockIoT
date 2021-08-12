import json
from register import *  # type: ignore
from blockchain import *  # type: ignore
import time
from threading import Thread
from web3.auto.gethdev import w3
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


def get_imports(package):
    with open("retel/libraries/"+package + ".py","r") as f:
        result = f.read()
    imports = result.split("#End_Imports")[0]
    functions = result.split("#End_Imports")[1]
    return (imports, functions)

def read(contract,sub_contracts):
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

def execute_transact():
    exec(open('retel/read.py').read(), globals())

def retel():
    erase()
    for key in contract_data.keys():
        contract = w3.eth.contract(
            address=contract_data[key][2],
            abi=contract_data[key][0],
            bytecode=contract_data[key][1])
        if contract.functions.return_type().call() == "device":
            contract.functions.step1().transact()
            sub_contracts = contracts.init_contracts_device(key, contract)
        else:
            continue
        read(contract, sub_contracts)
        execute_transact()
        erase()
    for key in contract_data.keys():
        contract = w3.eth.contract(
            address=contract_data[key][2],
            abi=contract_data[key][0],
            bytecode=contract_data[key][1])
        if contract.functions.return_type().call() == "patient":
            sub_contracts = contracts.init_contracts_patient(key, contract)
        else:
            continue
        read(contract,sub_contracts)
        execute_transact()
        erase()
