import requests
import time
import ciso8601
import json,csv
#End_Imports

def ripplehealth(url):
    count = 0
    with open("count.txt","r") as f:
        count = int(f.read())
    f.close()
    if count > 150:
        count = 0
    data = []
    with open("249.csv","r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        a = 0
        for row in csv_reader:
            a += 1
            if a == count:
                data = row
    with open("count.txt","w") as f:
        f.write(str(count+1))
    f.close()
    # result = r.json()
    # data = dict()
    # rtime = 0
    # for element in result.keys():
    #     # ts = ciso8601.parse_datetime(element)
    #     rtime = int(element) - int(element) % 86400
    #     if (str(rtime) in data):
    #         data[str(rtime)] = str(int(data[str(rtime)]) + 1)
    #     else:
    #         data[str(rtime)] = str(1)
    return json.dumps(data)
