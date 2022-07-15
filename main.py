import multiprocessing
import time,os,json,shutil
from subprocess import DEVNULL, call
from web3.auto.gethdev import w3
import json
import os,pyfiglet
import numpy as np
from colorama import init, Fore, Back, Style
from pathlib import Path
from tqdm import tqdm


def start_ethereum():
    call(["geth", "--dev", "--ipcpath", "~/Library/Ethereum/geth.ipc"],
         stderr=DEVNULL, stdout=DEVNULL)


def start_server():   
    call(["python3", "-m", "http.server ", "8000"],
         stderr=DEVNULL, stdout=DEVNULL)


def update_contracts():
    with open(r"contract_data.json", "r") as infile:
        contract_data = json.load(infile)
    return contract_data

def start_ipfs():
    call(["ipfs", "daemon"], stderr=DEVNULL, stdout=DEVNULL)


def start_dashboard():
    call(["python3", "dashboard.py"], stderr=DEVNULL, stdout=DEVNULL)


def start_main():
    call(["python3", "initialize.py"], stderr=DEVNULL, stdout=DEVNULL)


def publish_data():
    data = [[], [], [], []]
    the_min = 5679053100
    today_time = 5680237800
    for i in tqdm(range(1000)):
        with open("request.txt", "w") as f:
            f.write("")
        heart_rate = int(np.random.normal(loc=88, scale=11, size=None))
        blood_glucose = int(np.random.normal(loc=167, scale=56, size=None))
        systolic_bp = int(np.random.normal(loc=126, scale=18, size=None))
        diastolic_bp = int(np.random.normal(loc=50, scale=9, size=None))
        some_dict = dict()
        some_dict2 = {
            "Heart Rate": [int(today_time), heart_rate],
            "Blood Glucose": [int(today_time+1), blood_glucose],
            "Systolic BP": [int(today_time+2), systolic_bp],
            "Diastolic BP": [int(today_time+3), diastolic_bp]
        }
        data[0].append(some_dict2["Heart Rate"])
        data[1].append(some_dict2["Blood Glucose"])
        data[2].append(some_dict2["Systolic BP"])
        data[3].append(some_dict2["Diastolic BP"])
        today_time -= 10800
    the_json = {}
    with open("/Users/manan/Documents/Block_UI/BlockIoT_UI/resources/research_study/cases_all/249/observations.json", "r") as f:
        the_json = json.load(f)
        # the_json["1649174089"]["data"] = some_dict2["Blood Glucose"]
        # the_json["1649174091"]["data"] = some_dict2["Diastolic BP"]
        # the_json["1649174092"]["data"] = some_dict2["Systolic BP"]
    f.close()
    the_json["1649174088"]["numeric_lab_data"][0]["data"] = data[0]
    the_json["1649174089"]["numeric_lab_data"][0]["data"] = data[1]
    the_json["1649174090"]["numeric_lab_data"][0]["data"] = data[2]
    the_json["1649174091"]["numeric_lab_data"][0]["data"] = data[3]
    with open("/Users/manan/Documents/Block_UI/BlockIoT_UI/resources/research_study/cases_all/249/observations.json", "w") as f:
        json.dump(the_json, f)
    f.close()



def check_files():
    with open("/Users/manan/Documents/Block_UI/BlockIoT_UI/SEMRinterface/static/js/iot_hr.json", "w") as f:
        some_dict = {
    "Heart Rate": [],
    "Blood Glucose": [],
    "Systolic BP": [],
    "Diastolic BP": []
    }
        json.dump(some_dict, f)
    f.close()
    if os.path.isfile("contract_data.json"):
        os.remove("contract_data.json")
    with open(r"contract_data.json", "x") as infile:
        json.dump({}, infile)
    if os.path.isdir('Published/'):
        shutil.rmtree("Published/")
    os.mkdir("Published/")
    os.mkdir("Published/Device/")
    os.mkdir("Published/Patient/")
    os.mkdir("Published/Physician/")


if __name__ == '__main__':
    call(["clear"])
    result = pyfiglet.figlet_format("BlockIoT")
    print(Fore.LIGHTCYAN_EX+result+Style.RESET_ALL)
    print(Fore.LIGHTBLUE_EX,"Doing some file checks...")
    time.sleep(2)
    check_files()
    print("Files Processed")
    print("Running additional checks...")
    publish_data()
    print(Fore.LIGHTMAGENTA_EX,"Starting Execution", Style.RESET_ALL)
    time.sleep(2)
    exit(0)
    import initialize
    initialize()
    
