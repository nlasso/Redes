#!/usr/bin/env python

import re

f = open("/dev/stdin")
lines = f.readlines()
hopNum = 0
for line in lines:
  match = re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}", line)
  if match is not None:
    if hopNum == 0:
        print "%s" % (match.group())
    else:
        print "%d %s 11 1" % (hopNum, match.group())
    hopNum += 1
