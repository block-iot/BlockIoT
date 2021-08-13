import json
from solcx import compile_standard
from web3 import Web3
from web3 import EthereumTesterProvider
from web3.auto.gethdev import w3
#End_Imports

def deploy(name, device=False, patient=False):
    with open(r"contract_data.json", "r") as infile:
        contract_data = json.load(infile)
    if device == True:
        file1 = open("Published/Device/"+name + ".sol", "r")
    elif patient == True:
        file1 = open("Published/Patient/"+name + ".sol", "r")
    else:
        file1 = open("Published/"+name + ".sol", "r")
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            name + ".sol": {
                "content": file1.read()
            }
        },
        "settings":
            {
                "outputSelection": {
                    "*": {
                        "*": [
                            "metadata", "evm.bytecode", "evm.bytecode.sourceMap"
                        ]
                    }
                }
        }
    })
    w3.eth.default_account = w3.eth.accounts[0]
    bytecode = compiled_sol["contracts"][name +
                                         '.sol'][name]['evm']['bytecode']['object']
    abi = json.loads(
        compiled_sol["contracts"][name + '.sol'][name]['metadata'])['output']['abi']
    Greeter = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = Greeter.constructor().transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    contract_data[name] = [abi, bytecode, tx_receipt.contractAddress]
    file1.close()
    with open(r"contract_data.json", "w") as outfile:
        json.dump(contract_data, outfile)
