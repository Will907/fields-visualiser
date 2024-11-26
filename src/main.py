from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import time as t
import sys

#Physical constants
c = 299792458
mu_0 = 4 * np.pi * 1e-7
eps_0 = 1/(mu_0*(c**2) )
qe = 1.602e-19

class Point():
    def __init__(self,x,y):
            self.xpos = x
            self.ypos = y   
        

class PointCharge(Point):
    def __init__(self,x,y,q):
        super(PointCharge, self).__init__(x,y)
        self.q = q
#List of charges
charges = []

#Electric field plotter
def e_field(charges):
    qs = []
    if len(charges) > 0:
        for charge in charges:
            qs.append(np.abs(charge.q))
        qmax = np.max(qs)
    x_start, x_end = -5.0, 5.0 #replace with setting to alter
    y_start, y_end = -5.0, 5.0
    N = int(25 * np.max([x_end-y_start,y_end-y_start]))
    basestreams = 12 #replace with setting
    starts = []
    
    #create streamplot start locations
    for charge in charges:
        for i in range(int(abs(charge.q)*basestreams/qmax)):
            theta = 2*i*np.pi / (np.abs(charge.q)*basestreams/qmax)
            next = [0.3*np.cos(theta)+charge.xpos,0.3*np.sin(theta)+charge.ypos]
            if not(next[0] >= x_end or next[0] <= x_start or next[1] >= y_end or next[1] <= y_start):
                starts.append(next)
    r = max(((x_end-x_start)/N), ((y_end-y_start)/N))
    x_values = np.linspace(x_start, x_end, N)
    y_values = np.linspace(y_start, y_end, N)
    X, Y = np.meshgrid(x_values,y_values)
    u, v = np.zeros_like(X), np.zeros_like(Y)
    V = np.zeros_like(X)
    
    #electric field and potential superposition
    for charge in charges:
        e = e_eq(charge.q,charge.xpos,charge.ypos,X,Y)
        u += e[0]
        v += e[1]
        ve = e_pot(charge.q,charge.xpos,charge.ypos,X,Y)
        V += ve
    Vdev = np.std(V)
    levels = np.linspace(-2*Vdev,2*Vdev,30)
    magnitude = np.sqrt(u**2+v**2)
    
    #plot field and potential map
    ax.clear()
    if len(charges) > 0:
        field = ax.streamplot(x_values,y_values,u,v,density=8,start_points=starts,color=(0.2,0.2,0.2,0.7))
        potentials = ax.contourf(x_values,y_values,V,levels=levels,cmap="seismic",alpha=0.7,extend="both")
        potentials.cmap.set_under('blue')
        potentials.cmap.set_over('red')
        if not hasattr(ax, 'cbar') or ax.cbar is None:  # Only add the colorbar once
            ax.cbar = fig.colorbar(potentials, ax=ax)
            ax.cbar.set_label("Electric Potential (V)")
    else: 
        field = ax.streamplot(x_values,y_values,u,v)
    
    #plots point charges
    for charge in charges:
        if charge.q > 0:
            color = 'red' 
        else:
            color = 'blue'
        ax.scatter(charge.xpos, charge.ypos, color=color, s=100, zorder=5)
    
    pzero = ax.contour(x_values,y_values,V,levels=np.array([0]),colors="k")
    title = ax.set_title("Electric Field Visualisation")
    fig.canvas.draw()

#Calculations for the electric field
def e_eq(q,x1,y1,x2,y2):
    q *= qe
    r = np.sqrt((x2-x1)**2+(y2-y1)**2)
    r_v = [x2-x1,y2-y1]
    for i in range(len(r_v)):
        r_v[i] = np.nan_to_num(r_v[i] * (q/(4*np.pi*eps_0*r**3)))
    return np.nan_to_num(r_v)

#calculations for electric potential
def e_pot(q,x1,y1,x2,y2):
    q *= qe
    r = np.sqrt((x2-x1)**2+(y2-y1)**2)
    v = np.nan_to_num(q / (4*np.pi*eps_0*r))
    return v

#click event handling
def on_click(event):
    global qin
    global mode
    global moving
    global prevq
    xin, yin = event.xdata, event.ydata
    if mode == "add":
        print(qin)
        new_charge = PointCharge(xin,yin,qin)
        charges.append(new_charge)
        if moving:
            qin = prevq + 0
            moving = False
            mode = "move"
    elif mode == "del":
        if len(charges) > 0:
            mindist = None
            if xin is not None and yin is not None:
                for charge in charges:
                    dist = np.sqrt((xin-charge.xpos)**2+(yin-charge.ypos)**2)
                    if mindist == None:
                        mindist = dist + 0
                        remove = charges.index(charge)
                    elif dist <= mindist:
                        mindist = dist + 0
                        remove = charges.index(charge)
                charges.pop(remove)
    elif mode == "move":
        prevq = qin + 0
        if len(charges) > 0:
            mindist = None
            if xin is not None and yin is not None:
                for charge in charges:
                    dist = np.sqrt((xin-charge.xpos)**2+(yin-charge.ypos)**2)
                    if mindist == None:
                        mindist = dist + 0
                        moveq = charge.q
                        remove = charges.index(charge)
                    elif dist <= mindist:
                        mindist = dist + 0
                        moveq = charge.q
                        remove = charges.index(charge)
                qin = moveq
                charges.pop(remove)
                mode = "add"
                moving = True
    e_field(charges)

def keypress(event): #needs completing
    global mode
    sys.stdout.flush()
    if event.key == "d":
        mode = "del"
    elif event.key == "a":
        mode = "add"
    elif event.key == "m":
        mode = "move"

def setq(q):
    global qin
    qin = q

def get_figure():
    return fig

def get_mode():
    return mode

def set_mode(md):
    global mode
    mode = md.lower()

fig, ax = plt.subplots()
ax.set_aspect('equal', adjustable='box')
fig.canvas.mpl_connect('button_press_event', on_click)
fig.canvas.mpl_connect('key_press_event', keypress)
e_field(charges)
mode = "add"
qin = 1
moving = False
if __name__ == "__main__": plt.show()