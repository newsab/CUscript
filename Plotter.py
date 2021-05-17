import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits import mplot3d
from plotly.graph_objects import scatter3d
from Calculate import *

class Plotter:

    def __init__(self, dataController):
        """
        Comment
        """
        self.DC = dataController
        self.twoDPlot = plt.figure(figsize=(10, 7))
        self.threeDPlot = plt.figure(figsize=(10, 7))
        self.grafPlot = plt
        self.my_cmap = plt.get_cmap('rainbow')

    def setTwoDPlot(self):
        """
        Comment
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
        Comment
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
        Comment
        """
        self.grafPlot = plt
        autlon = self.DC.measurement.longitude
        autlat = self.DC.measurement.latitude
        dbValues = self.DC.measurementData 
        cal = Calculator(autlon, autlat, dbValues)
        cal.fillLists()
        ang = cal.angleList
        db = cal.dbList
        self.grafPlot.plot(ang, db)
        self.grafPlot.ylim(-100, 10)
        self.grafPlot.xlim(-180, 180)
        self.grafPlot.grid(True)