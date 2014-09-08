import json
from trainspotter import utils

class Train:
    def __init__(self,train,ckv):
        self.name = train[0]
        self.x = utils.sign(train[1],ckv)
        self.y = utils.sign(train[2],ckv)
        self.x_enc = train[1]
        self.y_enc = train[2]
        self.id = train[3]
        self.direction = train[4]
        self.productclass = train[5]
        self.delay = train[6]
        self.lstopname = train[7]
        self.pstopname = train[9]
        self.pstopno = train[10]
        self.nstopname = train[11]
        self.nstopno = train[12]
        self.dateRef = train[13]
        self.pstopdeparture = train[17]
        self.nstoparrival = train[16]
        self.ageofreport = train[14]
        self.lastreporting = train[15]
        self.zpathflags = train[20]
        self.additionaltype = train[21]
        self.hideMoments = train[22]

    def __repr__(self):
        return "<Train Object %s - '%s'>" % (self.id,self.name)

    def __str__(self):
        return json.dumps(self.__dict__)
