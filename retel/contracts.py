


def init_contracts_device(key,contract):
    contracts = "contract = w3.eth.contract(address=contract_data[**key**][2], abi=contract_data[**key**][0], bytecode=contract_data[**key**][1])\n"
    contracts = contracts.replace("**key**", "\'"+str(key)+"\'")
    contracts += "device_key = \'" + key + "\'\n"
    contracts += "patient_contract = w3.eth.contract(address=contract_data[**key**][2],abi=contract_data[**key**][0],bytecode=contract_data[**key**][1])"
    contracts = contracts.replace(
        "**key**", "\'"+str(contract.functions.get_patient_addr().call())+"\'")
    return contracts


def init_contracts_patient(key):
    contracts = "contract = w3.eth.contract(address=contract_data[**key**][2], abi=contract_data[**key**][0], bytecode=contract_data[**key**][1])\n"
    contracts = contracts.replace("**key**", "\'"+str(key)+"\'")
    return contracts


def init_contracts_physician(key):
    contracts = "contract = w3.eth.contract(address=contract_data[**key**][2], abi=contract_data[**key**][0], bytecode=contract_data[**key**][1])\n"
    contracts = contracts.replace("**key**", "\'"+str(key)+"\'")
    return contracts
