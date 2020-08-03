from sympy import *
from sympy.abc import x
import numpy as np
import time
start = time.time()

def PW(order, space):
    curr_space = space
    pw = [(1, 1), (0, 1+curr_space), (-1, 2+curr_space)]
    for i in range(order-1):
        temp = pw.copy()
        curr_start = pw[-1][1]
        curr_space = 2*curr_space
        curr_gap = (0, curr_start+curr_space)
        pw.append(curr_gap)
        for j in temp:
            val = -j[0]
            ran = curr_gap[1] + j[1]
            pw.append((val, ran))
    return pw

p_unformatted = PW(10, 2)
print(time.time()-start)

p_formatted = []
for i in p_unformatted:
    p_formatted.append((i[0], x<i[1]))
#print(p2)
p = Piecewise(*p_formatted, (0, sympify(1) <= x))
#print(p)
print(time.time()-start)

for i in range(3):
    p = integrate(p)
#print(p)
print(time.time()-start)

sample = []
for i in np.arange(0,10,0.1):
    sample.append(p.subs(x,i))

#print(sample)
print(time.time()-start)
