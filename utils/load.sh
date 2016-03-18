#!/bin/bash
 
 # up to user count :)
for var in $(seq 1 5)
do
   sh write_exac_42_comments_with_due_struct.sh  $var &
   sleep .1
   echo "one more spawned..."
done
