#! /usr/bin/env python

import sys
from scapy.all import *

#pkg_handler: Por cada paquete que es Sniffeado, muestra el resumen.
pkg_handler = lambda x: x.summary()
#count = 0 -> leer infinitos paquetes
#SNIFF
sniff(prn=pkg_handler, count = 0)