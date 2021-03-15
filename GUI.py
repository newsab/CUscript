from tkinter import *
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import time
import CuData

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


def clickStartBtn():
    global on
    global x
    global y
    global z
    global m

    if not on:
        on = True
        startBtn.config(text="Stoppa mätning")
        while on:
            _data, lo, la, al, me = CuData.getData()
            measurement = str(_data)
            tbMeasure.insert(1.0, measurement)
            tbMeasure.update()
            x = lo
            y = la
            z = al
            m = me
            # time.sleep(0.5)

    else:
        startBtn.config(text="Starta mätning")
        on = False


def clickPmuBtn():
    frequency = pmuEnt.get()
    tbOthers.insert(1.0, 'PMU frekvens satt till ' + frequency + '\n')
    tbOthers.update()


def clickPtuBtn():
    frequency = pmuEnt.get()
    tbOthers.insert(1.0, 'PTU frekvens satt till ' + frequency + '\n')
    tbOthers.update()


def clickRbuBtn():
    running = True
    count = 0
    tbOthers.insert(1.0, 'RBU startar'+'\n')

    while running:
        if count < 100:
            tbOthers.insert(1.0, 'RBU startad till: ' + str(count) + '%\n')
            tbOthers.update()
            count = count + 5
            time.sleep(1)
        else:
            tbOthers.insert(1.0, 'RBU startad!'+'\n')
            tbOthers.update()
            running = False


def clickGrafBtn():
    fig = plt.figure(figsize=(10, 7))
    sctt = plt.scatter(x, y, alpha=1, c=m, cmap=my_cmap, marker='^')
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

pmuLbl = Label(text="Sätt PMU Frekvens", bg=bgColor, fg=textColor)
pmuEnt = Entry(bg=frameColor, fg=textColor)
pmuBtn = Button(text="Spara och starta", width=20, height=2,
                bg=frameColor, fg=bgColor, command=clickPmuBtn)

ptuLbl = Label(text="Sätt PTU Frekvens", bg=bgColor, fg=textColor)
ptuEnt = Entry(bg=frameColor, fg=textColor)
ptuBtn = Button(text="Spara och starta", width=20, height=2,
                bg=frameColor, fg=bgColor, command=clickPtuBtn)

rbuLbl = Label(text="Starta RBU", bg=bgColor, fg=textColor)
rbuBtn = Button(text="Starta", width=20, height=2,
                bg=frameColor, fg=bgColor, command=clickRbuBtn)

grafBtn = Button(text="Visa Graf", width=20, height=2,
                 bg=frameColor, fg=bgColor, command=clickGrafBtn)
graf3dBtn = Button(text="Visa 3D Graf", width=20, height=2,
                   bg=frameColor, fg=bgColor, command=clickGraf3dBtn)

tbOthers.grid(row=0, column=0, columnspan=3)
tbMeasure.grid(row=0, column=3, columnspan=3)

rbuLbl.grid(row=1, column=1)
rbuBtn.grid(row=2, column=1)

startLbl.grid(row=1, column=2)
startBtn.grid(row=2, column=2)

pmuLbl.grid(row=3, column=1)
pmuEnt.grid(row=4, column=1)
pmuBtn.grid(row=5, column=1)

ptuLbl.grid(row=3, column=2)
ptuEnt.grid(row=4, column=2)
ptuBtn.grid(row=5, column=2)

grafBtn.grid(row=5, column=4)
graf3dBtn.grid(row=5, column=5)

win.mainloop()
