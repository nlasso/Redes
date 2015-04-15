#!/usr/bin/python3

import sys
import signal
from scapy.all import *


def signal_handler(signal, frame):
	print_output()
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


pkgs_by_type = defaultdict(int)
arp_pkgs = defaultdict(int)
def pkg_handler(pkg):
	if pkg.haslayer(Ether):
		pkgs_by_type[(hex(pkg[Ether].type))] += 1
		if pkg.haslayer(ARP) and pkg[ARP].op == 1:	#who-is
			arp_pkgs[pkg[ARP].psrc] += 1


def print_output():
	print()
	print_dict_count(pkgs_by_type)
	print()
	print_dict_count(arp_pkgs)

def print_dict_count(d):
	for key in d:
		print(key, ":", d[key])


sniff(prn=pkg_handler, count=0)
