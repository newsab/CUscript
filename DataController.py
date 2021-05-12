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
        self.pyro.stop()

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

    def insertMeasuringObjectToDb(self):
        table = 'MeasuringObject'
        column = 'name, organisationId'
        input = self.antenna.name + "', '" + self.organisation.id
        dbContext.insertData(table, column, input)

    def insertAntennaToDb(self):
        table = 'Antenna'
        column = 'name, measuringObjectId'
        input = self.antenna.name + "', '" + self.measuringObject.id
        dbContext.insertData(table, column, input)

    def insertMeasurementToDb(self):
        table = 'Measurement'
        column = 'time, frequency, longitude, latitude, altitude, info, antennaId'
        input = str(self.measurement.time) + "', '" + str(self.measurement.frequency) + "', '" + str(self.measurement.longitude) + "', '" + \
            str(self.measurement.latitude) + "', '" + str(self.measurement.altitude) + \
            "', '" + self.measurement.info + "', '" + str(self.antenna.id)
        dbContext.insertData(table, column, input)
        id = self.getLatestId()
        self.insertMeasurementDataToDb(id)

    def insertMeasurementDataToDb(self, fk):
        length = len(self.measurementData.longitude)
        count = 0
        table = 'MeasurementData'
        column = 'time, longitude, latitude, altitude, dbValue, measurementId'
        while count < length:
            input = str(self.measurementData.time[count]) + "', '" + str(self.measurementData.longitude[count]) + "', '" + str(
                self.measurementData.latitude[count]) + "', '" + str(self.measurementData.altitude[count]) + "', '" + str(self.measurementData.dbValue[count]) + "', '" + str(fk)
            dbContext.insertData(table, column, input)
            count = count + 1

    def getLatestId(self):
        id = dbContext.getLatestId('Measurement')
        return id

    def checkOrganisation(self, name):
        if name == "":
            name = "Oidentifierad"
        exists = dbContext.checkIfOrganisationExists('Organisation', name)
        id = exists[0]
        name = exists[1]
        self.organisation.id = id
        self.organisation.name = name

    def checkMeasuringObject(self, name):
        if name == "":
            name = "Oidentifierad"
        exists = dbContext.checkIfMeasuringObjectExists(
            'MeasuringObject', name, self.organisation.id)
        id = exists[0]
        name = exists[1]
        fk = exists[2]
        self.measuringObject.id = id
        self.measuringObject.name = name
        self.measuringObject.organisationId = fk

    def checkAntenna(self, name):
        if name == "":
            name = "Oidentifierad"
        exists = dbContext.checkIfAntennaExists(
            'Antenna', name, self.measuringObject.id)
        id = exists[0]
        name = exists[1]
        fk = exists[2]
        self.antenna.id = id
        self.antenna.name = name
        self.antenna.measuringObjectId = fk

    def getAllOrganisation(self):
        listOfNames = []
        names = dbContext.getAllName("Organisation")
        for name in names:
            listOfNames.append(str(name[1]))
        return listOfNames

    def getAllMeasuringObject(self, orgName):
        listOfNames = []
        if orgName == "":
            names = dbContext.getAllName("MeasuringObject")
            for name in names:
                listOfNames.append(str(name[1]))
            return listOfNames
        else:
            org = dbContext.getAllWhereNameIs('Organisation', orgName)
            names = dbContext.getAllName("MeasuringObject")
            if not org:
                listOfNames.append("")
            else:
                for name in names:
                    if name[2]==org[0]:
                        listOfNames.append(str(name[1]))              
            return listOfNames

    def getAllAntenna(self, objectName, OrgName):
        listOfNames = []
        if objectName == "":
            names = dbContext.getAllName("Antenna")
            for name in names:
                listOfNames.append(str(name[1]))
            return listOfNames
        else:
            obj = dbContext.getAllWhereNameIs2('MeasuringObject', objectName, OrgName)
            print(obj)
            names = dbContext.getAllName("Antenna")
            if not obj:
                listOfNames.append("")
            else:
                for name in names:
                    if name[2]==obj[0]:
                        listOfNames.append(str(name[1]))              
            return listOfNames

    def getAllMeasurement(self, antennaName, objectName, OrgName):
        listOfNames = []
        if antennaName == "":
            names = dbContext.getAllName("Measurement")
            for name in names:
                listOfNames.append(str(name[1]))
            return listOfNames
        else:
            ant = dbContext.getAllWhereNameIs3('Antenna', antennaName, objectName, OrgName)
            names = dbContext.getAllName("Measurement")
            if not ant:
                listOfNames.append("")
            else:
                for name in names:
                    if name[7]==ant[0]:
                        listOfNames.append(str(name[1]))              
            return listOfNames

    def setAllData(self, orgName, objectName, antennaName, measurementTime):
        orgs = dbContext.getAllName("Organisation")
        objects = dbContext.getAllName("MeasuringObject")
        antennas = dbContext.getAllName("Antenna")
        measurements = dbContext.getAllName("Measurement")
        measurementData = dbContext.getAllName("MeasurementData")
        for org in orgs:
            if org[1] == orgName:
                self.organisation.id = org[0]
                self.organisation.name = org[1]
        for obje in objects:
            if obje[1] == objectName and obje[2] == self.organisation.id:
                self.measuringObject.id = obje[0]
                self.measuringObject.name = obje[1]
                self.measuringObject.organisationId = obje[2]
        for antenna in antennas:
            if antenna[1] == antennaName and antenna[2] == self.measuringObject.id:
                self.antenna.id = antenna[0]
                self.antenna.name = antenna[1]
                self.antenna.measuringObjectId = antenna[2]
        for measurement in measurements:
            if measurement[1] == measurementTime and measurement[7] == self.antenna.id:
                self.measurement.id = measurement[0]
                self.measurement.time = measurement[1]
                self.measurement.frequency = measurement[2]
                self.measurement.longitude = measurement[3]
                self.measurement.latitude = measurement[4]
                self.measurement.altitude = measurement[5]
                self.measurement.info = measurement[6]
                self.measurement.antennaId = measurement[7]
        for line in measurementData:
            if line[6] == self.measurement.id:
                self.measurementData.time.append(line[1])
                self.measurementData.longitude.append(line[2])
                self.measurementData.latitude.append(line[3])
                self.measurementData.altitude.append(line[4])
                self.measurementData.dbValue.append(line[5])
                self.measurementData.measurementId = line[6]

    def newMeasurement(self, lon, lat, alt, antennaid):
        _lon = lon
        _lat = lat
        _alt = alt
        _antennaid = antennaid
        del self.measurementData
        del self.measurement
        del self.pyro
        self.measurementData = MeasurementData()
        self.measurement = Measurements()
        self.measurement.longitude = _lon
        self.measurement.latitude = _lat
        self.measurement.altitude = _alt
        self.measurement.antennaId = _antennaid
        self.pyro = StartAndStop()
