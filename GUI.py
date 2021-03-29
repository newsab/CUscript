import time
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d
import CuData
from pyro import *
from ShellCommands import *
from Measurements import *


global on
global a
global x
global y
global z
global m
global my_cmap

on = False
a = []
x = []
y = []
z = []
m = []
my_cmap = plt.get_cmap('autumn')
pmuSc = ShellCommands("172.16.0.3")
rbuSc = ShellCommands("172.16.0.6")
ptuSc = ShellCommands("172.16.0.9")
#pmuIp = "172.16.0.3"
#rbuIp = "172.16.0.6"
sas = StartAndStop()
print(sas)


def clickStartBtn():
    global on
    global a
    global x
    global y
    global z
    global m
    if not on:
        on = True
        startBtn.config(text="Stoppa mätning")
        frequency = fqEnt.get()
        sas.start(frequency)
        ptuSc.setFrequency(frequency)
    else:
        startBtn.config(text="Starta mätning")
        on = False
        sas.stop()
        a = sas.mesurement  # change to createDummy() to run txt-file
        print("list done!")
        for line in a:

            lo = line[1]
            la = line[2]
            al = line[3]
            me = line[4]
            x.append(float(lo))
            y.append(float(la))
            z.append(float(al))
            m.append(float(me))

            tbMeasure.insert(1.0, str(line) + '\n')
            tbMeasure.update()


def clickPmuBtn():

    msg2 = pmuSc.startStr2StrClient()
    tbOthers.insert(1.0, msg2 + '\n \n')
    tbOthers.update()
    time.sleep(0.5)

    msg3 = pmuSc.startPyro()
    tbOthers.insert(1.0, msg3 + '\n \n')
    tbOthers.update()
    time.sleep(0.5)

    msg4 = pmuSc.startPMUapp()
    tbOthers.insert(1.0, msg4 + '\n \n')
    tbOthers.update()
    time.sleep(0.5)

    tbOthers.insert(1.0, 'PMU Ready for take off! \n \n')
    tbOthers.update()


def clickRbuBtn():
    msg = rbuSc.coldRestart()
    tbOthers.insert(1.0, msg + '\n \n')
    tbOthers.update()
    time.sleep(2.5)

    msg2 = rbuSc.setBaudrate()
    tbOthers.insert(1.0, msg2 + '\n \n')
    tbOthers.update()
    time.sleep(0.5)

    msg3 = rbuSc.startStr2StrServer()
    tbOthers.insert(1.0, msg3 + '\n \n')
    tbOthers.update()
    time.sleep(0.5)

    tbOthers.insert(1.0, 'RBU Ready DO NOT MOVE!!! \n \n')
    tbOthers.update()


def clickGrafBtn():
    fig = plt.figure(figsize=(10, 7))
    sctt = plt.scatter(x, y, alpha=1, c=m, cmap=my_cmap, marker='o')
    fig.colorbar(sctt, shrink=0.8, aspect=5)
    plt.show()


def clickGraf3dBtn():
    fig = plt.figure(figsize=(10, 7))
    ax = plt.axes(projection="3d")
    sctt = ax.scatter3D(x, y, z, alpha=1, c=m, cmap=my_cmap, marker='p')
    ax.set_xlabel('Longitude', fontweight='bold')
    ax.set_ylabel('Latitude', fontweight='bold')
    ax.set_zlabel('Altitude', fontweight='bold')
    fig.colorbar(sctt, ax=ax, shrink=0.8, aspect=5)
    plt.show()


bgColor = 'black'
frameColor = '#222222'
textColor = '#cdcdcd'

win = Tk()
win.title("CU-applikation för PAMP")

win.geometry('1200x800')
win.configure(bg=bgColor)

tbMeasure = Text(bg=frameColor, fg=textColor, width=90)
tbOthers = Text(bg=frameColor, fg=textColor, width=60)

startLbl = Label(text="Starta mätning", bg=bgColor, fg=textColor)
startBtn = Button(text="Starta", width=20, height=2,
                  bg=frameColor, fg=bgColor, command=clickStartBtn)

#brLbl = Label(text="Sätt baudrate", bg=bgColor, fg=textColor)
#brEnt = Entry(bg=frameColor, fg=textColor)
pmuBtn = Button(text="Starta PMU", width=20, height=2,
                bg=frameColor, fg=bgColor, command=clickPmuBtn)

#fqLbl = Label(text="Sätt mätrekvens", bg=bgColor, fg=textColor)
fqEnt = Entry(bg=frameColor, fg=textColor)
rbuBtn = Button(text="Start Rbu", width=20, height=2,
                bg=frameColor, fg=bgColor, command=clickRbuBtn)

grafBtn = Button(text="Visa Graf", width=20, height=2,
                 bg=frameColor, fg=bgColor, command=clickGrafBtn)
graf3dBtn = Button(text="Visa 3D Graf", width=20, height=2,
                   bg=frameColor, fg=bgColor, command=clickGraf3dBtn)

tbOthers.grid(row=0, column=0, columnspan=3)
tbMeasure.grid(row=0, column=3, columnspan=3)

startLbl.grid(row=1, column=1)
startBtn.grid(row=1, column=2)

#brLbl.grid(row=2, column=1)
#brEnt.grid(row=3, column=1)
pmuBtn.grid(row=3, column=2)

#fqLbl.grid(row=4, column=1)
fqEnt.grid(row=5, column=1)
rbuBtn.grid(row=5, column=2)

grafBtn.grid(row=5, column=4)
graf3dBtn.grid(row=5, column=5)


win.mainloop()
