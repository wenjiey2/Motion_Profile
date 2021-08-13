import numpy as np
import math
import matplotlib.pyplot as plt
import time
import pickle

import scipy.integrate as integrate

# Sampling algorithm
def scurve(order, y, t_axis, scale, space, total, plot = True):
    curr = y
    t = t_axis
    extra = space
    for i in range(order):
        curr = integrate.cumtrapz(curr, t, initial = 0)
        curr = np.round(curr, 3)
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
    l = 2+space
    scale = 100
    peak = 2**order
    change = peak/2
    const = peak*space/2
    for i in range(order-1):
        change += peak/(2**(i+2))*space*(2**i)
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
    #print("maxD", d[-1])
    dr = dist/d[-1]
    tr = total_time/total
    if(tr < 1):
        d = d[0:len(d):int(1/tr)]
        t_axis = np.linspace(0., total*tr, len(d))
    else:
        d = interpolation.zoom(d,tr)
        t_axis = np.linspace(0., total*tr, len(d))
    d = d*dr
    if(plot):
        #plt.figure()
        plt.plot(t_axis, d, label="order="+str(order)+", spacing="+str(space))
        plt.legend(loc='upper right')
        #plt.show()
    print(time.time()-start)

    # Take another derivative for scaled velocity scurve
    v = np.diff(d)/np.diff(t_axis)
    v = np.append(v, 0)
    if(True):
        #plt.figure()
        plt.plot(t_axis, v, label="order="+str(order)+", spacing="+str(space))
        plt.legend(loc='upper right')
        #plt.show()
    print(time.time()-start)

#     a = np.diff(v)/np.diff(t_axis)
#     a = np.append(a, 0)
#     #print("amount of jerk:", np.amax(a))
#     j = np.diff(a)/np.diff(t_axis)
#     j = np.append(j, 0)
#     #print("maxJ", max(j))
#     p = np.diff(j)/np.diff(t_axis)
#     p = np.append(p, 0)
#     plt.plot(t_axis, j, label="order="+str(order))
#     plt.legend(loc='upper right')



# formulation algorithm
def Magnitude(order):
    m = np.array([1, 0, -1])
    for i in range(order-1):
        temp = np.append(0, -m)
        m = np.append(m, temp)
    return m
def PW_Width(order, space):
    intervals = np.array([1, space, 1])
    #bounds = [0]
    for i in range(order-1):
        temp = np.append(2*intervals[int(len(intervals)/2)], intervals)
        intervals = np.append(intervals, temp)
    #bounds.append(intervals[0])
    #for i in range(1, len(intervals)):
    #    bounds.append(bounds[-1]+intervals[i])
    return intervals
def Indefinite_Integral(num):
    f = 1
    ii = [f]
    for i in range(num):
        f = f/(i+1)
        ii.append(f)
    return ii
def PW(order, m, w, space, ii):
    l = 2**(order+1) - 1
    pw = []
    c = []
    # first interval of all orders
    pw.append([[[1], 1]])
    for j in range(order+1):
        f = ii[j+1]
        f1 = []
        for itr in range(j):
            f1.append(0)
        f1.append(f)
        pw[0].append([f1, f])
#     print(pw)
    #print(m[255])
    # later intervals which depend on the previous offsets
    total_time = np.zeros(l+1)
    total_time[1] = 1
    t = 1
    offset = 0
    for i in range(1, l):
        if m[i] == -1:
            pw.append([[[-1], -1]])
            c.append([-1])
        elif m[i] == 1:
            pw.append([[[1], 1]])
            c.append([1])
        elif m[i] == 0:
            pw.append([[[0], 0]])
        #print(pw)
        is_zero = int(m[i] == 0)
        if is_zero:
            is_zero += int(math.log(w[i], space))-1
            for j in range(is_zero - 1):
                pw[i].append([[0], 0])
            pw[i].append([[1], pw[i-1][is_zero][1]])
            c.append([pw[i-1][is_zero][1]])
#         if i == 254:
#             print("i=", i, "pw=", pw[i])
        idx = 1
        t_next = t + w[i]
        total_time[i+1] = t_next
        for j in range(is_zero, order+1):
            f = np.zeros(idx+1)
            #print(c)
#             if i == 254:
#                 print("i=", c[i-1])
            for num in range(idx):
                f[num+1] = ii[num+1]*c[i-1][-num-1]
#             print(f)
            k = pw[i-1][j+1][1] - evaluate(f, t)
#             if i == 254:
#                 print("pw=", pw[i-1], "t=", t, "eval=", evaluate(f, t))
            c[i-1].append(k)
            #print(c)
            f[0] = k
            #print(f)
            offset = evaluate(f, t_next)
            #print(offset)
            pw[i].append([f, offset])
            idx += 1
        t = t_next
        #print(pw)
    piecewise = [total_time, pw]
#     with open("test1.pkl", "wb") as f:
#         pickle.dump(piecewise, f)
    np.save("test1.npy", piecewise)
    #print(pw)

def evaluate(arr, num):
    sum = 0
    for i in range(len(arr)):
        sum += arr[i]*num**i
    return sum

def evaluate_dsc(arr, num, order):
    sum = 0
    if len(arr) == 1:
        sum = arr[0]*(num**order)
    else:
        for i in range(len(arr)):
            sum += arr[i]*num**i
    return sum

def diff_coef(arr, order):
    for i in range(len(arr)):
        if len(arr[i]) == 1:
            arr[i][0] *= order
        else:
            for j in range(len(arr[i])):
                arr[i][j] *= j
    return arr

def v_scurve(dist, total_time, data, order=3, plot = False):
    l = 2**(order+1) - 1
    d_ratio = dist / data[1][l][order+1][1]
#     print("dratio:", data[1][l][order+1])
    formulas = []
    #print(data[1][0][order+1][0])
    for i in range(l):
        formulas.append([])
        for e in range(len(data[1][i][order+1][0])):
            formulas[-1].append(data[1][i][order+1][0][e] * d_ratio)
    bounds = np.asarray(data[0][:l+1])
    #print(bounds)
#     v_pw = diff_coef(formulas, order+1)
#     print(v_pw[0])
    d = []
    j = 0
    f = 0
    t_unscaled = np.arange(0, data[0][l], 0.01)

    for i in t_unscaled:
        if i > bounds[j+1]:
            j += 1
        f = evaluate_dsc(formulas[j], i, order+1)
        #print(f)
        d.append(f)
    t_scaled = np.linspace(0, total_time, len(t_unscaled))
    #print(v)
    if(plot):
        v = np.diff(d)/np.diff(t_scaled)
        v = np.append(v, 0)
        a = np.diff(v)/np.diff(t_scaled)
        a = np.append(a, 0)
        #print("amount of jerk:", np.amax(a))
        #jk = np.diff(a)/np.diff(t_scaled)
        #jk = np.append(jk, 0)
        plt.plot(t_scaled, v, label="order="+str(order)+" formula")
        plt.legend(loc='upper right')
        #plt.show()
# this part can be precomputed
%matplotlib
start = time.time()
ii = Indefinite_Integral(20)
#print(ii)
print("Basic form of indefinite integral: ", time.time()-start)
start = time.time()
m = Magnitude(10)
print("Basic impulse pattern:", time.time()-start)
start = time.time()
w = PW_Width(10, 2)
print(w)
print("PW_Width:", time.time()-start)

start = time.time()
PW(8, m, w, 2, ii)
print("PW:", time.time()-start)

start = time.time()
# with open("test1.pkl", "rb") as f:
#     data = pickle.load(f)
data = np.load("test1.npy", allow_pickle=True)
#print(data)
print("Loading:", time.time()-start)

# real time
start = time.time()
#v_scurve(50, 10, data, 7, 2, True)
print("v_scurve", time.time()-start)
#MotionControl(50, 10, 5, 2)
v_scurve(50, 10, data, 6, True)
MotionControl(50, 10, 5, 2)
MotionControl(50, 10, 5, 2)
