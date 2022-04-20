import time,csv

while True:
    with open("request.txt","w") as f:
        f.write("publish")
    f.close()
    time.sleep(5)