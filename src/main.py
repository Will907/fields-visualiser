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
    {"x":3, "y":4, "q":1},
    {"x":3, "y":2, "q":1},
    {"x":3, "y":0, "q":1},
    {"x":3, "y":-2, "q":1},
    {"x":3, "y":-4, "q":1},
    {"x":-3, "y":4, "q":-1},
    {"x":-3, "y":2, "q":-1},
    {"x":-3, "y":0, "q":-1},
    {"x":-3, "y":-2, "q":-1},
    {"x":-3, "y":-4, "q":-1},
)
qs = []
for charge in charges:
    qs.append(np.abs(charge["q"]))
qmax = np.max(qs)

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
        ve = e_pot(charges[i]["q"],charges[i]["x"],charges[i]["y"],X,Y)
        try:
            V += ve
        except UnboundLocalError:
            V = ve
    Vdev = np.std(V)
    levels = np.linspace(-2*Vdev,2*Vdev,30)
    magnitude = np.sqrt(u**2+v**2)
    fig
    field = plt.streamplot(x_values,y_values,u,v,broken_streamlines=True,density=qmax*9,start_points=starts,color=(0.2,0.2,0.2,0.7))
    potentials = plt.contourf(x_values,y_values,V,levels=levels,cmap="seismic",alpha=0.7,extend="both")
    potentials.cmap.set_under('blue')
    potentials.cmap.set_over('red')
    cb = plt.colorbar()
    cb.set_label("Electric Potential (V)")
    for charge in charges:
        if charge["q"] > 0:
            color = 'red' 
        else:
            color = 'blue'
        plt.scatter(charge["x"], charge["y"], color=color, s=100, zorder=5)
    pzero = input("Display 0 potential line (y/n): ").strip().lower()
    if pzero.startswith("y"):
        pzero = plt.contour(x_values,y_values,V,levels=np.array([0]))

#Calculations for the electric field
def e_eq(q,x1,y1,x2,y2):
    q *= qe
    r = np.sqrt((x2-x1)**2+(y2-y1)**2)
    r_v = [x2-x1,y2-y1]
    for i in range(len(r_v)):
        r_v[i] = np.nan_to_num(r_v[i] * (q/(4*np.pi*eps_0*r**3)))
    return np.nan_to_num(r_v)

def e_pot(q,x1,y1,x2,y2):
    q *= qe
    r = np.sqrt((x2-x1)**2+(y2-y1)**2)
    v = np.nan_to_num(q / (4*np.pi*eps_0*r))
    return v

fig = plt.figure()
ax = fig.add_subplot()
ax.set_aspect('equal', adjustable='box')
e_field(charges)
plt.show()