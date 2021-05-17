import os
import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF
import sys

from DataController import *
from Plotter import *


class FileWriter:

    def __init__(self, dataController, path):
        self.DC = dataController
        self.name = self.DC.organisation.name + "_" + self.DC.measuringObject.name + "_" + self.DC.antenna.name + "_" + str(self.DC.measurement.frequency)
        self.fileName = self.name + ".txt"
        self.path = path + "/"
        self.tempPath = sys.path[0] + "/Measurements/"
        self.fullPath = os.path.join(self.path, self.fileName)

        
    def createTxtFile(self):
        f = open(self.fullPath, "wt")
        f.write("Drönarmätning utförd " + str(self.DC.measurement.time) + '\n')
        f.write("Företag: " + self.DC.organisation.name + "\n")
        f.write("Mätobjekt: " + self.DC.measuringObject.name + "\n")
        f.write("Antenn: " + self.DC.antenna.name + "\n")
        f.write("Placering: lon:" + str(self.DC.measurement.longitude) + " lat:" + str(self.DC.measurement.latitude) + " alt:" + str(self.DC.measurement.altitude) + "\n")
        f.write("Frekvens: " + str(self.DC.measurement.frequency) + "\n")
        f.write("Info: " + self.DC.measurement.info + "\n \n")
        f.close()
        count = 0
        length = len(self.DC.measurementData.longitude)
        while count < length:
            f = open(self.fullPath, "at")
            f.write(str(self.DC.measurementData.time[count]) + ", " + str(self.DC.measurementData.longitude[count]) + ", " + str(self.DC.measurementData.latitude[count]) + ", " + str(self.DC.measurementData.altitude[count]) + ", " + str(self.DC.measurementData.dbValue[count]) + "\n")
            f.close()
            count = count + 1

    def createPdfFile(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.image(self.tempPath + "logo.png", w=70, h=35,)
        pdf.set_font("Arial", size = 15)
        pdf.cell(200, 20, txt = "", ln = 1)
        pdf.cell(200, 8, txt = "Drönarmätning utförd " + str(self.DC.measurement.time), ln = 1)
        pdf.cell(200, 8, txt = "Företag: " + self.DC.organisation.name, ln = 1)
        pdf.cell(200, 8, txt = "Mätobjekt: " + self.DC.measuringObject.name, ln = 1)
        pdf.cell(200, 8, txt = "Antenn: " + self.DC.antenna.name, ln = 1)
        pdf.cell(200, 8, txt = "Placering: lon:" + str(self.DC.measurement.longitude) + " lat:" + str(self.DC.measurement.latitude) + " alt:" + str(self.DC.measurement.altitude), ln = 1)
        pdf.cell(200, 8, txt = "Frekvens: " + str(self.DC.measurement.frequency), ln = 1)
        pdf.multi_cell(190, 8, txt = "Info: " + self.DC.measurement.info)
        
        plotter = Plotter(self.DC)
        plotter.setGrafPlot()    
        plot3 = plotter.grafPlot
        plt.savefig(self.tempPath + self.name + "GrafPlot.png")
        pdf.image(self.tempPath + self.name + "GrafPlot.png", w=190, h=133)

        plotter.setTwoDPlot()    
        plot1 = plotter.twoDPlot
        plt.savefig(self.tempPath + self.name + "2dPlot.png")
        pdf.image(self.tempPath + self.name + "2dPlot.png", w=190, h=133)

        plotter.setThreeDPlot()    
        plot2 = plotter.threeDPlot
        plt.savefig(self.tempPath + self.name + "3dPlot.png")
        pdf.image(self.tempPath + self.name + "3dPlot.png", w=190, h=133)

        os.remove(self.tempPath + self.name + "GrafPlot.png")
        os.remove(self.tempPath + self.name + "2dPlot.png")
        os.remove(self.tempPath + self.name + "3dPlot.png")

        count = 0
        length = len(self.DC.measurementData.longitude)
        pdf.set_font("Arial", size = 10)

        while count < length:
            pdf.cell(200, 5, txt = str(self.DC.measurementData.time[count]) + ", " + str(self.DC.measurementData.longitude[count]) + ", " + str(self.DC.measurementData.latitude[count]) + ", " + str(self.DC.measurementData.altitude[count]) + ", " + str(self.DC.measurementData.dbValue[count]),ln = 1)
            count = count + 1

        pdf.output(self.path + self.name + ".pdf")  
    