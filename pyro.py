import Pyro4
import threading
import time
# use the URI that the server printed:


class StartAndStop:

    def __init__(self):
        self.quitflag = False
        self.quitlock = threading.Lock()
        self.thing = Pyro4.Proxy("PYRONAME:PMUApp")

    def start(self):
        while True:
            with self.quitlock:
                if self.quitflag:
                    return
            self.thing.startMeasure()

    def stop(self):
        with self.quitlock:
            self.quitflag = True
        self.thing.stopMeasure()
        t.join()

    t = threading.Thread(target=start)
    t.start()


def test():
    print("test1")
    p = StartAndStop()
   # p.start()
    time.sleep(5)
    print("HEEEJEEJEJE")
    p.stop()


test()
