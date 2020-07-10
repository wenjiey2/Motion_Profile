import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import time

# Piecewise unit function, assuming order >= 1 (acceleration or above)
def Piecewise(t, m, order, space):
    if order == 1:
        if(t < 1):
            return m
        elif(t < 1+space):
            return 0
        elif(t < 2+space):
            return -m
    peak = 2**order
    change = peak/2
    const = peak/2*space
    for i in range(order-1):
        change += peak/(2**(i+2))*space*(2**i)
    if t < change:
        return Piecewise(t, m, order-1, space)
    elif t < change + const:
        return 0
    elif t <= 2*change + const:
        return -1*Piecewise(t-change-const, m, order-1, space)
# Generate scurve of velocity
def scurve(m, order, y, t_axis):
    curr = y;
    for i in range(order):
        curr = integrate.cumtrapz(curr, t_axis, initial = 0)
        plt.figure()
        plt.plot(t_axis, curr)
        plt.show()
    #print(curr)
    return curr
# Function that interface with the user
def MotionControl(dist, m=1, order=3, space=2):
    # Generate Piecewise function
    start = time.time()
    peak = 2**order
    change = peak/2
    const = peak/2*space
    for i in range(order-1):
        change += peak/(2**(i+2))*space*(2**i)
    l = int(2*change+const)
    t_axis = np.linspace(0., l, l*10**order+1)
    y = []
    for i in range(len(t_axis)):
        y.append(Piecewise(t_axis[i], m, order, space))
    plt.figure()
    plt.plot(t_axis, y)
    plt.show()
    # Generate unscaled velocity scurve
    v = scurve(m, order, y, t_axis)
    # Generate dispalcement scurve
    d = integrate.cumtrapz(v, t_axis, initial = 0)
    plt.figure()
    plt.plot(t_axis, d)
    plt.show()
    # Scale velocity scurve based on displacement
    #print(d[-1])
    ratio = dist/d[-1]
    t_axis = np.linspace(0., l*ratio, l*10**order+1)
    v = np.asarray(v)*ratio
    plt.figure()
    v = plt.plot(t_axis, v)
    plt.show()
    print(time.time()-start)
# Testing MotionControl
MotionControl(100)
#MotionControl(175, 2, 4, 3)
#MotionControl(420, 1, 5, 4)
