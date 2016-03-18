#!/bin/bash
 
 # up to user count :)
for boo in $(seq 1 5)
do
	for var in $(seq 1 15)
	do
	   sh write_exac_42_comments_with_due_struct.sh  $var &
	   sleep .01
	   echo "one more spawned..."
	done
done
