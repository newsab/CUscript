from Organisations import *
from MeasuringObjects import *
from Antennas import *
from Measurements import *
from MeasurementData import *
from pyro import *
import DbController as dbContext

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


    def insertOrganisationToDb(self):
        table = 'Organisation'
        column = 'name'
        input = self.antenna.name
        dbContext.insertData(table, column, input)
    

    def insertMeasureingObjectToDb(self):    
        table = 'MeasureingObject'
        column = 'name, organisationId'
        input = self.antenna.name + "', '" + self.organisation.id
        dbContext.insertData(table, column, input)


    def insertAntennaToDb(self):
        table = 'Antenna'
        column = 'name, measureingObjectId'
        input = self.antenna.name + "', '" + self.measuringObject.id
        dbContext.insertData(table, column, input)


    def insertMeasurementToDb(self):
        table = 'Measurement'
        column = 'time, frequency, longitude, latitude, altitude, info, antennaId'
        input = str(self.measurement.time) + "', '" + str(self.measurement.frequency) + "', '" + str(self.measurement.longitude) + "', '" + str(self.measurement.latitude) + "', '" + str(self.measurement.altitude) + "', '" + self.measurement.info + "', '" + str(self.antenna.id)
        dbContext.insertData(table, column, input)
        id = self.getLatestId()
        self.insertMeasurementDataToDb(id)


    def insertMeasurementDataToDb(self, fk):
            length = len(self.measurementData.longitude)
            count = 0   
            table = 'MeasurementData'
            column = 'time, longitude, latitude, altitude, dbValue, measurementId'        
            while count < length:
                input = str(self.measurementData.time[count]) + "', '" + str(self.measurementData.longitude[count]) + "', '" + str(self.measurementData.latitude[count]) + "', '" + str(self.measurementData.altitude[count]) + "', '" + str(self.measurementData.dbValue[count]) + "', '" + str(fk)
                dbContext.insertData(table, column, input)
                count = count + 1


    def getLatestId(self):
        id = dbContext.getLatestId('Measurement')
        return id

    