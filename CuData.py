import time
#import Measurements

global count
global lines
global lon
global lat
global alt
global mea

count = 0
lon = []
lat = []
alt = []
mea = []
lines = list(open('./PAMP.txt'))


def getData():
    global count
    global lines
    line = lines[count]
    lo = line[32:44]
    la = line[48:60]
    al = line[64:67]
    me = line[70:84]
    lon.append(float(lo))
    lat.append(float(la))
    alt.append(float(al))
    mea.append(float(me))
    count = count + 1
    return line, lon, lat, alt, mea
