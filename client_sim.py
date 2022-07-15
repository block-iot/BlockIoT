import time,csv

while True:
    with open("/Users/manan/Documents/Block_UI/BlockIoT/request.txt", "w") as f:
        f.write("publish")
    f.close()
    time.sleep(5)
