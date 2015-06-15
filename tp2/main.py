#!/usr/bin/python3

import sys
import signal
import pickle
import time, math
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from statistics import mean, stdev

def main(target, reps):
	ECHO_REQUEST_TYPE = 8
	TTL_EXPIRED_IN_TRANSIT = 11
	timeToLive = 1
	rtts = []
	jumps = []
	ttls = []

	icmp = ICMP()
	icmp.type= ECHO_REQUEST_TYPE

	# Exploro los saltos
	while True:
		# Preparo paquete y mido tiempo
		pkt = IP(dst=target, ttl=timeToLive)/icmp/"X"
		startTime = time.time()
		icmpPacket = sr1(pkt, verbose=0, timeout=2)
		endTime = time.time()
		print("TTL=", timeToLive)
		if (not (icmpPacket is None)):
			# Calculo RTT
			rttTotal = (endTime - startTime) * 1000
			rttDec, rtt = math.modf(rttTotal)
			rtts.append(rtt)
			jumps.append(icmpPacket[IP].src)
			ttls.append(timeToLive)
			if (icmpPacket[ICMP].type == TTL_EXPIRED_IN_TRANSIT):
				print("Time Exceeded en la IP: ", icmpPacket[IP].src)
				print("El RTT para esta IP", icmpPacket[IP].src, " fue de: ", rtt)
			else:
				print("Llegaste hasta", target, " que tiene la IP: ", icmpPacket[IP].src)
				break
		timeToLive += 1

		if timeToLive > 35:
			print("ERROR: El host " + target + " es inalcanzable")
			exit()

	# Mido ZRTT
	avg_rtts = rtts
	total_rtts = [rtts]
	rtts = []

	for rep in range(1,reps):
		print ("Ejecutando repeticion " + str(rep) + "...")

		for i in range(0,len(jumps)):

			# Preparo paquete y mido tiempo
			pkt = IP(dst=jumps[i], ttl=ttls[i])/icmp/"X"
			startTime = time.time()
			icmpPacket = sr1(pkt, verbose=0, timeout=2)
			endTime = time.time()
			
			# Calculo RTT
			rttTotal = (endTime - startTime) * 1000
			rttDec, rtt = math.modf(rttTotal)
			rtts.append(rtt)

			# Sumo RTT
			#print(jumps[i])
			#print(avg_rtts[i])
			avg_rtts[i] += rtt
			#print(rtt)
			#print(avg_rtts[i])
		total_rtts.append(rtts)

	for i in range(0, len(avg_rtts)):
		avg_rtts[i] /= reps

	zrtts = []
	for i in range(0, len(avg_rtts)):
		zrtt = (avg_rtts[i]-mean(avg_rtts))/stdev(avg_rtts)
		zrtts.append(zrtt)

	#print(len(zrtts), len(avg_rtts), len(jumps))
	return (zrtts, avg_rtts, total_rtts, jumps)



if __name__ == "__main__":

	if len(sys.argv) < 2:
		print("ERROR: Debe especificar una URL o IP de destino")
		exit()

	if len(sys.argv) < 3:
		reps = 1
	else:
		reps = int(sys.argv[2])

	(zrtts, avg_rtts, total_rtts, jumps) = main(sys.argv[1], reps)

	print(zrtts)
	print(avg_rtts)
	print(total_rtts)
	print(jumps)


