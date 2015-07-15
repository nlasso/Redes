#!/bin/bash
./parse_throughput.py berkeley_throughput.dat
./parse_throughput.py cusat_throughput.dat
./parse_throughput.py hi_throughput.dat
./parse_throughput.py psu_throughput.dat
./parse_throughput.py pretoria_throughput.dat

cd data
./berkeley_chart.pg
./cusat_chart.pg
./hi_chart.pg
./psu_chart.pg
./pretoria_chart.pg

cp berkeley.pdf ../graphs/berkeley_rtt.pdf
cp cusat.pdf ../graphs/cusat_rtt.pdf
cp hi.pdf ../graphs/hi_rtt.pdf
cp psu.pdf ../graphs/psu_rtt.pdf
cp pretoria.pdf ../graphs/pretoria_rtt.pdf