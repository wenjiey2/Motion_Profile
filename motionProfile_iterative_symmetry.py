import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import time
#from pympler import summary
#from pympler import muppy

#all_objects = muppy.get_objects()
#print(len(all_objects))
#sum1 = summary.summarize(all_objects)
#summary.print_(sum1)

# Generate scurve of velocity
def scurve(order, y, t_axis, scale, space, total, plot = True):
    curr = y
    t = t_axis
    extra = space
    for i in range(order):
        curr = integrate.cumtrapz(curr, t, initial = 0)
        if(t[-1]*2 < total):
            curr = curr[:len(curr)-1]
            extra = extra*2
            gap = np.zeros(extra*scale)
            temp = np.append(-curr, 0)
            curr = np.append(curr, gap)
            curr = np.append(curr, temp)
            t = np.linspace(0., t[-1]*2+extra, (len(t)-1)*2+extra*scale+1)
    if(plot):
        plt.figure()
        plt.plot(t, curr)
        plt.show()
    return curr

# Function that interface with the user
def MotionControl(dist, total_time, order=3, space=2, plot = False):
    # Generate only the first section of the piecewise function to save runtime
    start = time.time()
    scale = int(5**order/order+50)
    peak = 2**order
    change = peak/2
    const = peak*space/2
    for i in range(order-1):
        change += peak/(2**(i+2))*space*(2**i)
    l = 2+space
    total = int(2*change+const)
    t_axis = np.linspace(0., l, l*scale+1)
    print(time.time()-start)

    # generate data points for y
    num = space*scale
    y = np.full(scale, 1)
    gap = np.zeros(num)
    gap = np.append(gap, -y)
    y = np.append(y, gap)
    y = np.append(y, 0)

    # plot the piecewise function
    if(plot):
        plt.figure()
        plt.plot(t_axis, y)
        plt.show()
    print(time.time()-start)

    # Generate velocity scurve
    v = scurve(order, y, t_axis, scale, space, total, plot)
    print(time.time()-start)

    # Generate dispalcement scurve
    t_axis = np.linspace(0., total, total*scale+1)
    d = integrate.cumtrapz(v, t_axis, initial = 0)
    v = None
    if(plot):
        plt.figure()
        plt.plot(t_axis, d)
        plt.show()
    print(time.time()-start)

    # Scale displacement scurve based on actual displacement & total time
    dr = dist/d[-1]
    tr = total_time/total
    t_axis = np.linspace(0., total*tr, total*scale+1)
    d = d*dr
    if(plot):
        plt.figure()
        plt.plot(t_axis, d)
        plt.show()
    print(time.time()-start)

    # Take another derivative for scaled velocity scurve
    v = np.diff(d)/np.diff(t_axis)
    v = np.append(v, 0)
    if(plot):
        plt.figure()
        plt.plot(t_axis, v)
        plt.show()
    print(time.time()-start)

# Testing MotionControl
MotionControl(5, 1, 2, 2, plot = True)
#MotionControl(100, plot = True)
#MotionControl(10, 20, 4, 3, plot = True)
#MotionControl(420, 30, 5, 4, plot = True)
#MotionControl(50, 10, 6, 4, plot = True)
#MotionControl(50, 10, 7, 2, plot = True)
#MotionControl(1000, 80, 8, 2)
#sum1 = summary.summarize(all_objects)
#summary.print_(sum1)
