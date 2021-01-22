#!/bin/bash

names=() # Create array
while IFS= read -r line # Read a line
do
	names+=("$line") # Append line to the array
done < "$1"

len=${#names[@]}
for (( i=0; i<len; i++ ))
do
	id=$(printf "%03d" $i)
	python3 ../map_designer.py 32 0 ${names[$i]} $id
done
