import time
from tkinter import *

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

import CuData
from pyro import *
from ShellCommands import *

global on
global x
global y
global z
global m
global my_cmap

on = False
x = []
y = []
z = []
m = []
my_cmap = plt.get_cmap('autumn')
pmuSc = ShellCommands("81.16.170.67")
rbuSc = ShellCommands("81.16.170.67")
sas = StartAndStop()

def clickStartBtn():
    if not on:
        on = True
        startBtn.config(text="Stoppa mätning")
        sas.start()
    else:
        startBtn.config(text="Starta mätning")
        on = False
        sas.stop()


def clickBrBtn():
    baudrate = brEnt.get()
    msg = rbuSc.setBaudrate(baudrate)
    tbOthers.insert(1.0, msg + '\n')
    tbOthers.update()
    time.sleep(0.5)

    msg2 = pmuSc.setBaudrate(baudrate)
    tbOthers.insert(1.0, msg2 + '\n')
    tbOthers.update()
    time.sleep(0.5)

    msg3 = rbuSc.startStr2StrServer()
    tbOthers.insert(1.0, msg3 + '\n')
    tbOthers.update()
    time.sleep(0.5)

    msg4 = pmuSc.startStr2StrClient()
    tbOthers.insert(1.0, msg4 + '\n')
    tbOthers.update()
    time.sleep(0.5)

    msg5 = pmuSc.startPyro()
    tbOthers.insert(1.0, msg5 + '\n')
    tbOthers.update()
    time.sleep(0.5)


def clickFqBtn():
    #kalla på funktion för att sätta frekvens
    print ('hej')


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
# win.geometry('1000x1000')
win.configure(bg=bgColor)

tbMeasure = Text(bg=frameColor, fg=textColor, width=90)
tbOthers = Text(bg=frameColor, fg=textColor, width=60)

startLbl = Label(text="Starta mätning", bg=bgColor, fg=textColor)
startBtn = Button(text="Starta", width=20, height=2,
                  bg=frameColor, fg=bgColor, command=clickStartBtn)

brLbl = Label(text="Sätt baudrate", bg=bgColor, fg=textColor)
brEnt = Entry(bg=frameColor, fg=textColor)
brBtn = Button(text="Spara", width=20, height=2,
                bg=frameColor, fg=bgColor, command=clickBrBtn)

fqLbl = Label(text="Sätt mätrekvens", bg=bgColor, fg=textColor)
fqEnt = Entry(bg=frameColor, fg=textColor)
fqBtn = Button(text="Spara", width=20, height=2,
                bg=frameColor, fg=bgColor, command=clickFqBtn)

grafBtn = Button(text="Visa Graf", width=20, height=2,
                 bg=frameColor, fg=bgColor, command=clickGrafBtn)
graf3dBtn = Button(text="Visa 3D Graf", width=20, height=2,
                   bg=frameColor, fg=bgColor, command=clickGraf3dBtn)

tbOthers.grid(row=0, column=0, columnspan=3)
tbMeasure.grid(row=0, column=3, columnspan=3)

startLbl.grid(row=1, column=1)
startBtn.grid(row=1, column=2)

brLbl.grid(row=2, column=1)
brEnt.grid(row=3, column=1)
brBtn.grid(row=3, column=2)

fqLbl.grid(row=4, column=1)
fqEnt.grid(row=5, column=1)
fqBtn.grid(row=5, column=2)

grafBtn.grid(row=5, column=4)
graf3dBtn.grid(row=5, column=5)


win.mainloop()
