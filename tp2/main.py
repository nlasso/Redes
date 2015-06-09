#!/usr/bin/python3

import sys
import signal
import pickle
from scapy.all import *

def main():
	timeToLive = 1
	target = "www.facebook.com"

	while True:
		pass
		icmp = ICMP()
		icmp.type=8
		pkt = IP(dst=target, ttl=timeToLive)/icmp/"XXXX"
		icmpPacket = sr1(pkt, verbose=0, timeout=2)
		if (not (icmpPacket is None)):
			icmpPacket[0].display()
			if (icmpPacket[ICMP].type == 11):
				print("Time Exceeded en la IP: ", icmpPacket[IP].src)
			else:
				print("Llegaste hasta", target, " que tiene la IP: ", icmpPacket[IP].src)
				break
		timeToLive += 1

if __name__ == "__main__":
	main()
