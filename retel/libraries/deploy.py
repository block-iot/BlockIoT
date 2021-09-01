import json
from solcx import compile_standard
from web3 import Web3
from web3 import EthereumTesterProvider
from web3.auto.gethdev import w3
#End_Imports


def deploy(name, device=False, patient=False, physician=False,data=""):
    with open(r"contract_data.json", "r") as infile:
        contract_data = json.load(infile)
    if data == "":
        if device == True:
            file1 = open("Published/Device/"+name + ".sol", "r")
        elif patient == True:
            file1 = open("Published/Patient/"+name + ".sol", "r")
        elif physician == True:
            file1 = open("Published/Physician/"+name + ".sol", "r")
        else:
            file1 = open("Published/"+name + ".sol", "r")
        data = file1.read()
        file1.close()
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            name + ".sol": {
                "content": data
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
    # w3 = Web3(EthereumTesterProvider())
    # # set pre-funded account as sender
    w3.eth.default_account = w3.eth.accounts[0]
    # Instantiate and deploy contract
    bytecode = compiled_sol["contracts"][name +
                                         '.sol'][name]['evm']['bytecode']['object']
    abi = json.loads(
        compiled_sol["contracts"][name + '.sol'][name]['metadata'])['output']['abi']
    # Submit the transaction that deploys the contract
    Greeter = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = Greeter.constructor().transact()
    # Wait for the transaction to be mined, and get the transaction receipt
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    # Create the contract instance with the newly-deployed address
    greeter = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    contract_data[name] = [abi, bytecode, tx_receipt.contractAddress]
    with open(r"contract_data.json", "w") as outfile:
        json.dump(contract_data, outfile)
