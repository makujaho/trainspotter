def sign(val,ckv):
    return ckv*(val%ckv)+int(val/ckv)
    
def calcCKV(date,d):
    return 22222 + ((int(date)+d) % 22222)
        
