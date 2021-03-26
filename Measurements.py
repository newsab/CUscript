class Measurements:

    def __init__(self, time, lon, lat, alt, measure):
        self.time = time
        self.lon = lon
        self.lat = lat
        self.alt = alt
        self.measure = measure


def createDummy():
    lines = list(open('./Measurements/test24-3medFrekvens.txt'))
    objects = []

    for line in lines:
        time = line[2:28]
        lo = line[34:44]
        la = line[48:58]
        al = line[62:66]
        mea = line[69:80]
        # print(time)
        # print(lo)
        # print(la)
        # print(al)
        #print(mea + "\n")
        obj = time, lo, la, al, mea
        objects.append(obj)

    return objects
