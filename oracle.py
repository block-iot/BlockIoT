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
import timeit

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

#Latency between a device and BlockIoT

#Time to do:
#Iterate through entire iteration of smart contracts
#Time for RETEL Execution- patient.sol, and device.sol
#Time to send information between contracts
#Overall gas costs per storage transaction.
#Time to parse device data?
#Overall time to register a patient
# Specific time to read, execute, transact, erase, etc. 
#Time to send alert to physician and patient

def oracle():
    #print("itr_diff, device_contract_diff, device_instruction_diff, device_transaction_end, device_transaction_diff, device_execute_diff, patient_contract_diff,pt_instruction_diff, patient_exec_diff")
    for i in range(0,1):
        itr_start_time = time.time()
        for key in contract_data.keys():
            device_contract_start = time.time()
            last = ''
            contract = w3.eth.contract(
                address=contract_data[key][2], abi=contract_data[key][0], bytecode=contract_data[key][1])
            if contract.functions.return_type().call() == "device":
                device_transaction_start = time.time()
                contract.functions.step1().transact()
                device_transaction_end = time.time()
                with open("devices.txt", "r") as f:
                    last = f.read()
                last = last.replace("**key**", "\'"+str(key)+"\'")
                last += "device_key = \'" + key + "\'\n"
                last += "patient_contract = w3.eth.contract(address=contract_data[**key**][2],abi=contract_data[**key**][0],bytecode=contract_data[**key**][1])"
                last = last.replace(
                "**key**", "\'"+str(contract.functions.get_patient_addr().call())+"\'")
            else:
                continue
            device_instruction_start = time.time()
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
            device_instruction_end = time.time()
            execute_start = time.time()
            exec(open('sample.py').read())
            execute_end = time.time()
            device_contract_end = time.time()
        input("")
        for key in contract_data.keys():
            patient_contract_start = time.time()
            last = ''
            contract = w3.eth.contract(
                address=contract_data[key][2], abi=contract_data[key][0], bytecode=contract_data[key][1])
            if contract.functions.return_type().call() == "patient":
                with open("patients.txt", "r") as f:
                    last = f.read()
            else:
                continue
            patient_instruction_start = time.time()
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
            patient_instruction_end = time.time()
            patient_exec_start = time.time()
            exec(open('sample.py').read(),globals())
            patient_exec_end = time.time()
            patient_contract_end = time.time()
        input("")
        itr_end_time = time.time()
        itr_diff = itr_end_time - itr_start_time
        device_contract_diff = device_contract_end - device_contract_start
        device_instruction_diff = device_instruction_end - device_instruction_start
        device_transaction_diff = device_transaction_end - device_transaction_start
        device_execute_diff = execute_end - execute_start

        patient_contract_diff = patient_contract_end - patient_contract_start
        pt_instruction_diff = patient_instruction_end - patient_instruction_start
        patient_exec_diff = patient_exec_end - patient_exec_start
       # print("{0},{1},{2},{3},{4},{5},{6},{7}".format(itr_diff, device_contract_diff, device_instruction_diff, device_transaction_diff, device_execute_diff, patient_contract_diff,
            #   pt_instruction_diff, patient_exec_diff))

        # print("{0}--{1}--{2}".format(starttime,endtime,endtime-starttime))
        #time.sleep(20)

#Output2- Total time to register a patient
#Output3- Total time to deploy contract
