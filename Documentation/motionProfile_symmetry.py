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
def scurve(m, order, y, t_axis, plot = True):
    curr = y;
    for i in range(order):
        curr = integrate.cumtrapz(curr, t_axis, initial = 0)
        if(plot):
            plt.figure()
            plt.plot(t_axis, curr)
            plt.show()
    return curr

# Function that interface with the user
def MotionControl(dist, m=1, order=3, space=2, plot = False):
    # Generate half of the piecewise function to save runtime
    start = time.time()
    scale = int(8**order/order+50)
    peak = 2**order
    change = peak/2
    const = change*space/2
    for i in range(order-1):
        change += peak/(2**(i+2))*space*(2**i)
    l = int(change+const)
    t_axis = np.linspace(0., l, l*scale+1)
    print(time.time()-start)

    # generate data points for y
    num = space*scale
    y = np.full(scale, m)
    temp = -y
    gap = np.zeros(num)
    y = np.append(y, gap)
    y = np.append(y, temp)
    y = np.append(y, gap)
    count = 1
    while(len(y) < l*scale):
        gap = np.zeros(count*num)
        y = np.append(y, gap)
        temp = -y
        y = np.append(y, temp)
        count *= 2
        gap = None
        temp = None
    y = np.append(y, 0)

    # plot the piecewise function
    if(plot):
        plt.figure()
        plt.plot(t_axis, y)
        plt.show()
    print(time.time()-start)

    # Generate unscaled half velocity scurve
    v = scurve(m, order, y, t_axis, plot)
    print(time.time()-start)

    # Restore the full velocity scurve
    v = v[:len(v)-1]
    temp = v[::-1]
    v = np.append(v, temp)
    v = np.append(v, 0)
    t_axis = np.linspace(0., l*2, l*scale*2+1)
    if(plot):
        plt.figure()
        plt.plot(t_axis, v)
        plt.show()
    print(time.time()-start)

    # Generate dispalcement scurve
    d = integrate.cumtrapz(v, t_axis, initial = 0)
    if(plot):
        plt.figure()
        plt.plot(t_axis, d)
        plt.show()
    print(time.time()-start)

    # Scale velocity scurve based on displacement
    #print(d[-1])
    ratio = dist/d[-1]
    d = None
    t_axis = np.linspace(0., l*ratio*2, l*scale*2+1)
    v = np.asarray(v)*ratio
    print(time.time()-start)
    if(plot):
        plt.figure()
        v = plt.plot(t_axis, v)
        plt.show()

# Testing MotionControl
#MotionControl(100, 1, 2, 2, plot = True)
#MotionControl(100, plot = True)
MotionControl(175, 1, 4, 3, plot = True)
#MotionControl(420, 1, 5, 4, plot = True)
#MotionControl(5000, 1, 6, 4, plot = True)
#MotionControl(60000, 1, 7, 2)
#sum1 = summary.summarize(all_objects)
#summary.print_(sum1)
