#!/usr/bin/python

import sys
import re

if len(sys.argv) < 2:
    print "Error: Source file name needed"
    exit()

f = open(sys.argv[1], 'r')
f_prefix = sys.argv[1].split(".")[0]
o = None

for line in f:
    m = re.match("^(\s|\t*)?([A-Z][A-Z ]*):\s*([0-9]+(\.[0-9]*)?)", line)
    if m != None:
        if m.group(2) == "ALPHA":
            if o != None:
                o.close()
            o = open("data/"+f_prefix+"_A"+m.group(3)+".gdat", 'w')
        if m.group(2) == "REPS":
            o.write(m.group(3)+" ")
        if m.group(2) == "ESTIMATED RTT":
            o.write(m.group(3)+" ")
        if m.group(2) == "ESTIMATED THROUGHPUT":
            o.write(m.group(3)+"\n")