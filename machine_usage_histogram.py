# to generate machine number, CPU and Memory use cat machine_events/* | awk -F "," '{print $2,$5,$6}' | sort -u -g | shuf -n 1 
# run: cat task_usage/* | python machine_usage_historgram.py <(cat task_events/*) 

import csv
import sys
import matplotlib.pyplot as plt

def is_inside(interval_a, interval_b):
   return interval_b[0] <= interval_a[0] and interval_a[1] <= interval_b[1]

DISPLAY_CPU = 0
DISPLAY_MEMORY = 1

START_TIME_INDEX = 0
END_TIME_INDEX = 1
MACHINE_ID_INDEX = 4
MAX_MEMORY_USAGE_INDEX = 10
MAX_CPU_RATE_INDEX = 5

MACHINE_NUMBER = "294823359"
MACHINE_CPU = 0.5
MACHINE_MEMORY = 0.4995

cpu_histogram = []
memory_histogram = []

current_timestamp_interval = (-1,-1)
current_cpu = 0
current_memory = 0

intervals = []

reader = csv.reader(sys.stdin)
for row in reader:
   if row[MACHINE_ID_INDEX] == MACHINE_NUMBER:
      timestamp_interval = (int(row[START_TIME_INDEX]), int(row[END_TIME_INDEX]))
      if is_inside(timestamp_interval, current_timestamp_interval):
         current_cpu += float(row[MAX_CPU_RATE_INDEX])
         current_memory += float(row[MAX_MEMORY_USAGE_INDEX])
      elif is_inside(current_timestamp_interval, timestamp_interval):
         current_timestamp_interval = timestamp_interval
         current_cpu += float(row[MAX_CPU_RATE_INDEX])
         current_memory += float(row[MAX_MEMORY_USAGE_INDEX]) 
      else:
         if timestamp_interval[0] < current_timestamp_interval[1]:
            print current_timestamp_interval, timestamp_interval
         assert timestamp_interval[0] >= current_timestamp_interval[1], "partially overlapping timestamp intervals" 
         cpu_histogram.append(current_cpu)
         memory_histogram.append(current_memory)
         current_cpu = 0
         current_memory = 0
         if current_timestamp_interval != (-1,-1):
            intervals.append(current_timestamp_interval)
         current_timestamp_interval = timestamp_interval

cpu_histogram.append(current_cpu)
memory_histogram.append(current_memory)
intervals.append(current_timestamp_interval)

machine_cpu_histogram = [MACHINE_CPU for elem in cpu_histogram]
machine_memory_histogram = [MACHINE_MEMORY for elem in memory_histogram]

print intervals

EVENT_TYPE_SCHEDULE = "1"
EVENT_TYPES_DESCHEDULE = ["2", "3", "4", "5", "6"]
MACHINE_ID_INDEX = 4
CPU_REQUEST_INDEX = 9
MEMORY_REQUEST_INDEX = 10
TIMESTAMP_INDEX = 0
EVENT_TYPE_INDEX = 5

current_interval = 0
current_requested_cpu = 0.0
current_requested_memory = 0.0
requested_cpu_histogram = []
requested_memory_histogram = []

f = open(sys.argv[1], 'r')
reader = csv.reader(f)
for row in reader:
   while current_interval < len(intervals) and int(row[TIMESTAMP_INDEX]) > intervals[current_interval][1]:
      requested_cpu_histogram.append(current_requested_cpu)
      requested_memory_histogram.append(current_requested_memory)
      current_interval += 1
   if current_interval == len(intervals):
      break
   if row[MACHINE_ID_INDEX] == MACHINE_NUMBER:
      if row[EVENT_TYPE_INDEX] == EVENT_TYPE_SCHEDULE:
         current_requested_cpu += float(row[CPU_REQUEST_INDEX])
         current_requested_memory += float(row[MEMORY_REQUEST_INDEX])
      if any(row[EVENT_TYPE_INDEX] == event_type for event_type in EVENT_TYPES_DESCHEDULE):
         current_requested_cpu -= float(row[CPU_REQUEST_INDEX])
         current_requested_memory -= float(row[MEMORY_REQUEST_INDEX])
         
if DISPLAY_CPU:
   plt.plot(cpu_histogram, 'g', label="cpu_usage")
   plt.plot(machine_cpu_histogram, 'y', label="available cpu")
   plt.plot(requested_cpu_histogram, 'g--', label="requested_cpu")
if DISPLAY_MEMORY: 
   plt.plot(memory_histogram, 'r--', label="memory_usage") 
   plt.plot(machine_memory_histogram, 'b', label="available memory")
   plt.plot(requested_memory_histogram, 'r', label="requested_memory")

plt.legend()
plt.show()
