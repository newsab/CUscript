class Measurements:

    def __init__(self, time, lon, lat, alt, measure ):
        self.time = time 
        self.lon = lon
        self.lat = lat
        self.alt = alt
        self.measure = measure

def createDummy():
    lines = list(open('./testfile.txt'))
    objects = list
    count = 0

    for line in lines:
        time = line[2:28]
        lo = line[32:42]
        la = line[46:56]
        al = line[60:64]
        mea = line[67:85]
        #print(time)
        #print(lo)
        #print(la)
        #print(al)
        #print(mea + "\n")
        obj = Measurements(time, lo, la, al, mea)
        objects[count] = obj
        count = count + 1   
    return objects