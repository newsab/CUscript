import datetime

class Measurements:

    def __init__(self):
        self.id = 0
        self.time = datetime.datetime.now()
        self.frequency = 0.0
        self.longitude = 0.0
        self.latitude = 0.0
        self.altitude = 0.0
        self.info = "" 
        self.antennaId = 0
