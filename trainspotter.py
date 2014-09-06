import json
import requests
import time
from trainspotter   import utils
from trainspotter   import train
from datetime       import datetime

def getTrains():
    trains = {}
    strTime = datetime.now().strftime('%H:%M:%S')
    strDate = datetime.now().strftime('%Y%m%d')
    for i in range(1,24):
        while True:
            r = requests.get('http://www.apps-bahn.de/bin/livemap/query-livemap.exe/dny?L=vs_livefahrplan&performLocating=1&performFixedLocating='+str(i)+'&look_requesttime='+strTime+'&livemapRequest=no&ts='+strDate)
            a = r.json()
            try:
                for i in a[0][:-1]:
                    p = train.Train(i, utils.calcCKV(a[0][-1][5], len(a[0])-1))
                    trains[p.id] = p
                else:
                    break
            except Exception as e:
                if 'error' in a:
                    time.sleep(5)
                pass

    else:
        return trains

t = getTrains()

for i in t:
    print(i)
