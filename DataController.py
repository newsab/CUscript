from Organisations import *
from MeasuringObjects import *
from Antennas import *
from Measurements import *
from MeasurementData import *
from pyro import *

class DataController:

    def __init__(self):
        self.organisation = Organisations()
        self.measuringObject = MeasuringObjects()
        self.antenna = Antennas()
        self.measurement = Measurements()
        self.measurementData = MeasurementData()
        self.pyro = StartAndStop()
        self.on = True

    def getFixStatus(self):
        fixStatus = self.pyro.getFixStatus()
        return fixStatus
    
    def setStartPosition(self):
        startPosition = self.pyro.getStartPosition()
        lon = startPosition[0]
        lat = startPosition[1]
        alt = startPosition[2]
        self.measurement.longitude = float(lon)
        self.measurement.latitude = float(lat)
        self.measurement.altitude = float(alt)

    def setFrequency(self, freq):
        self.measurement.frequency = freq 

    def startMeasurment(self, freq):
        self.setFrequency(freq)
        self.pyro.start(freq)

    def stopMeasurement(self):
        self.pyro.stop

    def setShowList(self):
        showList = self.pyro.showList
        line = showList[-1]
        tim = line[0]
        lon = float(line[1])
        lat = float(line[2])
        alt = float(line[3])
        db = float(line[4])
        self.measurementData.time.append(tim)
        self.measurementData.longitude.append(lon)
        self.measurementData.latitude.append(lat)
        self.measurementData.altitude.append(alt)
        self.measurementData.dbValue.append(db)


    def setMeasurementData(self):
        measurementList = self.pyro.mesurementList
        self.measurementData.time.clear()
        self.measurementData.longitude.clear()
        self.measurementData.latitude.clear()
        self.measurementData.altitude.clear()
        self.measurementData.dbValue.clear()
        for line in measurementList:
            tim = line[0]
            lon = float(line[1])
            lat = float(line[2])
            alt = float(line[3])
            db = float(line[4])
            self.measurementData.time.append(tim)
            self.measurementData.longitude.append(lon)
            self.measurementData.latitude.append(lat)
            self.measurementData.altitude.append(alt)
            self.measurementData.dbValue.append(db)