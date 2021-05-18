import threading
import time
from logging import shutdown
from os.path import commonpath, exists, lexists
import Pyro4
import FixTypes
import socket

class StartAndStop:
    
    def __init__(self):
        # Creates a boolean which is used to show if the measurementloop should stop or continue
        self.quitflag = False
        # Creates the Pyro proxy
        self.pmu = Pyro4.Proxy("PYRONAME:PMUApp")
        # Creates a thread with startPmuMeasurement as target
        self.t = threading.Thread(target=self.startPmuMeasurement)
        # Creates a float to store the frequency in
        self.freq = 0.0  
        # Creates a list to store the complete measurement data
        self.mesurementList = list  
        # Creates a list to store a smaller amount of measurement data for the live plot in GUI
        self.showList = list

    def startPmuMeasurement(self):
        """
        Calling the PMU function that starts the measurement and runs the 
        loop to update the showList as long the quitflag is set to False. 
        """
        try:
            self.quitflag = False
            self.pmu.starta(self.freq)
            while not self.quitflag:
                self.showList = self.pmu.getListToSend()
                time.sleep(0.3)
        except:
            print('Could not run function startPmuMeasurement from StartAndStop')

    def stop(self):
        """
        Calling the PMU function that stops the measurement and returns 
        the measurementList which includes all measurements made by the PMU. 
        Also sets the quitflag to True to stop the update of the showList.
        """
        try:
            self.quitflag = True
            self.mesurementList = self.pmu.stopMeasure()
        except:
            print('Could not run function stop from StartAndStop')

    def start(self, frequency):
        """
        Takes a frequency as parameter and starts the theard 
        which is calling the startPmuMeasurement.
        """
        try:
            self.freq = frequency
            self.t.start()
        except:
            print('Could not run function start from StartAndStop')

    def getStartPosition(self):
        """
        Asks PMU for singleposition and returns object including longitude, 
        latitude and altitude witch is used to get the AUTs position.
        """
        try:
            startPosition = self.pmu.getStartPosition()
            return startPosition
        except:
            print('Could not run function getStartPosition from StartAndStop')

    def getFixStatus(self):
        """
        Asks PMU for the fix status and returns the status as a string.
        """
        try:
            fixStatus = self.pmu.getFixStatus()
            status = FixTypes.rtkList[fixStatus]
            return status
        except:
            return "Kunde inte få kontakt med PMU"





    """
    def __init__(self):
            self.freq = 0.0
            self.mesurementList = []
            self.showList = []

    def start(self, frequency):
            self.freq = frequency
            self.setDummyData()

    def stop(self):
            print("Nu blev det stop")

    def getStartPosition(self):
            startPosition = '15.9181962', '59.3885022', 5.5
            return startPosition

    def getFixStatus(self):
        fixStatus = 4
        status = FixTypes.rtkList[fixStatus]
        return status

    def setDummyData(self):
        lines = list(open('./Measurements/test24-3medFrekvens.txt'))
        for line in lines:
            time = line[2:27]
            lo = line[32:44]
            la = line[48:60]
            al = line[63:66]
            mea = line[68:78]         
            obj = time, lo, la, al, mea
            self.mesurementList.append(obj)
            self.showList.append(obj)
    """