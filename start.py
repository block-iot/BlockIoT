import multiprocessing
import time,os,json,shutil
from subprocess import DEVNULL, call


def start_ethereum():
    call(["geth", "--dev", "--ipcpath", "~/Library/Ethereum/geth.ipc"],
         stderr=DEVNULL, stdout=DEVNULL)


def start_ipfs():
    call(["ipfs", "daemon"], stderr=DEVNULL, stdout=DEVNULL)


def start_dashboard():
    call(["python3", "dashboard.py"], stderr=DEVNULL, stdout=DEVNULL)


def start_main():
    call(["python3", "main.py"],stderr=DEVNULL, stdout=DEVNULL)


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
    p = multiprocessing.Process(target=start_ethereum)
    p.start()
    time.sleep(0.25)
    print("Ethereum Started")
    print("Doing some file checks...")
    time.sleep(0.25)
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
    print("Running main...")
    time.sleep(0.25)
    call(["python3", "main.py"])
