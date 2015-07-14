#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import math
import re
import sys

def plot_gauss():
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

def plot_zrtt_treshold(data, output_path):
    threshold = 1
    gateways, zrtts = [], []
    for hop in data:
        ip, pais, zrtt = hop
        gateways.append(ip+"\n"+pais)
        zrtts.append(float(zrtt))
    gateways.reverse()
    zrtts.reverse()
    
    fig = plt.figure()
    y_pos = np.arange(len(gateways))
    plt.barh(y_pos, zrtts, align='center', alpha=0.4)
    plt.yticks(y_pos, gateways, horizontalalignment='right', fontsize=9)
    plt.title('ZRTTs para cada hop')
    plt.xlabel('ZRTT')
    plt.ylabel('Hop')

    # Line at y=0
    plt.vlines(0, -1, len(gateways), alpha=0.4)

    # ZRTT threshold
    plt.vlines(threshold, -1, len(gateways), linestyle='--', color='b', alpha=0.4)
    plt.text(threshold, len(gateways) - 1, 'Umbral', rotation='vertical',
             verticalalignment='top', horizontalalignment='right')
    fig.set_size_inches(6, 9)
    plt.tight_layout() 
    plt.savefig(output_path, dpi=1000, box_inches='tight')

filename = sys.argv[1]
output_path = filename[:-4]+".png"
data = []
with open(sys.argv[1]) as f:
    lineas = f.readlines()
for linea in lineas:
    valores = linea.split(",")
    tupla = (valores[0], valores[3], valores[1])
    data.append(tupla)
plot_zrtt_treshold(data, output_path)

