#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import math
import re
import sys

f = open("/dev/stdin")
lines = f.readlines()
hopNum = 0
xpoints = []
ypoints = []
for line in lines:
    match = re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3} , (-?\d+\.\d*)", line)
    xpoints.append(match.group(1))
    ypoints.append(0.01)
    

mean = 0
variance = 1
sigma = math.sqrt(variance)
x = np.linspace(-3,3,100)
plt.plot(x, mlab.normpdf(x,mean,sigma))

plt.plot(xpoints, ypoints, 'ro')
plt.xlabel("ZRTT (en desvíos standards)")

plt.savefig(sys.argv[1])