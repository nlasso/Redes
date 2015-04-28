#!/usr/bin/python3

import sys
import signal
import pickle
from scapy.all import *

ether_types = {
	0x0800 : "IPv4",
	0x0806 : "ARP",
	0x0842 : "Wake-on-LAN",
	0x22F0 : "Audio Video Transport Protocol as defined in IEEE Std 1722-2011",
	0x22F3 : "IETF TRILL Protocol",
	0x6003 : "DECnet Phase IV",
	0x8035 : "Reverse Address Resolution Protocol",
	0x809B : "AppleTalk (Ethertalk)",
	0x80F3 : "AppleTalk Address Resolution Protocol (AARP)",
	0x8100 : "VLAN-tagged frame (IEEE 802.1Q) & Shortest Path Bridging IEEE 802.1aq[4]",
	0x8137 : "IPX",
	0x8138 : "IPX",
	0x8204 : "QNX Qnet",
	0x86DD : "IPv6",
	0x8808 : "Ethernet flow control",
	0x8809 : "Slow Protocols (IEEE 802.3)",
	0x8819 : "CobraNet",
	0x8847 : "MPLS unicast",
	0x8848 : "MPLS multicast",
	0x8863 : "PPPoE Discovery Stage",
	0x8864 : "PPPoE Session Stage",
	0x8870 : "Jumbo Frames[2]",
	0x887B : "HomePlug 1.0 MME",
	0x888E : "EAP over LAN (IEEE 802.1X)",
	0x8892 : "PROFINET Protocol",
	0x889A : "HyperSCSI (SCSI over Ethernet)",
	0x88A2 : "ATA over Ethernet",
	0x88A4 : "EtherCAT Protocol",
	0x88A8 : "Provider Bridging (IEEE 802.1ad) & Shortest Path Bridging IEEE 802.1aq[5]",
	0x88AB : "Ethernet Powerlink[citation needed]",
	0x88CC : "Link Layer Discovery Protocol (LLDP)",
	0x88CD : "SERCOS III",
	0x88E1 : "HomePlug AV MME[citation needed]",
	0x88E3 : "Media Redundancy Protocol (IEC62439-2)",
	0x88E5 : "MAC security (IEEE 802.1AE)",
	0x88F7 : "Precision Time Protocol (PTP) over Ethernet (IEEE 1588)",
	0x8902 : "IEEE 802.1ag Connectivity Fault Management (CFM) Protocol / ITU-T Recommendation Y.1731 (OAM)",
	0x8906 : "Fibre Channel over Ethernet (FCoE)",
	0x8914 : "FCoE Initialization Protocol",
	0x8915 : "RDMA over Converged Ethernet (RoCE)",
	0x892F : "High-availability Seamless Redundancy (HSR)",
	0x9000 : "Ethernet Configuration Testing Protocol[6]",
	0xCAFE : "Veritas Low Latency Transport (LLT)[7] for Veritas Cluster Server"
}



def signal_handler(signal, frame):
	print_output()
	save_output()
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def entropy(source):
	total = sum(source.values())
	probabilities = [occurrences/total for occurrences in source.values()]
	return -sum([prob*log(prob, 2) for prob in probabilites])


pkgs_by_type, traffic_by_type, arp_who_src, arp_who_dst, arp_is_src, arp_is_dst = data = [defaultdict(int) for _ in range(6)]
pkgs_by_type["desc"] = "Cantidad de paquetes por 'type' (capa 2)"
traffic_by_type["desc"] = "Tamaño de paquetes por 'type' (capa 2)"
arp_who_src["desc"] = "IPs emisoras de ARP who-has"
arp_who_dst["desc"] = "IPs buscadas por ARP who-has"
arp_is_src["desc"] = "IPs emisoras de ARP is-at"
arp_is_dst["desc"] = "IPs receptoras de ARP is-at"


def pkg_handler(pkg):
	if pkg.haslayer(Ether):
		ether_type = pkg[Ether].type
		pkgs_by_type[ether_type] += 1
		try:
			traffic_by_type[ether_type] += len(pkg)
		except IndexError:
			pass
		if pkg.haslayer(ARP):
			arp = pkg[ARP]
			if arp.op == 1:  # who-has
				arp_who_src[arp.psrc] += 1
				arp_who_dst[arp.pdst] += 1
			if arp.op == 2:  # is-at
				arp_is_src[arp.psrc] += 1
				arp_is_dst[arp.pdst] += 1


def print_output():
	for d in data:
		print()
		print_dict_count(d)


def save_output():
	with open("output", 'wb') as output_file:
		pickle.dump(data, output_file)


def print_dict_count(d):
	print(d["desc"], ":")
	for key in d:
		if key != "desc":
			text = key
			if key in ether_types:
				text = ether_types[key]
			print(text, ":", d[key])


if __name__=="__main__":
	sniff(prn=pkg_handler, count=0)
