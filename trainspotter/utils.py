def sign(val,ckv):
    return ckv*(val%ckv)+int(val/ckv)

def calcCKV(date,d):
    return 22222 + ((int(date)+d) % 22222)

def buildUrl(zoom=False, pos_x=0, pos_y=0):
    if zoom == False:
        return ""
    else:
        return ""
