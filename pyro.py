import threading
import time
from logging import shutdown
from os.path import commonpath, exists, lexists
import Pyro4

class StartAndStop:

    def __init__(self):
        """
        Creates a StartAndStop object which can communicate with the PMU. 
        The object should be killed after use with "del "object name"" function.
        """
        self.quitflag = False                                       #Creates a boolean which is used to show if the measurementloop should stop or countinue
        self.quitlock = threading.Lock()                            #Creates a threading lock
        self.pmu = Pyro4.Proxy("PYRONAME:PMUApp")                   #Creates the Pyro proxy
        self.t = threading.Thread(target=self.startPmuMeasurement)  #Creates a thread with startPmuMeasurement as target
        self.freq = 0.0                                             #Creates a float to store the frequency in  
        self.mesurementList = list                                  #Creates a list to store the complete measurementdata
        self.showList = list                                        #Creates a list to store a smaller amount of measurementdata for the live plot in GUI

    def startPmuMeasurement(self):
        """
        Calling the PMU function that starts the measurment and runs the 
        loop to update the showList as long the quitflag is set to False. 
        """
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
        """
        Calling the PMU function that stops the measurement and returns 
        the measurementList which includes all measurements made by the PMU. 
        Also sets the quitflag to True to stop the update of the showList.
        """
        try:
            self.quitflag = True
            self.mesurementList = self.pmu.stopMeasure()
            return self.mesurementList
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
        Asks PMU for singelposition and returns object including longitude, 
        latitude and altitude witch is used to get the AUTs position.
        """
        try:
            startPosition = self.pmu.getStartPosition()
            return startPosition
        except:
            print('Could not run function getStartPosition from StartAndStop')
