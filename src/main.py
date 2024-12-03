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

x_start, x_end = -5.0, 5.0 #replace with setting to alter
y_start, y_end = -5.0, 5.0
N = int(25 * np.max([x_end-y_start,y_end-y_start]))
x_values = np.linspace(x_start, x_end, N)
y_values = np.linspace(y_start, y_end, N)
X, Y = np.meshgrid(x_values,y_values)

class Point():
    def __init__(self,x,y):
            self.xpos = x
            self.ypos = y   
        

class PointCharge(Point):
    charges = []
    
    def __init__(self,x,y,q):
        super(PointCharge, self).__init__(x,y)
        self.q = q
        self.q_actual = q*qe
        self.u, self.v = np.zeros_like(X), np.zeros_like(Y)
        self.V = np.zeros_like(X)
        
        self.u, self.v = self.e_eq(X,Y)
        self.V = self.e_pot(X,Y)
    
    def e_pot(self,x1,y1):
        r = np.sqrt((self.xpos-x1)**2+(self.ypos-y1)**2)
        v = np.nan_to_num(self.q_actual / (4*np.pi*eps_0*r))
        return v
    
    def e_eq(self,x1,y1):
        r = np.sqrt((self.xpos-x1)**2+(self.ypos-y1)**2)
        r_v = [self.xpos-x1,self.ypos-y1]
        for i in range(len(r_v)):
            r_v[i] = np.nan_to_num(r_v[i] * (self.q_actual/(4*np.pi*eps_0*r**3)))
        r_v = np.nan_to_num(r_v)
        return r_v[0], r_v[1]
    
    @classmethod
    def get_closest(cls,x,y):
        if len(cls.charges) != 0:
            mindist = None
            for charge in cls.charges:
                dist = np.sqrt((x-charge.xpos)**2+(y-charge.ypos)**2)
                if mindist == None:
                    mindist = dist + 0
                    closest = cls.charges.index(charge)
                elif dist <= mindist:
                    mindist = dist + 0
                    closest = cls.charges.index(charge)
            return closest
    
    @classmethod
    def add_charge(cls,x,y,q):
        cls.charges.append(PointCharge(x,y,q))
    
    @classmethod
    def del_charge(cls,index):
        cls.charges.remove(index)
        
pcharges = PointCharge.charges
def e_field(charges):
    qs = []
    if len(charges) > 0:
        for charge in charges:
            qs.append(np.abs(charge.q))
        qmax = np.max(qs)
    
    basestreams = 12 #replace with setting
    starts = []
    
    #create streamplot start locations
    for charge in charges:
        for i in range(int(abs(charge.q)*basestreams/qmax)):
            theta = 2*i*np.pi / (np.abs(charge.q)*basestreams/qmax)
            next = [0.3*np.cos(theta)+charge.xpos,0.3*np.sin(theta)+charge.ypos]
            if not(next[0] >= x_end or next[0] <= x_start or next[1] >= y_end or next[1] <= y_start):
                starts.append(next)
    
    V_sum = np.zeros_like(X)
    u_sum, v_sum = np.zeros_like(X), np.zeros_like(Y)
    for charge in charges:
        V_sum += charge.V
        u_sum += charge.u
        v_sum += charge.v
    
    #electric field and potential superposition
    Vdev = np.std(V_sum)
    levels = np.linspace(-2*Vdev,2*Vdev,30)
    magnitude = np.sqrt(u_sum**2+v_sum**2)
    
    #plot field and potential map
    ax.clear()
    if len(charges) > 0:
        field = ax.streamplot(x_values,y_values,-u_sum,-v_sum,density=8,start_points=starts,color=(0.2,0.2,0.2,0.7))
        potentials = ax.contourf(x_values,y_values,V_sum,levels=levels,cmap="seismic",alpha=0.7,extend="both")
        potentials.cmap.set_under('blue')
        potentials.cmap.set_over('red')
        if not hasattr(ax, 'cbar') or ax.cbar is None:  # Only add the colorbar once
            ax.cbar = fig.colorbar(potentials, ax=ax)
            ax.cbar.set_label("Electric Potential (V)")
    else: 
        field = ax.streamplot(x_values,y_values,u_sum,v_sum)
    
    #plots point charges
    for charge in charges:
        if charge.q > 0:
            color = 'red' 
        else:
            color = 'blue'
        ax.scatter(charge.xpos, charge.ypos, color=color, s=100, zorder=5)
    
    pzero = ax.contour(x_values,y_values,V_sum,levels=np.array([0]),colors="k")
    title = ax.set_title("Electric Field Visualisation")
    fig.canvas.draw()

#click event handling
def on_click(event):
    global qin
    global mode
    global moving
    global prevq
    xin, yin = event.xdata, event.ydata
    if xin is None or yin is None:
        return
    if moving:
        mode = "add"
    if mode == "add":
        PointCharge.add_charge(xin,yin,qin)
        if moving:
            qin = prevq + 0
            moving = False
            mode = "move"
    elif mode == "del":
        if len(pcharges) > 0:
            if xin is not None and yin is not None:
                closest = pcharges[PointCharge.get_closest(xin,yin)]
                PointCharge.del_charge(closest)
    elif mode == "move":
        prevq = qin + 0
        if len(pcharges) > 0:
            if xin is not None and yin is not None:
                closest = pcharges[PointCharge.get_closest(xin,yin)]
                qin = closest.q
                PointCharge.del_charge(closest)
                mode = "add"
                moving = True
    e_field(pcharges)

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
e_field(pcharges)
mode = "add"
qin = 1
moving = False
if __name__ == "__main__": plt.show()