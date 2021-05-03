import time
from tkinter import *

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits import mplot3d
from plotly.graph_objects import scatter3d

from DataController import *
from ShellCommands import *
from Calculate import *

global DC
global on
global my_cmap
global scttLive
global canvasLive

DC = DataController()
on = False
scttLive = object
canvasLive = object
my_cmap = plt.get_cmap('rainbow')
pmuSc = ShellCommands("192.168.1.3")
rbuSc = ShellCommands("192.168.1.6")
ptuSc = ShellCommands("172.16.0.9")

def clickStartBtn():
    """
    Comment
    """
    global on
    frequency = fqEnt.get()
    updateFixStatus()
    if frequency == "":
        tbOthers.insert(1.0, 'Enter a frequency \n')
        tbOthers.update()
    else:
        if not on:
            startBtn.config(text="Stoppa mätning")
            on = True
            DC.startMeasurment(frequency)
            # ptuSc.setFrequency(frequency)
            time.sleep(5)
            while on:
                DC.setShowList()
                tim = str(DC.measurementData.time[-1])
                alt = str(DC.measurementData.altitude[-1])
                db = str(DC.measurementData.dbValue[-1])
                tbMeasure.insert(1.0, tim + ", " + alt + ", " + db + '\n')
                tbMeasure.update()
                livePlot()
                time.sleep(0.5)
        else:
            startBtn.config(text="Starta mätning")
            on = False
            DC.stopMeasurement()
            DC.setMeasurementData()
            print("list done!")
            length = len(DC.measurementData.longitude)
            count = 0           
            while count < length:
                tim = str(DC.measurementData.time[count])
                alt = str(DC.measurementData.altitude[count])
                db = str(DC.measurementData.dbValue[count])
                count = count + 1
                tbMeasure.insert(1.0, tim + ", " + alt + ", " + db + '\n')
                tbMeasure.update

def clickPmuBtn():
    """
    Comment
    """
    msg3 = pmuSc.startPMUapp()
    tbOthers.insert(1.0, msg3 + '\n \n')
    tbOthers.update()
    time.sleep(0.5)
    tbOthers.insert(1.0, 'PMU Ready for take off! \n \n')
    tbOthers.update()

def clickPosBtn():
    """
    Comment
    """
    updateFixStatus()
    DC.setStartPosition()
    lon = DC.measurement.longitude
    lat = DC.measurement.latitude
    alt = DC.measurement.altitude
    posLonLbl.config(text=str(lon))
    posLatLbl.config(text=str(lat))
    posAltLbl.config(text=str(alt))
    tbOthers.insert(1.0, 'AUT position is: \n' +
                    'Longitude:\n' + str(lon) + '\nLatitude:\n' + str(lat) + '\nAltitude:\n' + str(alt) + '\n')
    tbOthers.update()

def clickRbuBtn():
    """
    Comment
    """
    msg = rbuSc.coldRestart()
    tbOthers.insert(1.0, msg + '\n \n')
    tbOthers.update()
    time.sleep(2.5)
    tbOthers.insert(1.0, 'RBU Ready DO NOT MOVE!!! \n \n')
    tbOthers.update()

def clickGrafBtn():
    """
    Comment
    """
    plt.close()
    autlon = DC.measurement.longitude
    autlat = DC.measurement.latitude
    cal = Calculator(autlon, autlat, DC.measurementData)
    cal.fillLists()
    ang = cal.angleList
    db = cal.dbList
    fig = plt
    fig.plot(ang, db)
    fig.ylim(-100, 10)
    fig.xlim(-180, 180)
    fig.grid(True)
    fig.show()

def clickGraf2dBtn():
    """
    Comment
    """
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111)
    autlon = DC.measurement.longitude
    autlat = DC.measurement.latitude
    x = DC.measurementData.longitude
    y = DC.measurementData.latitude
    m = DC.measurementData.dbValue
    ax.scatter(autlon, autlat, alpha=1, c="black", marker='X', label='AUT')
    sctt = ax.scatter(x, y, alpha=1, c=m, cmap=my_cmap, marker='o')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    fig.colorbar(sctt, shrink=0.8, aspect=5)
    fig.legend()
    fig.show()

def clickGraf3dBtn():
    """
    Comment
    """
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")
    autlon = DC.measurement.longitude
    autlat = DC.measurement.latitude
    autalt = DC.measurement.altitude
    x = DC.measurementData.longitude
    y = DC.measurementData.latitude
    z = DC.measurementData.altitude
    m = DC.measurementData.dbValue
    ax.scatter(autlon, autlat, autalt, alpha=1, c="black", marker='X', label='AUT')
    sctt = ax.scatter(x, y, z, alpha=1, c=m, cmap=my_cmap, marker='p')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xlabel('Longitude', fontweight='bold')
    ax.set_ylabel('Latitude', fontweight='bold')
    ax.set_zlabel('Altitude', fontweight='bold')
    fig.colorbar(sctt, ax=ax, shrink=0.8, aspect=5)
    fig.legend()
    fig.show()

def createLiveFig():
    """
    Comment
    """
    global scttLive
    global canvasLive
    figLive = plt.figure(figsize=(5, 3))
    ax = figLive.add_subplot(111)
    x = DC.measurementData.longitude
    y = DC.measurementData.latitude
    m = DC.measurementData.dbValue
    scttLive = ax.scatter(x, y, alpha=1, c=m, cmap=my_cmap, marker='o')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    figLive.colorbar(scttLive, shrink=0.8, aspect=5)
    canvasLive = FigureCanvasTkAgg(figLive, master=win)
    canvasLive.get_tk_widget().grid(row=0, column=15, columnspan=2)

def livePlot():
    """
    Comment
    """
    global scttLive 
    global canvasLive
    autlon = DC.measurement.longitude
    autlat = DC.measurement.latitude
    x = DC.measurementData.longitude
    y = DC.measurementData.latitude
    m = DC.measurementData.dbValue
    plt.scatter(autlon, autlat, alpha=1, c="black", marker='X', label='AUT')
    scttLive = plt.scatter(x, y, alpha=1, c=m, cmap=my_cmap, marker='o')
    canvasLive.draw_idle()

def updateFixStatus():
    status = DC.getFixStatus()
    fixStatusLbl.config(text="Fix status: " + status)

bgColor = 'black'
frameColor = '#222222'
textColor = '#cdcdcd'

win = Tk()
win.title("CU-applikation för PAMP")
win.geometry('1360x768')
win.configure(bg=bgColor)

tbMeasure = Text(bg=frameColor, fg=textColor, width=60)

tbOthers = Text(bg=frameColor, fg=textColor, width=60)

startLbl = Label(text="", bg=bgColor, fg=textColor)

startBtn = Button(text="Starta mätning", width=15, height=2,
                  bg=frameColor, fg=bgColor, command=clickStartBtn)

pmuBtn = Button(text="Starta PMU", width=15, height=2,
                bg=frameColor, fg=bgColor, command=clickPmuBtn)

fqEnt = Entry(bg=frameColor, fg=textColor)

rbuBtn = Button(text="Start om RBU", width=15, height=2,
                bg=frameColor, fg=bgColor, command=clickRbuBtn)

grafBtn = Button(text="Visa Graf", width=15, height=2,
                 bg=frameColor, fg=bgColor, command=clickGrafBtn)
graf2dBtn = Button(text="Visa 2D Graf", width=15, height=2,
                 bg=frameColor, fg=bgColor, command=clickGraf2dBtn)
graf3dBtn = Button(text="Visa 3D Graf", width=15, height=2,
                   bg=frameColor, fg=bgColor, command=clickGraf3dBtn)

posLonLbl = Label(text="", bg=frameColor, fg=textColor)
posLatLbl = Label(text="", bg=frameColor, fg=textColor)
posAltLbl = Label(text="", bg=frameColor, fg=textColor)

orgLbl = Label(text="Organisation", bg=frameColor, fg=textColor)
objectLbl = Label(text="Mätobjekt", bg=frameColor, fg=textColor)
antennaLbl = Label(text="Antenn", bg=frameColor, fg=textColor)
infoLbl = Label(text="Info", bg=frameColor, fg=textColor)

orgEnt = Entry(bg=frameColor, fg=textColor)
objectEnt = Entry(bg=frameColor, fg=textColor)
antennaEnt = Entry(bg=frameColor, fg=textColor)
infoEnt = Text(bg=frameColor, fg=textColor, height=10, width=27)

fixStatusLbl = Label(text="", bg=frameColor, fg=textColor)

posBtn = Button(text="Ta ut AUT position", width=15, height=2,
                bg=frameColor, fg=bgColor, command=clickPosBtn)

tbOthers.grid(row=0, column=0, columnspan=3)
tbMeasure.grid(row=0, column=3, columnspan=3)
startLbl.grid(row=1, column=1)

posLonLbl.grid(row=1, column=1)
posLatLbl.grid(row=2, column=1)
posAltLbl.grid(row=3, column=1)
fqEnt.grid(row=4, column=1)

posBtn.grid(row=1, column=2)
pmuBtn.grid(row=2, column=2)
rbuBtn.grid(row=3, column=2)
startBtn.grid(row=4, column=2)

orgLbl.grid(row=1, column=15)
objectLbl.grid(row=2, column=15)
antennaLbl.grid(row=3, column=15)
infoLbl.grid(row=4, column=15)

orgEnt.grid(row=1, column=16)
objectEnt.grid(row=2, column=16)
antennaEnt.grid(row=3, column=16)
infoEnt.grid(row=4, column=16, rowspan=6)

fixStatusLbl.grid(row=1, column=3, columnspan=4)

grafBtn.grid(row=2, column=4)
graf2dBtn.grid(row=3, column=4)
graf3dBtn.grid(row=4, column=4)

# updateFixStatus()
createLiveFig()
win.mainloop()
