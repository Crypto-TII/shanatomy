#!/bin/bash

for (( i=75; i<100; i++ ))
do
	python3 map_attacker.py 32 22 $i 440 structures/sha_1_cnf.txt
done
