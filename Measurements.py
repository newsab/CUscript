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
"""
    def __init__(self, id, freq, lon, lat, alt, info, antennaId):
        self.id = id
        self.time = datetime.now()
        self.frequency = freq
        self.longitude = lon
        self.latitude = lat
        self.altitude = alt
        self.info = info 
        self.antennaId = antennaId
"""