
from datetime import datetime, timedelta
import time
import numpy as np
import json
#End_Imports


def publish_data(data,medication,dose):
    with open("request.txt", "r") as f:
        requests = f.read()
    if "publish" in requests:
        with open("request.txt", "w") as f:
            f.write("")
        heart_rate = int(np.random.normal(loc=88, scale=11, size=None))
        blood_glucose = int(np.random.normal(loc=167, scale=56, size=None))
        systolic_bp = int(np.random.normal(loc=126, scale=18, size=None))
        diastolic_bp = int(np.random.normal(loc=50, scale=9, size=None))
        today_time = time.time()
        some_dict = {
            "heart_rate":[str(int(today_time)),heart_rate],
            "glucose": [str(int(today_time+1)),blood_glucose],
            "systolic": [str(int(today_time+2)),systolic_bp],
            "diastolic": [str(int(today_time+3)),diastolic_bp]
        }
        with open("output.json","w") as f:
            json.dump(some_dict, f)
        f.close()
    else:
        pass