#!/usr/bin/python3

import sys
import signal
import pickle
from scapy.all import *

def main():

	timeToLive = 50
	target = "www.facebook.com"

	for x in range(1,timeToLive):
		icmp = ICMP()
		icmp.type=8
		pkt = IP(dst=target, ttl=x)/icmp/"XXXX"
		icmpPacket = sr1(pkt, verbose=0)
		if (icmpPacket[ICMP].type == 11):
			print("Time Exceeded en la IP: ", icmpPacket[IP].src)
		else:
			print("Llegaste hasta: ", target)
		#Esto fue de prueba, sino les anda pruebenlo igual entiendo que si está en el scope del FOR no debería importar.
		#del(pkt.getlayer(IP).chksum) 

if __name__ == "__main__":
	main()

#ip = IP(dst=target, ttl=timeToLive)
##traceroute(["www.google.com"], maxttl=20)
#icmpPacket = sr1(ip/icmp/"XXXXXXXX")
#icmpPacket[0].display()
#print(icmpPacket[IP].src)
##icmpPacket.show()
##print(icmpPacket[ICMP].src)
##print(icmpPacket[ICMP].type)
#timeToLive += 1
#while (icmpPacket[ICMP].type == 11):
#	#print(icmpPacket[ICMP].src)
#	print(timeToLive)
#	print(icmpPacket[IP].src)
#	ip = IP(dst=target, ttl=timeToLive)
#	icmpPacket = sr1(ip/icmp/"XXXXXXXX")
#	#icmpPacket.show()
#	timeToLive+=1
#	
#print(icmpPacket[ICMP].src)
