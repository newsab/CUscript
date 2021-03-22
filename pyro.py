import threading
import time
from logging import shutdown

import Pyro4

# use the URI that the server printed:


class StartAndStop:

    def __init__(self):
        self.quitflag = False
        self.quitlock = threading.Lock()
        self.thing = Pyro4.Proxy("PYRONAME:PMUApp")
        #self.py = self.thing.__copy__()
        self.t = threading.Thread(target=self.start2)

    def start2(self):
        print("Hej från tråden")
        self.thing.startaStart()

    def stop(self):
        with self.quitlock:
            if self.quitflag:
                print("Hej tråden ska vi nysta?")
                # self.t._stop()
                self.thing.stopMeasure()
                return

        print("Måste starta först!")

    def start(self):
        with self.quitlock:
            self.quitflag = True
        self.t.start()
