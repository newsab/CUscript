import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits import mplot3d
from plotly.graph_objects import scatter3d
from Calculate import *

class Plotter:

    def __init__(self, dataController):
        """
        Class with the purpose of creating plotter for the GUI and FileWriter grafs.
        Takes a dataController as a parameter. 
        """
        self.DC = dataController
        self.twoDPlot = plt.figure(figsize=(10, 7))
        self.threeDPlot = plt.figure(figsize=(10, 7))
        self.grafPlot = plt
        self.my_cmap = plt.get_cmap('rainbow')

    def setTwoDPlot(self):
        """
        Sets the instance variable twoDPlot to a new 2D figure and gets the position of the antenna under test and mark it as a black cross in the figure.
        Gets the measurement data from the given dataController and places every measuring point och the figure as a dot and colorize it after dbValue.
        """
        self.twoDPlot = plt.figure(figsize=(10, 7))
        ax = self.twoDPlot.add_subplot(111)
        autlon = self.DC.measurement.longitude
        autlat = self.DC.measurement.latitude
        x = self.DC.measurementData.longitude
        y = self.DC.measurementData.latitude
        m = self.DC.measurementData.dbValue
        ax.scatter(autlon, autlat, alpha=1, c="black", marker='X', label='AUT')
        sctt = ax.scatter(x, y, alpha=1, c=m, cmap=self.my_cmap, marker='o')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        self.twoDPlot.colorbar(sctt, shrink=0.8, aspect=5)
        self.twoDPlot.legend()

    def setThreeDPlot(self):
        """
        Sets the instance variable threeDPlot to a new 3D figure and gets the position of the antenna under test and mark it as a black cross in the figure.
        Gets the measurement data from the given dataController and places every measuring point och the figure as a dot and colorize it after dbValue.
        """
        self.threeDPlot = plt.figure(figsize=(10, 7))
        ax = self.threeDPlot.add_subplot(111, projection="3d")
        autlon = self.DC.measurement.longitude
        autlat = self.DC.measurement.latitude
        autalt = self.DC.measurement.altitude
        x = self.DC.measurementData.longitude
        y = self.DC.measurementData.latitude
        z = self.DC.measurementData.altitude
        m = self.DC.measurementData.dbValue
        ax.scatter(autlon, autlat, autalt, alpha=1, c="black", marker='X', label='AUT')
        sctt = ax.scatter(x, y, z, alpha=1, c=m, cmap=self.my_cmap, marker='p')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_xlabel('Longitude', fontweight='bold')
        ax.set_ylabel('Latitude', fontweight='bold')
        ax.set_zlabel('Altitude', fontweight='bold')
        self.threeDPlot.colorbar(sctt, ax=ax, shrink=0.8, aspect=5)
        self.threeDPlot.legend()
    
    def setGrafPlot(self):
        """
        Sets the instance variable grafPlot to a new 2D figure and draws a line where the X-axis show the degree between -180 and 180 and the Y-axis show the dbValue.
        Gets the measurement data from the given dataController.
        """

        self.grafPlot = plt.figure(figsize=(10, 7))
        ax = self.grafPlot.add_subplot(111)
        autlon = self.DC.measurement.longitude
        autlat = self.DC.measurement.latitude
        dbValues = self.DC.measurementData 
        cal = Calculator(autlon, autlat, dbValues)
        cal.fillLists()
        ang = cal.angleList
        db = cal.dbList
        ax.plot(ang, db)
        self.grafPlot.legend()