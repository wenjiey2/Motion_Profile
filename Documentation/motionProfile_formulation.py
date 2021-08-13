from sympy import *
from sympy.abc import x
import numpy as np
import time
start = time.time()
overallStart = time.time()
#p = Piecewise( (10, x<1), (0, x<2), (-10,x<3),(0, x<4), (-10, x<5), (0, x<6),
#(10, x<7), (0, sympify(1) <= x) )
#p = Piecewise( (10, x<1), (0, x<2), (-10,x<3),(0, x<4), (-10, x<5), (0, x<6),
#(10, x<7), (0, x<8), (-10, x<9), (0,x<10),(10, x<11), (0, x<12), (10, x<13),
#(0, x<14), (-10, x<15),  (0,True))
#create a piecewise with peaks of 1
def PW(order, space, total_time):
    curr_space = space
    pw_unscaled = [(1, x < 1), (0, x < 1+curr_space), (-1, x < 2+curr_space)]
    for i in range(order-1):
        temp = pw_unscaled.copy()
        curr_start = int(str(pw_unscaled[-1][1])[4:])
        curr_space = 2*curr_space
        curr_gap = (0, x < curr_start+curr_space)
        pw_unscaled.append(curr_gap)
        for j in temp:
            val = -j[0]
            ran = int(str(curr_gap[1])[4:]) + int(str(j[1])[4:])
            pw_unscaled.append((val, x < ran))    # rescale total time
    ratio = total_time / int(str(pw_unscaled[-1][1])[4:])
    pw = []
    for i in range(len(pw_unscaled)):
        pw.append((pw_unscaled[i][0], x < int(str(pw_unscaled[i][1])[4:])*ratio))
    #print(pw)
    return pw
order = 5
TotalDist = 10
TotalTime = 15
pwf = PW(order, 2, TotalTime)
print(pwf)
print(time.time()-start)
#format sumpy piecewise with creation function PW
p = Piecewise(*pwf, (0, sympify(1) <= x))
#print(p)
#check time to get set number of data points with lambdify instead of subs
#because it is 10x faster
f = lambdify(x,p)
start = time.time()
for i in np.arange(0,18,0.1):
    f(i)
print(time.time()-start)
pos = p
#integrate order + 1 times
for i in range(order +1 ):
    pos = integrate(pos)
###print(pos)
#checking time it takes for repeated integration
f = lambdify(x,pos)
start = time.time()
for i in np.arange(0,18,1):
    f(i)
print(time.time()-start)
#get first tuple in pos for formatting purpose
#Holder = str(pos.args[0])
Holder2 = []
#ammend each tuple until the len value with commas in order to create a
#tuple that can be used in the piecewise function
unscaledpos = pos.args[len(pos.args) - 1][0]
ScaleRatio = TotalDist/unscaledpos
ScaleHolder = []
#using rescaled pos
for i in range (0,len(pos.args)):
    #Holder = Holder + "," + str(pos.args[i])
    #find the scaled equation
    scaledEquation= pos.args[i][0]*ScaleRatio
    #make a list that has the correct format to be appended into holder2 because u cant assign directly into
    #pos.args[i][0]
    FormList = [scaledEquation , pos.args[i][1]]
    #Holder2.append(pos.args[i])
    Holder2.append(FormList)
#print(Holder2)
#reformat as a tuple
#res = tuple(eval(str(Holder2)))
#res = str(res)[1:len(str(res) )-1]    # remove brakets at ends of tuple
#unpack tuple into Usable Piecewise
UsablePiecewise = Piecewise(*Holder2)
#grab calculated position that needs to be scaled
print(UsablePiecewise)
#check recreated piecewise
#with low number of points checked the difference is marginal. can tell with
#an increased number of points
f = lambdify(x,UsablePiecewise)
start = time.time()
for i in np.arange(0,1,1):
    f(i)
print(time.time()-start)
print("total time is " + str(time.time() - overallStart))
