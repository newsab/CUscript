import threading
import time
from logging import shutdown
from os.path import commonpath, exists, lexists

import Pyro4

# use the URI that the server printed:


class StartAndStop:

    def __init__(self):
        self.quitflag = False
        self.freq = 0.0
        self.quitlock = threading.Lock()
        self.thing = Pyro4.Proxy("PYRONAME:PMUApp")
        self.t = threading.Thread(target=self.start2)
        self.mesurement = list
        self.showList = list
        print(self.thing)

    def start2(self):
        self.quitflag = False
        print("Hej från tråden")
        self.thing.starta(self.freq)
        time.sleep(2)
        print("Jag kom forbi!!!!")
        while not self.quitflag:
            self.showList = self.thing.getListToSend()
            obj = self.showList[-1]
            print(obj)
            time.sleep(0.3)

    def stop(self):
        print("Hej tråden ska vi nysta?")
        self.quitflag = True
        self.mesurement = self.thing.stopMeasure()
        print("Progress when ju need sucess")
        return self.mesurement

    def start(self, frequency):
        self.freq = frequency
        self.t.start()
