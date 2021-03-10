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
lines = list(open('./testfile.txt'))

def getData():  
    global count  
    global lines
    line = lines[count]
    lo = line[32:42]
    la = line[46:56]
    al = line[60:64]
    me = line[67:85]
    lon.append(float(lo))
    lat.append(float(la))
    alt.append(float(al))
    mea.append(float(me))
    count = count + 1
    return line, lon, lat, alt, mea
    