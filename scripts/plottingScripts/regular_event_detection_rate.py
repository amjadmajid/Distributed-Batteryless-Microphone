import matplotlib.pyplot as plt
import numpy as np
import sys, os, json
plt.style.use('seaborn-ticks')

fontSize=18

labels = ["300 lux", "500 lux", "800 lux", "1400 lux"]
# color_list = ["#66a61e" , '#e7298a', '#7570b3', '#d95f02', '#1b9e77']
f = plt.figure(figsize=(8,3.6))

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
    orange_bar = plt.bar(np.arange(4)*bw+i, totalDet[i], width=bw-0.01, color='#9ecae1',  hatch="o")
    green_bar = plt.bar(np.arange(4)*bw+i, uniqueDet[i], width=bw-0.01, color='#08519c')

for i in range(3):
    plt.axvline(x=0.84+i, color='lightgrey')

plt.axhline(y=100, color="r", linestyle="dashed")

for group_idx in range(4):

    for bar_idx in range(4):
        plt.text( group_idx+bar_idx*bw-0.05 ,-44 , intervals[bar_idx] , color='r' ,fontsize=11, verticalalignment='bottom')

plt.xticks(np.arange(4)+0.45, labels, fontsize=fontSize-2)
plt.yticks(fontsize=fontSize-2)
plt.ylabel("Percent of events (%)", fontsize=fontSize-2)
plt.xlim([-0.12,3.812])
plt.tight_layout()
orange_bar.set_label('detected events')
green_bar.set_label('unique events')
plt.legend(fontsize=fontSize)
plt.savefig('../../paper/figures/regular_events_capture_rate_2.eps')
plt.show()
