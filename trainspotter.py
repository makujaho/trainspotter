import json
import requests

from trainspotter   import utils
from trainspotter   import train
from datetime       import datetime

def getTrains():
    time=datetime.now().strftime('%H:%M:%S')
    for i in range(1,24):
        r = requests.get('http://www.apps-bahn.de/bin/livemap/query-livemap.exe/dny?L=vs_livefahrplan&performLocating=1&performFixedLocating='+str(i)+'&look_requesttime='+time+'&livemapRequest=no&ts=20140710')
        a = r.json()
        try:
            for i in a[0][:-1]:
                if i[6] != '':
                    p = train.Train(i, utils.calcCKV(a[0][-1][5], len(a[0])-1))
                    print(p)
        except Exception as e:
            print(e)
            pass

getTrains()

