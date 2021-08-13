import os,json
import shutil
# shutil.rmtree("Published/")
# os.remove("contract_data.json")
# with open(r"contract_data.json", "x") as infile:
#     json.dump({}, infile)

from threading import Thread
from register import * # type: ignore
from blockchain import * # type: ignore
from retel.retel import * # type: ignore

# Keywords such as BL_timestamp signify what type of data will be present there. 

physicians = {}
with open(r"config.json", "r") as infile:
    physicians = json.load(infile)

#When command arrives
for value in physicians.values():
    registration_real(value)
    retel_initialize()

loop()