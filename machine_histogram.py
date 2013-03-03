# to generate machine number use cat machine_events/* | awk -F "," '{print $2}' | sort -u -g | shuf -n 1 
# run: cat task_events/* | 

import csv
import sys
import matplotlib.pyplot as plt


MACHINE_NUMBER = "294823359"
EVENT_TYPE_SCHEDULE = "1"
EVENT_TYPES_DESCHEDULE = ["2", "3", "4", "5", "6"]

timestamps_seen = 0 # total number of time stamps seen so far
current_timestamp = 0
current_sum = 0
timestamp_record_rate = 5 # record every fifth timeStamp

histogram = []

reader = csv.reader(sys.stdin)
for row in reader:
   if int(row[0]) > current_timestamp:
      if timestamps_seen % timestamp_record_rate == 0:
         histogram.append(current_sum)
      current_timestamp = int(row[0])
      timestamps_seen += 1
   if row[4] == MACHINE_NUMBER:
      if row[5] == EVENT_TYPE_SCHEDULE:
         current_sum += 1
      if any(row[5] == event_type for event_type in EVENT_TYPES_DESCHEDULE):
         current_sum -= 1

histogram.append(current_sum)

#print histogram

plt.plot(histogram)
histogram = [elem + 1 for elem in histogram]
plt.plot(histogram, 'r--')
plt.ylabel('histogram')
plt.show()

print current_sum
    
