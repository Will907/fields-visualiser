from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

#Physical constants
c = 299792458
mu_0 = 4 * np.pi * 1e-7
eps_0 = 1/(mu_0*(c**2) )
qe = 1.602e-16

#List of charges - replace later with set function
charges = (
    {"x":-1, "y":0, "q":-1},
    {"x":1, "y":0, "q":1},
    {"x":-1, "y":-0.5, "q":-2},
)

#Electric field plotter
def e_field(charges):
    N = 20
    basestreams = 12
    x_start, x_end = -2.0, 2.0
    y_start, y_end = -2.0, 2.0
    r = max(((x_end-x_start)/N), ((y_end-y_start)/N))
    x_values = np.linspace(x_start, x_end, N)
    y_values = np.linspace(y_start, y_end, N)
    #x_values = []
    #y_values = []
    #coords = []
    #xsort = []
    #ysort = []
    """for charge in charges:
        for i in range(N):
            for stream in range(basestreams):
                theta = 2*np.pi * stream / basestreams
                x = charge["x"] + r*i*np.cos(theta)
                y = charge["y"] + r*i*np.sin(theta)
                x_values.append(x)
                y_values.append(y)
    for val in range(len(x_values)):
        coords.append([x_values[val],y_values[val]])
    coords = sorted(coords, key=lambda x: x[0])
    for i in range(len(coords)):
        xsort.append(coords[i][0])
        ysort.append(coords[i][1])"""
    X, Y = np.meshgrid(x_values,y_values)
    
    for i in range(len(charges)):
        e = e_eq(charges[i]["q"],charges[i]["x"],charges[i]["y"],X,Y)
        try:
            u += e[0]
            v += e[1]
        except UnboundLocalError:
            u = e[0]
            v = e[1]
    strm = plt.streamplot(x_values,y_values,u,v,cmap="plasma",broken_streamlines=False)

#Calculations for the electric field
def e_eq(q,x1,y1,x2,y2):
    q *= qe
    r = np.sqrt((x2-x1)**2+(y2-y1)**2)
    r_v = [x2-x1,y2-y1]
    for i in range(len(r_v)):
        r_v[i] *= (q/(4*np.pi*eps_0*r**3))
    return np.nan_to_num(r_v)

fig = plt.figure()
e_field(charges)
plt.show()