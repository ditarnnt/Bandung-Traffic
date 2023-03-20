#page = requests.get('https://traffic.api.here.com/traffic/6.2/flow.xml?bbox=39.039696,-77.222108;38.775208,-76.821107?apiKey=z1hUE5rH83_F6uIgubqDkRHn6JQK8s5tUa106Nudp6c')

import pandas as pd
import numpy as np
import urllib.request as urllib2
import json
import pickle
import datetime as dt
from apscheduler.schedulers.blocking import BlockingScheduler
import ssl

#page = requests.get('https://traffic.api.here.com/traffic/6.2/flow.xml?bbox=39.039696,-77.222108;38.775208,-76.821107?apiKey=z1hUE5rH83_F6uIgubqDkRHn6JQK8s5tUa106Nudp6c')

import pandas as pd
import numpy as np
import urllib.request as urllib2
from urllib.request import urlopen
import json
import pickle
import datetime as dt
from apscheduler.schedulers.blocking import BlockingScheduler
import ssl

def get_traffic():
    apiKey = "z1hUE5rH83_F6uIgubqDkRHn6JQK8s5tUa106Nudp6c"
    #app_code = "your_app_code"
    fname=str(dt.datetime.now())[:19].replace(":","-")
    base="https://data.traffic.hereapi.com/v7/flow?locationReferencing=shape&in=bbox:107.54908372065572,-6.926620456605005,107.72967148820469,-6.896286771555365&apiKey=z1hUE5rH83_F6uIgubqDkRHn6JQK8s5tUa106Nudp6c&responseattributes=sh,fc"

    #"https://traffic.ls.hereapi.com/traffic/6.1/flow.json?bbox=107.54908372065572,-6.926620456605005,107.72967148820469,-6.896286771555365&apiKey=z1hUE5rH83_F6uIgubqDkRHn6JQK8s5tUa106Nudp6c&responseattributes=sh,fc"
    try:
        gcontext = ssl.SSLContext(ssl.PROTOCOL_TLS)
        response = urllib2.urlopen(base,context=gcontext)
        data=json.load(response)
        with open(fname+".p", 'wb') as fp:
            pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)
        print (f"Success {fname}")
    except:
        print (f"Failed {fname}")

if __name__=="__main__":
  sched = BlockingScheduler(timezone = "Asia/Jakarta")
  sched.add_job(get_traffic, 'cron', day_of_week='*', hour='*', minute='0,30')
  sched.start()