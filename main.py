#! /usr/bin/env python

import sys
from scapy.all import *

sniff(iface="ath0",prn=lambda x:x.sprintf("{Dot11Beacon:%Dot11.addr3%\t%Dot11Beacon.info%\t%PrismHeader.channel%\tDot11Beacon.cap%}"))

#p=sr1(IP(dst=sys.argv[1])/ICMP())
#if p:
#    p.show()