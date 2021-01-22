#!/bin/bash

FILE=times/20r_as_is.txt

if [ -e $FILE ]
then
	rm $FILE
fi

for i in $(seq -f "%03g" 0 99)
do
	cryptominisat5 --maxtime 10 temp/to_solve_$i.cnf | grep "Total time" >> $FILE
done

