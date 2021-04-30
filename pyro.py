import threading
import time
from logging import shutdown
from os.path import commonpath, exists, lexists
import Pyro4
import FixTypes
import socket


class StartAndStop:
      
    def __init__(self):
        self.hostname = socket.gethostbyname(socket.gethostname())
        print(self.hostname)
        # Creates a boolean which is used to show if the measurementloop should stop or countinue
        self.quitflag = False
        self.quitlock = threading.Lock()  # Creates a threading lock
        self.deamon = Pyro4.Daemon(self.hostname)
        self.pmu = Pyro4.Proxy("PYRONAME:PMUApp")  # Creates the Pyro proxy
        # Creates a thread with startPmuMeasurement as target
        self.t = threading.Thread(target=self.startPmuMeasurement)
        # Creates a thread with setFixStatus as target
        #self.t2 = threading.Thread(target=self.setFixStatus)
        self.freq = 0.0  # Creates a float to store the frequency in
        self.mesurementList = list  # Creates a list to store the complete measurementdata
        # Creates a list to store a smaller amount of measurementdata for the live plot in GUI
        self.showList = list
        # Creates a string to store the fix status
        #self.fixStatus = 0
    
    def startPmuMeasurement(self):
        try:
            self.quitflag = False
            self.pmu.starta(self.freq)
            time.sleep(2)
            while not self.quitflag:
                self.showList = self.pmu.getListToSend()
                time.sleep(0.3)
        except:
            print('Could not run function startPmuMeasurement from StartAndStop')

    def stop(self):
        try:
            self.quitflag = True
            self.mesurementList = self.pmu.stopMeasure()
            return self.mesurementList
        except:
            print('Could not run function stop from StartAndStop')

    def start(self, frequency):
        try:
            self.freq = frequency
            self.t.start()
        except:
            print('Could not run function start from StartAndStop')

    def getStartPosition(self):
        try:
            startPosition = self.pmu.getStartPosition()
            return startPosition
        except:
            print('Could not run function getStartPosition from StartAndStop')

    def getFixStatus(self):
        fixStatus = self.pmu.getFixStatus()
        status = FixTypes.rtkList[fixStatus]
        return status
 
    """
    def __init__(self):
            self.freq = 0.0
            self.mesurementList = []
            self.showList = []

    def start(self, frequency):
        try:
            self.freq = frequency
            print("1")
            self.setDummyData()
            print("7")
        except:
            print('Could not run function start from StartAndStop')

    def stop(self):
        try:
            return self.mesurementList
        except:
            print('Could not run function stop from StartAndStop')

    def getStartPosition(self):
        try:
            startPosition = '15.9181962', '59.3885022', 5.5
            return startPosition
        except:
            print('Could not run function getStartPosition from StartAndStop')

    def getFixStatus(self):
        fixStatus = 4
        status = FixTypes.rtkList[fixStatus]
        return status

    def setDummyData(self):
        print("2")
        lines = list(open('./Measurements/test24-3medFrekvens.txt'))
        print("3")
        for line in lines:
            time = line[2:27]
            lo = line[32:44]
            la = line[48:60]
            al = line[63:66]
            mea = line[68:78]         
            obj = time, lo, la, al, mea
            print(time)
            print(lo)
            print(la)
            print(al)
            print(mea)
            self.mesurementList.append(obj)
            print("6")
            self.showList.append(obj)
            print("5")
    """ 