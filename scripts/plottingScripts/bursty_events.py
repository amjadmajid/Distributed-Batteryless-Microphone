import matplotlib.pyplot as plt
import numpy as np
import sys, os, json

plt.style.use('seaborn-ticks')
fontSize=20

DESYNC =False

if DESYNC:
    files = [
    "desync_40_50_70_100/524-541lux.json",
    "desync_40_50_70_100/812-836lux.json",
    "desync_40_50_70_100/1400-1413lux.json",
    "desync_40_50_70_100/1705-1737lux.json",
    #"desync_40_50_70_100/2305-2335lux.json",
    ]
else:
    files = [
    "524-541lux.json",
    "812-836lux.json",
    "1400-1413lux.json",
    "1705-1737lux.json",
    #"2305-2335lux.json"
    ]

color_list = ["#a8ddb5" , '#7bccc4', '#43a2ca', '#0868ac', '#eff3ff']
f = plt.figure(figsize=(8,4))

# plt.tick_params(axis='x', pad=15, bottom=False)


for i in range(len(files)):
    file = "../../data/bursty_events/470uf/"+files[i]
    print(file)
    with open(file, "r") as read_file:
        data = json.load(read_file)

    medianprops = {'color':color_list[3], 'linewidth': 2}
    boxprops = {'color': color_list[3], 'linestyle': '-'}
    whiskerprops = {'color': color_list[3], 'linestyle': '-'}
    capprops = {'color': color_list[3], 'linestyle': '-'}
    # flierprops = {'color': color_list[i], 'marker': 'x'}
    
    bw=0.2
    gap=0.2
    plt.boxplot(data, positions=np.arange(4)*0.2+i, widths=0.2, showfliers=False, \
    medianprops=medianprops, boxprops=boxprops, whiskerprops=whiskerprops, capprops=capprops) #, flierprops=flierprops)
for i in range(3):
    plt.axvline(x=0.8+i, color='r', linestyle="dashed")

plt.xlabel("Light intensity (lux)", fontsize = fontSize)
plt.ylabel("Event detection", fontsize = fontSize)
plt.xticks(np.arange(4)+0.275,(500,800,1400,1700,2300),fontsize=fontSize)
plt.yticks(range(0,10,2),range(0,10,2),fontsize=fontSize)
plt.xlim([-0.11,3.71])
plt.ylim([-0.8,8.2])

for group_idx in range(4):

    for bar_idx in range(4):
        plt.text( group_idx+bar_idx*bw-0.05 , -0.3 , bar_idx+1 , color='r' ,fontsize=11, verticalalignment='top')


plt.tight_layout()
if DESYNC:
    f.savefig("../../paper_IPSN_2020/figures/events_burst_rand.eps", bbox_inches='tight')
else:
    f.savefig("../../paper_IPSN_2020/figures/events_burst_problem.eps", bbox_inches='tight')
plt.show()
