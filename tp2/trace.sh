#!/bin/bash

./main.py berkeley.edu 50 > results/berkeley.dat # Universidad de Berkeley, California, EEUU
echo "Completado berkley.edu"

./main.py en.psu.ru 50 > esults/psu.dat # Perm State University -- Universidad en Perm, Rusia
echo "Completado en.psu.ru"

./main.py www.univ-antananarivo.mg 50 > results/antananarivo.dat # Universidad de Madagascar (Este de Africa)
echo "Completado antananarivo (que nombre!)"

./main.py english.hi.is 50 > results/hi.dat # Iceland University
echo "Completado Islandia"

./main.py www.mu.ac.in 50 > results/muac.dat # Universidad de Bombay (India)
echo "Completado mu.ac (Bombay - India)"

./main.py www.u-tokyo.ac.jp 50 > results/tokyo.dat # Universidad de Tokyo, Japón
echo "Compeltado Tokyo"
