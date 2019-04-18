import matplotlib.pyplot as plt
import numpy as np
import sys, os, json
plt.style.use('seaborn-ticks')

fontSize=16

labels = ["300lux", "500lux", "800lux", "1400lux"]
# color_list = ["#66a61e" , '#e7298a', '#7570b3', '#d95f02', '#1b9e77']
f = plt.figure(figsize=(8,4))

plt.tick_params(axis='x', pad=10, bottom=False)
intervals = [1,2,4,6]
totalDet=[]
uniqueDet=[]

gap = .1
bw = (1-gap)/4

for i ,interval in enumerate(intervals):

    with open("../../data/regular_repeating_events/detection_duplicity_"+str(interval)+"sec.json", "r") as read_file:
        jsondict = json.load(read_file)

    totalDet.append([100*x/240.0 for x in jsondict["totalDet"]])     # Normalize to percentages
    uniqueDet.append([100*x/240.0 for x in jsondict["uniqueDet"]])

print(totalDet)
print(uniqueDet)
print()

totalDet = np.transpose(totalDet)
uniqueDet = np.transpose(uniqueDet)
print(totalDet)
print(uniqueDet)

for i in range(4):
    plt.bar(np.arange(4)*bw+i, totalDet[i], width=bw-0.01, color='#d95f02')
    plt.bar(np.arange(4)*bw+i, uniqueDet[i], width=bw-0.01, color='#66a61e')

for i in range(3):
    plt.axvline(x=0.84+i, color='lightgrey')

plt.axhline(y=100, color='lightgrey', linestyle=":")

for group_idx in range(4):

    for bar_idx in range(4):
        plt.text( group_idx+bar_idx*bw-0.05 ,-44 , intervals[bar_idx] , color='r' ,fontsize=11, verticalalignment='bottom')

plt.xticks(np.arange(4)+0.45, labels, fontsize=fontSize-2)
plt.yticks(fontsize=fontSize-2)
plt.ylabel("Percent of events (%)", fontsize=fontSize-2)
plt.xlim([-0.12,3.812])
plt.tight_layout()
plt.savefig('../../paper/figures/regular_events_capture_rate.eps')
plt.show()
