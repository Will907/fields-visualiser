from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

#Physical constants
c = 299792458
mu_0 = 4 * np.pi * 1e-7
eps_0 = 1/(mu_0*(c**2) )
qe = 1.602e-19

#List of charges - replace later with set function
charges = (
    {"x":1, "y":1, "q":-1},
    {"x":-1, "y":-1, "q":-1},
    {"x":-1, "y":1, "q":1},
    {"x":1, "y":-1, "q":1},
)
qs = []
for charge in charges:
    qs.append(np.abs(charge["q"]))
qs = np.max(qs)

#Electric field plotter
def e_field(charges):
    N = 500
    basestreams = 24
    starts = []
    for charge in charges:
        for i in range(int(abs(charge["q"])*basestreams)):
            theta = 2*i*np.pi / (np.abs(charge["q"])*basestreams)
            starts.append([0.3*np.cos(theta)+charge["x"],0.3*np.sin(theta)+charge["y"]])
    x_start, x_end = -5.0, 5.0
    y_start, y_end = -5.0, 5.0
    r = max(((x_end-x_start)/N), ((y_end-y_start)/N))
    x_values = np.linspace(x_start, x_end, N)
    y_values = np.linspace(y_start, y_end, N)
    X, Y = np.meshgrid(x_values,y_values)
    
    for i in range(len(charges)):
        e = e_eq(charges[i]["q"],charges[i]["x"],charges[i]["y"],X,Y)
        try:
            u += e[0]
            v += e[1]
        except UnboundLocalError:
            u = e[0]
            v = e[1]
    magnitude = np.sqrt(u**2+v**2)
    strm = plt.streamplot(x_values,y_values,u,v,broken_streamlines=True,density=qs*10,start_points=starts)
    for charge in charges:
        if charge["q"] > 0:
            color = 'red' 
        else:
            color = 'blue'
        plt.scatter(charge["x"], charge["y"], color=color, s=200, zorder=5)

#Calculations for the electric field
def e_eq(q,x1,y1,x2,y2):
    q *= qe
    r = np.sqrt((x2-x1)**2+(y2-y1)**2)
    r_v = [x2-x1,y2-y1]
    for i in range(len(r_v)):
        r_v[i] = np.nan_to_num(r_v[i] * (q/(4*np.pi*eps_0*r**3)))
    return np.nan_to_num(r_v)

fig = plt.figure(figsize=(5,5))
e_field(charges)
plt.show()