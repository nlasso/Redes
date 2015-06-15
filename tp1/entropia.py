#!/usr/bin/python3
import sys
import pickle
from math import *


def entropia(ips):
	N = sum(ips.values())
	Ps = [ k/N for k in ips.values() ]
	H = -sum([ p*log(p,2) for p in Ps ])
	return H


def leer_entrada():
	if len(sys.argv) < 2:
		print("Usage: " + sys.argv[0] + " nombre_de_archivo")
		exit(1)
	for filename in sys.argv[1:]:
		print(filename)
		with open(filename, 'rb') as archivo:
			data = pickle.load(archivo)
		imprimir_entropia(data)


def imprimir_entropia(data):
	field_names = ["pkgs_by_type", "traffic_by_type", "arp_who_src", "arp_who_dst", "arp_is_src", "arp_is_dst"]
	fields_by_name = {}

	for count, name in enumerate(field_names):
		fields_by_name[name] = data[count]

	for field_name in fields_by_name.keys():
		data = fields_by_name[field_name]
		field_description = data["desc"]
		del data["desc"]

		if "Tamaño" not in field_description:
			print("Entropía de", field_description, entropia(data))

leer_entrada()