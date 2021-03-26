import threading
import time
from logging import shutdown
from os.path import commonpath, exists, lexists

import Pyro4

# use the URI that the server printed:


class StartAndStop:

    def __init__(self):
        self.quitflag = False
        self.quitlock = threading.Lock()
        self.thing = Pyro4.Proxy("PYRONAME:PMUApp")
        self.t = threading.Thread(target=self.start2)
        self.mesurement = list
        print(self.thing)

    def start2(self, frequency):
        fre = frequency
        print("Hej från tråden")
        self.thing.starta(fre)

    def stop(self):
        print("Hej tråden ska vi nysta?")
        # self.t.join()
        self.mesurement = self.thing.stopMeasure()
        print("Progress")
        return self.mesurement

    def start(self, frequency):
        fre = frequency
        if self.t.is_alive():
            print("test")
            self.t.start()
        else:
            self.start2(fre)
