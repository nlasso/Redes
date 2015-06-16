#!/usr/bin/python3
import sys
import pickle

from main import ether_types
from matplotlib import pyplot as plt
from matplotlib import numpy as np

def leer_entrada():
	if len(sys.argv) < 2:
		print("Usage: " + sys.argv[0] + " nombre_de_archivo")
		exit(1)
	for filename in sys.argv[1:]:
		print(filename)
		with open(filename, 'rb') as archivo:
			data = pickle.load(archivo)
		graficar(data, filename)

def get_host_list(ips):
	return [int(ip.split(".")[3]) for ip in ips]

def get_ips_count_from_dict(d):
	values = list(d.values())
	keys = list(d.keys())
	return values, keys

def torta(ips_count, filename, field_name="", field_description=""):
	values, keys = get_ips_count_from_dict(ips_count)
	colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'blue', 'red', 'orange', 'yellow', 'white'] * 10
	plt.pie(values, labels=keys, autopct='%1.1f%%', shadow=True, colors=colors)
	plt.axis('equal')
	plt.savefig(str("imgs/" + filename + "-" + field_name + "-torta.png"))

def barras(ips_count, filename, field_name="", field_description=""):
	if len(ips_count) > 10:
		hosts = get_host_list(ips_count.keys())
	else:
		hosts = list(ips_count.keys())
	cant_ips = len(hosts)
	
	fig, ax = plt.subplots()
	index = np.arange(cant_ips)
	bar_width = 0.3
	opacity = 0.4
	rects1 = plt.bar(index, ips_count.values(), bar_width,
	                 alpha=opacity,
	                 color='b',
	                 label=field_description)
	plt.xlabel('IPs')
	plt.ylabel('Cantidad' if 'Tamaño' not in field_description else 'Bytes') 
	plt.xticks(index + bar_width, hosts)
	plt.tight_layout()
	plt.legend(framealpha=0.5)
	plt.savefig(str("imgs/" + filename + "-" + field_name + ".png"))


def graficar(data, filename):
	field_names = ["pkgs_by_type", "traffic_by_type", "arp_who_src", "arp_who_dst", "arp_is_src", "arp_is_dst"]
	fields_by_name = {}

	for count, name in enumerate(field_names):
		fields_by_name[name] = data[count]

	for field_name in fields_by_name.keys():
		data = fields_by_name[field_name]
		field_description = data["desc"]
		del data["desc"]

		if "type" in field_name:
			new_data = {}
			for key in data.keys():
				try:
					new_data[ether_types[key]] = data[key]
				except KeyError:
					new_data[hex(key)] = data[key]
			data = new_data

		barras(data, filename, field_name, field_description)
		plt.close()
		if "Tamaño" not in field_description:
			torta(data, filename, field_name, field_description)
			plt.close()

leer_entrada()