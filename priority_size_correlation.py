# run cat clusterdata-2011-1/task_events/* | head -n 100000000 | python google_clusterdata_analysis/memory_cpu_correlation.py

import csv
import sys
import numpy as np

import matplotlib.pyplot as plt
import scipy.stats

SELECT_RATE = 100

EVENT_TYPE_SCHEDULE = "1"

EVENT_TYPE_INDEX = 6 - 1
PRIORITY_INDEX = 9 - 1
CPU_REQUEST_INDEX = 10 - 1
MEMORY_REQUEST_INDEX = 11 - 1

cpu_histogram = []
memory_histogram = []
priority_histogram = []

rows_read = 0

reader = csv.reader(sys.stdin)
for row in reader:
   if row[EVENT_TYPE_INDEX] == EVENT_TYPE_SCHEDULE:
      if rows_read % SELECT_RATE == 0:
         cpu_histogram.append(float(row[CPU_REQUEST_INDEX]))
         memory_histogram.append(float(row[MEMORY_REQUEST_INDEX]))
         priority_histogram.append(int(row[PRIORITY_INDEX]))
      rows_read = (rows_read + 1) % SELECT_RATE

print len(cpu_histogram)

priority_cpu_R = scipy.stats.pearsonr(priority_histogram, cpu_histogram)[0] 
priority_memory_R = scipy.stats.pearsonr(priority_histogram, memory_histogram)[0] 
print priority_cpu_R**2
print priority_memory_R**2 

