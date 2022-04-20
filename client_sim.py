import time,csv

while True:
    with open("/home/shuklm/Code/BlockIoT_3.0/request.txt","w") as f:
        f.write("publish")
    f.close()
    time.sleep(5)