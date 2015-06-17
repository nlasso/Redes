#!/bin/bash

./main.py berkeley.edu 50 berkeley.txt berkeleyIPs.txt> results/berkeley.dat # Universidad de Berkeley, California, EEUU
./main.py test berkeley.edu > results/berkeley_throughput.dat # Universidad de Berkeley, California, EEUU
echo "Completado berkley.edu"

./main.py en.psu.ru 50 perm.txt permIPs.txt> results/psu.dat # Perm State University -- Universidad en Perm, Rusia
./main.py test en.psu.ru > results/psu_throughput.dat
echo "Completado en.psu.ru"

./main.py www.univ-antananarivo.mg 50 madagascar.txt madagascarIPs.txt> results/antananarivo.dat # Universidad de Madagascar (Este de Africa)
./main.py test www.univ-antananarivo.mg > results/antananarivo_throughput.dat
echo "Completado antananarivo (que nombre!)"

./main.py english.hi.is 50 iceland.txt icelandIPs.txt> results/hi.dat # Iceland University
./main.py test english.hi.is > results/hi_throughput.dat
echo "Completado Islandia"

#./main.py www.mu.ac.in 50 > results/muac.dat # Universidad de Bombay (India)
#./main.py test www.mu.ac.in > results/muac_throughput.dat
#echo "Completado mu.ac (Bombay - India)"

./main.py www.u-tokyo.ac.jp 50 tokyo.txt tokyoIPs.txt> results/tokyo.dat # Universidad de Tokyo, Japón
./main.py test www.u-tokyo.ac.jp > results/tokyo_throughput.dat
echo "Compeltado Tokyo"
