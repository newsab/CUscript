from math import acos, degrees, sin, cos, sqrt, atan2, radians 
from pyro import *

class Calculator:
    	
        def __init__(self, autLon, autLat):
                self.lon1 = autLon
                self.lat1 = autLat
                self.lon2 = 0.0
                self.lat2 = 0.0
                self.lon3 = 0.0
                self.lat3 = 0.0
                self.degree = 0.0
                sas = StartAndStop()
                sas.setDummyData()
                self.listToCheck = sas.mesurementList
                self.angleList = []
                self.dbList = []

        def fillLists(self):
                for line in self.listToCheck:
                        if(self.lon2 == 0.0):
                                print(line)
                                self.lon2 = line[1]
                                self.lat2 = line[2]
                                dbValue = line[4]
                                self.angleList.append(0.0)
                                self.dbList.append(dbValue)
                        else: 
                                self.lon3 = line[1]
                                self.lat3 = line[2]
                                angle = self.degree + self.getAngle()
                                self.degree = angle
                                dbValue = line[4]
                                print(str(self.lon1) + ", " + str(self.lat1) + ", " + str(self.lon2) + ", " + str(self.lat2) + ", " + str(self.lon3) + ", " + str(self.lat3) + ", " + str(angle) + ", " + str(dbValue))
                                self.angleList.append(angle)
                                self.dbList.append(dbValue)
                                self.lon2 = self.lon3
                                self.lat2 = self.lat3
                                

        def getAngle(self):
                A = self.getDistance(self.lon1, self.lat1, self.lon2, self.lat2)
                B = self.getDistance(self.lon1, self.lat1, self.lon3, self.lat3)
                C = self.getDistance(self.lon2, self.lat2, self.lon3, self.lat3)
                degree = degrees(acos((A * A + B * B - C * C)/(2.0 * A * B)))

                return degree

        def getDistance(self, lon1, lat1, lon2, lat2):
                # approximate radius of earth in km
                R = 6373.0

                lat1r = radians(float(lat1))
                lon1r = radians(float(lon1))
                lat2r= radians(float(lat2))
                lon2r = radians(float(lon2))

                dlon = lon2r - lon1r
                dlat = lat2r - lat1r

                a = sin(dlat / 2)**2 + cos(lat1r) * cos(lat2r) * sin(dlon / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))

                distance = (R * c)*100

                print("Result:", distance, " m")
                
                return distance