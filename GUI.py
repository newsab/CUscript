import time
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits import mplot3d
from plotly.graph_objects import scatter3d

from DataController import *
from ShellCommands import *
from FileWriter import *
from Plotter import *

global DC
global on
global my_cmap
global scttLive
global canvasLive
global organisationList
global measuringObjectList
global antennaList
global measurementList
global DC
global plotter

DC = DataController()
on = False
scttLive = object
canvasLive = object
my_cmap = plt.get_cmap('rainbow')
organisationList = DC.getAllOrganisation()
measuringObjectList = DC.getAllMeasuringObject("")
antennaList = DC.getAllAntenna("")
measurementList = DC.getAllMeasurement("")
pmuSc = ShellCommands("192.168.1.3")
rbuSc = ShellCommands("192.168.1.6")
ptuSc = ShellCommands("172.16.0.9")

def clickStartBtn():
    """
    Comment
    """
    global on
    frequency = fqEnt.get()
    if frequency == "":
        tbOthers.insert(1.0, 'Enter a frequency \n \n')
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
                    'Longitude:\n' + str(lon) + '\nLatitude:\n' + str(lat) + '\nAltitude:\n' + str(alt) + '\n \n')
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
    plotter.setGrafPlot()
    fig = plotter.grafPlot
    fig.show()

def clickGraf2dBtn():
    """
    Comment
    """
    plt.close()
    plotter.setTwoDPlot()
    fig2d = plotter.twoDPlot
    fig2d.show()

def clickGraf3dBtn():
    """
    Comment
    """
    plt.close()
    plotter.setThreeDPlot()
    fig3d = plotter.threeDPlot
    fig3d.show()

def clickNewMeasurementBtn():
    DC.newMeasurement(DC.measurement.longitude, DC.measurement.latitude, DC.measurement.altitude, DC.measurement.antennaId)
    tbOthers.insert(1.0, 'New measurement \n \n')
    tbOthers.update()

def clickSaveMeasurementBtn():
    path = saveFile()
    org = orgEnt.get() 
    obj = objectEnt.get()
    ant = antennaEnt.get()
    inf = infoEnt.get("1.0", END)
    DC.checkOrganisation(org)
    DC.checkMeasuringObject(obj)
    DC.checkAntenna(ant)
    DC.insertMeasurementToDb(inf)
    fileWriter = FileWriter(DC, path)
    fileWriter.createFile()
    tbOthers.insert(1.0, 'Measurement has been saved \n \n')
    tbOthers.update()

def clickOpenOldMeasurementBtn():
    print("hej")
    newWindow = Toplevel(win)
    newWindow.title("Öppna tidigare mätning")
    newWindow.geometry("400x400")
    Label(newWindow, 
          text ="Välj en tidigare mätning").grid(row=1, column=1)
    orgEnt2 = ttk.Combobox(newWindow, values=organisationList)
    orgEnt2.bind('<KeyRelease>', updateOrganisationCombobox)
    orgEnt2.grid(row=2, column=1)
    objectEnt2 = ttk.Combobox(newWindow, values=measuringObjectList)
    objectEnt2.bind('<KeyRelease>', updateMeasuringObjectCombobox)
    objectEnt2.grid(row=3, column=1)
    antennaEnt2 = ttk.Combobox(newWindow, values=antennaList)
    antennaEnt2.bind('<KeyRelease>', updateAntennaCombobox)
    antennaEnt2.grid(row=4, column=1)
    measurementEnt2 = ttk.Combobox(newWindow, values=measurementList)
    measurementEnt2.bind('<KeyRelease>', updateMeasurementCombobox)
    measurementEnt2.grid(row=5, column=1)

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

def updateOrganisationCombobox():
    typed = orgEnt.get()
    if typed == "":
        data = DC.getAllOrganisation()
    else:  
        data = []   
        for item in DC.getAllOrganisation():
            if typed.lower() in item.lower():
                data.append(item)
    updateOrganisationList(data)

def updateOrganisationList(data):
    global organisationList
    organisationList.clear()
    for item in data:
        organisationList.append(item)       
    orgEnt['values'] = organisationList

def updateMeasuringObjectCombobox():
    typed = objectEnt.get()
    if typed == "":
        data = DC.getAllMeasuringObject(orgEnt.get())
    else:  
        data = []   
        for item in DC.getAllMeasuringObject(orgEnt.get()):
            if typed.lower() in item.lower():
                data.append(item)
    updateMeasuringObjectList(data)

def updateMeasuringObjectList(data):
    global measuringObjectList
    measuringObjectList.clear()
    for item in data:
        measuringObjectList.append(item)       
    objectEnt['values'] = measuringObjectList

def updateAntennaCombobox():
    typed = antennaEnt.get()
    if typed == "":
        data = DC.getAllAntenna(objectEnt.get())
    else:  
        data = []   
        for item in DC.getAllAntenna(objectEnt.get()):
            if typed.lower() in item.lower():
                data.append(item)
    updateAntennaList(data)

def updateAntennaList(data):
    global antennaList
    antennaList.clear()
    for item in data:
        antennaList.append(item)       
    antennaEnt['values'] = antennaList

def updateMeasurementCombobox():
    typed = measurementEnt2.get()
    if typed == "":
        data = DC.getAllMeasurement(antennaEnt.get())
    else:  
        data = []   
        for item in DC.getAllMeasurement(antennaEnt.get()):
            if typed.lower() in item.lower():
                data.append(item)
    updateMeasurementList(data)

def updateMeasurementList(data):
    global antennaList
    antennaList.clear()
    for item in data:
        antennaList.append(item)       
    antennaEnt['values'] = antennaList

def updateAllComboboxes(e):
    updateOrganisationCombobox()
    updateMeasuringObjectCombobox()
    updateAntennaCombobox()

def saveFile():
    path = filedialog.askdirectory(initialdir="./Measurements/")
    return(str(path))

bgColor = 'black'
frameColor = '#222222'
textColor = '#cdcdcd'

win = Tk()
win.title("CU-applikation för PAMP")
win.geometry('1360x768')
win.configure(bg=bgColor)

tbMeasure = Text(bg=frameColor, fg=textColor, width=60)
tbOthers = Text(bg=frameColor, fg=textColor, width=60)


posLonLbl = Label(text="", bg=frameColor, fg=textColor)
posLatLbl = Label(text="", bg=frameColor, fg=textColor)
posAltLbl = Label(text="", bg=frameColor, fg=textColor)
fqEnt = Entry(bg=frameColor, fg=textColor)


posBtn = Button(text="Ta ut AUT position", width=15, height=2,
                bg=frameColor, fg=bgColor, command=clickPosBtn)
rbuBtn = Button(text="Start om RBU", width=15, height=2,
                bg=frameColor, fg=bgColor, command=clickRbuBtn)
startBtn = Button(text="Starta mätning", width=15, height=2,
                  bg=frameColor, fg=bgColor, command=clickStartBtn)



saveMeasurementBtn = Button(text="Spara mätning", width=15, height=2,
                   bg=frameColor, fg=bgColor, command=clickSaveMeasurementBtn)
newMeasurementBtn = Button(text="Initsiera ny mätning", width=15, height=2,
                   bg=frameColor, fg=bgColor, command=clickNewMeasurementBtn)
openOldMeasurementBtn = Button(text="Öppna mätning", width=15, height=2,
                bg=frameColor, fg=bgColor, command=clickOpenOldMeasurementBtn)


fixStatusLbl = Label(text="", bg=frameColor, fg=textColor)
grafBtn = Button(text="Visa Graf", width=15, height=2,
                 bg=frameColor, fg=bgColor, command=clickGrafBtn)
graf2dBtn = Button(text="Visa 2D Graf", width=15, height=2,
                 bg=frameColor, fg=bgColor, command=clickGraf2dBtn)
graf3dBtn = Button(text="Visa 3D Graf", width=15, height=2,
                   bg=frameColor, fg=bgColor, command=clickGraf3dBtn)


orgLbl = Label(text="Organisation", bg=frameColor, fg=textColor)
objectLbl = Label(text="Mätobjekt", bg=frameColor, fg=textColor)
antennaLbl = Label(text="Antenn", bg=frameColor, fg=textColor)
infoLbl = Label(text="Info", bg=frameColor, fg=textColor)


orgEnt = ttk.Combobox(win, values=organisationList)
orgEnt.bind('<KeyRelease>', updateAllComboboxes)
orgEnt.bind('<<ComboboxSelected>>', updateAllComboboxes)
objectEnt = ttk.Combobox(win, values=measuringObjectList)
objectEnt.bind('<KeyRelease>', updateAllComboboxes)
objectEnt.bind('<<ComboboxSelected>>', updateAllComboboxes)
antennaEnt = ttk.Combobox(win, values=antennaList)
antennaEnt.bind('<KeyRelease>', updateAllComboboxes)
antennaEnt.bind('<<ComboboxSelected>>', updateAllComboboxes)
infoEnt = Text(bg=frameColor, fg=textColor, height=10, width=27)


tbOthers.grid(row=0, column=0, columnspan=3)
tbMeasure.grid(row=0, column=3, columnspan=3)


posLonLbl.grid(row=1, column=1)
posLatLbl.grid(row=2, column=1)
posAltLbl.grid(row=3, column=1)
fqEnt.grid(row=4, column=1)


posBtn.grid(row=1, column=2)
rbuBtn.grid(row=3, column=2)
startBtn.grid(row=4, column=2)


saveMeasurementBtn.grid(row=5, column=2)
newMeasurementBtn.grid(row=6, column=2)
openOldMeasurementBtn.grid(row=7, column=2)


fixStatusLbl.grid(row=1, column=3, columnspan=4)
grafBtn.grid(row=2, column=4)
graf2dBtn.grid(row=3, column=4)
graf3dBtn.grid(row=4, column=4)


orgLbl.grid(row=1, column=15)
objectLbl.grid(row=2, column=15)
antennaLbl.grid(row=3, column=15)
infoLbl.grid(row=4, column=15)


orgEnt.grid(row=1, column=16)
objectEnt.grid(row=2, column=16)
antennaEnt.grid(row=3, column=16)
infoEnt.grid(row=4, column=16, rowspan=6)


# updateFixStatus()
plotter = Plotter(DC)
createLiveFig()
win.mainloop()
