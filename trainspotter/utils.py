def sign(val,ckv):
    return ckv*(val%ckv)+int(val/ckv)

def calcCKV(date,d):
    return 22222 + ((int(date)+d) % 22222)

def buildUrl(zoom=False, pos_x=0, pos_y=0):
    if zoom == False:
        return ""
    else:
        return ""

def convert_coord(coord):
    return coord/1000000.0

def get_productclass_name(productclass):
    return {
        1: 'ICE',
        2: 'IC / EC / CNL',
        4: 'EN',
        8: 'RB / RE',
        16: 'S',
        16386: 'EC',
        16388: 'EC',
        16392: 'RB / RE / NEG'
    }.get(productclass, 'Unknown')
