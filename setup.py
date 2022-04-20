import multiprocessing
import time,os,json,shutil
from subprocess import DEVNULL, call
from web3.auto.gethdev import w3
import json
import os,pyfiglet
from colorama import init, Fore, Back, Style
from pathlib import Path

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


call(["clear"])
result = pyfiglet.figlet_format("BlockIoT Setup")
print(Fore.LIGHTCYAN_EX+result+Style.RESET_ALL)
print(Fore.LIGHTBLUE_EX,"Welcome to Setup!",Style.RESET_ALL)
print(Fore.RED,"Installing Requirements.txt", Style.RESET_ALL)
time.sleep(1.5)
call(["pip3","install","-r","requirements.txt"])
time.sleep(1.5)
print(Fore.GREEN,"Successfully Installed Packages", Style.RESET_ALL)
time.sleep(1.5)
print(Fore.RED,"Installing Geth... Please cross your fingers", Style.RESET_ALL)
time.sleep(1.5)
call(["sudo","add-apt-repository","-y","ppa:ethereum/ethereum"])
call(["sudo","apt-get","update"])
call(["sudo","apt-get","install","ethereum"])
time.sleep(1.5)
print(Fore.GREEN,"Successfully Installed Geth! Geth Version:", Style.RESET_ALL)
call(["geth","version"])
time.sleep(1.5)
print(Fore.RED,"Installing IPFS Daemon", Style.RESET_ALL)
time.sleep(1.5)
call(["wget","https://dist.ipfs.io/go-ipfs/v0.12.0/go-ipfs_v0.12.0_linux-amd64.tar.gz"])
call(["tar","-xvzf","go-ipfs_v0.12.0_linux-amd64.tar.gz"])
call(["sudo","bash","install.sh"],cwd="go-ipfs")
time.sleep(1.5)
print(Fore.GREEN,"Successfully Installed IPFS! IPFS Version: ", Style.RESET_ALL)
call(["ipfs","--version"])
print(Fore.RED,"Installing Solidity", Style.RESET_ALL)
time.sleep(1.5)
import solcx
solcx.install_solc('0.8.13')
time.sleep(1.5)
print(Fore.GREEN,"Successfully Installed Solidity! Solidity Version:", Style.RESET_ALL)
print(solcx.get_solc_version())
print(Fore.RED,"Creating Files", Style.RESET_ALL)
check_files()
time.sleep(1.5)
print(Fore.GREEN,"Successfully created all files", Style.RESET_ALL)
print(Fore.LIGHTCYAN_EX,"Setup Successful. Please see the README.md to start running...", Style.RESET_ALL)
