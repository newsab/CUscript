import datetime

class Measurements:

    def __init__(self):
        """
        Class that stores information about the current measurement and the position of the antenna under test.
        """
        self.id = 0
        self.time = datetime.datetime.now()
        self.frequency = 0.0
        self.longitude = 0.0
        self.latitude = 0.0
        self.altitude = 0.0
        self.info = ""
        self.antennaId = 0
