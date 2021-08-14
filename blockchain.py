import sys
import time
import pprint

from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3
from eth_tester import PyEVMBackend

import json
from solcx import compile_standard
# from web3 import Web3
# from web3 import EthereumTesterProvider
# from web3.auto.gethdev import w3
from solcx import compile_source

import eth_tester.backends.pyevm.main as py_evm_main

# def deploy(name, device=False, patient=False, physician=False):
#     with open(r"contract_data.json","r") as infile:
#         contract_data = json.load(infile)
#     if device == True:
#         file1 = open("Published/Device/"+name + ".sol","r")
#     elif patient == True:
#         file1 = open("Published/Patient/"+name + ".sol","r")
#     elif physician == True:
#         file1 = open("Published/Physician/"+name + ".sol", "r")
#     else:
#         file1 = open("Published/"+name + ".sol","r")
#     compiled_sol = compile_standard({
#         "language": "Solidity",
#         "sources": {
#             name + ".sol": {
#                 "content": file1.read()
#             }
#         },
#         "settings":
#             {
#                 "outputSelection": {
#                     "*": {
#                         "*": [
#                             "metadata", "evm.bytecode"
#                             , "evm.bytecode.sourceMap"
#                         ]
#                     }
#                 }
#             }
#     })
#     # w3 = Web3(EthereumTesterProvider())
#     # # set pre-funded account as sender
#     w3.eth.default_account = w3.eth.accounts[0]
#     # Instantiate and deploy contract
#     bytecode = compiled_sol["contracts"][name + '.sol'][name]['evm']['bytecode']['object']
#     abi = json.loads(compiled_sol["contracts"][name + '.sol'][name]['metadata'])['output']['abi']
#     # Submit the transaction that deploys the contract
#     Greeter = w3.eth.contract(abi=abi, bytecode=bytecode)
#     tx_hash = Greeter.constructor().transact()
#     # Wait for the transaction to be mined, and get the transaction receipt
#     tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

#     # Create the contract instance with the newly-deployed address
#     greeter = w3.eth.contract(address=tx_receipt.contractAddress,abi=abi)
#     contract_data[name] = [abi,bytecode,tx_receipt.contractAddress]
#     file1.close()
#     with open(r"contract_data.json","w") as outfile:
#         json.dump(contract_data, outfile)


def deploy(name, device=False, patient=False, physician=False):
    # Increase the gas limit
    py_evm_main.GENESIS_GAS_LIMIT = 30000000

    w3 = Web3(EthereumTesterProvider(PyEVMBackend()))

    with open(r"contract_data.json","r") as infile:
        contract_data = json.load(infile)
    if device == True:
        # file1 = open("Published/Device/"+name + ".sol","r")
        contract_source_path = "Published/Device/"+name + ".sol"
    elif patient == True:
        file1 = open("Published/Patient/"+name + ".sol","r")
        contract_source_path = "Published/Patient/"+name + ".sol"
    elif physician == True:
        file1 = open("Published/Physician/"+name + ".sol", "r")
        contract_source_path = "Published/Physician/"+name + ".sol"
    else:
        file1 = open("Published/"+name + ".sol","r")
        contract_source_path = "Published/"+name + ".sol"

    compiled_sol = compile_source_file(contract_source_path)
    
    contract_id, contract_interface = compiled_sol.popitem()

    bytecode=contract_interface['bin']

    address = deploy_contract(w3, contract_interface)
    print(f'Deployed {contract_id} to: {address}\n')
    abi=contract_interface["abi"]
    contract = w3.eth.contract(address=address, abi=abi, bytecode=bytecode)

    tx_hash = contract.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Transaction receipt mined:")
    pprint.pprint(dict(tx_receipt))
    print("\nWas transaction successful?")
    pprint.pprint(tx_receipt["status"])
    
    contract_data[name] = [abi,bytecode,tx_receipt.contractAddress]
    with open(r"contract_data.json","w") as outfile:
        json.dump(contract_data, outfile)

def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()

   return compile_source(source)


def deploy_contract(w3, contract_interface):
    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']).constructor().transact()

    address = w3.eth.get_transaction_receipt(tx_hash)['contractAddress']
    return address
