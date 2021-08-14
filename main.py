import multiprocessing
import time,os,json,shutil
from subprocess import DEVNULL, call
from web3.auto.gethdev import w3
import json
import os,pyfiglet
from colorama import init, Fore, Back, Style
from pathlib import Path

def start_ethereum():
    call(["geth", "--dev", "--ipcpath", "~/Library/Ethereum/geth.ipc"],
         stderr=DEVNULL, stdout=DEVNULL)


def start_server():   
    call(["python3", "-m", "http.server ", "8000"],
         stderr=DEVNULL, stdout=DEVNULL)

def start_ipfs():
    call(["ipfs", "daemon"], stderr=DEVNULL, stdout=DEVNULL)


def start_dashboard():
    call(["python3", "dashboard.py"], stderr=DEVNULL, stdout=DEVNULL)


def start_main():
    call(["python3", "initialize.py"], stderr=DEVNULL, stdout=DEVNULL)


def check_files():
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
    p = multiprocessing.Process(target=start_main)
    p.start()
    time.sleep(3)
    p.terminate()
    p = multiprocessing.Process(target=start_main)
    p.start()
    time.sleep(3)
    p.terminate()
    p = multiprocessing.Process(target=start_main)
    p.start()
    time.sleep(3)
    p.terminate()
    print(Fore.LIGHTMAGENTA_EX,"Starting Execution", Style.RESET_ALL)
    time.sleep(2)
    import initialize
    initialize()
    
