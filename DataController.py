from Organisations import *
from MeasuringObjects import *
from Antennas import *
from Measurements import *
from MeasurementData import *
from pyro import *
from Calculate import *
import DbController as dbContext


class DataController:

    def __init__(self):
        """
        Class with the purpose of processing data. 
        Contains a instance of each database class and a Pyro.
        """
        self.organisation = Organisations()
        self.measuringObject = MeasuringObjects()
        self.antenna = Antennas()
        self.measurement = Measurements()
        self.measurementData = MeasurementData()
        self.pyro = object

    def getFixStatus(self):
        """
        Ask the instantiated pyro for the fix status.
        Returns fix status as a string.
        """
        self.pyro = StartAndStop()
        fixStatus = self.pyro.getFixStatus()
        del self.pyro
        return fixStatus

    def setStartPosition(self):
        """
        Ask the instantiated pyro for the start position of the antenna under test and sets the longitude, latitude and altitude of the instantiated measurement.
        """
        self.pyro = StartAndStop()
        startPosition = self.pyro.getStartPosition()
        lon = startPosition[0]
        lat = startPosition[1]
        alt = startPosition[2]
        self.measurement.longitude = float(lon)
        self.measurement.latitude = float(lat)
        self.measurement.altitude = float(alt)
        del self.pyro

    def startMeasurment(self, freq):
        """
        Take a frequency as a parameter.
        Sets the frequency of the instantiated measurement to the given frequency and asks the instantiated pyro to start a measurement with the given frequency.
        """
        self.pyro = StartAndStop()
        self.measurement.frequency = freq
        self.pyro.start(freq)

    def stopMeasurement(self):
        """
        Asks the instantiated pyro to stop the measurement.
        Then asks the instantiated pyro for the showList and take the last stored line. 
        Then picks out the data and append it to the instantiated measurementDatas lists.
        """
        self.pyro.stop()
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
        del self.pyro

    def setShowList(self):
        """
        Asks the instantiated pyro for the showList and take the last stored line. 
        Then picks out the data and append it to the instantiated measurementDatas lists.
        """
        try:
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
        except:
            pass

    def insertMeasurementToDb(self):
        """
        Asks the DbController to insert the instantiated measurements data into the database table called Measurement adding the instantiated antennas id as foreign key.
        Will then ask the DbController to return the last inputed id in database table Measurement which will be the id of the recently inputed measurement.
        At last it will call the method insertMeasurementData() in the same DataController sending the id as a foreign key.
        """
        table = 'Measurement'
        column = 'time, frequency, longitude, latitude, altitude, info, antennaId'
        input = str(self.measurement.time) + "', '" + str(self.measurement.frequency) + "', '" + str(self.measurement.longitude) + "', '" + \
            str(self.measurement.latitude) + "', '" + str(self.measurement.altitude) + \
            "', '" + self.measurement.info + "', '" + str(self.antenna.id)
        dbContext.insertData(table, column, input)
        id = self.getLatestId()
        self.insertMeasurementDataToDb(id)

    def insertMeasurementDataToDb(self, fk):
        """
        Takes a foreign key to a measurement as a parameter.
        Then takes the amount of measurement data stored in the instantiated measurementData. 
        For each line in the instantiated measurementData lists the DbController is asked to insert the data stored in each list at a given index and connect it to a specific measurement by the given foreign key in the database table called MeasurementData. 
        After this the counter will increase by 1 and therefore pick the line in each list and stop doing so when there is no lines left.
        """
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
        """
        Ask the DbController for the latest Id in database table Measurement and returns it.
        """
        id = dbContext.getLatestId('Measurement')
        return id

    def checkOrganisation(self, name):
        """
        Takes a name of a organization as a parameter. If the parameter is a empty string the name will be set to "oidentifierad".
        Then asks the DbController to to check if name exists in the Database (if it's not in the databse it will be added by the DbController)
        Takes the returned organization and set its values into the instantiated organisation.
        """
        if name == "":
            name = "Oidentifierad"
        exists = dbContext.checkIfOrganisationExists('Organisation', name)
        id = exists[0]
        name = exists[1]
        self.organisation.id = id
        self.organisation.name = name

    def checkMeasuringObject(self, name):
        """
        Takes a name of a measuring object as a parameter. If the parameter is a empty string the name will be set to "oidentifierad".
        Then asks the DbController to to check if name exists in the Database (if it's not in the databse it will be added by the DbController)
        Takes the returned measuring object and set its values into the instantiated measuringObject.
        """
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
        """
        Takes a name of a antenna as a parameter. If the parameter is a empty string the name will be set to "oidentifierad".
        Then asks the DbController to to check if name exists in the Database (if it's not in the databse it will be added by the DbController)
        Takes the returned antenna and set its values into the instantiated antenna.
        """
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
        """
        Asks DbController for a list containing all organizations.
        Returns that list.
        """
        listOfNames = []
        names = dbContext.getAllName("Organisation")
        for name in names:
            listOfNames.append(str(name[1]))
        return listOfNames

    def getAllMeasuringObject(self, orgName):
        """
        Takes a organization name as a parameter.
        Asks DbController for a list containing all measuring objects connected to the given organization.
        Returns that list.
        """
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
                    if name[2] == org[0]:
                        listOfNames.append(str(name[1]))
            return listOfNames

    def getAllAntenna(self, objectName, OrgName):
        """
        Takes a organization name and measuring object name as a parameters.
        Asks DbController for a list containing all antennas connected to the given measuring objects, which need to be connected to the given organization.
        Returns that list.
        """
        listOfNames = []
        if objectName == "":
            names = dbContext.getAllName("Antenna")
            for name in names:
                listOfNames.append(str(name[1]))
            return listOfNames
        else:
            obj = dbContext.getAllWhereNameIs2(
                'MeasuringObject', objectName, OrgName)
            names = dbContext.getAllName("Antenna")
            if not obj:
                listOfNames.append("")
            else:
                for name in names:
                    if name[2] == obj[0]:
                        listOfNames.append(str(name[1]))
            return listOfNames

    def getAllMeasurement(self, antennaName, objectName, OrgName):
        """
        Takes a organization name, a measuring object name and a antenna name as a parameters.
        Asks DbController for a list containing all measurements connected to the given antenna, which need to be connected to the given measuring objects, which need to be connected to the given organization.
        Returns that list.
        """
        listOfNames = []
        if antennaName == "":
            names = dbContext.getAllName("Measurement")
            for name in names:
                listOfNames.append(str(name[1]))
            return listOfNames
        else:
            ant = dbContext.getAllWhereNameIs3(
                'Antenna', antennaName, objectName, OrgName)
            names = dbContext.getAllName("Measurement")
            if not ant:
                listOfNames.append("")
            else:
                for name in names:
                    if name[7] == ant[0]:
                        listOfNames.append(str(name[1]))
            return listOfNames

    def setAllData(self, orgName, objectName, antennaName, measurementTime):
        """
        Takes a organization name, a measuring object name, a antenna name and a measurement time as a parameters.
        Asks DbController for a list containing all measurement data connected to the given measurement, which need to be connected to the given antenna, which need to be connected to the given measuring objects, which need to be connected to the given organization.
        Returns that list.
        """
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
        del self.measurementData
        self.measurementData = MeasurementData()
        for line in measurementData:
            if line[6] == self.measurement.id:
                self.measurementData.time.append(line[1])
                self.measurementData.longitude.append(line[2])
                self.measurementData.latitude.append(line[3])
                self.measurementData.altitude.append(line[4])
                self.measurementData.dbValue.append(line[5])
                self.measurementData.measurementId = line[6]

    def newMeasurement(self, lon, lat, alt, antennaid):
        """
        Takes antenna under tests longitude, latitude, altitude and antennaId as parameters.
        Deletes the instantiated measurementData, measurement and pyro. 
        Instantiate new measurementData, measurement and pyro and sets the given values to the instantiated measurement.
        """
        _lon = lon
        _lat = lat
        _alt = alt
        _antennaid = antennaid
        del self.measurementData
        del self.measurement
        self.measurementData = MeasurementData()
        self.measurement = Measurements()
        self.measurement.longitude = _lon
        self.measurement.latitude = _lat
        self.measurement.altitude = _alt
        self.measurement.antennaId = _antennaid

    def getDistanceFromAUT(self):
        """
        Asks the instantiated pyro for the current position of the PMU.
        Instantiate a new Calculator with the longitude and latitude of the antenna under test as parameter (and the list of dbValues from the instantiated measurementData even though its not used).
        The asks the calculator for the distance between antenna under test and the PMU.
        Returns the distance in meters.
        """
        self.pyro = StartAndStop()
        position = self.pyro.getStartPosition()
        cal = Calculator(self.measurement.longitude,
                         self.measurement.latitude, self.measurementData.dbValue)
        distance = cal.getDistance(
            position[0], position[1], self.measurement.longitude, self.measurement.latitude)
        del self.pyro
        return distance
