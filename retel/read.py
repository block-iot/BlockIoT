from web3.auto.gethdev import w3
import json
with open(r"contract_data.json", "r") as infile:
    contract_data = json.load(infile)
from web3.auto.gethdev import w3
import json
with open(r"contract_data.json", "r") as infile:
    contract_data = json.load(infile)




contract = w3.eth.contract(address=contract_data['a6cdrttaH4cH5GVm_ihwT'][2], abi=contract_data['a6cdrttaH4cH5GVm_ihwT'][0], bytecode=contract_data['a6cdrttaH4cH5GVm_ihwT'][1])

last = {'1619827200': '1', '1619913600': '1', '1620000000': '1', '1620086400': '1', '1620172800': '1', '1620259200': '1', '1620345600': '1', '1620432000': '1', '1620518400': '1', '1620604800': '1', '1620691200': '1', '1620777600': '1', '1620864000': '1', '1620950400': '1', '1621036800': '1', '1621123200': '1', '1621209600': '1', '1621296000': '1', '1621382400': '1', '1621468800': '1', '1621555200': '1', '1621641600': '1', '1621728000': '1', '1621814400': '1', '1621900800': '1', '1621987200': '1', '1622073600': '1', '1622160000': '1', '1622246400': '1', '1622332800': '1', '1622419200': '1', '1622505600': '1', '1622592000': '1'}

report = adherence(last,'')

contract.functions.adherence(report[0],report[1]).transact()

last = {'1619827200': '1', '1619913600': '1', '1620000000': '1', '1620086400': '1', '1620172800': '1', '1620259200': '1', '1620345600': '1', '1620432000': '1', '1620518400': '1', '1620604800': '1', '1620691200': '1', '1620777600': '1', '1620864000': '1', '1620950400': '1', '1621036800': '1', '1621123200': '1', '1621209600': '1', '1621296000': '1', '1621382400': '1', '1621468800': '1', '1621555200': '1', '1621641600': '1', '1621728000': '1', '1621814400': '1', '1621900800': '1', '1621987200': '1', '1622073600': '1', '1622160000': '1', '1622246400': '1', '1622332800': '1', '1622419200': '1', '1622505600': '1', '1622592000': '1'}

report = adherence(last,'')

contract.functions.adherence(report[0],report[1]).transact()