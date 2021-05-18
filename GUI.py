import time
from tkinter import ttk
import tkinter
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
global ax
global organisationList
global measuringObjectList
global antennaList
global measurementList
global plotter
global orgEnt
global objectEnt
global antennaEnt

DC = DataController()
on = False
scttLive = object
canvasLive = object
figLive = object
ax = object
my_cmap = plt.get_cmap('rainbow')
organisationList = DC.getAllOrganisation()
measuringObjectList = []#DC.getAllMeasuringObject("")
antennaList = []#DC.getAllAntenna("", "")
measurementList = []#DC.getAllMeasurement("", "", "")
pmuSc = ShellCommands("192.168.1.3")
rbuSc = ShellCommands("192.168.1.6")
ptuSc = ShellCommands("192.168.1.9")

def clickStartBtn():
    """
    Comment
    """
    global on

    frequency = fqEnt.get()
    if frequency == "":
        tbOthers.insert(1.0, 'Ange frekvens \n \n')
        tbOthers.update()
    else:
        if not on:
            startBtn.config(text="Stoppa mätning")
            on = True
            DC.startMeasurment(frequency)
            try:
                #ptuSc.setFrequency(frequency)
                tbOthers.insert(1.0, 'PTU:s frekvens är nu satt till ' + str(frequency) + '\n \n')
                tbOthers.update()
            except:
                tbOthers.insert(1.0, 'Kunde inte sätt frekvens på PTU \n \n')
                tbOthers.update()
            while on:
                DC.setShowList()
                try:
                    tim = str(DC.measurementData.time[-1])
                    alt = str(DC.measurementData.altitude[-1])
                    db = str(DC.measurementData.dbValue[-1])
                    tbMeasure.insert(1.0, tim + ", " + alt + ", " + db + '\n')
                    tbMeasure.update()
                    livePlot()
                except:
                    pass
                time.sleep(0.5)
        else:
            startBtn.config(text="Starta mätning")
            on = False
            DC.stopMeasurement()
            DC.setMeasurementData()
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
    try:
        updateFixStatus()
        DC.setStartPosition()
        lon = DC.measurement.longitude
        lat = DC.measurement.latitude
        alt = DC.measurement.altitude
        posLonLbl.config(text=str(lon))
        posLatLbl.config(text=str(lat))
        posAltLbl.config(text=str(alt))
        tbOthers.insert(1.0, 'Position på AUT: \n' +
                        'Longitud:\n' + str(lon) + '\nLatitud:\n' + str(lat) + '\nAltitud:\n' + str(alt) + '\n \n')
        tbOthers.update()
    except:
        tbOthers.insert(1.0, 'Kunde inte hämta position\n \n')
        tbOthers.update()

def clickRtkBtn():
    """
    Comment
    """
    try:
        msg = rbuSc.coldRestart()
        tbOthers.insert(1.0, msg + '\n \n')
        tbOthers.update()
        tbOthers.insert(1.0, 'RTK är nu omstartad, vänligen vänta någon minut för att uppnå RTK\n \n')
        tbOthers.update()
    except:
        tbOthers.insert(1.0, 'Kunde inte starta om RBU\n \n')
        tbOthers.update()

def clickGrafBtn():
    """
    Comment
    """
    try:
        plt.close()
        plotter.setGrafPlot()
        fig = plotter.grafPlot
        fig.show()
    except:
        tbOthers.insert(1.0, 'Kunde inte öppna grafen\n \n')
        tbOthers.update()

def clickGraf2dBtn():
    """
    Comment
    """
    try:
        plt.close()
        plotter.setTwoDPlot()
        fig2d = plotter.twoDPlot
        fig2d.show()
    except:
        tbOthers.insert(1.0, 'Kunde inte öppna grafen\n \n')
        tbOthers.update()

def clickGraf3dBtn():
    """
    Comment
    """
    try:
        plt.close()
        plotter.setThreeDPlot()
        fig3d = plotter.threeDPlot
        fig3d.show()
    except:
        tbOthers.insert(1.0, 'Kunde inte öppna grafen\n \n')
        tbOthers.update()

def clickNewMeasurementBtn():
    """
    Comment
    """
    try:
        DC.newMeasurement(DC.measurement.longitude, DC.measurement.latitude, DC.measurement.altitude, DC.measurement.antennaId)
        tbOthers.insert(1.0, 'Ny mätning startad \n \n')
        tbOthers.update()
        tbMeasure.delete('1.0', tkinter.END)
        tbMeasure.update()
        livePlot()
    except:
        tbOthers.insert(1.0, 'Kunde inte initsiera en ny mätning\n \n')
        tbOthers.update()

def setDcToSave():
    """
    Comment
    """
    org = orgEnt.get().lower() 
    obj = objectEnt.get().lower()
    ant = antennaEnt.get().lower()
    DC.measurement.info = infoEnt.get("1.0", tkinter.END).lower()
    DC.checkOrganisation(org)
    DC.checkMeasuringObject(obj)
    DC.checkAntenna(ant)
    return DC

def clickSaveMeasurementBtn():
    """
    Comment
    """
    try:
        path = getSavePath()
        setDcToSave()
        DC.insertMeasurementToDb()
        tbOthers.insert(1.0, 'Mätningen har sparats till databasen\n \n')
        tbOthers.update()
    except:
        tbOthers.insert(1.0, 'Kunde inte spara mätningen till databasen\n \n')
        tbOthers.update()
    try: 
        path = getSavePath()
        fileWriter = FileWriter(DC, path)
        fileWriter.createTxtFile()
        tbOthers.insert(1.0, 'Mätningen har sparats som en .txt-fil\n' + path + '\n \n')
        tbOthers.update()
    except:
        tbOthers.insert(1.0, 'Kunde inte spara mätningen som .txt-fil\n \n')
        tbOthers.update()

def clickSaveAsPdfBtn():
    """
    Comment
    """
    try:
        path = getSavePath()
        setDcToSave()
        fileWriter = FileWriter(DC, path)
        fileWriter.createPdfFile()
        tbOthers.insert(1.0, 'Mätningen har sparats som en .pdf-fil\n' + path + '\n \n')
        tbOthers.update()
    except:
        tbOthers.insert(1.0, 'Kunde inte spara mätningen som .pdf-fil\n \n')
        tbOthers.update()

def clickDistanceBtn():
    """
    Comment
    """
    try:
        distance = DC.getDistanceFromAUT()
        distanceLbl.config(text=str(distance) + " meter från AUT")
    except:
        tbOthers.insert(1.0, 'Gick inte att hämta in uppgifter om distans mellan AUT och PMU \n \n')
        tbOthers.update()

def clickPmuBtn():
    """
    Comment
    """
    try:
        tbOthers.insert(1.0, 'Lägg in funktion för omstart av PMU \n \n')
        tbOthers.update()
    except:
        tbOthers.insert(1.0, 'Kunde inte starta om PMU\n \n')
        tbOthers.update()

def clickRbuBtn():
    """
    Comment
    """
    try:
        tbOthers.insert(1.0, 'Lägg in funktion för omstart av RBU \n \n')
        tbOthers.update()
    except:
        tbOthers.insert(1.0, 'Kunde inte starta om RBU\n \n')
        tbOthers.update()

def clickPmuStatusBtn():
    """
    Comment
    """
    try:
        tbOthers.insert(1.0, 'Lägg in funktion för att få status av PMU \n \n')
        tbOthers.update()
    except:
        tbOthers.insert(1.0, 'Kunde inte hämta status på PMU \n \n')
        tbOthers.update()

def clickFixUpdateBtn():
    """
    Comment
    """
    updateFixStatus()
    try:
        updateFixStatus()
    except:
        tbOthers.insert(1.0, 'Kunde inte uppdatera fix status \n \n')
        tbOthers.update()

def createLiveFig():
    """
    Comment
    """
    global scttLive
    global canvasLive
    global ax
    figLive = plt.figure(figsize=(5, 3), )
    figLive.patch.set_facecolor('#ececec')
    ax = figLive.add_subplot(111)
    x = DC.measurementData.longitude
    y = DC.measurementData.latitude
    m = DC.measurementData.dbValue
    scttLive = ax.scatter(x, y, alpha=1, c=m, cmap=my_cmap, marker='o')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    figLive.colorbar(scttLive, shrink=0.8, aspect=5)
    canvasLive = FigureCanvasTkAgg(figLive, master=win)
    canvasLive.get_tk_widget().grid(row=0, column=6, columnspan=3)

def livePlot():
    """
    Comment
    """
    global scttLive 
    global canvasLive
    global ax
    plt.cla()
    autlon = DC.measurement.longitude
    autlat = DC.measurement.latitude
    x = DC.measurementData.longitude
    y = DC.measurementData.latitude
    m = DC.measurementData.dbValue
    plt.scatter(autlon, autlat, alpha=1, c="black", marker='X', label='AUT')
    scttLive = plt.scatter(x, y, alpha=1, c=m, cmap=my_cmap, marker='o')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    canvasLive.draw_idle()

def updateFixStatus():
    """
    Comment
    """
    status = DC.getFixStatus()
    fixStatusLbl.config(text="Fix status: " + status)

def updateOrganisationCombobox():
    """
    Comment
    """
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
    """
    Comment
    """
    global organisationList
    organisationList.clear()
    for item in data:
        organisationList.append(item)       
    orgEnt['values'] = organisationList

def updateMeasuringObjectCombobox():
    """
    Comment
    """
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
    """
    Comment
    """
    global measuringObjectList
    measuringObjectList.clear()
    for item in data:
        measuringObjectList.append(item)       
    objectEnt['values'] = measuringObjectList

def updateAntennaCombobox():
    """
    Comment
    """
    typed = antennaEnt.get()
    if typed == "":
        data = DC.getAllAntenna(objectEnt.get(), orgEnt.get())
    else:  
        data = []   
        for item in DC.getAllAntenna(objectEnt.get(), orgEnt.get()):
            if typed.lower() in item.lower():
                data.append(item)
    updateAntennaList(data)

def updateAntennaList(data):
    """
    Comment
    """
    global antennaList
    antennaList.clear()
    for item in data:
        antennaList.append(item)       
    antennaEnt['values'] = antennaList

def updateAllComboboxes(e):
    """
    Comment
    """
    updateOrganisationCombobox()
    updateMeasuringObjectCombobox()
    updateAntennaCombobox()
    
def getSavePath():
    """
    Comment
    """
    path = filedialog.askdirectory(initialdir="./Measurements/")
    return(str(path))

def clickOpenOldMeasurementBtn():
    """
    Comment
    """
    try:
        global organisationList
        global measuringObjectList
        global antennaList
        global measurementList
        global orgEnt
        global objectEnt
        global antennaEnt

        def clickLoadBtn():
            """
            Comment
            """
            DC.setAllData(orgEntNW.get(), objectEntNW.get(), antennaEntNW.get(), measurementEntNW.get())
            updateGui()
            newWindow.destroy()
        
        def updateOrganisationComboboxNW():
            """
            Comment
            """
            typed = orgEntNW.get()
            if typed == "":
                data = DC.getAllOrganisation()
            else:  
                data = []   
                for item in DC.getAllOrganisation():
                    if typed.lower() in item.lower():
                        data.append(item)
            updateOrganisationListNW(data)

        def updateOrganisationListNW(data):
            """
            Comment
            """
            global organisationList
            organisationList.clear()
            for item in data:
                organisationList.append(item)       
            orgEntNW['values'] = organisationList

        def updateMeasuringObjectComboboxNW():
            """
            Comment
            """
            typed = objectEntNW.get()    
            if typed == "":
                data = DC.getAllMeasuringObject(orgEntNW.get())

            else:  
                data = []   
                for item in DC.getAllMeasuringObject(orgEntNW.get()):
                    if typed.lower() in item.lower():
                        data.append(item) 
            updateMeasuringObjectListNW(data)

        def updateMeasuringObjectListNW(data):
            """
            Comment
            """
            global measuringObjectList
            measuringObjectList.clear()
            for item in data:
                measuringObjectList.append(item)       
            objectEntNW['values'] = measuringObjectList

        def updateAntennaComboboxNW():
            """
            Comment
            """
            typed = antennaEntNW.get()
            typed2 = objectEntNW.get()
            if typed2 == "":
                data = []
            else:
                if typed == "":
                    data = DC.getAllAntenna(objectEntNW.get(), orgEntNW.get())
                else:  
                    data = []   
                    for item in DC.getAllAntenna(objectEntNW.get(), orgEntNW.get()):
                        if typed.lower() in item.lower():
                            data.append(item)
            updateAntennaListNW(data)

        def updateAntennaListNW(data):
            """
            Comment
            """
            global antennaList
            antennaList.clear()
            for item in data:
                antennaList.append(item)       
            antennaEntNW['values'] = antennaList

        def updateMeasurementComboboxNW():
            """
            Comment
            """
            typed = measurementEntNW.get()
            typed2 = antennaEntNW.get()
            if typed2 == "":
                data = []
            else:
                if typed == "":
                    data = DC.getAllMeasurement(antennaEntNW.get(), objectEntNW.get(), orgEntNW.get())
                else:  
                    data = []   
                    for item in DC.getAllMeasurement(antennaEntNW.get(), objectEntNW.get(), orgEntNW.get()):
                        if typed.lower() in item.lower():
                            data.append(item)
            updateMeasurementListNW(data)

        def updateMeasurementListNW(data):
            """
            Comment
            """
            global measurementList
            measurementList.clear()
            for item in data:
                measurementList.append(item)       
            measurementEntNW['values'] = measurementList

        def updateAllComboboxesNW(e):
            """
            Comment
            """
            updateOrganisationComboboxNW()
            updateMeasuringObjectComboboxNW()
            updateAntennaComboboxNW()
            updateMeasurementComboboxNW()

        def updateGui():
            """
            Comment
            """
            tbOthers.insert(1.0, 'Visar gammal mätning utförd på:\nOrganisation: ' + DC.organisation.name + '\nUtförd: ' + str(DC.measurement.time) + '\nMärobjekt: ' + DC.measuringObject.name + '\nAntenn: ' + DC.antenna.name + '\nFrekvens: ' + str(DC.measurement.frequency)  + '\nInfo: ' + DC.measurement.info + '\n\n')
            tbOthers.update()

            length = len(DC.measurementData.longitude)
            count = 0           
            while count < length:
                tim = str(DC.measurementData.time[count])
                alt = str(DC.measurementData.altitude[count])
                db = str(DC.measurementData.dbValue[count])
                count = count + 1
                tbMeasure.insert(1.0, tim + ", " + alt + ", " + db + '\n')
                tbMeasure.update
            livePlot()
    except:
        tbOthers.insert(1.0, 'Kunde inte öppna fönster för att ladda in tidigare mätning\n \n')
        tbOthers.update()

    tbMeasure.delete('1.0', tkinter.END)
    orgEnt.set("")
    objectEnt.set("")
    antennaEnt.set("")
    infoEnt.delete('1.0', tkinter.END)
    organisationList = DC.getAllOrganisation()
    measuringObjectList = []
    antennaList = []
    measurementList = []
    newWindow = tkinter.Toplevel(win, bg="#ececec")
    newWindow.title("Öppna tidigare mätning")
    newWindow.geometry("300x300")
    ttk.Label(newWindow, 
        text ="Välj en tidigare mätning").grid(row=1, column=1)
    orgEntNW = ttk.Combobox(newWindow, values=organisationList)
    orgEntNW.bind('<KeyRelease>', updateAllComboboxesNW)
    orgEntNW.bind('<<ComboboxSelected>>', updateAllComboboxesNW)
    orgEntNW.grid(row=2, column=1)
    objectEntNW = ttk.Combobox(newWindow, values=measuringObjectList)
    objectEntNW.bind('<KeyRelease>', updateAllComboboxesNW)
    objectEntNW.bind('<<ComboboxSelected>>', updateAllComboboxesNW)
    objectEntNW.grid(row=3, column=1)
    antennaEntNW = ttk.Combobox(newWindow, values=antennaList)
    antennaEntNW.bind('<KeyRelease>', updateAllComboboxesNW)
    antennaEntNW.bind('<<ComboboxSelected>>', updateAllComboboxesNW)
    antennaEntNW.grid(row=4, column=1)
    measurementEntNW = ttk.Combobox(newWindow, values=measurementList)
    measurementEntNW.bind('<KeyRelease>', updateAllComboboxesNW)
    measurementEntNW.bind('<<ComboboxSelected>>', updateAllComboboxesNW)
    measurementEntNW.grid(row=5, column=1)

    loadBtn = ttk.Button(newWindow, text="Ladda upp mätning", command=clickLoadBtn)
    loadBtn.grid(row=6, column=1) 

win = tkinter.Tk()
win.title("CU-applikation för PAMP")
win.geometry('1200x700')
win.configure(bg="#ececec")


tbOthers = tkinter.Text(width=50, bg="#ececec")
tbMeasure = tkinter.Text(width=50, bg="#ececec")


posLonLbl = ttk.Label(text="")
posLatLbl = ttk.Label(text="")
posAltLbl = ttk.Label(text="")
fqEnt = ttk.Entry(width=10)
distanceLbl = ttk.Label(text="")
distanceBtn = ttk.Button(text="Distans till AUT", command=clickDistanceBtn)
pmuBtn = ttk.Button(text="Starta om PMU", command=clickPmuBtn)
rbuBtn = ttk.Button(text="Starta om RBU", command=clickRbuBtn)
pmuStatusBtn = ttk.Button(text="PMU status", command=clickPmuStatusBtn)
fixUpdateBtn = ttk.Button(text="Uppdatera fix status", command=clickFixUpdateBtn)


posBtn = ttk.Button(text="Ta ut AUT position", command=clickPosBtn)
rtkBtn = ttk.Button(text="Start om RTK", command=clickRtkBtn)
startBtn = ttk.Button(text="Starta mätning", command=clickStartBtn)
saveMeasurementBtn = ttk.Button(text="Spara mätning", command=clickSaveMeasurementBtn)
newMeasurementBtn = ttk.Button(text="Initsiera ny mätning", command=clickNewMeasurementBtn)
openOldMeasurementBtn = ttk.Button(text="Öppna mätning", command=clickOpenOldMeasurementBtn)
saveAsPdfBtn = ttk.Button(text="Skapa PDF", command=clickSaveAsPdfBtn)


fixStatusLbl = ttk.Label(text="")
grafBtn = ttk.Button(text="Visa Graf", command=clickGrafBtn)
graf2dBtn = ttk.Button(text="Visa 2D Graf", command=clickGraf2dBtn)
graf3dBtn = ttk.Button(text="Visa 3D Graf", command=clickGraf3dBtn)


orgLbl = ttk.Label(text="Organisation")
objectLbl = ttk.Label(text="Mätobjekt")
antennaLbl = ttk.Label(text="Antenn")
infoLbl = ttk.Label(text="Info")


orgEnt = ttk.Combobox(win, values=organisationList)
orgEnt.bind('<KeyRelease>', updateAllComboboxes)
orgEnt.bind('<<ComboboxSelected>>', updateAllComboboxes)
objectEnt = ttk.Combobox(win, values=measuringObjectList)
objectEnt.bind('<KeyRelease>', updateAllComboboxes)
objectEnt.bind('<<ComboboxSelected>>', updateAllComboboxes)
antennaEnt = ttk.Combobox(win, values=antennaList)
antennaEnt.bind('<KeyRelease>', updateAllComboboxes)
antennaEnt.bind('<<ComboboxSelected>>', updateAllComboboxes)
infoEnt = tkinter.Text(height=10, width=27)
measurementEnt = ttk.Combobox(win, values=measurementList)

tbOthers.grid(row=0, column=0, columnspan=3)
tbMeasure.grid(row=0, column=3, columnspan=3)

posLonLbl.grid(row=4, column=1)
posLatLbl.grid(row=5, column=1)
posAltLbl.grid(row=6, column=1)
distanceLbl.grid(row=7, column=1) 

fqEnt.grid(row=27, column=1)

posBtn.grid(row=6, column=2)
distanceBtn.grid(row=7, column=2)

startBtn.grid(row=27, column=2)
newMeasurementBtn.grid(row=26, column=2)

fixUpdateBtn.grid(row=6, column=4)
pmuStatusBtn.grid(row=7, column=4)

pmuBtn.grid(row=25, column=4)
rbuBtn.grid(row=26, column=4)
rtkBtn.grid(row=27, column=4)

fixStatusLbl.grid(row=1, column=3, columnspan=4)

grafBtn.grid(row=5, column=6)
graf2dBtn.grid(row=6, column=6)
graf3dBtn.grid(row=7, column=6)

saveMeasurementBtn.grid(row=25, column=6)
openOldMeasurementBtn.grid(row=26, column=6)
saveAsPdfBtn.grid(row=27, column=6)

orgLbl.grid(row=1, column=8)
orgEnt.grid(row=2, column=8)
objectLbl.grid(row=3, column=8)
objectEnt.grid(row=4, column=8)
antennaLbl.grid(row=5, column=8)
antennaEnt.grid(row=6, column=8)
infoLbl.grid(row=7, column=8)
infoEnt.grid(row=8, column=8, rowspan=20)


# updateFixStatus()
plotter = Plotter(DC)
createLiveFig()
win.mainloop()