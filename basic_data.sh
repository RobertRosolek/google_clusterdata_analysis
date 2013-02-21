#!/bin/bash

# this may be considerably bigger than number of machines as 
# after a reboot machine can get a new id
echo "Number of different machine ids:"
awk -F "," '{print $2}' machine_events/part-00000-of-00001.csv | sort -u -g | wc -l
echo 

# this might be more accurate approximation of a number of machines
echo "Number of machines at the beginning of trace:"
grep ^0 machine_events/part-00000-of-00001.csv | awk -F "," '{print $2}' | sort -u -g | wc -l
echo

echo "Number of job ids:"
cat job_events/* | awk -F "," '{print $3}' | sort -u -g | wc -l
echo 



