#!/usr/bin/python3

from __future__ import print_function
import sys
import signal
import pickle
import time, math
import logging
import urllib.request
import json
from socket import gethostbyname
from statistics import mean, stdev
from scapy.all import *

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

ECHO_REQUEST_TYPE = 8
TTL_EXPIRED_IN_TRANSIT = 11

def get_rtt(target, ttl=35):
    icmp = ICMP()
    icmp.type= ECHO_REQUEST_TYPE
    pkt = IP(dst=target, ttl=ttl)/icmp/"X"
    startTime = time.time()
    response = sr1(pkt, verbose=0, timeout=2)
    endTime = time.time()
    rttTotal = (endTime - startTime) * 1000
    return response, rttTotal

def explore_hops(target, target_txt):
    timeToLive = 1
    rtts = []
    hops = []
    ttls = []
    while timeToLive < 35:
        response, rtt = get_rtt(target, timeToLive)
        print("TTL=", timeToLive)
        if not response is None:
            rtts.append(rtt)
            hops.append(response[IP].src)
            ttls.append(timeToLive)
            if response[ICMP].type == TTL_EXPIRED_IN_TRANSIT:
                print("El RTT para esta IP", response[IP].src, "fue de:", rtt)
            else:
                print("Llegaste hasta", target_txt, "que tiene la IP:", response[IP].src)
                break
        timeToLive += 1
    if timeToLive == 35:
        print("ERROR: El host" + target + "es inalcanzable")
    return rtts, hops, ttls


def main(target_txt, reps):
    target = gethostbyname(target_txt)

    rtts, hops, ttls = explore_hops(target_txt, target)

    # Mido ZRTT
    avg_rtts = rtts
    total_rtts = [rtts]
    rtts = []

    for rep in range(1, reps):
        print ("Ejecutando repeticion", str(rep), "...")
        for i in range(0, len(hops)):
            response, rtt = get_rtt(target, ttls[i])
            if response is None or hops[i] != response[IP].src:
                print("WARNING: La ruta parece haber cambiado")
                print("Quería llegar a", hops[i], "pero me respondió", response[IP].src if not response is None else response)
            rtts.append(rtt)
            avg_rtts[i] += rtt
        total_rtts.append(rtts)

    # Promedio
    for i in range(0, len(avg_rtts)):
        avg_rtts[i] /= reps

    # Deltas
    delta_rtts = [avg_rtts[1]]
    for i in range(1, len(avg_rtts)):
        delta_rtts.append(avg_rtts[i] - avg_rtts[i-1])

    # ZRTT
    zrtts = []
    for delta_rtt in delta_rtts:
        zrtt = (delta_rtt - mean(delta_rtts)) / stdev(delta_rtts)
        zrtts.append(zrtt)

    return zrtts, avg_rtts, hops


def test_connection(target_txt, alpha=0.1, reps=10):
    target = gethostbyname(target_txt)
    n_reply = 0
    n_request = 0
    estimated_rtt = None
    for i in range(reps):
        response, sample_rtt = get_rtt(target)
        n_request += 1
        if response is None:
            continue
        else:
            n_reply += 1
        if estimated_rtt is None:
            estimated_rtt = sample_rtt
        else:
            estimated_rtt = alpha * estimated_rtt + (1 - alpha) * sample_rtt
    if estimated_rtt is None:
        print("ERROR: No hubo respuesta alguna")
        return 0, 0
    estimated_packet_loss_probability = n_reply / n_request
    MSS = get_mss()
    estimated_throughput = MSS / estimated_rtt * (1 / math.sqrt(estimated_packet_loss_probability))
    return estimated_rtt, estimated_throughput


def get_mss():
    r = sr1(IP(dst="dc.uba.ar")/TCP(dport=[80], flags="S"), verbose=0, timeout=2)
    options = r.payload.options
    for option, value in options:
        if option == "MSS":
            return value

def tableOutput(hops, zrtts, avg_rtts):
	myFile = open('output.txt', 'w')
	latexHeader = '\\begin{tabular}{|l@{\hspace{5ex}}c@{\hspace{5ex}}l|}\n'
	hline = '\\hline\n'
	tableHeader = '\\rule{0pt}{1.2em}IP & ZRTT & AVG\\_RTT & PAIS & CIUDAD\\\\[0.2em]\n'
	latexFooter = '\\end{tabular}\n'
	print(latexHeader, hline, tableHeader, hline, file=myFile)

	for i, hop in enumerate(hops):
		url = 'http://api.hostip.info/get_json.php?ip=' + hop
		response = urllib.request.urlopen(url).read().decode("utf-8")
		temp = json.loads(response)
		city = temp['city']
		country = temp['country_name']
		print('\\rule{0pt}{1.2em}', hop, ' & ', zrtts[i], '&', avg_rtts[i], '&' ,country , '&' , city, '\\\\[0.2em]', file=myFile)

	print(hline, latexFooter, file=myFile)
	myFile.close()

if __name__ == "__main__":
	assert len(sys.argv) >= 2, "You must provide a target"
	if "test" in sys.argv:
		target = sys.argv[2]
		for alpha in [i*0.1 for i in range(1, 10)]:
			print("ALPHA: ", alpha)
			for reps in range(10, 60, 10):
				print("\tREPS: ", reps)
				estimated_rtt, estimated_throughput = test_connection(target)
				print("\t\tESTIMATED RTT: %f.3" % estimated_rtt)
				print("\t\tESTIMATED THROUGHPUT: %f.3" % estimated_throughput)
	if "print" in sys.argv:
		tableOutput()
	else:
		if len(sys.argv) < 3:
			reps = 1
		else:
			reps = int(sys.argv[2])
		zrtts, avg_rtts, hops = main(sys.argv[1], reps)
		#Print to file
		tableOutput(hops, zrtts, avg_rtts)
		#Print output to console
		for i, hop in enumerate(hops):
			print(hop)
			print("\tZRTT:", zrtts[i])
			print("\tAVG RTT:", avg_rtts[i])
