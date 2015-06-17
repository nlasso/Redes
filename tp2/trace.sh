#!/bin/bash

./main.py berkeley.edu 50 > results/berkeley.dat # Universidad de Berkeley, California, EEUU
./main.py test berkeley.edu > results/berkeley_throughput.dat # Universidad de Berkeley, California, EEUU
echo "Completado berkley.edu (Estados unidos)"

./main.py en.psu.ru 50 > results/psu.dat # Perm State University -- Universidad en Perm, Rusia
./main.py test en.psu.ru > results/psu_throughput.dat
echo "Completado en.psu.ru (Rusia)"

./main.py english.hi.is 50 > results/hi.dat # Iceland University
./main.py test english.hi.is > results/hi_throughput.dat
echo "Completado Islandia (Islandia)"

#./main.py u-tokyo.ac.jp 50 > results/tokyo.dat # Universidad de Tokyo, Japón
#./main.py test u-tokyo.ac.jp > results/tokyo_throughput.dat
#echo "Completado Tokyo (Japon)"

./main.py cusat.ac.in 50 > results/cusat.dat # Universidad de Tokyo, Japón
./main.py test cusat.ac.in > results/cusat_throughput.dat
echo "Completado Cusat (India)"

./main.py up.ac.za > results/pretoria.dat
./main.py test up.ac.za > results/pretoria_throughput.dat
echo "Completado Pretoria (Sud-Africa)"
