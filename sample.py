import json
from register import *  # type: ignore
from blockchain import *  # type: ignore
from parser import *  # type: ignore
import time
from threading import Thread
from web3.auto.gethdev import w3
import plotly.graph_objects as go
from datetime import datetime
from datetime import timedelta
import schedule
import ast
import copy
import pretty_errors
from Library.api import *


def adherence(data, specs):
    report = dict()
    if specs == '':
        specs = {'time': [0,1, 7, 30, 365], 'limit': [0,0, 0.30, 0.70, 0.10]}
    df_data = data
    df_data = dict((int(k), int(v)) for k, v in df_data.items())
    overall_comp = sum(df_data.values(
    ))/(int(((((datetime.today().timestamp() - min(list(df_data.keys())))))/60)/60)/24)
    report['time'] = [int(100*overall_comp)]
    days = dict()
    for element in specs['time']:
        adherence = dict()
        adherence = datetime.now() - timedelta(element)
        for element in df_data:
            if int(element) > int(adherence.timestamp()):
                days[element] = df_data[element]
        comp = sum(days.values())/element
        report['time'].append(int(100*comp))
    report['abnormal'] = []
    for i in range(0, len(specs['limit'])):
        if report['time'][i] < specs['limit'][i]:
            report['abnormal'].append(1)
        else:
            report['abnormal'].append(0)
    report_keys = ["overall", "7-day", "30-day",
                   "1-year", "overall_limit", "7-day-limit", "30-day-limit", "365-day-limit"]
    report_values = [item for sublist in list(report.values()) for item in sublist]
    return (report_keys, report_values)


with open(r"contract_data.json", "r") as infile:
    contract_data = json.load(infile)

contract = w3.eth.contract(address=contract_data['a6cdrttaH4cH5GVm_ihwT'][2],abi=contract_data['a6cdrttaH4cH5GVm_ihwT'][0],bytecode=contract_data['a6cdrttaH4cH5GVm_ihwT'][1])

last = {'1627689600': '1', '1627603200': '1', '1627516800': '10', '1627344000': '1'}

report = adherence(last,'')

contract.functions.adherence(report[0],report[1]).transact()