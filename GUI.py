import time
from tkinter import *

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits import mplot3d
from plotly.graph_objects import scatter3d

from Measurements import *
from pyro import *
from ShellCommands import *

global on
global a
global x
global y
global z
global lon
global lat
global alt
global m
global my_cmap
global sas
global scttLive
global canvasLive

on = False
a = []
x = []
y = []
z = []
lon = []
lat = []
alt = []
m = []
sas = object
scttLive = object
canvasLive = object
my_cmap = plt.get_cmap('rainbow')
pmuSc = ShellCommands("172.16.0.3")
rbuSc = ShellCommands("172.16.0.6")
ptuSc = ShellCommands("172.16.0.9")


def clickStartBtn():
    """
    Comment
    """
    global on
    global a
    global sas

    frequency = fqEnt.get()
    updateFixStatus()

    if frequency == "":
        tbOthers.insert(1.0, 'Enter a frequency \n')
        tbOthers.update()
    else:
        if not on:
            startBtn.config(text="Stoppa mätning")
            clearPlotLists()
            on = True
            sas = StartAndStop()
            sas.start(frequency)
            time.sleep(5)

            while on:
                showList = sas.showList
                obj = showList[-1]
                tbMeasure.insert(1.0, str(obj) + '\n')
                tbMeasure.update()
                updatePlotList(obj)
                livePlot()
                time.sleep(0.5)
            # ptuSc.setFrequency(frequency)
        else:
            startBtn.config(text="Starta mätning")
            on = False
            sas.stop()
            clearPlotLists()
            a = sas.mesurementList  # change to createDummy() to run txt-file
            print("list done!")
            for line in a:
                updatePlotList(line)
                tbMeasure.insert(1.0, str(line) + '\n')
                tbMeasure.update
            del sas


def clickPmuBtn():
    """
    Comment
    """
    # updateFixStatus()

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
    global lon
    global lat
    global alt
    sas = StartAndStop()
    startPosition = sas.getStartPosition()
    updateFixStatus()
    lon = []
    lat = []
    alt = []
    lo = startPosition[0]
    la = startPosition[1]
    al = startPosition[2]
    lon.append(float(lo))
    lat.append(float(la))
    alt.append(float(al))
    posLonLbl.config(text=str(lon))
    posLatLbl.config(text=str(lat))
    posAltLbl.config(text=str(alt))
    tbOthers.insert(1.0, 'AUT position is: \n' +
                    'Longitude:\n' + str(lon) + '\nLatitude:\n' + str(lat) + '\nAltitude:\n' + str(alt) + '\n')
    tbOthers.update()
    del sas


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
    updateFixStatus()


def clickGrafBtn():
    """
    Comment
    """
    updateFixStatus()
    fig = plt.figure(figsize=(10, 7))
    ax1 = fig.add_subplot(111)
    ax1.scatter(lon, lat, alpha=1, c="black", marker='X', label='AUT')
    sctt = ax1.scatter(x, y, alpha=1, c=m, cmap=my_cmap, marker='o')
    fig.colorbar(sctt, shrink=0.8, aspect=5)
    fig.legend()
    fig.show()


def clickGraf3dBtn():
    """
    Comment
    """
    updateFixStatus()
    fig = plt.figure(figsize=(15, 11))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(lon, lat, alt, alpha=1, c="black", marker='X', label='AUT')
    sctt = ax.scatter(x, y, z, alpha=1, c=m, cmap=my_cmap, marker='p')
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
    ax1 = figLive.add_subplot(111)
    ax1.scatter(lat, lon, alpha=1, c="black", marker='X')
    scttLive = ax1.scatter(x, y, alpha=1, c=m, cmap=my_cmap, marker='o')
    figLive.colorbar(scttLive, shrink=0.8, aspect=5)
    canvasLive = FigureCanvasTkAgg(figLive, master=win)
    canvasLive.get_tk_widget().grid(row=0, column=15)


def livePlot():
    """
    Comment
    """
    global scttLive
    global canvasLive
    plt.scatter(lon, lat, alpha=1, c="black", marker='X', label='AUT')
    scttLive = plt.scatter(x, y, alpha=1, c=m, cmap=my_cmap, marker='o')
    canvasLive.draw_idle()


def clearPlotLists():
    """
    Comment
    """
    global x
    global y
    global z
    global m
    x[:] = []
    y[:] = []
    z[:] = []
    m[:] = []


def updatePlotList(line):
    """
    Comment
    """
    lo = line[1]
    la = line[2]
    al = line[3]
    me = line[4]
    x.append(float(lo))
    y.append(float(la))
    z.append(float(al))
    m.append(float(me))


def updateFixStatus():
    sas2 = StartAndStop()
    status = sas2.getFixStatus()
    fixStatusLbl.config(text="Fix status: " + status)
    print(status)


bgColor = 'black'
frameColor = '#222222'
textColor = '#cdcdcd'

win = Tk()
win.title("CU-applikation för PAMP")
win.geometry('1448x800')
win.configure(bg=bgColor)

tbMeasure = Text(bg=frameColor, fg=textColor, width=87)

tbOthers = Text(bg=frameColor, fg=textColor, width=48)

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
graf3dBtn = Button(text="Visa 3D Graf", width=20, height=2,
                   bg=frameColor, fg=bgColor, command=clickGraf3dBtn)

posLonLbl = Label(text="", bg=frameColor, fg=textColor)
posLatLbl = Label(text="", bg=frameColor, fg=textColor)
posAltLbl = Label(text="", bg=frameColor, fg=textColor)

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

fixStatusLbl.grid(row=1, column=3, columnspan=4)

grafBtn.grid(row=3, column=4)
graf3dBtn.grid(row=3, column=5)

# updateFixStatus()
createLiveFig()
win.mainloop()
