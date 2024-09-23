from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt

c = 299792458
mu_0 = 4 * np.pi * 1e-7
eps_0 = 1/(mu_0*(c**2) )
qe = 1.602e-16

charges = (
    {"x":1, "y":1, "q":-1},
    {"x":-1, "y":1, "q":-1},
    {"x":1, "y":0, "q":-1},
    {"x":-1, "y":0, "q":1},
    {"x":1, "y":-1, "q":1},
    {"x":-1, "y":-1, "q":1}
)

def e_field(charges):

    N = 50
    x_start, x_end = -2.0, 2.0
    y_start, y_end = -2.0, 2.0
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
    strm = plt.streamplot(x_values,y_values,u,v,broken_streamlines=False)
    #for i in range(len(charges)):
        #fig.add_trace(go.Scatter(x=charges[i]["x"],y=charges[i]["y"],mode="markers",name="source"))


def e_eq(q,x1,y1,x2,y2):
    q *= qe
    r = np.sqrt((x2-x1)**2+(y2-y1)**2)
    r_v = [x2-x1,y2-y1]
    for i in range(len(r_v)):
        r_v[i] *= (q/(4*np.pi*eps_0*r**3))
    return r_v

fig = plt.figure()
e_field(charges)
plt.show()