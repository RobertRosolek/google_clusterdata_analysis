# run cat clusterdata-2011-1/task_events/* | head -n 100000000 | python google_clusterdata_analysis/memory_cpu_correlation.py

import csv
import sys
import numpy as np

from pylab import *
import matplotlib.pyplot as plt
import scipy.stats
from scipy.cluster.vq import *

SELECT_RATE = 100

EVENT_TYPE_SCHEDULE = "1"

EVENT_TYPE_INDEX = 6 - 1
CPU_REQUEST_INDEX = 10 - 1
MEMORY_REQUEST_INDEX = 11 - 1

K = 6
COLORS = [(random(), random(), random()) for i in range(K)]

cpu_histogram = []
memory_histogram = []

rows_read = 0

reader = csv.reader(sys.stdin)
for row in reader:
   if row[EVENT_TYPE_INDEX] == EVENT_TYPE_SCHEDULE:
      if rows_read % SELECT_RATE == 0:
         cpu_histogram.append(float(row[CPU_REQUEST_INDEX]))
         memory_histogram.append(float(row[MEMORY_REQUEST_INDEX]))
      rows_read = (rows_read + 1) % SELECT_RATE

print len(cpu_histogram)

R = scipy.stats.pearsonr(cpu_histogram, memory_histogram)[0] 
print R * R

plt.scatter(cpu_histogram, memory_histogram)
plt.yscale('log')
plt.xscale('log')
plt.ylim(10**-4, 10**0)
plt.xlim(10**-4, 10**0)
plt.title('Scatter plot memory usage / cpu usage, correlation = %f' % (R * R) )
plt.ylabel('memory usage')
plt.xlabel('cpu usage')
plt.savefig('logscale_scatter_memcpu.png')

# K means clustering
# based on http://blog.mpacula.com/2011/04/27/k-means-clustering-example-python/
res, idx = kmeans2(np.array(zip(cpu_histogram, memory_histogram)), K)

colors = [COLORS[i] for i in idx]

# plot colored points
plt.scatter(cpu_histogram, memory_histogram, c=colors)
 
 # mark centroids as (X)
plt.scatter(res[:,0],res[:,1], marker='o', s = 500, linewidths=2, c='none')
plt.scatter(res[:,0],res[:,1], marker='x', s = 500, linewidths=2)
  
plt.savefig('kmeans.png')



log_cpu = []
log_mem = []
for cpu, mem in zip(cpu_histogram, memory_histogram):
   if cpu != 0 and mem != 0:
      log_cpu.append(log10(cpu))
      log_mem.append(log10(mem))
#print log_cpu
heatmap, xedges, yedges = np.histogram2d(log_cpu, log_mem, bins=13, range=[[-4,0], [-4,0]])
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.clf()
plt.imshow(heatmap, extent = extent, origin='lower', interpolation='nearest')
plt.colorbar()
plt.savefig('heatmap.png')

#fig = plt.figure()
#ax2 = fig.add_subplot(111)
#ax2.imshow(heatmap, extent = extent,origin='lower')
#ax2.set_title("imshow origin='lower'");
# ax2.set_yscale('log')

#fig.savefig('heatmap.png')

# plt.show()
