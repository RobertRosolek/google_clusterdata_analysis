# to generate job id, task number, cpu request, memory request, start timestamp, end timestamp use command:
# cat task_events/* | head -n 1000000 | awk -F "," '{print $3, $4}' | shuf -n 1 
# this way you obtain job id and task number, now you need to find records for schedule and deschedule, for example using:
# cat task_events/* | grep "<job id>,<task number>" -m 3
# to generate machine number, CPU and Memory use cat machine_events/* | awk -F "," '{print $2,$5,$6}' | sort -u -g | shuf -n 1 
# run: cat task_usage/* | python machine_usage_historgram.py <(cat task_events/*) 

import csv
import sys
import matplotlib.pyplot as plt

def is_inside(interval_a, interval_b):
   return interval_b[0] <= interval_a[0] and interval_a[1] <= interval_b[1]
