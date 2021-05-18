from math import acos, degrees, sin, cos, sqrt, atan2, radians 
from pyro import *

class Calculator:
    	
        def __init__(self, autLon, autLat, measurementData):
                """
                Class with the purpose of calculate the angle between measuring points.
                Takes the longitude and latitude of the antenna under test and a measurementData object as parameters.
                Stores the antenna under tests position in lon1 and lat1, the previous measuring point in lon2 and lat2 and the latest measuring point in lon3 and lat3.
                """
                self.lon1 = autLon
                self.lat1 = autLat
                self.lon2 = 0.0
                self.lat2 = 0.0
                self.lon3 = 0.0
                self.lat3 = 0.0
                self.degree = -180.0
                self.measurementObject = measurementData
                self.angleList = []
                self.dbList = []

        def fillLists(self):
                """
                Count the amount of measurement points in the measurement and for each point the angle from previous point is calculated by the getAngle() method starting at an angle of -180.
                If it is the first measuring point no calculation is done and the point is set to the first one at an starting angle at -180 degree. 
                If the angle is going above 180 degree and a whole circle is done the calculation will stop.
                Every calculated angle is stored in the angleList and the DB value is stored in the dbList. 
                Values associated with each other are stored at the same index.
                """        
                length = len(self.measurementObject.longitude)
                count = 0          
                while count < length:
                        if(self.lon2 == 0.0):
                                self.lon2 = self.measurementObject.longitude[count]
                                self.lat2 = self.measurementObject.latitude[count]
                                dbValue = self.measurementObject.dbValue[count]
                                self.angleList.append(-180.0)
                                self.dbList.append(float(dbValue))
                        elif(self.degree > 180.0):
                                break
                        else: 
                                self.lon3 = self.measurementObject.longitude[count]
                                self.lat3 = self.measurementObject.latitude[count]
                                angle = self.degree + self.getAngle()
                                self.degree = angle
                                dbValue = self.measurementObject.dbValue[count]
                                self.angleList.append(angle)
                                self.dbList.append(float(dbValue))
                                self.lon2 = self.lon3
                                self.lat2 = self.lat3
                        count = count + 1

        def getAngle(self):
                """
                Calculates the angle between two point by creating a triangle. 
                Triangle is made by using the getDistance() method to get the length of the three sides.
                Parameters to send in to the getDistance() method is taken from the instance variables.
                """
                A = self.getDistance(self.lon1, self.lat1, self.lon2, self.lat2)
                B = self.getDistance(self.lon1, self.lat1, self.lon3, self.lat3)
                C = self.getDistance(self.lon2, self.lat2, self.lon3, self.lat3)
                degree = degrees(acos((A * A + B * B - C * C)/(2.0 * A * B)))

                return degree

        def getDistance(self, lon1, lat1, lon2, lat2):
                """
                Takes the longitude and latitude from two coordinates and calculates the distance between them. 
                Returns the distance in meters.
                """   
                R = 6373.0 # approximate radius of earth in km                          
                lat1r = radians(float(lat1))
                lon1r = radians(float(lon1))
                lat2r= radians(float(lat2))
                lon2r = radians(float(lon2))
                dlon = lon2r - lon1r
                dlat = lat2r - lat1r
                a = sin(dlat / 2)**2 + cos(lat1r) * cos(lat2r) * sin(dlon / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance = (R * c)*1000
                
                return distance