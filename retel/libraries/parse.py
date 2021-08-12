import requests
import time
import ciso8601
#End_Imports

def ripplehealth(url):
    r = requests.get(url)
    result = r.json()
    data = dict()
    rtime = 0
    for element in result.keys():
        # ts = ciso8601.parse_datetime(element)
        rtime = int(element) - int(element) % 86400
        if (str(rtime) in data):
            data[str(rtime)] = str(int(data[str(rtime)]) + 1)
        else:
            data[str(rtime)] = str(1)
    return str(data)
