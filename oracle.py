import json
from register import *  # type: ignore
from blockchain import *  # type: ignore
from parser import *  # type: ignore
import time
from threading import Thread
from web3.auto.gethdev import w3
import plotly.graph_objects as go
from datetime import datetime
import schedule
import ast
import copy
import subprocess
import pretty_errors
from Library.api import *

with open(r"contract_data.json", "r") as infile:
    contract_data = json.load(infile)



def call_contract(key, function):
    print(function)
    with open(r"contract_data.json", "r") as infile:
        contract_data = json.load(infile)
    contract2 = w3.eth.contract(
        address=contract_data[key][2], abi=contract_data[key][0], bytecode=contract_data[key][1])
    # contract.functions.return_type().transact()

    # print(function)
    eval(function)
    return True

# Delegator


def oracle():
    for key in contract_data.keys():
        last = ''
        contract = w3.eth.contract(
            address=contract_data[key][2], abi=contract_data[key][0], bytecode=contract_data[key][1])
        if contract.functions.return_type().call() == "device":
            contract.functions.step1().transact()
            with open("devices.txt", "r") as f:
                last = f.read()
            last = last.replace("**key**", "\'"+str(key)+"\'")
            last += "device_key = \'" + key + "\'\n"
            last += "patient_contract = w3.eth.contract(address=contract_data[**key**][2],abi=contract_data[**key**][0],bytecode=contract_data[**key**][1])"
            last = last.replace(
            "**key**", "\'"+str(contract.functions.get_patient_addr().call())+"\'")
        else:
            continue
        length = contract.functions.get_event_length().call()
        i = 0
        instruction = ""
        # Get Instruction
        while i < length:
            instruction += contract.functions.get_event(i).call()
            i += 1
        instruction_list = instruction.split("::")
        # print(instruction_list)
        # Execute one by one
       # print(instruction_list)
        if instruction_list == ['']:
            continue
        with open("sample.py", "w") as f:
            f.write(last)
        for element in instruction_list:
            if element == '':
                continue
            # print(element)
            with open("sample.py", "a") as f:
                f.write("\n"+element+"\n")
            # Return data if its there
            # if type(data) == str and data != '':
            #     contract.functions.set_data(str(data)).transact()
            #     last = data
        exec(open('sample.py').read())
    for key in contract_data.keys():
        last = ''
        contract = w3.eth.contract(
            address=contract_data[key][2], abi=contract_data[key][0], bytecode=contract_data[key][1])
        if contract.functions.return_type().call() == "patient":
            with open("patients.txt", "r") as f:
                last = f.read()
        else:
            continue
        length = contract.functions.get_event_length().call()
        i = 0
        instruction = ""
        # Get Instruction
        while i < length:
            instruction += contract.functions.get_event(i).call()
            i += 1
        instruction_list = instruction.split("::")
        # print(instruction_list)
        # Execute one by one
        last += "\ncontract = w3.eth.contract(address=contract_data[**key**][2],abi=contract_data[**key**][0],bytecode=contract_data[**key**][1])\n"
        last = last.replace("**key**", "\'"+str(key)+"\'")
       # print(instruction_list)
        if instruction_list == ['']:
            continue
        with open("sample.py", "w") as f:
            f.write(last)
        for element in instruction_list:
            if element == '':
                continue
            # print(element)
            with open("sample.py", "a") as f:
                f.write("\n"+element+"\n")
            # Return data if its there
            # if type(data) == str and data != '':
            #     contract.functions.set_data(str(data)).transact()
            #     last = data
        exec(open('sample.py').read(),globals())
